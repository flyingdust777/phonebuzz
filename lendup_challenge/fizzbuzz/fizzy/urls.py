from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('makeCall', views.makeCall, name='makeCall'),
    path('handleCall', views.handleCall, name='handleCall'),
    path('phase1',views.phase1, name='phase1')
]