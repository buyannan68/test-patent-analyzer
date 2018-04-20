# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from patentanalysis import models

import json
import xlrd
import math

from custom_funcs import generic_ngram
from custom_funcs import generic_chemical_extraction, textrazor_chemical_extraction
from custom_funcs import generic_wordcloud
from custom_funcs import generic_similarity

dic_fields = {}
dic_fields['Publication Number'] = 'id'
dic_fields['Publication Date'] = 'date'
dic_fields['Title - DWPI'] = 'title_dwpi'
dic_fields['Abstract - DWPI'] = 'abstract_dwpi'

rec_num_in_page = 5

# Create your views here.
@login_required(login_url="/login/")
def index(request):
	user = request.user
	result = {'user': user}
	return render(request, 'index.html', {'data': result})

@login_required(login_url="/login/")
def collection_create(request):
	if request.method == "POST":
		collection_name = request.POST.get("collection_name", None)
		models.Collection.objects.create(name=collection_name, user=request.user, status='step1')
	collection_list_user = models.Collection.objects.filter(user=request.user)
	#Find latest collection and latest file
	# collection_list_latest = models.Collection.objects.order_by('created_on')[:10]
	sql = """
		select max(a.id) as id, a.collection_id, a.filename, a.filepath, a.user_id, a.upload_on from mysite.patentanalysis_collectionfile as a inner join mysite.patentanalysis_collection as b on (a.collection_id = b.id)  group by a.collection_id order by collection_id, a.id desc
	"""
	collection_list_latest = models.CollectionFile.objects.raw(sql)[:10]
	print collection_list_latest
	return render(request, 'collection_create.html', {"data_user": collection_list_user, "data_latest": collection_list_latest })

@login_required(login_url="/login/")
def collection_upload(request):
	collection_id = '0'
	collection_id_post = 0
	result_added = 0
	if request.method == "POST":

		# print request.POST['collection_id']
		if request.POST['collection_id']:
			collection_id = request.POST['collection_id']
			collection_id_post = request.POST['collection_id']

		# file_upload = request.FILES.get("file_name", None)
		if not request.FILES.get("file_name", None):
			return HttpResponse("no files for upload")
		file_upload = request.FILES.get("file_name", None)
		destination = open(file_upload.name,'wb+')
		for chunk in file_upload.chunks():
			destination.write(chunk)
		destination.close()

		File = models.CollectionFile()
		File.user = request.user
		File.filename = file_upload
		File.filepath = file_upload
		File.collection_id = request.POST['collection_id']
		File.save()

		result_added = 1

		#if new file uploaded, then delete all the related files including PubColRel data as well.
		######### need to add the deletion of model file
		######### change 'step' in the collecion table
		print 'current added file', File.id
		if File.id <> "":
			models.PubColRel.objects.filter(collection_id = request.POST['collection_id']).delete()

	collection_list_user = models.Collection.objects.filter(user=request.user)
	collection = []
	if len(collection_list_user) == 0:
		collection = []
	else:
		collection = models.Collection.objects.filter(user=request.user).order_by('-created_on')[:1]
	if collection_id == '0':
		if len(collection) > 0:
			collection_id = collection[0].id
		else:
			collection_id = '0'
	file_list = models.CollectionFile.objects.filter(collection_id=collection_id)
	collection = collection_id
	return render(request, 'collection_upload.html', {'data_collection': collection_list_user, 
		'data_file': file_list, 
		'data_collection_latest': collection, 
		'data_collection_id_post': collection_id_post, 
		'data_result_added': result_added})

@login_required(login_url="/login/")
def collection_upload_view_update(request):
	collection_id = ""
	if request.method == "POST":
		collection_id = request.POST['collection_id']
	file_list = models.CollectionFile.objects.filter(collection_id=collection_id)
	file_list_json = []
	for f in file_list:
		file_list_json.append({'user':str(f.user), 'filename':str(f.filename), 'upload_on':str(f.upload_on)[0:19], 'id': str(f.id)})
	# print file_list_json
	return HttpResponse(json.dumps({
			"status": 0,
			"result": file_list_json
		}))

@login_required(login_url="/login/")
def collection_display(request, file_id):
	file = models.CollectionFile.objects.get(id=file_id)
	publications = []
	fields = []
	# with xlrd.open_workbook("C:\\Users\\U582788\\Desktop\\OTC\\Analytics\\APAC\\Patents_test.xlsx") as data:
	with xlrd.open_workbook(str(file.filepath)) as data:
		table = data.sheet_by_index(0)
		#change per file format

		for field in table.row_values(0):
		# for field in table.row_values(1):
			if field == "PDF Copy":
				pass
			else:
				fields.append(field)
		for line in range(1, table.nrows):
		# for line in range(2, table.nrows):
			row = table.row_values(line)
			if row:
				publications.append({'id':row[0], "date":row[1], "title_dwpi":row[2], "title":row[3],
									 "assignee_applicant":row[4], "inventor":row[5], "abstract_dwpi":row[6],
									 "abstract":row[7], "priority_number":row[8], "priority_date": row[9],
									 "inpadoc_family_members":row[10],"dwpis_family_members":row[11],
									 "claims":row[12], "ipc_current":row[13], "inpadoc_legal_status":row[14],
									 "abstract_dwpi_novelty":row[15], "abstract_dwps_use":row[16],
									 "abstract_dwpi_advantage":row[17]})#, "pdf":row[18]})
	combined_data = {'fields': fields, 'publications': publications, 'collection': file.id}
	# Calculate the overlap rate

	# Check whether the data has been imported or not
	records_already_exists = models.PubColRel.objects.filter(collection_id = file.collection_id)
	if len(records_already_exists) <> 0:
		combined_data['imported'] = 'true'

	return render(request, 'collection_display.html', {"data": combined_data})

@login_required(login_url="/login/")
def collection_import(request):
	if request.method == "POST":
		file_id = request.POST['file_id']
		file = models.CollectionFile.objects.get(id=file_id)
		publications = []
		fields = []
		# with xlrd.open_workbook("C:\\Users\\U582788\\Desktop\\OTC\\Analytics\\APAC\\Patents_test.xlsx") as data:
		with xlrd.open_workbook(str(file.filepath)) as data:
			table = data.sheet_by_index(0)
			#change per file format
			for field in table.row_values(0):
			# for field in table.row_values(1):
				fields.append(field)
			for line in range(1, table.nrows):
			# for line in range(2, table.nrows):
				row = table.row_values(line)
				if row:
					publications.append({'id':row[0], "date":row[1], "title_dwpi":row[2], "title":row[3],
										 "assignee_applicant":row[4], "inventor":row[5], "abstract_dwpi":row[6],
										 "abstract":row[7], "priority_number":row[8], "priority_date": row[9],
										 "inpadoc_family_members":row[10],"dwpis_family_members":row[11],
										 "claims":row[12], "ipc_current":row[13], "inpadoc_legal_status":row[14],
										 "abstract_dwpi_novelty":row[15], "abstract_dwps_use":row[16],
										 "abstract_dwpi_advantage":row[17]})#, "pdf":row[18]})
		for pub in publications:
			#publication
			pub_new = models.Publication()
			pub_new.pub_num = pub['id']
			if pub['date'] == '-':
				pub_new.date = '9999-12-31'
			else:
				pub_new.date = pub['date']
			pub_new.title_dwpi = pub['title_dwpi']
			pub_new.title = pub['title']
			pub_new.assignee = pub['assignee_applicant']
			pub_new.iventor = pub['inventor']
			pub_new.abstract = pub['abstract']
			pub_new.abstract_dwpi = pub['abstract_dwpi']
			pub_new.pri_num = pub['priority_number']
			pub_new.pri_date = pub['priority_date']
			pub_new.inpadoc_fam = pub['inpadoc_family_members']
			pub_new.dwpi_fam = pub['dwpis_family_members']
			pub_new.claim = pub['claims']
			pub_new.ipc_cur = pub['ipc_current']
			pub_new.inpadoc_stus = pub['inpadoc_legal_status']
			pub_new.abstract_dwpi_nov = pub['abstract_dwpi_novelty']
			pub_new.abstract_dwpi_use = pub['abstract_dwps_use']
			pub_new.abstract_dwpi_adv = pub['abstract_dwpi_advantage']
			# print pub_new
			pub_new.save()
			#publication collection relation
			pub_col_new = models.PubColRel()
			pub_col_new.collection_id = file.collection_id
			pub_col_new.publication = pub_new
			# print pub_col_new
			pub_col_new.save()

	return HttpResponse(json.dumps({
			"status": 0,
			"result": len(publications)
		}))

@login_required(login_url="/login/")
def collection_build(request):
	if request.method == "POST":
		print 'build model file_id:', request.POST.get('file_id')
		print 'build model field:', request.POST.get('field')

		file = models.CollectionFile.objects.get(id=request.POST.get('file_id'))

		result = 0
		if generic_ngram.build_model(dic_fields[request.POST.get('field')], file.collection_id):
			result = 1

		return HttpResponse(json.dumps({
			"result": result
		}))

@login_required(login_url="/login/")
def collection_analyze(request, file_id):
	field_cur = ""
	if request.method == "POST":
		print file_id
		print request.POST['field']
		field_cur = request.POST['field']
	if field_cur == "":
		field_cur = "Title - DWPI"
	field_list= []
	file = models.CollectionFile.objects.get(id=file_id)
	collection = models.Collection.objects.get(id=file.collection_id)
	return render(request, 'collection_analyze.html', {'field_cur': field_cur, 'field_list': field_list, 'file_id': file_id, 'collection_name': collection.name})

@login_required(login_url="/login/")
def collection_analyze_view_update(request):
	if request.method == "POST":

		file_id = request.POST.get('file')
		file = models.CollectionFile.objects.get(id=file_id)
		status = 0
		field = request.POST['field']
		page_id = 0
		record_id = 0
		next_page = False

		# Store Phrase
		phrase = []
		if request.POST.get('phrase') is not None:
			phrase = json.loads(request.POST.get('phrase'))

			for p in phrase:
				phrase_new = models.Phrase()
				phrase_new.collection_id = file.collection_id
				phrase_new.text = p['text']
				phrase_new.category = p['type']
				phrase_new.publication_id = p['pub_id']
				phrase_new.field_analyze = dic_fields[field]
				phrase_new.source = "manual"
				phrase_new.save()

		# Get new data
		# Get the latest record_id
		record_latest = models.Phrase.objects.filter(collection_id = file.collection_id).filter(field_analyze=dic_fields[field]).order_by('-id')[:1]
		record_all = models.Phrase.objects.filter(collection_id = file.collection_id).filter(field_analyze=dic_fields[field]).order_by('publication_id').values('publication_id').distinct()
		print "record_all", len(record_all)

		if len(record_latest) > 0:
			record_id = record_latest[0].publication_id

		if len(record_all) > 0:
			page_id = int(len(record_all) / rec_num_in_page)

		if request.POST.get('record_id') == None:
			pass
		else:
			record_id = request.POST['record_id']

		if request.POST.get('page_id') == None:
			pass
		else:
			page_id = request.POST['page_id']

		sql = """
			select * from mysite.patentanalysis_publication as a inner join mysite.patentanalysis_pubcolrel as b on (a.id = b.publication_id) where a.id > """ + str(record_id) +  """ and b.collection_id =
		"""
		# publications = models.CollectionFile.objects.raw(sql + str(file.collection_id) + " limit " + str(rec_num_in_page * int(page_id)) + "," + str(rec_num_in_page))
		publications = models.CollectionFile.objects.raw(sql + str(file.collection_id) + " limit " + str(rec_num_in_page))

		# pub_num_all = models.PubColRel.objects.filter(collection_id = file.collection_id).filter(id__gt = record_id).count()
		pub_num_all = models.PubColRel.objects.filter(collection_id = file.collection_id).count()

		all_phrases = []

		last_record_no = 0

		for index, pub in enumerate(publications):
			# print index, p
			phrase_list = generic_ngram.keyword_extract(file.collection_id, dic_fields[field], index + rec_num_in_page * int(page_id))
			# phrase_list = generic_ngram.keyword_extract(file.collection_id, dic_fields[field], index + rec_num_in_page)

			all_phrases.append({'id': pub.id, 'index': index, 'pub_num': pub.pub_num, 'title': pub.title, 'phrase_list': phrase_list})

		if pub_num_all > rec_num_in_page * (int(page_id) + 1):
			next_page = True

		return HttpResponse(json.dumps({
				"status": status,
				"result": all_phrases,
				"page_id": int(page_id) + 1,
				"next_page": next_page,
				"page_total": int(math.ceil(float(pub_num_all) / float(rec_num_in_page))),
			}))

@login_required(login_url="/login/")
def find_similar(request):

	collection_list = models.Collection.objects.filter(user_id = request.user).filter(status = 'step3')
	
	return render(request, 'collection_find_similar.html', {'collection': collection_list})

@login_required(login_url="/login/")
def find_simliar_list(request):

	if request.method == "POST":
		status = 1
		result = ""
		# Construct the comparison pool
		task_id = request.POST['task']
		user_input = request.POST['user_input']
		cur_field = request.POST['analyze_field']
		comparison_pool = {'task_id': int(task_id), 'user_id': request.user.id, 'cur_field': dic_fields[cur_field]}
		# comparison_pool = {'task_id': 0, 'user_id': 2, 'cur_field': 'abstract_dwpi'}

		word_list, sim_pub_num, sim_score = generic_similarity.find_similar(comparison_pool, user_input)

		pub_list = models.Publication.objects.filter(pub_num__in=sim_pub_num).values_list('pub_num', 'title', dic_fields[cur_field]).distinct()

		result = []
		# print word_list['word']

		for index, pub in enumerate(pub_list):
			result.append({'pub_num': pub[0], 'title': pub[1], 'text': pub[2], 'score': round(sim_score[index], 2)})

		result = sorted(result, key=lambda d: d['score'], reverse=True)

		return HttpResponse(json.dumps({
					"status": status,
					"result": result,
					"word_list": [word for word in word_list['word']]
				}))

@login_required(login_url="/login/")
def extract_chemical(request):
	if request.method == "POST":
		pass
	# records_already_exists = models.PubColRel.objects.filter(collection_id = collection_list_user.collection_id)

	collection_already_imported = models.PubColRel.objects.filter(collection__user_id = request.user).order_by('collection_id').values('collection_id').distinct()

	collection_name = []
	for index, c in enumerate(collection_already_imported):
		collection = models.Collection.objects.get(id = int(c['collection_id']))
		collection_name.append(collection)

	return render(request, 'collection_extract_chemical.html', {'collection_list': collection_name})

from django.utils.cache import get_cache_key

@login_required(login_url="/login/")
def extract(request):

	result = {}
	exists = False

	if request.method == "POST":
		algo = request.POST['algorithm']
		field = request.POST['field']
		collection_id = request.POST['collection']

		file = models.CollectionFile.objects.filter(collection_id = collection_id).order_by('-id').values('id').distinct()

		chem_phrase_exists = models.ChemicalPhrase.objects.filter(collection_id = collection_id).filter(field_analyze = dic_fields[field]).filter(source = algo.lower())

		if len(chem_phrase_exists) > 0:
			# Compare whether there is new file or not
			if chem_phrase_exists[0].collectionfile_id < file[0]['id']:
				chem_phrase_exists.delete()
			else:
				exists = True

		if exists:
			print "old"
			for phrase in chem_phrase_exists:
				result[phrase.text] = phrase.count
			result = sorted(result.items(), key=lambda d: d[1], reverse=True)
		else:
			print "new"
			if algo == "Native":
				result = generic_chemical_extraction.extract(dic_fields[field], collection_id)
			else:
				result = textrazor_chemical_extraction.extract(dic_fields[field], collection_id)

			generic_wordcloud.generate_wordcloud_by_freq(result, collection_id, dic_fields[field], algo)
			result = sorted(result.items(), key=lambda d: d[1], reverse=True)

			for phrase in result:
				chemphrase = models.ChemicalPhrase()
				chemphrase.text	= phrase[0]
				chemphrase.count = int(phrase[1])
				chemphrase.collection_id = collection_id
				chemphrase.collectionfile_id = file[0]['id']
				chemphrase.source = algo.lower()
				chemphrase.field_analyze = dic_fields[field]
				chemphrase.save()

		print result
		status = 0

		return HttpResponse(json.dumps({
					"status": status,
					"result": result
				}))

@login_required(login_url="/login/")
def test(request):
	return render(request, 'test.html')