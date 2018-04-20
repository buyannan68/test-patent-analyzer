"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from patentanalysis import views
from account import views as auth_views

urlpatterns = [
	url(r'^login', auth_views.my_login, name='login'),
    url(r'^logout', auth_views.my_logout, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^collection/create', views.collection_create, name='collection_create'),
    url(r'^collection/upload', views.collection_upload, name='collection_upload'),
    url(r'^update_view/', views.collection_upload_view_update, name='collection_upload_view_update'),
    url(r'^collection/display/(?P<file_id>[0-9]+)', views.collection_display, name='collection_display'),
    url(r'^import_data/', views.collection_import, name='collection_import_data'),
    url(r'^build_model/', views.collection_build, name='collection_build_model'),
    url(r'^collection/analyze/(?P<file_id>[0-9]+)', views.collection_analyze, name='collection_analyze'),
    url(r'^update_analyze_view/', views.collection_analyze_view_update, name='collection_analyze_view_update'),
    # url(r'^update_analyze_next/', views.collection_analyze_view_next, name='collection_analyze_view_next'),
    url(r'^collection/find_similar', views.find_similar, name='find_similar'),
    url(r'^collection/extract_chemical', views.extract_chemical, name='extract_chemical'),
    url(r'^extract/', views.extract, name='extract'),
    url(r'^update_simliar_view/', views.find_simliar_list, name='find_simliar_list'),
    url(r'^test/', views.test, name='test'),
]
