import pandas as pd
import itertools as iter
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
# import os, errno
import MySQLdb

# Read & process patent data
# data = pd.read_excel("C:\Users\U582788\Desktop\OTC\Analytics\APAC\Patents_ngram_test.xlsx", sheetname="Sheet1", header=0)
#
# data["Abstract - DWPI"] = data["Abstract - DWPI"].str.replace("\d+", " removemezzz ")
# data["Abstract - DWPI"] = data["Abstract - DWPI"].str.replace("-", "replacelater")
# data["Abstract - DWPI"] = data["Abstract - DWPI"].str.replace(r'[^\w\s]', " removemezzz ")
#
# corpus = data["Abstract - DWPI"]

# print corpus

conn = MySQLdb.connect(host="localhost",user="root",passwd="b2y25n14",db="mysite",charset="utf8")

# print data_mysql["abstract_dwpi"]

# Set up filter lists
# 'removemezzz' already added to the stopwords file!!!
# stop_words = pd.read_excel("C:\Users\U582788\Desktop\OTC\Analytics\APAC\Stop words.xlsx", sheetname="Sheet1", header=0)
stop_words = pd.read_excel("..\patentanalysis\custom_funcs\dicts\Stop words.xlsx", sheetname="Sheet1", header=0)
stop_words = stop_words["STOPWORD"].tolist()
verb_pos = ["VB", "VBD", "VBG", "VBP", "VBZ"]
verb_list = ["contains", "consists", "enables"]


########################################################################
###### For Initialization Before Getting Keywords for Each Patent ######
########################################################################

def bigram_tfidf(corpus):
    # get tf-idf score matrix for all ngrams
    tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df=0, stop_words=None)
    tfidf_matrix_bigram = tf.fit_transform(corpus)
    #dense = tfidf_matrix_bigram.todense()
    feature_names = [w.replace('replacelater', '-') for w in tf.get_feature_names()]

    return tfidf_matrix_bigram, feature_names


def bigram_filter(feature_names):

    # filter feature names
    features = pd.DataFrame(feature_names, columns=["Phrase"])
    features["word1"], features["word2"] = features["Phrase"].str.split().str
    features = features[(~features.word1.isin(stop_words)) & (~features.word1.isin(verb_list)) & (~features.word2.isin(stop_words))]

    # tag POS and filter
    tags = nltk.tag.pos_tag_sents(map(nltk.word_tokenize, features["Phrase"]))
    df_tmp = pd.DataFrame(tags, index=features.index, columns=["word1", "word2"])
    df_tmp = df_tmp.join(
        pd.DataFrame(df_tmp["word1"].values.tolist(), index=features.index, columns=["word_1", "tag_1"]))
    df_tmp = df_tmp.join(
        pd.DataFrame(df_tmp["word2"].values.tolist(), index=features.index, columns=["word_2", "tag_2"]))
    df_tmp = df_tmp[(~df_tmp.tag_1.isin(verb_pos)) & df_tmp.tag_2.str.startswith("NN")]

    # return filtered list
    index = df_tmp.index.tolist()
    features_bigram = features.ix[index, [0]]

    return features_bigram, index


def trigram_tfidf(corpus):

    # get tf-idf score matrix for all ngrams
    tf = TfidfVectorizer(analyzer='word', ngram_range=(3, 3), min_df=0, stop_words=None)
    tfidf_matrix_trigram = tf.fit_transform(corpus)
    #dense = tfidf_matrix_trigram.todense()
    feature_names = [w.replace('replacelater', '-') for w in tf.get_feature_names()]

    return tfidf_matrix_trigram, feature_names


def trigram_filter(feature_names):

    # filter feature names
    features = pd.DataFrame(feature_names, columns=["Phrase"])

    features["word1"], features["word2"], features["word3"] = features["Phrase"].str.split().str
    features = features[(~features.word1.isin(stop_words)) & (~features.word1.isin(verb_list)) &
                            (~features.word2.isin(stop_words)) & (~features.word3.isin(stop_words))]

    # tag POS and filter
    tags = nltk.tag.pos_tag_sents(map(nltk.word_tokenize, features["Phrase"]))
    df_tmp = pd.DataFrame(tags, index=features.index, columns=["word1", "word2", "word3"])
    df_tmp = df_tmp.join(
        pd.DataFrame(df_tmp["word1"].values.tolist(), index=features.index, columns=["word_1", "tag_1"]))
    df_tmp = df_tmp.join(
        pd.DataFrame(df_tmp["word3"].values.tolist(), index=features.index, columns=["word_3", "tag_3"]))
    df_tmp = df_tmp[(~df_tmp.tag_1.isin(verb_pos)) & df_tmp.tag_3.str.startswith("NN")]

    # return filtered list
    index = df_tmp.index.tolist()
    features_trigram = features.ix[index, [0]]

    return features_trigram, index


def fourgram_tfidf(corpus):
    # get tf-idf score matrix for all ngrams
    tf = TfidfVectorizer(analyzer='word', ngram_range=(4, 4), min_df=0, stop_words=None)
    tfidf_matrix_fourgram = tf.fit_transform(corpus)
    #dense = tfidf_matrix_fourgram.todense()
    feature_names = [w.replace('replacelater', '-') for w in tf.get_feature_names()]

    return tfidf_matrix_fourgram, feature_names


def fourgram_filter(feature_names):
    # filter feature names
    features = pd.DataFrame(feature_names, columns=["Phrase"])

    features["word1"], features["word2"], features["word3"], features["word4"] = features["Phrase"].str.split().str
    features = features[(~features.word1.isin(stop_words)) & (~features.word1.isin(verb_list)) &
                        (~features.word2.isin(stop_words)) & (~features.word3.isin(stop_words)) & (
                        ~features.word4.isin(stop_words))]

    # tag POS and filter
    tags = nltk.tag.pos_tag_sents(map(nltk.word_tokenize, features["Phrase"]))
    df_tmp = pd.DataFrame(tags, index=features.index,
                          columns=["word1", "word2", "word3", "word4"])
    df_tmp = df_tmp.join(
        pd.DataFrame(df_tmp["word1"].values.tolist(), index=features.index, columns=["word_1", "tag_1"]))
    df_tmp = df_tmp.join(
        pd.DataFrame(df_tmp["word4"].values.tolist(), index=features.index, columns=["word_4", "tag_4"]))
    df_tmp = df_tmp[(~df_tmp.tag_1.isin(verb_pos)) & df_tmp.tag_4.str.startswith("NN")]

    # return filtered list
    index = df_tmp.index.tolist()
    features_fourgram = features.ix[index, [0]]

    return features_fourgram, index


def build_model(field, collection_id):

    cur_field = field

    sql = "select pub_num, " + str(cur_field) + " from mysite.patentanalysis_publication as a inner join mysite.patentanalysis_pubcolrel as b on (a.id = b.publication_id) where b.collection_id = " + str(collection_id)

    data_mysql = pd.read_sql(sql, conn, index_col="pub_num")

    data_mysql[cur_field] = data_mysql[cur_field].str.replace("\d+", " removemezzz ")
    data_mysql[cur_field] = data_mysql[cur_field].str.replace("-", "replacelater")
    data_mysql[cur_field] = data_mysql[cur_field].str.replace(r'[^\w\s]', " removemezzz ")

    corpus = data_mysql[cur_field]

    # print corpus

    # pre-store collection ngrams
    matrix_2, features_2 = bigram_tfidf(corpus)
    features_bigram, index_2 = bigram_filter(features_2)

    matrix_3, features_3 = trigram_tfidf(corpus)
    features_trigram, index_3 = trigram_filter(features_3)

    matrix_4, features_4 = fourgram_tfidf(corpus)
    features_fourgram, index_4 = fourgram_filter(features_4)

    save_all = [matrix_2, index_2, features_bigram, matrix_3, index_3, features_trigram, matrix_4, index_4, features_fourgram]
    # collection_name = "collection_test"   #input collection name
    with open('..\patentanalysis\custom_funcs\collection_models/' + str(collection_id) + "_" + cur_field + "_ngram.txt", "wb") as fp:
        pickle.dump(save_all, fp)

    return True;


#####################################################
##### Keywords Extraction for Individual Patent #####
#####################################################

def keyword_extract(collection_id, field, patent_key):
    # load pre-stored ngrams
    with open('..\patentanalysis\custom_funcs\collection_models/' + str(collection_id) + "_" + field + "_ngram.txt", "rb") as fp:
        collection_ngram = pickle.load(fp)

    matrix_2 = collection_ngram[0]
    index_2 = collection_ngram[1]
    features_bigram = collection_ngram[2]
    matrix_3 = collection_ngram[3]
    index_3 = collection_ngram[4]
    features_trigram = collection_ngram[5]
    matrix_4 = collection_ngram[6]
    index_4 = collection_ngram[7]
    features_fourgram = collection_ngram[8]


    # get bigram
    dense_2 = matrix_2.todense()
    doc_2 = dense_2[patent_key].tolist()[0]

    scores_2 = pd.DataFrame(doc_2, columns=["Score"])
    scores_2 = scores_2[(scores_2.Score > 0) & (scores_2.index.isin(index_2))]
    sorted_scores_2 = scores_2.sort_values(by="Score", ascending=False)
    result2 = sorted_scores_2.join(features_bigram)

    # get trigram
    dense_3 = matrix_3.todense()
    doc_3 = dense_3[patent_key].tolist()[0]

    scores_3 = pd.DataFrame(doc_3, columns=["Score"])
    scores_3 = scores_3[(scores_3.Score > 0) & (scores_3.index.isin(index_3))]
    sorted_scores_3 = scores_3.sort_values(by="Score", ascending=False)
    result3 = sorted_scores_3.join(features_trigram)

    # get fourgram
    dense_4 = matrix_4.todense()
    doc_4 = dense_4[patent_key].tolist()[0]

    scores_4 = pd.DataFrame(doc_4, columns=["Score"])
    scores_4 = scores_4[(scores_4.Score > 0) & (scores_4.index.isin(index_4))]
    sorted_scores_4 = scores_4.sort_values(by="Score", ascending=False)
    result4 = sorted_scores_4.join(features_fourgram)


    # merge results
    merge_result = pd.concat([result2, result3, result4], axis=0, ignore_index=True)

    # remove duplicate ones with lower tf-idf score
    check_phrase = list()
    for i, j in iter.combinations(merge_result.Phrase, 2):
        if i in j:
            check_phrase.append((i, j))

    to_remove = list()
    for short, long in check_phrase:
        if merge_result[merge_result.Phrase == short]["Score"].iloc[0] > merge_result[merge_result.Phrase == long]["Score"].iloc[0]:
            to_remove.append(long)
        else:
            to_remove.append(short)

    result = merge_result[~merge_result.Phrase.isin(to_remove)]
    result = result.sort_values(by="Score", ascending=False)

    # return result['Phrase'].to_dict()
    return result['Phrase'].values.tolist()

# Print Result
# import time
# start =time.clock()
# print(keyword_extract("4", 0))
# end1 = time.clock()
# print "Running 1 " + str(end1 - start)
# print(keyword_extract("4", 1))
# end2 = time.clock()
# print "Running 2 " + str(end2 - end1)
# print(keyword_extract("4", 2))
# end3 = time.clock()
# print "Running 3 " + str(end3 - end2)

#
# build_model("abstract_dwpi", "4")
# print keyword_extract("4", 1)
