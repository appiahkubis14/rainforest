from django.urls import path
from .views import *

app_name = "rootApp"

urlpatterns = [
    path('', mapView, name='map'),    
    path('asd/', test2, name='help'), 

    path('district/', DistrictView.as_view(),name='district'),

    path('district/<int:typevalue>', DistrictView.as_view(),name='district'),

    path('proarea/', ProAreaView.as_view(),name='proarea'),


    path('studyarea/', studyAreaView.as_view(),name='studyarea'),
      

    path('analysis/', analysisView, name='help'), 

    path('analysistimeseries/', analysistimeseriesView, name='help'), 


    path('fetchcloud/', fetchcloudffree, name='fetchcloud'), 


    path('getdist/', getdistrictdet, name='getdist'), 
    
    
      
	
 ]


