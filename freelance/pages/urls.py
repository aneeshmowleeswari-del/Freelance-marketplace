from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('',views.home, name='home'),
    path('about/',views.about,name='about'),
    path('categories/', views.categories_view, name='category'),
    path('contact/', views.contact, name='contact'),
    path('joblisting',views.job_listing, name='job_listing'),

]