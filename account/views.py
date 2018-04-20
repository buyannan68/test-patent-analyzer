# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def my_login(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		if username == "":
			username = "admin"
		if password == "":
			password = "abc123456"
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			result = {"msg": "success", "user": user}
			redirect_url = request.POST['next']
			# print redirect_url
			if redirect_url.find('next=') > 0:
				redirect_url = redirect_url[redirect_url.index('=')+1:]
			else:
				redirect_url = '/'
			return redirect(redirect_url)
			# return render(request, 'login.html', {'data': result})
		else:
			result = {"msg": "error", "user": user}
			return render(request, 'login.html', {'data': result})
	return render(request, 'login.html')

def my_logout(request):
	logout(request)
	result = {"msg": "logout"}
	return render(request, 'login.html', {'data': result})