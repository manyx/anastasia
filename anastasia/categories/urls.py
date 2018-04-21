from django.conf.urls import url
from categories import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^categories/$', views.CategoriesList.as_view()),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.CategoryDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)