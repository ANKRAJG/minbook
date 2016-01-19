from django.conf.urls import url
from bookmarks import views


urlpatterns = [
    url(r'^$', views.bookmarks, name='bookmarks'), 
    url(r'^tags/$', views.edit_tags, name='edit_tags'),
    url(r'^(?P<pk>[0-9]+)/$', views.show_url, name='show_url'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit_url_tags, name='edit_url_tags'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete_url, name='delete_url'),
    
    url(r'^tags/(?P<pk>[0-9]+)/$', views.show_tags, name='show_tags'),
    url(r'^tags/(?P<pk>[0-9]+)/edit/$', views.edit_tags_edit, name='edit_tags_edit'),
    url(r'^tags/(?P<pk>[0-9]+)/delete/$', views.delete_tag, name='delete_tag'),
    url(r'^tags/new/$', views.new_tag, name='new_tag'),
    
    #Javascript - JQuery - Ajax
    url(r'^save/$', views.save_data, name='save_data'),
    url(r'^search/$', views.search_data, name='search_data'),
]