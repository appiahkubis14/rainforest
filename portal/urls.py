from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'portal'


urlpatterns = [
    path('', views.index, name=''),
	path("dashboard/", views.dashboard, name="dashboard"),


	path("dashboard2/", views.dashboard2, name="dashboard"),

	path("dashboardseed/", views.dashboardSeed, name="dashboard"),


	path("seedlingmap/", views.seedlingmonitoringmapView, name="dashboard"),



	


	path("logout/",LogoutView.as_view(), name="dashboard"),
	

	path("map/", views.map, name="map"),

	path("biomap/", views.biomap, name="map"),

	path("report/", views.report, name="report"),

	path("dashres/", views.dashboardResults, name="map"),

	path("dashres2/", views.dashboardResults2, name="map"),


	path("dashres_seed/", views.dashboardResultsSeed, name="map"),



	path("print/", views.prntsht, name="print"),

	path("groupdetail/", views.groupdetails, name="print"),


	# path('savedata/', views.saveDataView, name='csvupload'),
	# path("blog/", views.blog, name="blog"),
	# path("blog_details/", views.blog_details, name="blog_details"),
	# path("contact/", views.contact, name="contact"),
	# path("gallery/", views.gallery, name="gallery"),

	path('saverecords/', views.SaverecdataView.as_view()),

	path('saverecord/', views.Saverecdata2View.as_view()),

	path('reportres/', views.reportResults),

	path('indivdetail/', views.indivdetails),

	path('groupreport/', views.reportgroupResults),

	path('getfarm/', views.getfarmView),

	path('gettrees/', views.gettreesView),
	path('gettrees/<slug:code>/', views.gettreesView),

	

	path('login/', views.loginView),

	path('loginauthenticate/', views.loginauthenticateView),


	path('districtapi/', views.districtApiView),

	path('regionapi/', views.regionApiView),


	

	path('farmboundarylayer/', views.farmBoundarylayerView),
    path('get-boundary/<int:farm_id>/', views.get_farm_boundary, name='get_farm_boundary'),
    path('update-farm-boundary/<int:farm_id>/', views.update_farm_boundary, name='update_farm_boundary'),
    
	path('seedling-map/', views.seedling_map, name='seedling_map'),
    path('api/seedling-surveys/', views.get_seedling_surveys, name='get_seedling_surveys'),
    path('api/update-survey-boundary/<int:survey_id>/', views.update_survey_boundary, name='update_survey_boundary'),
    path('api/living-species-locations/<int:survey_id>/', views.get_living_species_locations, name='get_living_species_locations'),
	
	
	path('seedling-surveys/', views.seedling_survey_list, name='seedling_survey_list'),
    path('api/seedling-surveys/datatable/', views.get_seedling_surveys_datatable, name='get_seedling_surveys_datatable'),
    path('api/seedling-surveys/detail/<int:survey_id>/', views.get_seedling_survey_detail, name='get_seedling_survey_detail'),
    path('api/seedling-surveys/stats/', views.get_seedling_survey_stats, name='get_seedling_survey_stats'),
    path('api/seedling-surveys/delete/', views.delete_seedling_survey, name='delete_seedling_survey'),


	path('seedling-dashboard/', views.seedling_dashboard, name='seedling_dashboard'),
    path('api/seedling-dashboard/stats/', views.get_dashboard_stats, name='get_dashboard_stats'),
    path('api/seedling-dashboard/recent-surveys/', views.get_recent_surveys, name='get_recent_surveys'),
    # You

	path('beneficiary-report/', views.beneficiary_report, name='beneficiary_report'),
    path('api/beneficiaries/datatable/', views.get_beneficiary_datatable, name='beneficiary_datatable'),
    path('api/beneficiaries/stats/', views.get_beneficiary_stats, name='beneficiary_stats'),
    path('api/beneficiaries/detail/<int:beneficiary_id>/', views.get_beneficiary_detail, name='beneficiary_detail'),


	path('tree-species/', views.tree_species_list, name='tree_species_list'),
    path('tree-species-datatable/', views.get_tree_species_datatable, name='get_tree_species_datatable'),
    path('tree-species-detail/<int:species_id>/', views.get_tree_species_detail, name='get_tree_species_detail'),


	path('monitoriing-dashboard/', views.monitoring_dashboard, name='dashboard'),
    path('dashboard-data/', views.dashboard_data, name='dashboard_data'),

	path('treelayer/', views.treelayerView.as_view(),name='treelayer'),
	path('treelayer/<slug:typevalue>/', views.treelayerView.as_view(),name='treelayer'),



	path('districtboundaryapi/', views.DistrictBoundarylayerView.as_view()),


	path('treespeciesapi/', views.treespeciesApiView),
	path('forestdistapi/', views.forestDistApiView),
	path('stoolapi/', views.stoolApiView),


	path('enumeratorlogin/', views.enumeratorloginView),
	path('registerenumerator/', views.registerenumeratorView.as_view()),

	path('communityapi/', views.communityApiView),

	
	path('trainingapi/', views.trainingView.as_view()),

	path('seedlingsmonitoringapi/', views.seedlingsmonitoringView.as_view()),

	path('lmbmonitoringapi/', views.lmbMonitoringView.as_view()),

	path('alternativemonitoringapi/', views.alternativeMonitoringView.as_view()),

	path('syncapi/', views.SyncdbView),

	path('searchfarmer/', views.searchfarmerView),
	
	path('biomas/', views.biomasView),


	path('biomasmap/', views.biomasmapView),

	path('biomaspoint/', views.biomaspointView),
	# path('calculate/', views.calculateView),

	path('farmerapi/', views.farmerView.as_view()),

	path('farmerlist/', views.farmerlistView),



	path('savefirebasecode/', views.saveFirebaseCodeView),

	path('savespeciesphoto/', views.saveSpeciesphotoview.as_view()),


	path('deforestationapi/', views.deforestationView.as_view()),



	

	path('treespecieslist/', views.treeSpecieslistView),
	
	path("searchtreeregisterfarmer/",views.searchtreeregisterfarmerView),

	path("sendnotifications/",views.send_notifications),

	path("specieslist/",views.seedlingsMonitoringSpeciesView),

	path("ratinguser/",views.ratingView),

	path("webspecieslist/",views.speciesListView),

	path("speciestbl/",views.speciestblView),


	path("seedlingmonreport/",views.seedlingMonitoringreport),

	path("seedlingmontblreport/",views.seedlingMontblreport),

	path("seedlingmondetails/",views.seedlingMondetails),

	path("fetchalltreefarmer/",views.FetchAlltreefarmerView),



	path('organisationapi/', views.organisationApiView),

	# path("seedlingmonitoring_api/",views.seedlingsMonitoring_list ,name="seedlingsmonitoring-detail"),
    

	path('api/v2/monitoring/', views.create_or_update_seedling_survey, name='create_survey'),
    






	path('api/survey/<int:survey_id>/boundary/', views.get_farm_boundary_geojson, name='survey_boundary'),
    
    path('api/surveys/boundaries/', views.get_all_farm_boundaries_geojson, name='all_boundaries'),
    
    path('api/survey/<int:survey_id>/species-points/', views.get_living_species_points_geojson, name='species_points'),
    
    path('api/survey/<int:survey_id>/map-data/', views.get_survey_complete_map_data, name='complete_map_data'),

]
