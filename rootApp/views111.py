# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import datetime, pdfkit, random, os, calendar
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
# from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
# from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
# from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from djgeojson.views import GeoJSONLayerView
from django.contrib.gis.db.models import Extent
from django.core.serializers import serialize
from .models import *
from .controllers.function import *
from datetime import datetime, date
from djgeojson.views import GeoJSONLayerView
from django.contrib.gis.geos import GEOSGeometry, LineString, Point



def rootView(request):
	toHTML  ={}

	return render(request, 'rootApp/landing.html', toHTML)



def mapView(request):
	toHTML  ={}

	daterange = range(2015,int(date.today().year)+1)




	return render(request, 'rootApp/index.html', locals())


def reportView(request):
	toHTML  ={}

	return render(request, 'rootApp/report.html', toHTML)


def helpView(request):
	toHTML  ={}

	return render(request, 'rootApp/help.html', toHTML)

def listdata():
	asd=[]
	trainsam = trainingdata.objects.all()
	for aa in trainsam :
		asd.append(ee.Feature(ee.Geometry.Point(aa.lat, aa.lng), {"landcover": aa.value }),)
	return asd



def testingnumber(request):

	loaddef()
	

	try:
		

		features = [
		 
		  ee.Feature(ee.Geometry.Point(-2.5,6.2), {'landcover': 0}),
		  ee.Feature(ee.Geometry.Point(- 2.5 ,6.4806,), {'landcover': 1}),
		  ee.Feature(ee.Geometry.Point(-2.3,6.5806), {'landcover': 2})
		];

		
		# features = listdata();

		sefwi = ee.FeatureCollection("users/eopokukwarteng/sefwi")

		data = ee.FeatureCollection(listdata())

		Sentinel2Collection=ee.ImageCollection("COPERNICUS/S2_SR") \
		.filterDate('2019-01-01','2019-01-28') \
		.filterBounds(sefwi) \
		.sort('CLOUD_COVER', True)


		filtered = Sentinel2Collection \
		  .filterMetadata('IMAGE_QUALITY', 'equals', 9)

		Sentinel_med = Sentinel2Collection.median()
		Sentinel_crop = Sentinel_med.clip(sefwi)


		#Collecting training data
		#Merging the three geometry layers into a single featurecollection
		# newfc= ee.FeatureCollection(features)
		print(data)

		# Select the bands for training
		bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7','B8','B8A']

		# Sample the input imagery to get a FeatureCollection of training data.
		training = Sentinel_crop.select(bands).sampleRegions({
		  'collection': data,
		  'properties':['landcover'],
		  'scale': 20
		})
		# print(training, 'training')


		# # Making a Random Forest classifier and training it.
		# classifier= ee.Classifier.smileRandomForest(4).train({
		#   'features': training,
		#   'classProperty': 'landcover',
		#   'inputProperties': bands
		# })
		# # print(classifier)

		# #Classifying the input imagery
		# classification= Sentinel_crop.select(bands).classify(classifier)

		# # Define a palette for the Land Use classification.
		# palette = [
		#   'cyan', # forest (0)  # red
		#   'red', # urban (1)  # green
		#   'green' #  agriculture (2) # blue
		# ]


		# idfeatures = classification.getMapId(palette)

		# # print (idfeatures)

		# toHTML['mapid'] = idfeatures['tile_fetcher'].url_format
		# toHTML['token'] = idfeatures['token']



	except Exception as e:
		raise e
		toHTML['mapid'] = 'error'






	return JsonResponse(toHTML, safe=False)










def test2(request):

	loaddef()
	toHTML={}

	try:
		# # start= request.GET.get('start')
		# # end= request.GET.get('end')

		# start="2020-01-01"
		# end= date.today()
		# CLOUD_FILTER = 60
		# # START_DATE = '2021-01-01'
		# # END_DATE = '2021-06-25'

		# datefrom = datetime.strptime(start, "%Y-%m-%d")
		# dateto = str(end)


		# AOI = ee.FeatureCollection("users/eopokukwarteng/sef_pilot")

		# # AOI=ee.Geometry.Point([-2.7634471830822593,6.291906530887788])
		# traindata = ee.FeatureCollection("users/eopokukwarteng/sefwi_training_final")
		# # /Loading Sentinel 2 data and filtering by date and bounds
		# Sentinel2Collection=ee.ImageCollection("COPERNICUS/S2_SR") \
		# 	.filterDate(ee.Date(datefrom), ee.Date(dateto)) \
		# 	.filterBounds(AOI) \
		# 	.filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', CLOUD_FILTER))\
		# 	.median()\
		# 	.clip(AOI)


		# newfc = traindata


		# # Select the bands for training
		# bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7','B8','B8A']

		# # Sample the input imagery to get a FeatureCollection of training data.
		# training = Sentinel2Collection.select(bands).sampleRegions(
		#   collection=newfc,
		#   properties=['landcover'],
		#   scale= 100
		# )
		# # print(training, 'training')

		# # Making a Random Forest classifier and training it.
		# classifier= ee.Classifier.smileRandomForest(8).train(
		#   features=training,
		#   classProperty='landcover',
		#   inputProperties=bands
		# )


		# #Classifying the input imagery
		# classification= Sentinel2Collection.select(bands).classify(classifier)

		# Define a palette for the Land Use classification.
		classification=ee.Image("users/eopokukwarteng/classification_2020")
		# palette = [
		# 	"cyan",    # "Agroforestry Cocoa #0
		# 	"#ED022A" , # "Built"	#1
		# 	"#A7D282", # "Cocoa"	#2
		# 	"#FFDB5C", # "Cropland"	#3
		# 	"#358221", # "Forest"	#4
		# 	"#87D19E", # "MonoCocoa"	#5
		# 	"#EECFA8", # "OpenForest"	#6
		# 	"#1A5BAB" # "Water"	#7
		# ]

		palette = [
			"cyan",    # "Agroforestry Cocoa #0
			"#ED022A" , # "Built"	#1
			"#FFDB5C", # "Cropland"	#2
			"#358221", # "Forest"	#3
			"#87D19E", # "MonoCocoa"	#4
			"#EECFA8", # "OpenForest"	#5
			"#1A5BAB" # "Water"	#6
		]



# Agroforestry Cocoa	0
# Built	1
# Cropland	2
# Forest	3
# MonoCocoa	4
# OpenForest	5
# Water	6

		style={
			'min':0, 
			'max':6, 
			'palette': palette
			# print (idfeatures)
		}

		idfeatures = classification.getMapId(style)

		toHTML['mapid'] = idfeatures['tile_fetcher'].url_format
		toHTML['token'] = idfeatures['token']
	except Exception as e:

		toHTML['mapid'] = 'error'
		raise e

	return JsonResponse(toHTML, safe=False)




def computeArea(dataset, poly=None):
	loaddef()
	if poly:
		galamsey_aoi = poly
	else:
		galamsey_aoi = ee.FeatureCollection("users/eopokukwarteng/sef_pilot")
	dataset = ee.Image(dataset)
	area = dataset.multiply(ee.Image.pixelArea()).divide(1000*1000)

	stat = area.reduceRegion(
		**{
			'reducer': ee.Reducer.sum(),
			'geometry': galamsey_aoi,
			'crs': 'EPSG:4326',
			'scale': 30,
			'maxPixels': 1e13
		})


	return stat.getInfo()['classification']


def getsentinel(start,end,coord=None):

	loaddef()
	toHTML={}

	try:
		# # start= request.GET.get('start')
		# # end= request.GET.get('end')

		# datefrom = datetime.strptime(start, "%Y-%m-%d")
		# dateto = datetime.strptime(end, "%Y-%m-%d")


		# AOI = ee.FeatureCollection("users/eopokukwarteng/sef_pilot")
		

		# # AOI=ee.Geometry.Point([-2.7634471830822593,6.291906530887788])
		# traindata = ee.FeatureCollection("users/eopokukwarteng/sef_training")
		# # /Loading Sentinel 2 data and filtering by date and bounds

		# Sentinel2Collection=ee.ImageCollection("COPERNICUS/S2_SR") \
		# 	.filterDate(ee.Date(datefrom), ee.Date(dateto).advance(15, 'day')) \
		# 	.filterBounds(AOI) \
		# 	.filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', 60))\
		# 	.median()\
		# 	.clip(AOI)

		# Sentinel2Collection=ee.Image("users/eopokukwarteng/classification_2021")

		   
	
		# # Select the bands for training
		# bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7','B8','B8A']



		# # trainingGcp = traindata.filter(ee.Filter.lt('random', 0.6));
		# # validationGcp = traindata.filter(ee.Filter.gte('random', 0.6));
		# # Sample the input imagery to get a FeatureCollection of training data.
		# training = Sentinel2Collection.select(bands).sampleRegions(
		#   collection=traindata,
		#   properties=['landcover'],
		#   scale= 100
		# )
		# # print(training, 'training')

		# # Making a Random Forest classifier and training it.
		# classifier= ee.Classifier.smileRandomForest(8).train(
		#   features=training,
		#   classProperty='landcover',
		#   inputProperties=bands
		# )
		# classification= Sentinel2Collection.select(bands).classify(classifier)

		classification=ee.Image("users/eopokukwarteng/classification_2021")

		if coord : 
			classy = classification.clip(coord)
		else:
			classy=classification

		return classy

	except Exception as e:

		raise

def swap(array):
	array[0], array[1] = array[1], array[0]
	return array

def analysistimeseriesView(request):

	loaddef()
	toHTML={}

	Agroforestrycocoa_arr=[]
	Built_arr=[]
	Cocoa_arr=[]
	Cropland_arr=[]
	Forest_arr=[]
	MonoCocoa_arr=[]
	OpenForest_arr=[]
	Water_arr=[]


	try:


		year1 =str(request.GET.get('start'))
		year2 =str(request.GET.get('end'))

		
		
		
		year=[]
		if year1 == year2:
			asd = [year1]
		else:
			asd = [year1,year2]

		status = True
		if request.GET.get("range") == "on" :


			arr =request.GET.get("class")

			arrclass=arr.split (",")


			

			asd = range(int(year1),int(year2)+1)

			status = False


		for aa in asd : 

			# print(aa)
			year.append(aa)
			coords = request.GET.get("coords")

			if coords:
				a = coords.replace("(", "[")
				b = a.replace(")", "]")
				c = b.replace("LatLng", "")


				getbounds = eval('[' + c + ']')

				bound = [swap(aa) for aa in getbounds]

				poly = ee.Geometry.Polygon(bound)

				image=ee.Image("users/eopokukwarteng/classification_"+str(aa)).clip(poly)


			else:

				image=ee.Image("users/eopokukwarteng/classification_"+str(aa))


			if request.GET.get("range") == "on" :

				resultstime = []

				if  'Agroforestrycocoa' in arrclass :
					Agroforestrycocoa=computeArea(image.select('classification').eq(0)) * 100  
					Agroforestrycocoa_arr.append(Agroforestrycocoa)
					

				if  'Built' in arrclass :      
					Built=computeArea(image.select('classification').eq(1)) * 100 

					Built_arr.append(Built)
					

				if  'Cropland' in arrclass :
					Cropland=computeArea(image.select('classification').eq(2)) * 100
					Cropland_arr.append(Cropland)
					
				if  'Forest' in arrclass :
					Forest=computeArea(image.select('classification').eq(3)) * 100
					Forest_arr.append(Forest)
					

				if  'MonoCocoa' in arrclass :
					MonoCocoa=computeArea(image.select('classification').eq(4))
					MonoCocoa_arr.append(MonoCocoa)
					

				if  'OpenForest' in arrclass :
					OpenForest=computeArea(image.select('classification').eq(5)) * 100
					OpenForest_arr.append(OpenForest)

					

				


				# print(resultstime)

			else:
				Agroforestrycocoa=computeArea(image.select('classification').eq(0)) * 100        
				Built=computeArea(image.select('classification').eq(1)) * 100 
				Cropland=computeArea(image.select('classification').eq(2)) * 100
				Forest=computeArea(image.select('classification').eq(3)) * 100
				MonoCocoa=computeArea(image.select('classification').eq(4))
				OpenForest=computeArea(image.select('classification').eq(5)) * 100
				Water=computeArea(image.select('classification').eq(6)) * 100

				
				
				# Agroforestrycocoa_arr.append(Agroforestrycocoa)
				# Built_arr.append(Built)
				# Cocoa_arr.append(Cocoa)
				# Cropland_arr.append(Cropland)
				# Forest_arr.append(Forest)
				# MonoCocoa_arr.append(MonoCocoa)
				# OpenForest_arr.append(OpenForest)
				# Water_arr.append(Water)








		if  'Agroforestrycocoa' in arrclass :
			resultstime.append({'name':"Agroforestrycocoa", 'data':Agroforestrycocoa_arr})
		if  'Built' in arrclass :  
			resultstime.append({'name':"Built", 'data':Built_arr})
		if  'Cropland' in arrclass :
			resultstime.append({'name':"Cropland", 'data':Cropland_arr})
		if  'Forest' in arrclass :
			resultstime.append({'name':"Forest",'data': Forest_arr})
		if  'MonoCocoa' in arrclass :
			resultstime.append({'name':"MonoCocoa" , 'data':MonoCocoa_arr})
		if  'OpenForest' in arrclass :
			resultstime.append({'name':"OpenForest" , 'data':OpenForest_arr})



		print(resultstime)
	except Exception as e:

		chart = 'error'
		raise

		 
	
	return render(request, 'rootApp/analysis.html', locals())





def analysisView(request):

	loaddef()
	toHTML={}

	Agroforestrycocoa_arr=[]
	Built_arr=[]
	Cocoa_arr=[]
	Cropland_arr=[]
	Forest_arr=[]
	MonoCocoa_arr=[]
	OpenForest_arr=[]
	Water_arr=[]


	try:


		year1 =str(request.GET.get('start'))
		year2 =str(request.GET.get('end'))

		year=[]
		if year1 == year2:
			asd = [year1]
		else:
			asd = [year1,year2]

		status = True
		if request.GET.get("range") == "on" :

			asd = range(int(year1),int(year2)+1)

			status = False


		for aa in asd : 

			print(aa)
			year.append(aa)
			coords = request.GET.get("coords")

			if coords:
				a = coords.replace("(", "[")
				b = a.replace(")", "]")
				c = b.replace("LatLng", "")


				getbounds = eval('[' + c + ']')

				bound = [swap(aa) for aa in getbounds]

				poly = ee.Geometry.Polygon(bound)

				image=ee.Image("users/eopokukwarteng/classification_"+str(aa)).clip(poly)


			else:

				image=ee.Image("users/eopokukwarteng/classification_"+str(aa))


			# "cyan",    # "Agroforestry Cocoa #0
			# 	"#ED022A" , # "Built"	#1
			# 	"#FFDB5C", # "Cropland"	#2
			# 	"#358221", # "Forest"	#3
			# 	"#87D19E", # "MonoCocoa"	#4
			# 	"#EECFA8", # "OpenForest"	#5
			# 	"#1A5BAB" # "Water"	#6


			if request.GET.get("range") == "on" :
				# Agroforestrycocoa=computeArea(image.select('classification').eq(0)) * 100        
				# Built=computeArea(image.select('classification').eq(1)) * 100 
				Cocoa=computeArea(image.select('classification').eq(0)) * 100
				# Cropland=computeArea(image.select('classification').eq(3)) * 100
				Forest=computeArea(image.select('classification').eq(3)) * 100
				# MonoCocoa=computeArea(image.select('classification').eq(5))
				# OpenForest=computeArea(image.select('classification').eq(6)) * 100
				# Water=computeArea(image.select('classification').eq(7)) * 100


				
				# Agroforestrycocoa_arr.append(Agroforestrycocoa)
				# Built_arr.append(Built)
				Cocoa_arr.append(Cocoa)
				# Cropland_arr.append(Cropland)
				Forest_arr.append(Forest)
				# MonoCocoa_arr.append(MonoCocoa)
				# OpenForest_arr.append(OpenForest)
				# Water_arr.append(Water)

			else:
				Agroforestrycocoa=computeArea(image.select('classification').eq(0)) * 100        
				Built=computeArea(image.select('classification').eq(1)) * 100 
				# Cocoa=computeArea(image.select('classification').eq(2)) * 100
				Cropland=computeArea(image.select('classification').eq(2)) * 100
				Forest=computeArea(image.select('classification').eq(3)) * 100
				MonoCocoa=computeArea(image.select('classification').eq(4))
				OpenForest=computeArea(image.select('classification').eq(5)) * 100
				Water=computeArea(image.select('classification').eq(6)) * 100


				print("***********************")
				print(Agroforestrycocoa)
				print("***********************")
				
				Agroforestrycocoa_arr.append(Agroforestrycocoa)
				Built_arr.append(Built)
				# Cocoa_arr.append(Cocoa)
				Cropland_arr.append(Cropland)
				Forest_arr.append(Forest)
				MonoCocoa_arr.append(MonoCocoa)
				OpenForest_arr.append(OpenForest)
				Water_arr.append(Water)



	except Exception as e:

		chart = 'error'
		raise

		 
	
	return render(request, 'rootApp/analysis.html', locals())






def get_s2_sr_cld_col(aoi, start_date, end_date):
	# Import and filter S2 SR.
	CLOUD_FILTER =70
	s2_sr_col = (ee.ImageCollection('COPERNICUS/S2_SR')
		.filterBounds(aoi)
		.filterDate(start_date, end_date)
		.filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', CLOUD_FILTER)))

	# Import and filter s2cloudless.
	s2_cloudless_col = (ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY')
		.filterBounds(aoi)
		.filterDate(start_date, end_date))

	# Join the filtered s2cloudless collection to the SR collection by the 'system:index' property.
	return ee.ImageCollection(ee.Join.saveFirst('s2cloudless').apply(**{
		'primary': s2_sr_col,
		'secondary': s2_cloudless_col,
		'condition': ee.Filter.equals(**{
			'leftField': 'system:index',
			'rightField': 'system:index'
		})
	}))



# s2_sr_cld_col_eval = get_s2_sr_cld_col(AOI, START_DATE, END_DATE)


def add_cloud_bands(img):
	CLD_PRB_THRESH = 50
	# Get s2cloudless image, subset the probability band.
	cld_prb = ee.Image(img.get('s2cloudless')).select('probability')

	# Condition s2cloudless by the probability threshold value.
	is_cloud = cld_prb.gt(CLD_PRB_THRESH).rename('clouds')

	# Add the cloud probability layer and cloud mask as image bands.
	return img.addBands(ee.Image([cld_prb, is_cloud]))


def add_shadow_bands(img):
	NIR_DRK_THRESH = 0.15
	CLD_PRJ_DIST = 1
	# Identify water pixels from the SCL band.
	not_water = img.select('SCL').neq(6)

	# Identify dark NIR pixels that are not water (potential cloud shadow pixels).
	SR_BAND_SCALE = 1e4
	dark_pixels = img.select('B8').lt(NIR_DRK_THRESH*SR_BAND_SCALE).multiply(not_water).rename('dark_pixels')

	# Determine the direction to project cloud shadow from clouds (assumes UTM projection).
	shadow_azimuth = ee.Number(90).subtract(ee.Number(img.get('MEAN_SOLAR_AZIMUTH_ANGLE')));

	# Project shadows from clouds for the distance specified by the CLD_PRJ_DIST input.
	cld_proj = (img.select('clouds').directionalDistanceTransform(shadow_azimuth, CLD_PRJ_DIST*10)
		.reproject(**{'crs': img.select(0).projection(), 'scale': 100})
		.select('distance')
		.mask()
		.rename('cloud_transform'))

	# Identify the intersection of dark pixels with cloud shadow projection.
	shadows = cld_proj.multiply(dark_pixels).rename('shadows')

	# Add dark pixels, cloud projection, and identified shadows as image bands.
	return img.addBands(ee.Image([dark_pixels, cld_proj, shadows]))




def add_cld_shdw_mask(img):
	BUFFER = 50
	# Add cloud component bands.
	img_cloud = add_cloud_bands(img)

	# Add cloud shadow component bands.
	img_cloud_shadow = add_shadow_bands(img_cloud)

	# Combine cloud and shadow mask, set cloud and shadow as value 1, else 0.
	is_cld_shdw = img_cloud_shadow.select('clouds').add(img_cloud_shadow.select('shadows')).gt(0)

	# Remove small cloud-shadow patches and dilate remaining pixels by BUFFER input.
	# 20 m scale is for speed, and assumes clouds don't require 10 m precision.
	is_cld_shdw = (is_cld_shdw.focal_min(2).focal_max(BUFFER*2/20)
		.reproject(**{'crs': img.select([0]).projection(), 'scale': 20})
		.rename('cloudmask'))

	# Add the final cloud-shadow mask to the image.
	return img_cloud_shadow.addBands(is_cld_shdw)






# s2_sr_cld_col = get_s2_sr_cld_col(AOI, START_DATE, END_DATE)


def apply_cld_shdw_mask(img):
	# Subset the cloudmask band and invert it so clouds/shadow are 0, else 1.
	not_cld_shdw = img.select('cloudmask').Not()

	# Subset reflectance bands and update their masks, return the result.
	return img.select('B.*').updateMask(not_cld_shdw)



# s2_sr_median = (s2_sr_cld_col.map(add_cld_shdw_mask)
#                              .map(apply_cld_shdw_mask)
#                              .median())



def fetchcloudffree(request):
	loaddef()

	toHTML={}
	AOI = ee.FeatureCollection("users/eopokukwarteng/sef_pilot")
	START_DATE = '2020-06-01'
	END_DATE = '2020-06-02'
	

	


	style={'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 2500, 'gamma': 1.1}
	idfeatures = s2_sr_median.getMapId(style)

	toHTML['mapid'] = idfeatures['tile_fetcher'].url_format
	toHTML['token'] = idfeatures['token']
	return JsonResponse(toHTML, safe=False)



	# return s2_sr_median





def getdistrictdet(request):

	status={}
	coords=request.GET.get ("coord")
	if coords:
		a = coords.replace("(", "[")
		b = a.replace(")", "]")
		c = b.replace("LatLng", "")

		getbounds = eval('[' + c + ']')

		bound = [swap(aa) for aa in getbounds][0]

	

		poly = Point(bound[0], bound[1])

		ds=District.objects.get(geom__contains = poly)

		
		status["status"] = '''
				{0}  with a total area of  {1} sq.km
				 '''.format(ds.district.title().replace("Assembly" , "") ,round(ds.geom.area , 5)  )

		status["distcode"]=ds.id  
		
	else:
		status = 0

	return JsonResponse (status, safe=False)


# return render(request, 'rootApp/distinfo.html', locals())














class DistrictView(GeoJSONLayerView):
	model = District
	precision = 4
	simplify = 0.001
	properties = ('district',"district_code")

	# def get_queryset(self):
	# 	qs = super(DistrictView, self).get_queryset()
	# 	# vallen = len(self.kwargs.get('typevalue'))
	# 	if self.kwargs.get('typevalue') != 'NONE':
	# 		qs = qs.filter(id = self.kwargs.get('typevalue'))
	# 	return qs


class ProAreaView(GeoJSONLayerView):
	model = ProtectedArea
	precision = 4
	simplify = 0.001
	properties = ('reserve_na',"area_sqkm")



class studyAreaView(GeoJSONLayerView):
	model = Studyaarea
	precision = 4
	simplify = 0.001
	# properties = ('reserve_na',"area_sqkm")


























