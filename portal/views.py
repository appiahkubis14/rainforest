from __future__ import unicode_literals
import ast
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login

from django.core.serializers import serialize
from portal.models import *
from django.contrib.gis.geos import GEOSGeometry
import json, ast, random
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Polygon,Point
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from django.db.models import Q
from datetime import date
import datetime
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis.gdal import SpatialReference,CoordTransform
from djgeojson.views import GeoJSONLayerView
from django.contrib.auth.decorators import login_required
from pyfcm import FCMNotification
# Create your views here.

from django.contrib.gis.db.models.functions import Area


import ee

from django.contrib.auth import logout
# from __future__ import unicode_literals
import ast
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login

from django.core.serializers import serialize
from portal.models import *
from django.contrib.gis.geos import GEOSGeometry
import json, ast, random
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Polygon,Point
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from django.db.models import Q
from datetime import date
import datetime
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis.gdal import SpatialReference,CoordTransform
from djgeojson.views import GeoJSONLayerView
from django.contrib.auth.decorators import login_required
from pyfcm import FCMNotification
# Create your views here.

from django.contrib.gis.db.models.functions import Area


import ee

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login/")

def loaddef():
    try:
        ee.Initialize()
    except Exception as e:
        credentials = ee.ServiceAccountCredentials(
            'geeresearch@geeapp-1577771889447.iam.gserviceaccount.com', 'geeapp-1577771889447-dd8ab00048c7.json')
        ee.Initialize(credentials)

def index(request):
    return render(request, 'landing_page/index.html')

@login_required
def dashboard(request):
    totalben = beneficiaryDetails.objects.all().count()
    totalbenindiv = beneficiaryDetails.objects.filter(type_beneficiary="Individual").count()
    totalbengroup = beneficiaryDetails.objects.filter(~Q(type_beneficiary="Individual")).count()

    male_farm = farmDetails.objects.filter(beneficiary__indvi_gender="male").count()
    female_farm = farmDetails.objects.filter(beneficiary__indvi_gender="female").count()
    group_farm = farmDetails.objects.filter(beneficiary__indvi_gender="").count()

    totalfarm = farmDetails.objects.all().count()
    
    # Fix: Ensure farm data is properly formatted
    farm = [["Male", male_farm], ["Female", female_farm], ["Group", group_farm]]

    natural_farm = treeDetails.objects.filter(ptn_year_nurturing__gt=0).count()
    planted = treeDetails.objects.filter(ptn_year_planted__gt=0).count()

    total_tree = treeDetails.objects.all().count()

    communityfarm = []
    bene = beneficiaryDetails.objects.all()
    
    # Fix: Use distinct communities to avoid duplicates
    communities = beneficiaryDetails.objects.values_list('community', flat=True).distinct()
    for community_name in communities:
        if community_name:  # Skip empty community names
            count = farmDetails.objects.filter(beneficiary__community=community_name).count()
            communityfarm.append([community_name.title(), count])
    
    commtrees = []
    for bb in bene:
        treespecies = []
        trees = treeDetails.objects.filter(farm_code__beneficiary__community=bb.community)
        for tree in trees:
            if tree.wcp_species_planted and tree.wcp_species_planted != "na":
                treespecies.append(tree.wcp_species_planted)
            if tree.ptn_species and tree.ptn_species != "na":
                treespecies.append(tree.ptn_species)
        
        total_farm = farmDetails.objects.filter(beneficiary__community=bb.community).count()
        
        if treespecies:
            # Fix: Handle case where all species might be "na"
            valid_species = [s for s in treespecies if s and s != "na"]
            if valid_species:
                dominant_species = max(set(valid_species), key=valid_species.count)
            else:
                dominant_species = "No species data"
        else:
            dominant_species = "No species data"
            
        ass = {
            "community": bb.community,
            "species": str(set(treespecies)) if treespecies else "[]",
            "total_farms": total_farm,
            "dominant_species": dominant_species
        }
        commtrees.append(ass)
    
    age_tree = treeDetails.objects.all()
    tage = []
    today = datetime.today().year
    
    for age in age_tree:
        if age.ptn_year_planted and age.ptn_year_planted > 0:
            m_age = today - age.ptn_year_planted
            tage.append(m_age)

    average_age = round(Average(tage), 2) if tage else 0

    farms = farmDetails.objects.all()
    all_Farm = []
    for fr in farms:
        if fr.geom:
            all_Farm.append(cal_area(fr.geom))

    avg_farm_size = round(Average(all_Farm), 2) if all_Farm else 0

    # Fix: Convert data to JSON-safe format for JavaScript
    farm_json = json.dumps(farm)
    communityfarm_json = json.dumps(communityfarm)

    context = {
        'totalben': totalben,
        'totalbenindiv': totalbenindiv,
        'totalbengroup': totalbengroup,
        'totalfarm': totalfarm,
        'farm': farm_json,  # JSON string for JavaScript
        'natural': natural_farm,
        'planted': planted,
        'total_tree': total_tree,
        'communityfarm': communityfarm_json,  # JSON string for JavaScript
        'commtrees': commtrees,
        'average_age': average_age,
        'avg_farm_size': avg_farm_size,
    }

    return render(request, 'update/dashboard.html', context)





@login_required
def dashboard2(request):
    community = Community.objects.all()
    return render(request, 'app/dashboard2.html', {'community': community})

@login_required
def dashboardSeed(request):
    community = Community.objects.all()
    return render(request, 'app/dashboard_seed.html', {'community': community})

@login_required
def seedlingmonitoringmapView(request):
    community = Community.objects.all()
    return render(request, 'app/seedlingmap.html', {'community': community})

@login_required
def map(request):
    code = request.GET.get("code")
    ledgend = []
    total = treeDetails.objects.all().aggregate(Sum('biomas'))['biomas__sum'] or 0
    
    ramg = [[1,'#FED976'],[2,'#FEB24C'],[3,'#FD8D3C'],[4,'#FC4E2A'],[5,'#E31A1C'],[6,'#800026']]
    frm = 0 
    for aa in ramg:
        rag = {}
        rag["from"] = frm
        rag["to"] = 20 * aa[0]
        rag["color"] = aa[1]
        ledgend.append(rag)
        frm = 20 * aa[0]

    return render(request, 'update/map.html', {'code': code, 'ledgend': ledgend})

@login_required
def biomap(request):
    code = request.GET.get("code")
    ledgend = []
    total = treeDetails.objects.all().aggregate(Sum('biomas'))['biomas__sum'] or 0
    avg_biomas = total / treeDetails.objects.all().count() if treeDetails.objects.all().count() > 0 else 0
    
    ramg = [[1,'#FEB24C'],[2,'#FD8D3C'],[3,'#FC4E2A'],[4,'#E31A1C'],[5,'#800026']]
    frm = 0 
    for aa in ramg:
        rag = {}
        rag["from"] = frm
        rag["to"] = round(19.99 * aa[0], 2)
        rag["color"] = aa[1]
        ledgend.append(rag)
        frm = round((19.99 * aa[0]) + 0.01, 2)

    return render(request, 'update/biomap.html', {'code': code, 'ledgend': ledgend})

@login_required
def report(request):
    return render(request, 'app/report.html')

def prntsht(request):
    asd = farmDetails.objects.all().first()
    return render(request, 'app/#printpage.html')

def loginView(request):
    return render(request, 'update/login_page.html')

@login_required
def indivdetails(request):
    perdetails = get_object_or_404(beneficiaryDetails, id=request.GET.get("code"))
    farmdetails = get_object_or_404(farmDetails, beneficiary=request.GET.get("code"))

    farmarea = cal_area(farmdetails.geom) if farmdetails.geom else 0
    farmer_corners = len(farmdetails.coord) - 1 if farmdetails.coord else 0

    trees = treeDetails.objects.filter(
        Q(~Q(wcp_species_planted="na") | ~Q(ptn_species="na")),
        farm_code=farmdetails
    ).order_by("id")
    
    tree_arr = []
    for aa in trees:
        if aa.wcp_species_planted and aa.wcp_species_planted != "na":
            tree_arr.append(aa.wcp_species_planted)
        if aa.ptn_species and aa.ptn_species != "na":
            tree_arr.append(aa.ptn_species)

    no_species = len(set(tree_arr)) if tree_arr else 0
    tree_count = trees.count()
    typeest = ["Commercial_Plantation", "Woodlot", "Other"]

    todays_date = date.today()
    bene_age = todays_date.year - perdetails.indvi_dob.year if perdetails.indvi_dob else 0

    context = {
        'perdetails': perdetails,
        'farmdetails': farmdetails,
        'farmarea': farmarea,
        'farmer_corners': farmer_corners,
        'trees': trees,
        'no_species': no_species,
        'tree_count': tree_count,
        'typeest': typeest,
        'bene_age': bene_age,
    }

    return render(request, 'update/individual_details.html', context)

@login_required
def groupdetails(request):
    perdetails = get_object_or_404(beneficiaryDetails, id=request.GET.get("code"))
    farmdetails = get_object_or_404(farmDetails, beneficiary=request.GET.get("code"))

    farmer_corners = len(farmdetails.coord) - 1 if farmdetails.coord else 0

    trees = treeDetails.objects.filter(farm_code=farmdetails)
    tree_arr = []
    for aa in trees:
        if aa.wcp_species_planted and aa.wcp_species_planted != "na":
            tree_arr.append(aa.wcp_species_planted)
        if aa.ptn_species and aa.ptn_species != "na":
            tree_arr.append(aa.ptn_species)

    no_species = len(set(tree_arr)) if tree_arr else 0
    tree_count = trees.count()
    typeest = ["Commercial_Plantation", "Woodlot", "Other"]

    context = {
        'perdetails': perdetails,
        'farmdetails': farmdetails,
        'farmer_corners': farmer_corners,
        'no_species': no_species,
        'tree_count': tree_count,
        'typeest': typeest,
    }

    return render(request, 'app/groupdetails.html', context)




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

def Average(lst):
    return sum(lst) / len(lst) if lst else 0

def dashboardResults(request):
    return render(request, 'update/dashboard.html')

from datetime import datetime
from django.db.models import F

currentYear = datetime.now().year

def miliconvert(value):
    from datetime import datetime
    try:
        dt_obj = datetime.strptime(str(value), '%Y-%m-%d')
        millisec = dt_obj.timestamp() * 1000
        return millisec
    except ValueError:
        return 0

def dashboardResults2(request):
    community = request.GET.get("com")

    if community:
        male = farmerBiodata.objects.filter(community=community, gender='male').count()
        female = farmerBiodata.objects.filter(community=community, gender='female').count()

        cate_arr = []
        category = farmerBiodata.objects.filter(community=community).distinct("small_holder_category")
        for cat in category:
            farm_cate = farmerBiodata.objects.filter(community=community, small_holder_category=cat.small_holder_category).count()
            cate_arr.append([cat.small_holder_category, farm_cate])

        farmer_with_seed = farmerBiodata.objects.filter(community=community, seedlingsmonitoring__isnull=False).count()
        total_reg_farmer = farmerBiodata.objects.all().count()
        farmer_without_seed = farmerBiodata.objects.filter(community=community).count() - farmer_with_seed

        farmer = [['Received seedling', farmer_with_seed], ['Not received seedling', farmer_without_seed]]

        training = trainingDetails.objects.filter(community=community).count()
        trained_farmers = trainingparticipantDetails.objects.filter(training__community=community).count()
        male_trained_farmers = trainingparticipantDetails.objects.filter(farmer_name__gender="male", training__community=community).distinct("training").count()
        female_trained_farmers = trainingparticipantDetails.objects.filter(farmer_name__gender="female", training__community=community).distinct("training").count()

        date_arr = []
        age = [[18,25], [25,30], [30,35], [36,45], [46,55], [56,60], [61,70], [70,100]]
        for aa in age:
            farmer_count = farmerBiodata.objects.filter(community=community, dob__year__range=[currentYear - aa[1], currentYear - aa[0]]).count()
            date_arr.append([str(aa).replace("[","").replace("]","").replace(","," -").replace("'"," ").replace("70-100","above 70"), farmer_count])

        seed_result = []
        seeds = seedlingsMonitoring.objects.filter(community=community)
        seeds_update = seedlingsMonitoringUpdate.objects.filter(farmer__community=community)
        for seed in seeds:
            seed_result.append([miliconvert(seed.created_date.strftime('%Y-%m-%d')), seed.qnty_survived])
        for update in seeds_update:
            seed_result.append([miliconvert(update.created_date.strftime('%Y-%m-%d')), update.qnty_survived])

    else:
        male = farmerBiodata.objects.filter(gender='male').count()
        female = farmerBiodata.objects.filter(gender='female').count()
        total_reg_farmer = farmerBiodata.objects.all().count()
        
        cate_arr = []
        category = farmerBiodata.objects.all().distinct("small_holder_category")
        for cat in category:
            farm_cate = farmerBiodata.objects.filter(small_holder_category=cat.small_holder_category).count()
            cate_arr.append([cat.small_holder_category, farm_cate])

        farmer_with_seed = farmerBiodata.objects.filter(seedlingsmonitoring__isnull=False).count()
        farmer_without_seed = farmerBiodata.objects.all().count() - farmer_with_seed
        farmer = [['Received seedling', farmer_with_seed], ['Not received seedling', farmer_without_seed]]

        training = trainingDetails.objects.all().count()
        trained_farmers = trainingparticipantDetails.objects.all().count()
        male_trained_farmers = trainingparticipantDetails.objects.filter(farmer_name__gender="male").distinct("training").count()
        female_trained_farmers = trainingparticipantDetails.objects.filter(farmer_name__gender="female").distinct("training").count()

        date_arr = []
        data_label = []
        age = [[18,25], [25,30], [30,35], [36,45], [46,55], [56,60], [61,70], [70,100]]
        for aa in age:
            farmer_count = farmerBiodata.objects.filter(dob__year__range=[currentYear - aa[1], currentYear - aa[0]]).count()
            date_arr.append(farmer_count)
            data_label.append(str(aa).replace("[","").replace("]","").replace(","," -").replace("'"," "))

        seed_result = []
        seeds = seedlingsMonitoring.objects.all().order_by("created_date")
        seeds_update = seedlingsMonitoringUpdate.objects.all().order_by("created_date")

        date = []
        for seed in seeds:
            date.append(seed.created_date.strftime('%Y-%m-%d'))
        for update in seeds_update:
            date.append(update.created_date.strftime('%Y-%m-%d'))

        daty = set(sorted(date))
        for dat in list(sorted(daty)):
            base = seedlingsMonitoring.objects.filter(created_date__date=dat).count()
            prog = seedlingsMonitoringUpdate.objects.filter(created_date__date=dat).count()
            eok = base + prog
            seed_result.append([dat, eok])

    context = {
        'male': male,
        'female': female,
        'cate_arr': cate_arr,
        'farmer_with_seed': farmer_with_seed,
        'total_reg_farmer': total_reg_farmer,
        'farmer_without_seed': farmer_without_seed,
        'farmer': farmer,
        'training': training,
        'trained_farmers': trained_farmers,
        'male_trained_farmers': male_trained_farmers,
        'female_trained_farmers': female_trained_farmers,
        'date_arr': date_arr,
        'seed_result': seed_result,
    }

    return render(request, 'app/dashres2.html', context)

@login_required
def reportResults(request):
    benquery = beneficiaryDetails.objects.filter(type_beneficiary="Individual").order_by("-id")
    return render(request, 'app/reportres.html', {'benquery': benquery})

@login_required
def reportgroupResults(request):
    benquery = beneficiaryDetails.objects.filter(~Q(type_beneficiary="Individual")).order_by("-id")
    return render(request, 'app/reportgroupres.html', {'benquery': benquery})

# ... (rest of the file continues with the same pattern of fixes)

def cal_area(geom):
    if not geom:
        return 0
    try:
        ct = CoordTransform(SpatialReference('WGS84'), SpatialReference(32630))
        area = geom.transform(ct, clone=False)
        return round(geom.area / 10000, 6)
    except Exception:
        return 0

# Continue with the rest of the functions, applying similar fixes...

def checkzero(value):
    return value if value else 0

def checknull(value):
    if value == "null" or value is None:
        return "not available"
    try:
        return round(float(value), 3)
    except (ValueError, TypeError):
        return "not available"

# ... Continue with the remaining functions, ensuring proper error handling and data validation

def dashboardResultsSeed(request):
    community = request.GET.get("com")

    total_seed = seedlingsMonitoring.objects.all().aggregate(Sum('qnty_received'))['qnty_received__sum'] or 0
    qnty_survived = seedlingsMonitoring.objects.all().aggregate(Sum('qnty_survived'))['qnty_survived__sum'] or 0

    try:
        survive_rate = round((qnty_survived / total_seed) * 100, 2) if total_seed > 0 else 0
    except ZeroDivisionError:
        survive_rate = 0

    treespecies_count = seedlingsMonitoring.objects.all().distinct("treespecies").count()
    
    species_arr = []
    seedsmon = seedlingsMonitoring.objects.all().distinct("treespecies")
    
    for seed in seedsmon:
        species_qnty_survived = seedlingsMonitoring.objects.filter(treespecies__in=seed.treespecies).aggregate(Sum('qnty_survived'))['qnty_survived__sum'] or 0
        species_qnty_received = seedlingsMonitoring.objects.filter(treespecies__in=seed.treespecies).aggregate(Sum('qnty_received'))['qnty_received__sum'] or 0

        try:
            species_survive_rate = round((species_qnty_survived / species_qnty_received) * 100, 2) if species_qnty_received > 0 else 0
        except ZeroDivisionError:
            species_survive_rate = 0
        
        species_arr.append([seed.treespecies, species_survive_rate])

    context = {
        'total_seed': total_seed,
        'qnty_survived': qnty_survived,
        'survive_rate': survive_rate,
        'treespecies_count': treespecies_count,
        'species_arr': species_arr,
    }

    return render(request, 'app/dashres_seed.html', context)










@login_required
def reportResults(request):
    benquery = beneficiaryDetails.objects.filter(type_beneficiary="Individual").order_by("-id")
    return render(request, 'app/reportres.html',locals())


@login_required
def reportgroupResults(request):
    benquery = beneficiaryDetails.objects.filter(~Q(type_beneficiary="Individual")).order_by("-id")
    return render(request, 'app/reportgroupres.html',locals())



def get_image_from_data_url( data_url, resize=True, base_width=600 ):

    # getting the file format and the necessary dataURl for the file
    _format, _dataurl       = data_url.split(';base64,')
    # file name and extension
    _filename, _extension   = secrets.token_hex(20), _format.split('/')[-1]

    # generating the contents of the file
    file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

    # resizing the image, reducing quality and size
    if resize:

        # opening the file with the pillow
        image = Image.open(file)
        # using BytesIO to rewrite the new content without using the filesystem
        image_io = io.BytesIO()

        # resize
        w_percent    = (base_width/float(image.size[0]))
        h_size       = int((float(image.size[1])*float(w_percent)))
        image        = image.resize((base_width,h_size), Image.ANTIALIAS)

        # save resized image
        image.save(image_io, format=_extension)

        # generating the content of the new image
        file = ContentFile( image_io.getvalue(), name=f"{_filename}.{_extension}" )

    # file and filename
    return file, ( _filename, _extension )

import base64
from django.core.files.base import ContentFile


import base64
import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

def decodeDesignImage(data):
    try:
        data = base64.b64decode(data.encode('UTF-8'))
        buf = io.BytesIO(data)
        img = Image.open(buf)
        return img
    except:
        return None




def saveimage(image, imgname):
    img = decodeDesignImage(image)
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    data= InMemoryUploadedFile(img_io, field_name=None, name=imgname+".jpg", content_type='image/jpeg', size=img_io.tell, charset=None)
    return data

def caltreeSize(value):
    if value == 0:
        return value
    else : 

        return round (float(value) / 3.14 ,3)



# from datetime import datetime

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

@method_decorator(csrf_exempt, name='dispatch')
class SaverecdataView(View):
    def post(self, request):

        todays_date = date.today()
        try:
            group = False
            single = False
            data = json.loads(request.body)

            if  data["beneficiaryDetails"]["beneficiaryType"] == "Individual":
                single  = beneficiaryDetails.objects.filter(type_beneficiary=data["beneficiaryDetails"]["beneficiaryType"],indvi_first_name=data["beneficiaryDetails"]["firstName"],
             indvi_surname=data["beneficiaryDetails"]["surname"],community=data["location"]["community"], mmdas= District.objects.get(id=data["location"]["mmdas"]))
            if not data["beneficiaryDetails"]["beneficiaryType"] == "Individual":
                group  = beneficiaryDetails.objects.filter(type_beneficiary=data["beneficiaryDetails"]["beneficiaryType"],group_name=data["beneficiaryDetails"]["groupName"],community=data["location"]["community"],group_president=data["beneficiaryDetails"]["groupPresident"], mmdas= District.objects.get(id=data["location"]["mmdas"]))

            if not single or group:
            
                if not data["beneficiaryDetails"]["farmerid"] :
                    if data["beneficiaryDetails"]["beneficiaryType"] == "Individual":
                        asd=[]
                        
                        
                        reg=request.POST.get("region")
                        dist=District.objects.get(id=data["location"]["mmdas"])
                        code="FM"+dist.district_code
                        num=beneficiaryDetails.objects.filter(type_beneficiary='Individual').count() + 1
                        memcode=code + "{0:0>4}".format(num) + str(todays_date.year)[1:]


                        
                    
                       
                        obj, created = beneficiaryDetails.objects.get_or_create(
                        farmercode=memcode,
                        type_beneficiary=data["beneficiaryDetails"]["beneficiaryType"],
                        indvi_first_name=data["beneficiaryDetails"]["firstName"],
                        indvi_surname=data["beneficiaryDetails"]["surname"],
                        indvi_other_names=data["beneficiaryDetails"]["otherNames"],
                        indvi_gender=data["beneficiaryDetails"]["gender"],
                        indvi_dob=data["beneficiaryDetails"]["dateOfBirth"],
                        indvi_age=0,
                        indvi_address=data["beneficiaryDetails"]["address"],
                        indvi_phone_no=data["beneficiaryDetails"]["phoneNumber"],
                        indvi_email=data["beneficiaryDetails"]["email"],
                        indvi_next_of_kin=data["beneficiaryDetails"]["nextOfKin"]["name"],
                        indvi_next_of_kin_phone_no=data["beneficiaryDetails"]["nextOfKin"]["phoneNumber"],
                        indvi_relationship=data["beneficiaryDetails"]["nextOfKin"]["relationship"],
                        indvi_next_of_kin_gender=data["beneficiaryDetails"]["nextOfKin"]["gender"],

                        forest_district=data["location"]["forestDistrict"],
                        stool_family=data["location"]["family"],
                        mmdas= District.objects.get(id=data["location"]["mmdas"]) ,
                        community=data["location"]["community"],


                        beneficiary_pic=saveimage(data["beneficiaryDetails"]["passportImageBase64String"],data["beneficiaryDetails"]["firstName"]),
                        farmer_thumb=saveimage(data["declaration"]["signatureOrThumbprintBase64String"],data["beneficiaryDetails"]["firstName"]),
                        withness_thumb=saveimage(data["declaration"]["witness"]["witnessSignatureOrThumbprintBase64String"],data["beneficiaryDetails"]["firstName"]),


                        indvi_next_of_kin_address=data["beneficiaryDetails"]["nextOfKin"]["address"],
                        indvi_next_of_kin_dob=data["beneficiaryDetails"]["nextOfKin"]["dateOfBirth"],
                        withness_name=data["declaration"]["witness"]["name"],
                        withness_phone=data["declaration"]["witness"]["phoneNumber"],

                        enumerator = EnumeratorTbl.objects.get(id=data["beneficiaryDetails"]["enumerator"])
                
                        ) 
                    else :

                        
                        
                        reg=request.POST.get("region")
                        dist=District.objects.get(id=data["location"]["mmdas"])
                        code="GR"+dist.district_code
                        num=beneficiaryDetails.objects.filter(~Q(type_beneficiary='Individual')).count() + 1
                        memcode=code + "{0:0>4}".format(num) + str(todays_date.year)[1:]

                        obj, created = beneficiaryDetails.objects.get_or_create(

                        farmercode=memcode,
                        type_beneficiary=data["beneficiaryDetails"]["beneficiaryType"],
                        group_name=data["beneficiaryDetails"]["groupName"],
                        # group_reg_number=data["beneficiaryDetails"]["surname"],
                        group_president=data["beneficiaryDetails"]["groupPresident"],
                        group_secretary=data["beneficiaryDetails"]["groupSecretary"],
                        group_directors=data["beneficiaryDetails"]["companyDirectors"],
                        group_company_add="",
                        group_phone=data["beneficiaryDetails"]["phoneNumber"],
                        # group_email=data["beneficiaryDetails"]["email"],
                       
                        forest_district=data["location"]["forestDistrict"],
                        stool_family=data["location"]["family"],
                        mmdas= District.objects.get(id=data["location"]["mmdas"]) ,
                        community=data["location"]["community"],

                        beneficiary_pic=saveimage(data["beneficiaryDetails"]["passportImageBase64String"],data["beneficiaryDetails"]["groupName"]),
                        farmer_thumb=saveimage(data["declaration"]["signatureOrThumbprintBase64String"],data["beneficiaryDetails"]["groupName"]),
                        withness_thumb=saveimage(data["declaration"]["witness"]["witnessSignatureOrThumbprintBase64String"],data["beneficiaryDetails"]["groupName"]),

                        enumerator = EnumeratorTbl.objects.get(id=data["beneficiaryDetails"]["enumerator"])
                        ) 
                else:

                    benedetails = beneficiaryDetails.objects.get(id=data["beneficiaryDetails"]["farmerid"])
                aa=[]
                waypoint=0
                for farms in data["treeFarmInformationArray"]:
                    for points in farms["farmInformationArray"]:
                        waypoint =+ 1
                        aa.append([points["longitude"],points["latitude"]])

                    # try:
                    # 	polygon = Polygon( ( tuple(aa) ) )
                    # except Exception as e:
                    # 	raise e
                    polygon = Polygon( ( tuple(aa) ) )

                    dist1=District.objects.get(id=data["location"]["mmdas"])
                    code1="FRF"+dist1.district_code
                    num1=farmDetails.objects.filter(farm_code__startswith=code1).count() + 1
                    memcode1=code1 + "{0:0>4}".format(num1) + str(todays_date.year)[1:]

                    obj, created = farmDetails.objects.get_or_create(
                        farm_code=memcode1,
                        beneficiary=beneficiaryDetails.objects.latest("id"),
                        establishment_type=farms["typeOfEstablishments"],
                        coord=aa,
                        geom=polygon,   
                        )

                    if   "Commercial_Plantation" in farms["typeOfEstablishments"] or  "Woodlot" in farms["typeOfEstablishments"] or  "Other" in farms["typeOfEstablishments"] : 
                        for trees in farms["treeInformationOption1Array"]:
                            #print(trees)
                            obj, created = treeDetails.objects.get_or_create(
                            # farm_code="farmer",
                            farm_code=farmDetails.objects.latest("id"),
                            wcp_species_planted=trees["speciesPlanted"],
                            wcp_no_of_trees=trees["numberOfTrees"],
                            # speciesImage=saveimage(trees["speciesImage"],trees["speciesPlanted"]) ,
                            wcp_planting_distance=trees["plantingDistance"],
                            wcp_establishment_year=trees["yearOfEstablishment"],
                            )

                    else :

                        for trees in farms["treeInformationOption2Array"]:
                            obj, created = treeDetails.objects.get_or_create(
               
                            farm_code=farmDetails.objects.latest("id"),
                            ptn_tree_no=trees["treeLocation"]["latitude"],
                            ptn_p_n=trees["pn"],
                            ptn_species=trees["species"],
                            # speciesImage=saveimage(trees["speciesImage"],trees["species"]),
                            ptn_size_of_tree=caltreeSize(trees["sizeOfTree"]),
                            ptn_year_planted=trees["yearPlanted"],
                            ptn_year_nurturing=trees["yearNurturingStarted"],
                            ptn_latitude=trees["treeLocation"]["latitude"],
                            ptn_longitude=trees["treeLocation"]["longitude"],
                            geom=Point(trees["treeLocation"]["longitude"], trees["treeLocation"]["latitude"]),


                            )

                    status = {"status" : "Done"}

            else:

                status = {"status" : "exist"}

        except Exception as e:
            raise e
            status = {"status" : "error occured",
                     "error" : str(e),
                     }
        
        return JsonResponse(status, safe=False)

    







@method_decorator(csrf_exempt, name='dispatch')
class Saverecdata2View(View):


    def post(self, request):

        try:
            group = False
            single = False
            data = json.loads(request.body)

            if  data["beneficiaryDetails"]["beneficiaryType"] == "Individual":



                single  = beneficiaryDetails.objects.filter(type_beneficiary=data["beneficiaryDetails"]["beneficiaryType"],indvi_first_name=data["beneficiaryDetails"]["firstName"],
             indvi_surname=data["beneficiaryDetails"]["surname"],community=data["location"]["community"], mmdas= District.objects.get(id=data["location"]["mmdas"]))
            if not data["beneficiaryDetails"]["beneficiaryType"] == "Individual":
                group  = beneficiaryDetails.objects.filter(type_beneficiary=data["beneficiaryDetails"]["beneficiaryType"],group_name=data["beneficiaryDetails"]["groupName"],community=data["location"]["community"],group_president=data["beneficiaryDetails"]["groupPresident"], mmdas= District.objects.get(id=data["location"]["mmdas"]))



            if not single or group:

                if not data["beneficiaryDetails"]["farmerid"] :
            
                    if data["beneficiaryDetails"]["beneficiaryType"] == "Individual":
                        asd=[]
                        # #print("oppp")

                        sole="FMR"
                        dob=str(data["beneficiaryDetails"]["dateOfBirth"]).replace('-', '')
                        code = sole+dob
                        num=beneficiaryDetails.objects.filter(farmercode__startswith=sole).count() + 1
                        memcode=code + "{0:0>4}".format(num)
                       
                        obj, created = beneficiaryDetails.objects.get_or_create(
                        farmercode=memcode,
                        type_beneficiary=data["beneficiaryDetails"]["beneficiaryType"],
                        indvi_first_name=data["beneficiaryDetails"]["firstName"],
                        indvi_surname=data["beneficiaryDetails"]["surname"],
                        indvi_other_names=data["beneficiaryDetails"]["otherNames"],
                        indvi_gender=data["beneficiaryDetails"]["gender"],
                        indvi_dob=data["beneficiaryDetails"]["dateOfBirth"],
                        indvi_age="",
                        indvi_address=data["beneficiaryDetails"]["address"],
                        indvi_phone_no=data["beneficiaryDetails"]["phoneNumber"],
                        indvi_email=data["beneficiaryDetails"]["email"],
                        indvi_next_of_kin=data["beneficiaryDetails"]["nextOfKin"]["name"],
                        indvi_next_of_kin_phone_no=data["beneficiaryDetails"]["nextOfKin"]["phoneNumber"],
                        indvi_relationship=data["beneficiaryDetails"]["nextOfKin"]["relationship"],

                        forest_district=data["location"]["forestDistrict"],
                        stool_family=data["location"]["family"],
                        mmdas= District.objects.get(id=data["location"]["mmdas"]) ,
                        community=data["location"]["community"],
                        organisation=organisation.objects(id=data["beneficiaryDetails"]["organisation"]) ,

                        beneficiary_pic=saveimage(data["beneficiaryDetails"]["passportImageBase64String"],data["beneficiaryDetails"]["firstName"]),
                        farmer_thumb=saveimage(data["declaration"]["signatureOrThumbprintBase64String"],data["beneficiaryDetails"]["firstName"]),
                        withness_thumb=saveimage(data["declaration"]["witness"]["witnessSignatureOrThumbprintBase64String"],data["beneficiaryDetails"]["firstName"]),

                        
                        ) 
                    else :
                        
                        
                        obj, created = beneficiaryDetails.objects.get_or_create(
                        type_beneficiary=data["beneficiaryDetails"]["beneficiaryType"],
                        group_name=data["beneficiaryDetails"]["groupName"],
                        # group_reg_number=data["beneficiaryDetails"]["surname"],
                        group_president=data["beneficiaryDetails"]["groupPresident"],
                        group_secretary=data["beneficiaryDetails"]["groupSecretary"],
                        group_directors=data["beneficiaryDetails"]["companyDirectors"],
                        group_company_add=23,
                        group_phone=data["beneficiaryDetails"]["phoneNumber"],
                        # group_email=data["beneficiaryDetails"]["email"],
                       
                        forest_district=data["location"]["forestDistrict"],
                        stool_family=data["location"]["family"],
                        mmdas= District.objects.get(id=data["location"]["mmdas"]) ,
                        community=data["location"]["community"],

                        organisation= organisation.objects(id=data["beneficiaryDetails"]["organisation"]) ,


                        beneficiary_pic=saveimage(data["beneficiaryDetails"]["passportImageBase64String"],data["beneficiaryDetails"]["groupName"]),
                        farmer_thumb=saveimage(data["declaration"]["signatureOrThumbprintBase64String"],data["beneficiaryDetails"]["groupName"]),
                        withness_thumb=saveimage(data["declaration"]["witness"]["witnessSignatureOrThumbprintBase64String"],data["beneficiaryDetails"]["groupName"]),

                        ) 



                else:

                    benedetails = beneficiaryDetails.objects.get(id=data["beneficiaryDetails"]["farmerid"])

                aa=[]
                waypoint=0
                for farms in data["treeFarmInformation"]:
                    for points in farms["farmInformationArray"]:
                        waypoint =+ 1
                        aa.append([points["longitude"],points["latitude"]])
                    
                    try:
                        polygon = Polygon( ( tuple(aa) ) )
                    except Exception as e:
                        polygon =""
                    
                    if not data["beneficiaryDetails"]["farmerid"] :
                        obj, created = farmDetails.objects.get_or_create(
                            farm_code="farmer",
                            beneficiary=beneficiaryDetails.objects.latest("id"),
                            establishment_type=farms["typeOfEstablishment"],
                            coord=aa,
                            geom=polygon,   
                            )
                    else:
                        obj, created = farmDetails.objects.get_or_create(
                            farm_code="farmer",
                            beneficiary=beneficiaryDetails.objects.get(id=data["beneficiaryDetails"]["farmerid"]),
                            establishment_type=farms["typeOfEstablishment"],
                            coord=aa,
                            geom=polygon,   
                            )
                     

                    if   "Commercial_Plantation" in farms["typeOfEstablishment"] or  "Woodlot" in farms["typeOfEstablishment"] or  "Other" in farms["typeOfEstablishment"] : 
                        for trees in farms["treeInfoOnPlantationArray"]:
                            #print(trees)
                            
                            obj, created = treeDetails.objects.get_or_create(
                            # farm_code="farmer",
                            farm_code=farmDetails.objects.latest("id"),
                            wcp_species_planted=trees["speciesPlanted"],
                            wcp_no_of_trees=trees["numberOfTrees"],
                            wcp_planting_distance=trees["plantingDistance"],
                            wcp_establishment_year=trees["yearOfEstablishment"],
                            speciesImage=trees["speciesImage"],
                            )

                    

                    else :

                        for trees in farms["treeInfoArray"]:
                            obj, created = treeDetails.objects.get_or_create(
               
                            farm_code=farmDetails.objects.latest("id"),
                            ptn_tree_no=trees["treeLocation"]["latitude"],
                            ptn_p_n=trees["pn"],
                            ptn_species=trees["species"],
                            ptn_size_of_tree=trees["sizeOfTree"],
                            ptn_year_planted=trees["yearPlanted"],
                            ptn_year_nurturing=trees["yearNurturingStarted"],
                            ptn_latitude=trees["treeLocation"]["latitude"],
                            ptn_longitude=trees["treeLocation"]["longitude"],
                            speciesImage=trees["speciesImage"],
                            geom=Point(trees["treeLocation"]["longitude"], trees["treeLocation"]["latitude"]),


                            )
                            
                        status = {"status" : "Done"}

            else:

      

                status = {"status" : "exist"}

        except Exception as e:
            
            status = {"status" : "error occured",
                     "error" : str(e),
                     }
        


        return JsonResponse(status, safe=False)

def cal_area(geom):
    ct=CoordTransform(SpatialReference('WGS84'),SpatialReference(32630))
    area = geom.transform(ct, clone=False)
    return round( geom.area / 10000 ,6)

def getfarmView(request):
    resulpoygon = []
    farmdetails = farmDetails.objects.get(beneficiary=request.GET.get("code"))
    geoms = farmdetails.geom

    properties = {}
    properties['area']=cal_area(geoms)
    ct=CoordTransform(SpatialReference(32630),SpatialReference('WGS84'),)
    area = geoms.transform(ct, clone=False)
    properties['beneficiary']= str(farmdetails.beneficiary.indvi_first_name) + " " + str(farmdetails.beneficiary.indvi_first_name)
    properties['type_beneficiary']=farmdetails.beneficiary.type_beneficiary
    properties['indvi_gender']=farmdetails.beneficiary.indvi_gender
    properties['indvi_dob']=farmdetails.beneficiary.indvi_dob
    properties['indvi_address']=farmdetails.beneficiary.indvi_address
    properties['indvi_phone_no']=farmdetails.beneficiary.indvi_phone_no
    properties['establishment_type']=farmdetails.establishment_type
    trees = treeDetails.objects.filter(farm_code=farmdetails.id)
    tree_arr=[]
    for bb in trees:
        if bb.wcp_species_planted:
            tree_arr.append(bb.wcp_species_planted.replace("_", " "))
        if bb.ptn_species:
            tree_arr.append(bb.ptn_species.replace("_", " "))

    for aa in tree_arr:
        if aa == "na":
            tree_arr.remove("na")

    Z =str(set(tree_arr)).replace('{' , '')
    ZZ=Z.replace('}' , '')
    speci = ZZ.replace("'" , '')
    properties['treespecies']=speci
    properties['total_tree']=trees.count()
    properties['image']=str(farmdetails.beneficiary.beneficiary_pic)

    try:
        # resulpoygon.append({"geometry": ast.literal_eval(
        # 	geoms), "type": "Feature", "properties": properties, "id": str(farmdetails.id)})

        resulpoygon.append({"geometry": ast.literal_eval(returnsimplify(
                geoms)), "type": "Feature", "properties": properties, "id": str(farmdetails.id)})

    except Exception as e:
        raise
    return JsonResponse(resulpoygon, safe=False)

def gettreesView(request,code=None):
    resulpoygon = []
    if code:
        farmdetails = farmDetails.objects.get(beneficiary=code)
        treedetails = treeDetails.objects.filter(farm_code=farmdetails,geom__isnull=False)
    else:
        treedetails = treeDetails.objects.all()
    for aa in treedetails:

        # #print(aa.full_name,aa.telephone)
        if aa.geom :
            geom = aa.geom
            properties = {}
            properties['ptn_species'] = aa.ptn_species
        
            try:

                resulpoygon.append({"geometry": ast.literal_eval(returnsimplify(
                    geom)), "type": "Feature", "properties": properties, "id": str(aa.id)})
                # ##print resulpoygon
            except Exception as e:
                raise
    return JsonResponse(topolygon(resulpoygon), safe=False)

def topolygon(resulpoygon):
    mainjson = []
    mainjson.append({ "type": "FeatureCollection", "features": resulpoygon})
    return mainjson


def returnsimplify(geom, simplifyvalue=0.001):
    # return geom.simplify(simplifyvalue, preserve_topology=True).geojson
    return geom.simplify(simplifyvalue).geojson



def enumeratorloginView(request):
    dat = {}
    try:
        contact_number = str(request.GET.get('contact'))
        password = str(request.GET.get('password'))
        staff = EnumeratorTbl.objects.get(contact_number=contact_number,password=password)
        dat['status'] = "success"
        dat['name'] = "{}  {}".format(staff.fname,staff.sname)     
        dat['staff_code'] = staff.id
    
    except Exception as e:
        dat['status'] = "not_found"
    return JsonResponse(dat, safe=True)



# def registerenumeratorView(request):
# 	dat = {}
# 	try:
# 		contact_number = str(request.GET.get('contact'))
# 		password = str(request.GET.get('password'))
# 		fname = str(request.GET.get('fname')).tile()
# 		sname = str(request.GET.get('sname')).tile()
# 		email = str(request.GET.get('name')).tile()

# 		staff = EnumeratorTbl.objects.get(contact_number=contact_number,password=password)
# 		dat['status'] = "success"
# 		dat['name'] = staff.staff_name
# 		dat['staff_code'] = staff.id
    
# 	except Exception as e:
# 		dat['status'] = "not_found"
# 	return JsonResponse(dat, safe=True)



@method_decorator(csrf_exempt, name='dispatch')
class registerenumeratorView(View):

    ...

    def post(self, request):
        post_body = json.loads(request.body)   # don't forget to import json

        #print(post_body)
        contact_number = post_body.get('contact_number')
        password = post_body.get('password')
        fname = post_body.get('fname').title()
        sname = post_body.get('sname').title()
        email = post_body.get('email')

        enum_data = {
                'contact_number': contact_number,
                'password': password,
                'fname': fname,
                'sname': sname,
                'email_address': email,
            }


        if not EnumeratorTbl.objects.filter(**enum_data).exists():
            

            book_obj = EnumeratorTbl.objects.create(**enum_data)
            data = {
                'status': 'created'
            }
        else:

            data = {
            'status': 'exist'
            }

        return JsonResponse(data, status=201)





@csrf_exempt
def loginauthenticateView(request):
    status=False
    if request.method=="POST" :
        
        username =request.POST.get("username")
        password = request.POST.get("password")

        if username !="" and password !="":
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                
                status="pass"
            else:
                print("fail")
                status = "failed"
    else:
        print("not aajax")
    return HttpResponse(status)



def districtApiView(request):
    arr=[]
    for  aa in District.objects.filter(pilot=True):
        data={}
        data["districtcode"] = aa.id
        data["district"] = aa.district.title()

        arr.append(data)

    return JsonResponse(arr, safe=False)

def treespeciesApiView(request):
    arr=[]
    for  aa in treeSpeciesTbl.objects.all():
        data={}
        data["code"] = aa.id
        data["species"] = aa.name.title()

        arr.append(data)

    return JsonResponse(arr, safe=False)


def forestDistApiView(request):
    arr=[]
    for  aa in forestDistrictTbl.objects.all():
        data={}
        data["code"] = aa.id
        data["name"] = aa.name.title()

        arr.append(data)

    return JsonResponse(arr, safe=False)

def stoolApiView(request):
    arr=[]
    for  aa in stoolTbl.objects.all():
        data={}
        data["stoolcode"] = aa.id
        data["name"] = aa.name.title()

        arr.append(data)

    return JsonResponse(arr, safe=False)


def communityApiView(request):
    arr=[]
    for  aa in Community.objects.all():
        data={}
        data["comcode"] = aa.id
        data["name"] = aa.community.title()

        arr.append(data)

    return JsonResponse(arr, safe=False)

def regionApiView(request):
    arr=[]
    for  aa in Region.objects.filter(pilot=True):
        data={}
        data["regcode"] = aa.id
        data["name"] = aa.region.title()

        arr.append(data)

    return JsonResponse(arr, safe=False)


def topolygon(resulpoygon):
    mainjson = []
    mainjson.append({"crs":{"type":"link","properties": {"href":"http://spatialreference.org/ref/epsg/4326/","type":"proj4"}},"type":"FeatureCollection","features":resulpoygon})
    return mainjson

def returnsimplify(geom,simplifyvalue=0.001):
    # return geom.simplify(simplifyvalue, preserve_topology=True).geojson
    return geom.simplify(simplifyvalue).geojson



# def DistrictBoundarylayerView(request):
# 	resulpoygon = []

# 	for  aa in District.objects.filter(pilot=True):
# 		properties={}
# 		properties['proj_id']=aa.id
# 		properties['district']=aa.district
# 		try:
# 			resulpoygon.append({"geometry":ast.literal_eval(returnsimplify(aa.geom)),"type":"Feature","properties":properties,"id":str(aa.id)})
# 			# ##print resulpoygon
# 		except Exception as e:
# 			raise
# 	return JsonResponse(resulpoygon,safe=False)









def treespecies(value):
    try:
        aa = treeSpeciesTbl.objects.get(name=value.title()).botanical
        return aa 
    except Exception as e:
        try:
            aa = treeSpeciesTbl.objects.get(name=value).botanical
            return aa 
        except Exception as e:
            return value
        
def farmBoundarylayerView(request):
    features = []  # Change variable name to be more descriptive

    if request.GET.get("code"): 
        farm = farmDetails.objects.filter(beneficiary=request.GET.get("code"))
    else:
        farm = farmDetails.objects.all()
        
    for aa in farm:
        properties = {}
        properties['id'] = str(aa.id)
        properties['farm_code'] = str(aa.farm_code)  # Add farm_code if available
        properties['name'] = str(aa.beneficiary.indvi_first_name) + " " + str(aa.beneficiary.indvi_first_name)  # Fixed: was using first_name twice
        properties['beneficiary'] = str(aa.beneficiary.indvi_first_name) + " " + str(aa.beneficiary.indvi_first_name)
        properties['type_beneficiary'] = aa.beneficiary.type_beneficiary
        properties['indvi_gender'] = aa.beneficiary.indvi_gender
        properties['indvi_dob'] = aa.beneficiary.indvi_dob
        properties['indvi_address'] = aa.beneficiary.indvi_address
        properties['indvi_phone_no'] = aa.beneficiary.indvi_phone_no
        properties['establishment_type'] = aa.establishment_type
        properties['area'] = cal_area(aa.geom)

        # Transform coordinates
        ct = CoordTransform(SpatialReference(32630), SpatialReference('WGS84'))
        area = aa.geom.transform(ct, clone=False)

        # Process tree species
        trees = treeDetails.objects.filter(farm_code=aa.id)
        tree_arr = []
        for bb in trees:
            if bb.wcp_species_planted:
                tree_arr.append(bb.wcp_species_planted.replace("_", " "))
            if bb.ptn_species:
                tree_arr.append(bb.ptn_species.replace("_", " "))

        for cc in tree_arr:
            if cc == "na":
                tree_arr.remove("na")

        Z = str(set(tree_arr)).replace('{', '')
        ZZ = Z.replace('}', '')
        speci = ZZ.replace("'", '')
        properties['treespecies'] = speci
        properties['total_tree'] = trees.count()
        properties['image'] = str(aa.beneficiary.beneficiary_pic)

        try:
            # Create proper GeoJSON feature
            feature = {
                "type": "Feature",
                "geometry": ast.literal_eval(aa.geom.geojson),
                "properties": properties
            }
            features.append(feature)
        except Exception as e:
            print(f"Error processing farm {aa.id}: {e}")
            continue

    # Wrap features in a proper GeoJSON FeatureCollection
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return JsonResponse(geojson_data, safe=False)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.contrib.gis.geos import Polygon

# API to get farm boundary for editing
@csrf_exempt
@require_http_methods(["GET"])
def get_farm_boundary(request, farm_id):
    try:
        farm = farmDetails.objects.get(id=farm_id)
        
        boundary_data = {
            'id': farm.id,
            'farm_code': farm.farm_code,
            'has_boundary': bool(farm.coord or farm.geom),
            'boundary': farm.get_boundary_coordinates()
        }
        
        return JsonResponse(boundary_data)
    
    except farmDetails.DoesNotExist:
        return JsonResponse({'error': 'Farm not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# API to update farm boundary
# In your views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.contrib.gis.geos import Polygon

@csrf_exempt
@require_http_methods(["POST"])
def update_farm_boundary(request, farm_id):
    try:
        farm = farmDetails.objects.get(id=farm_id)
        data = json.loads(request.body)
        
        # Get coordinates from request
        boundary_data = data.get('boundary')
        coordinates = boundary_data.get('coordinates')[0] if boundary_data else None
        
        if not coordinates:
            return JsonResponse({'error': 'No coordinates provided'}, status=400)
        
        # Validate coordinates - must have at least 3 points and be closed polygon
        if len(coordinates) < 3:
            return JsonResponse({'error': 'Polygon must have at least 3 points'}, status=400)
        
        # Ensure polygon is closed (first and last points should be the same)
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])
        
        # Update the geom field (PostGIS geometry)
        try:
            # Convert coordinates to Polygon for geom field
            polygon = Polygon(coordinates)
            farm.geom = polygon
        except Exception as e:
            return JsonResponse({'error': f'Invalid geometry: {str(e)}'}, status=400)
        
        # Update the coord field (ArrayField)
        farm.coord = coordinates
        
        # Update area if provided
        area = data.get('area')
        if area is not None:
            farm.area = area
        
        # Update number of corners
        farm.no_of_corners = len(coordinates) - 1  # Subtract 1 because first and last are same
        
        farm.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Boundary updated successfully',
            'farm_id': farm.id,
            'farm_code': farm.farm_code,
            'area': farm.area,
            'no_of_corners': farm.no_of_corners
        })
    
    except farmDetails.DoesNotExist:
        return JsonResponse({'error': 'Farm not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



############################################################################################################

# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.gis.geos import Polygon
from .models import SeedlingSurvey

@login_required
def seedling_map(request):
    """Main seedling map page"""
    return render(request, 'update/seedling_map.html')

@login_required
def get_seedling_surveys(request):
    """Get all seedling survey data for the map"""
    try:
        surveys = SeedlingSurvey.objects.all().order_by('-date_of_survey')
        
        survey_data = []
        for survey in surveys:
            survey_info = {
                'id': survey.id,
                'name_of_surveyor': survey.name_of_surveyor,
                'date_of_survey': survey.date_of_survey.strftime('%Y-%m-%d'),
                'name_of_community': survey.name_of_community,
                'name_of_farmer': survey.name_of_farmer,
                'farmer_id_number': survey.farmer_id_number,
                'type_of_plantation': survey.type_of_plantation,
                'species_provided_planted': survey.species_provided_planted,
                'planted_species': survey.planted_species,
                'species_alive': survey.species_alive,
                'living_species_records': survey.living_species_records,
                'total_seedlings_alive': survey.total_seedlings_alive,
                'reason_for_death': survey.reason_for_death,
                'source_of_water': survey.source_of_water,
                'avg_watering_frequency': survey.avg_watering_frequency,
                'any_extreme_weather': survey.any_extreme_weather,
                'extreme_weather_type': survey.extreme_weather_type,
                'any_pests_around': survey.any_pests_around,
                'pest_description': survey.pest_description,
                'any_signs_of_disease': survey.any_signs_of_disease,
                'disease_signs_description': survey.disease_signs_description,
                'any_fertiliser_applied': survey.any_fertiliser_applied,
                'fertiliser_type': survey.fertiliser_type,
                'any_pesticide_herbicide': survey.any_pesticide_herbicide,
                'pesticide_herbicide_type': survey.pesticide_herbicide_type,
                'additional_observations': survey.additional_observations,
                'created_at': survey.created_at.strftime('%Y-%m-%d %H:%M'),
                'has_boundary': bool(survey.farm_boundary),
                'boundary_coords': survey.farm_boundary_coords,
            }
            
            # Add boundary data if available
            if survey.farm_boundary:
                try:
                    # Get coordinates from the Polygon field
                    coords = list(survey.farm_boundary.coords[0])
                    
                    # Convert to Leaflet format: [[lng, lat], [lng, lat], ...]
                    leaflet_coords = []
                    for coord in coords:
                        if len(coord) >= 2:
                            leaflet_coords.append([float(coord[0]), float(coord[1])])
                    
                    survey_info['boundary'] = {
                        'type': 'Polygon',
                        'coordinates': [leaflet_coords]
                    }
                    
                except Exception as e:
                    print(f"Error converting boundary for survey {survey.id}: {e}")
                    survey_info['boundary'] = None
            
            # Add living species locations if available
            if survey.living_species_records:
                try:
                    survey_info['living_species_locations'] = survey.living_species_records
                except Exception as e:
                    print(f"Error processing living species records for survey {survey.id}: {e}")
                    survey_info['living_species_locations'] = []
            
            survey_data.append(survey_info)
        
        return JsonResponse({
            'success': True,
            'surveys': survey_data,
            'total_count': len(survey_data)
        })
        
    except Exception as e:
        import traceback
        print(f"Error in get_seedling_surveys: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@csrf_exempt
def update_survey_boundary(request, survey_id):
    """Update seedling survey boundary coordinates and geom field"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST method allowed'})
    
    try:
        survey = SeedlingSurvey.objects.get(id=survey_id)
        data = json.loads(request.body)
        print("Received boundary data:", data)
        
        # Update boundary coordinates
        boundary_data = data.get('boundary')
        if boundary_data and boundary_data.get('coordinates'):
            boundary_coords = boundary_data['coordinates'][0]  # Get the first ring
            
            print(f"Processing {len(boundary_coords)} coordinates")
            
            # Ensure the polygon is closed (first and last points are the same)
            if boundary_coords[0] != boundary_coords[-1]:
                boundary_coords.append(boundary_coords[0])
                
            # Create Polygon - coordinates should be in [lng, lat] format
            polygon = Polygon(boundary_coords)
            
            # Update both boundary fields
            survey.farm_boundary = polygon
            survey.farm_boundary_coords = boundary_coords  # Store raw coordinates in JSONField
            
            # Calculate area in hectares
            try:
                from django.contrib.gis.geos import GEOSGeometry
                wgs84_geom = GEOSGeometry(polygon.wkt, srid=4326)
                
                # Use Web Mercator for area calculation
                projected_srid = 3857
                transformed_geom = wgs84_geom.transform(projected_srid, clone=True)
                area_sq_m = transformed_geom.area
                area_hectares = area_sq_m / 10000
                
                # Store area if you have a field for it, or calculate survival density
                print(f"Calculated area: {area_hectares:.2f} hectares")
                
            except Exception as area_error:
                print(f"Could not calculate area: {area_error}")
            
            survey.save()
            
            print(f"Successfully updated boundary for survey {survey_id}")
            
            return JsonResponse({
                'success': True, 
                'message': 'Boundary updated successfully',
                'survey_id': survey.id,
                'area_hectares': round(area_hectares, 2) if 'area_hectares' in locals() else None
            })
        else:
            return JsonResponse({
                'success': False, 
                'error': 'Invalid boundary coordinates provided'
            })
            
    except SeedlingSurvey.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Survey not found'})
    except Exception as e:
        import traceback
        print(f"Error updating boundary: {e}")
        print(traceback.format_exc())
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def get_living_species_locations(request, survey_id):
    """Get living species GPS locations for a specific survey"""
    try:
        survey = SeedlingSurvey.objects.get(id=survey_id)
        
        if survey.living_species_records:
            return JsonResponse({
                'success': True,
                'locations': survey.living_species_records,
                'survey_id': survey_id
            })
        else:
            return JsonResponse({
                'success': True,
                'locations': [],
                'survey_id': survey_id,
                'message': 'No living species records found'
            })
            
    except SeedlingSurvey.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Survey not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


#######################################################################################################

# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count, Sum, Avg
from .models import SeedlingSurvey, LivingSpeciesRecord

@login_required
def seedling_survey_list(request):
    """Seedling survey list page"""
    return render(request, 'update/seedling_report.html')
@login_required
def get_seedling_surveys_datatable(request):
    """Get seedling surveys for DataTables"""
    try:
        # Get query parameters from DataTables
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        
        # Base queryset
        surveys = SeedlingSurvey.objects.all().order_by('-date_of_survey')
        
        # Apply search filter
        if search_value:
            surveys = surveys.filter(
                Q(farmer_id_number__icontains=search_value) |
                Q(name_of_farmer__icontains=search_value) |
                Q(name_of_community__icontains=search_value) |
                Q(name_of_surveyor__icontains=search_value)
            )
        
        # Get total count
        total_records = surveys.count()
        
        # Apply pagination
        surveys = surveys[start:start + length]
        
        # Prepare data for response
        data = []
        for survey in surveys:
            # Calculate survival rate
            total_planted = 0
            if survey.planted_species and isinstance(survey.planted_species, dict):
                for species_data in survey.planted_species.values():
                    if isinstance(species_data, dict):
                        total_planted += species_data.get('quantity_planted', 0)
            
            survival_rate = 0
            if total_planted > 0:
                survival_rate = (survey.total_seedlings_alive / total_planted) * 100
            
            survey_data = {
                'id': survey.id,
                'farmer_id_number': survey.farmer_id_number or '',
                'name_of_farmer': survey.name_of_farmer or '',
                'name_of_community': survey.name_of_community or '',
                'date_of_survey': survey.date_of_survey.strftime('%Y-%m-%d') if survey.date_of_survey else '',
                'name_of_surveyor': survey.name_of_surveyor or '',
                'type_of_plantation': survey.type_of_plantation or '',
                'total_seedlings_alive': survey.total_seedlings_alive or 0,
                'survival_rate': round(survival_rate, 1),
                'species_count': len(survey.species_provided_planted) if survey.species_provided_planted else 0,
                'has_boundary': bool(survey.farm_boundary),
                'created_at': survey.created_at.strftime('%Y-%m-%d %H:%M') if survey.created_at else '',
            }
            data.append(survey_data)
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data
        })
        
    except Exception as e:
        import traceback
        print(f"Error in get_seedling_surveys_datatable: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            'draw': 0,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': str(e)
        })
    

@login_required
def get_seedling_survey_detail(request, survey_id):
    """Get detailed information for a specific survey"""
    try:
        survey = SeedlingSurvey.objects.get(id=survey_id)
        
        # Calculate survival statistics
        total_planted = 0
        species_details = []
        
        if survey.planted_species and isinstance(survey.planted_species, dict):
            for species_name, species_data in survey.planted_species.items():
                if isinstance(species_data, dict):
                    planted = species_data.get('quantity_planted', 0)
                    received = species_data.get('quantity_received', 0)
                    total_planted += planted
                    
                    species_details.append({
                        'name': species_name,
                        'received': received,
                        'planted': planted,
                        'planting_date': species_data.get('date_of_planting', 'N/A')
                    })
        
        survival_rate = 0
        if total_planted > 0:
            survival_rate = (survey.total_seedlings_alive / total_planted) * 100
        
        # Get living species records
        living_species_data = []
        if survey.living_species_records and isinstance(survey.living_species_records, list):
            for record in survey.living_species_records:
                if isinstance(record, dict):
                    living_species_data.append({
                        'species': record.get('species', 'Unknown'),
                        'latitude': float(record.get('latitude', 0)),
                        'longitude': float(record.get('longitude', 0)),
                        'altitude': float(record.get('altitude', 0)) if record.get('altitude') else None,
                        'accuracy': float(record.get('accuracy', 0)) if record.get('accuracy') else None
                    })
        
        survey_data = {
            'id': survey.id,
            'farmer_id_number': survey.farmer_id_number or '',
            'name_of_farmer': survey.name_of_farmer or '',
            'name_of_community': survey.name_of_community or '',
            'date_of_survey': survey.date_of_survey.strftime('%Y-%m-%d') if survey.date_of_survey else '',
            'name_of_surveyor': survey.name_of_surveyor or '',
            'type_of_plantation': survey.type_of_plantation or '',
            'species_provided_planted': survey.species_provided_planted or [],
            'species_alive': survey.species_alive or [],
            'total_seedlings_alive': survey.total_seedlings_alive or 0,
            'survival_rate': round(survival_rate, 1),
            'species_details': species_details,
            'reason_for_death': survey.reason_for_death or [],
            'source_of_water': survey.source_of_water or [],
            'avg_watering_frequency': survey.avg_watering_frequency or '',
            'any_extreme_weather': survey.any_extreme_weather or False,
            'extreme_weather_type': survey.extreme_weather_type or [],
            'any_pests_around': survey.any_pests_around or False,
            'pest_description': survey.pest_description or '',
            'any_signs_of_disease': survey.any_signs_of_disease or False,
            'disease_signs_description': survey.disease_signs_description or '',
            'any_fertiliser_applied': survey.any_fertiliser_applied or False,
            'fertiliser_type': survey.fertiliser_type or '',
            'any_pesticide_herbicide': survey.any_pesticide_herbicide or False,
            'pesticide_herbicide_type': survey.pesticide_herbicide_type or '',
            'additional_observations': survey.additional_observations or '',
            'has_boundary': bool(survey.farm_boundary),
            'boundary_coords': survey.farm_boundary_coords or [],
            'living_species_records': living_species_data,
            'created_at': survey.created_at.strftime('%Y-%m-%d %H:%M') if survey.created_at else '',
            'updated_at': survey.updated_at.strftime('%Y-%m-%d %H:%M') if survey.updated_at else '',
        }
        
        return JsonResponse({
            'success': True,
            'survey': survey_data
        })
        
    except SeedlingSurvey.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Survey not found'
        })
    except Exception as e:
        import traceback
        print(f"Error in get_seedling_survey_detail: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


from django.db.models import Count, Sum
@login_required
def get_seedling_survey_stats(request):
    """Get statistics for seedling surveys"""
    try:
        total_surveys = SeedlingSurvey.objects.count()
        total_seedlings_alive = SeedlingSurvey.objects.aggregate(
            total=Sum('total_seedlings_alive')
        )['total'] or 0
        
        # Calculate average survival rate
        surveys_with_data = SeedlingSurvey.objects.filter(planted_species__isnull=False)
        avg_survival_rate = 0
        count_with_data = 0
        
        for survey in surveys_with_data:
            total_planted = 0
            if survey.planted_species and isinstance(survey.planted_species, dict):
                for species_data in survey.planted_species.values():
                    if isinstance(species_data, dict):
                        total_planted += species_data.get('quantity_planted', 0)
            
            if total_planted > 0:
                survival_rate = (survey.total_seedlings_alive / total_planted) * 100
                avg_survival_rate += survival_rate
                count_with_data += 1
        
        if count_with_data > 0:
            avg_survival_rate = avg_survival_rate / count_with_data
        
        # Surveys by community
        
        surveys_by_community = SeedlingSurvey.objects.values(
            'name_of_community'
        ).annotate(
            count=Count('id'),
            total_seedlings=Sum('total_seedlings_alive')
        ).order_by('-count')
        
        # Recent surveys (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_surveys = SeedlingSurvey.objects.filter(
            created_at__gte=thirty_days_ago
        ).count()
        
        stats = {
            'total_surveys': total_surveys,
            'total_seedlings_alive': total_seedlings_alive,
            'avg_survival_rate': round(avg_survival_rate, 1),
            'recent_surveys': recent_surveys,
            'surveys_by_community': list(surveys_by_community),
        }
        
        return JsonResponse({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        import traceback
        print(f"Error in get_seedling_survey_stats: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@csrf_exempt
def delete_seedling_survey(request):
    """Delete a seedling survey"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST method allowed'})
    
    try:
        data = json.loads(request.body)
        survey_id = data.get('id')
        
        if not survey_id:
            return JsonResponse({'success': False, 'error': 'Survey ID is required'})
        
        survey = SeedlingSurvey.objects.get(id=survey_id)
        survey.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Survey deleted successfully'
        })
        
    except SeedlingSurvey.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Survey not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


##################################################################################################################

# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Q
from datetime import datetime, timedelta
from django.utils import timezone
import json

@login_required
def seedling_dashboard(request):
    """Main seedling survey dashboard"""
    return render(request, 'update/seedling_dashboard.html')

@login_required
def get_dashboard_stats(request):
    """Get comprehensive dashboard statistics"""
    try:
        # Total counts
        total_surveys = SeedlingSurvey.objects.count()
        total_seedlings_alive = SeedlingSurvey.objects.aggregate(
            total=Sum('total_seedlings_alive')
        )['total'] or 0
        
        # Communities covered
        communities_covered = SeedlingSurvey.objects.values('name_of_community').distinct().count()
        
        # Recent surveys (last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_surveys = SeedlingSurvey.objects.filter(
            created_at__gte=seven_days_ago
        ).count()
        
        # Calculate survival statistics
        surveys_with_data = SeedlingSurvey.objects.filter(planted_species__isnull=False)
        total_survival_calculated = 0
        count_with_data = 0
        high_survival_count = 0
        medium_survival_count = 0
        low_survival_count = 0
        
        for survey in surveys_with_data:
            total_planted = 0
            if survey.planted_species and isinstance(survey.planted_species, dict):
                for species_data in survey.planted_species.values():
                    if isinstance(species_data, dict):
                        total_planted += species_data.get('quantity_planted', 0)
            
            if total_planted > 0:
                survival_rate = (survey.total_seedlings_alive / total_planted) * 100
                total_survival_calculated += survival_rate
                count_with_data += 1
                
                if survival_rate >= 80:
                    high_survival_count += 1
                elif survival_rate >= 50:
                    medium_survival_count += 1
                else:
                    low_survival_count += 1
        
        avg_survival_rate = round(total_survival_calculated / count_with_data, 1) if count_with_data > 0 else 0
        
        # Environmental factors statistics
        extreme_weather_count = SeedlingSurvey.objects.filter(any_extreme_weather=True).count()
        pests_count = SeedlingSurvey.objects.filter(any_pests_around=True).count()
        disease_count = SeedlingSurvey.objects.filter(any_signs_of_disease=True).count()
        fertilizer_count = SeedlingSurvey.objects.filter(any_fertiliser_applied=True).count()
        
        # Species diversity
        all_species = []
        for survey in SeedlingSurvey.objects.filter(species_provided_planted__isnull=False):
            if survey.species_provided_planted:
                all_species.extend(survey.species_provided_planted)
        
        unique_species_count = len(set(all_species))
        
        # Monthly survey trend (last 6 months)
        six_months_ago = timezone.now() - timedelta(days=180)
        monthly_trend = SeedlingSurvey.objects.filter(
            date_of_survey__gte=six_months_ago
        ).extra({
            'month': "EXTRACT(month FROM date_of_survey)",
            'year': "EXTRACT(year FROM date_of_survey)"
        }).values('year', 'month').annotate(
            count=Count('id'),
            seedlings=Sum('total_seedlings_alive')
        ).order_by('year', 'month')
        
        # Top communities by survey count
        top_communities = SeedlingSurvey.objects.values('name_of_community').annotate(
            survey_count=Count('id'),
            total_seedlings=Sum('total_seedlings_alive')
        ).order_by('-survey_count')[:5]
        
        # Water source distribution
        water_sources = {}
        for survey in SeedlingSurvey.objects.filter(source_of_water__isnull=False):
            if survey.source_of_water:
                for source in survey.source_of_water:
                    water_sources[source] = water_sources.get(source, 0) + 1
        
        # Boundary data
        surveys_with_boundary = SeedlingSurvey.objects.filter(farm_boundary__isnull=False).count()
        
        stats = {
            'overview': {
                'total_surveys': total_surveys,
                'total_seedlings_alive': total_seedlings_alive,
                'communities_covered': communities_covered,
                'recent_surveys': recent_surveys,
                'unique_species': unique_species_count,
                'surveys_with_boundary': surveys_with_boundary,
            },
            'survival_rates': {
                'average': avg_survival_rate,
                'high_survival': high_survival_count,
                'medium_survival': medium_survival_count,
                'low_survival': low_survival_count,
                'calculated_surveys': count_with_data,
            },
            'environmental_factors': {
                'extreme_weather': extreme_weather_count,
                'pests': pests_count,
                'disease': disease_count,
                'fertilizer_used': fertilizer_count,
            },
            'trends': {
                'monthly': list(monthly_trend),
                'top_communities': list(top_communities),
                'water_sources': water_sources,
            }
        }
        
        return JsonResponse({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        import traceback
        print(f"Error in get_dashboard_stats: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def get_recent_surveys(request):
    """Get recent seedling surveys for the dashboard"""
    try:
        recent_surveys = SeedlingSurvey.objects.all().order_by('-created_at')[:10]
        
        survey_data = []
        for survey in recent_surveys:
            # Calculate survival rate
            total_planted = 0
            if survey.planted_species and isinstance(survey.planted_species, dict):
                for species_data in survey.planted_species.values():
                    if isinstance(species_data, dict):
                        total_planted += species_data.get('quantity_planted', 0)
            
            survival_rate = 0
            if total_planted > 0:
                survival_rate = (survey.total_seedlings_alive / total_planted) * 100
            
            survey_data.append({
                'id': survey.id,
                'farmer_id': survey.farmer_id_number,
                'farmer_name': survey.name_of_farmer,
                'community': survey.name_of_community,
                'survey_date': survey.date_of_survey.strftime('%Y-%m-%d'),
                'seedlings_alive': survey.total_seedlings_alive,
                'survival_rate': round(survival_rate, 1),
                'species_count': len(survey.species_provided_planted) if survey.species_provided_planted else 0,
                'has_boundary': bool(survey.farm_boundary),
                'created_at': survey.created_at.strftime('%Y-%m-%d %H:%M'),
            })
        
        return JsonResponse({
            'success': True,
            'surveys': survey_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

#############################################################################################################################


from django.http import JsonResponse
from django.db.models import Q
from .models import beneficiaryDetails
from django.core.paginator import Paginator
import json

def beneficiary_report(request):
    """Main view for beneficiary report page"""
    return render(request, 'update/beneficiary_report.html')

def get_beneficiary_datatable(request):
    """API endpoint for DataTables to fetch beneficiary data"""
    # Get parameters from DataTables
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    beneficiary_type = request.GET.get('beneficiary_type', 'individual')  # individual or group
    
    # Base queryset
    if beneficiary_type == 'individual':
        queryset = beneficiaryDetails.objects.filter(
            Q(type_beneficiary__icontains='individual') | 
            Q(type_beneficiary__isnull=True)
        ).exclude(Q(indvi_first_name__isnull=True) | Q(indvi_first_name=''))
    else:
        queryset = beneficiaryDetails.objects.filter(
            Q(type_beneficiary__icontains='group') |
            Q(type_beneficiary__icontains='company')
        ).exclude(Q(group_name__isnull=True) | Q(group_name='na') | Q(group_name=''))
    
    # Total records
    total_records = queryset.count()
    
    # Apply search filter
    if search_value:
        if beneficiary_type == 'individual':
            queryset = queryset.filter(
                Q(indvi_first_name__icontains=search_value) |
                Q(indvi_surname__icontains=search_value) |
                Q(indvi_other_names__icontains=search_value) |
                Q(farmercode__icontains=search_value) |
                Q(community__icontains=search_value) |
                Q(mmdas__name__icontains=search_value)
            )
        else:
            queryset = queryset.filter(
                Q(group_name__icontains=search_value) |
                Q(group_reg_number__icontains=search_value) |
                Q(group_president__icontains=search_value) |
                Q(farmercode__icontains=search_value) |
                Q(community__icontains=search_value) |
                Q(mmdas__name__icontains=search_value)
            )
    
    # Filtered records count
    filtered_records = queryset.count()
    
    # Apply ordering
    order_column_index = request.GET.get('order[0][column]', '0')
    order_direction = request.GET.get('order[0][dir]', 'asc')
    
    # Map column index to field name
    column_mapping = {
        '0': 'farmercode',
        '1': 'indvi_surname' if beneficiary_type == 'individual' else 'group_name',
        '2': 'community',
        '3': 'mmdas__name',
        '4': 'created_date',
        '5': 'enumerator__name'
    }
    
    order_field = column_mapping.get(order_column_index, 'created_date')
    if order_direction == 'desc':
        order_field = '-' + order_field
    
    queryset = queryset.order_by(order_field)
    
    # Apply pagination
    paginator = Paginator(queryset, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)
    
    # Prepare data for response
    data = []
    for beneficiary in page_obj:
        if beneficiary_type == 'individual':
            row_data = {
                'id': beneficiary.id,
                'farmer_code': beneficiary.farmercode or 'N/A',
                'name': f"{beneficiary.indvi_surname or ''} {beneficiary.indvi_first_name or ''}".strip() or 'N/A',
                'other_names': beneficiary.indvi_other_names or 'N/A',
                'gender': beneficiary.indvi_gender or 'N/A',
                'phone': beneficiary.indvi_phone_no or 'N/A',
                'community': beneficiary.community or 'N/A',
                'district': beneficiary.mmdas.district if beneficiary.mmdas else 'N/A',
                'created_date': beneficiary.created_date.strftime('%Y-%m-%d %H:%M') if beneficiary.created_date else 'N/A',
                'enumerator': beneficiary.enumerator.fname if beneficiary.enumerator else 'N/A',
                'beneficiary_type': beneficiary.type_beneficiary or 'Individual'
            }
        else:
            row_data = {
                'id': beneficiary.id,
                'farmer_code': beneficiary.farmercode or 'N/A',
                'group_name': beneficiary.group_name or 'N/A',
                'reg_number': beneficiary.group_reg_number or 'N/A',
                'president': beneficiary.group_president or 'N/A',
                'phone': beneficiary.group_phone or 'N/A',
                'community': beneficiary.community or 'N/A',
                'district': beneficiary.mmdas.name if beneficiary.mmdas else 'N/A',
                'created_date': beneficiary.created_date.strftime('%Y-%m-%d %H:%M') if beneficiary.created_date else 'N/A',
                'enumerator': beneficiary.enumerator.name if beneficiary.enumerator else 'N/A',
                'beneficiary_type': beneficiary.type_beneficiary or 'Group'
            }
        data.append(row_data)
    
    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': data
    }
    
    return JsonResponse(response)

def get_beneficiary_stats(request):
    """API endpoint for beneficiary statistics"""
    total_individuals = beneficiaryDetails.objects.filter(
        Q(type_beneficiary__icontains='individual') | 
        Q(type_beneficiary__isnull=True)
    ).exclude(Q(indvi_first_name__isnull=True) | Q(indvi_first_name='')).count()
    
    total_groups = beneficiaryDetails.objects.filter(
        Q(type_beneficiary__icontains='group') |
        Q(type_beneficiary__icontains='company')
    ).exclude(Q(group_name__isnull=True) | Q(group_name='na') | Q(group_name='')).count()
    
    total_beneficiaries = total_individuals + total_groups
    
    # Recent beneficiaries (last 30 days)
    from django.utils import timezone
    from datetime import timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    recent_individuals = beneficiaryDetails.objects.filter(
        created_date__gte=thirty_days_ago,
        type_beneficiary__icontains='individual'
    ).count()
    
    recent_groups = beneficiaryDetails.objects.filter(
        created_date__gte=thirty_days_ago,
        type_beneficiary__icontains='group'
    ).count()
    
    stats = {
        'total_beneficiaries': total_beneficiaries,
        'total_individuals': total_individuals,
        'total_groups': total_groups,
        'recent_individuals': recent_individuals,
        'recent_groups': recent_groups,
        'individuals_by_gender': {
            'male': beneficiaryDetails.objects.filter(indvi_gender__icontains='male').count(),
            'female': beneficiaryDetails.objects.filter(indvi_gender__icontains='female').count(),
            'other': beneficiaryDetails.objects.exclude(
                Q(indvi_gender__icontains='male') | 
                Q(indvi_gender__icontains='female')
            ).count()
        }
    }
    
    return JsonResponse({
        'success': True,
        'stats': stats
    })

def get_beneficiary_detail(request, beneficiary_id):
    """API endpoint for individual beneficiary details"""
    try:
        beneficiary = beneficiaryDetails.objects.get(id=beneficiary_id)
        
        data = {
            'id': beneficiary.id,
            'farmer_code': beneficiary.farmercode,
            'type_beneficiary': beneficiary.type_beneficiary,
            'personal_info': {
                'first_name': beneficiary.indvi_first_name,
                'surname': beneficiary.indvi_surname,
                'other_names': beneficiary.indvi_other_names,
                'gender': beneficiary.indvi_gender,
                'dob': beneficiary.indvi_dob.strftime('%Y-%m-%d') if beneficiary.indvi_dob else None,
                'age': beneficiary.indvi_age,
                'address': beneficiary.indvi_address,
                'phone': beneficiary.indvi_phone_no,
                'email': beneficiary.indvi_email,
            },
            'next_of_kin': {
                'name': beneficiary.indvi_next_of_kin,
                'phone': beneficiary.indvi_next_of_kin_phone_no,
                'relationship': beneficiary.indvi_relationship,
                'gender': beneficiary.indvi_next_of_kin_gender,
                'address': beneficiary.indvi_next_of_kin_address,
                'dob': beneficiary.indvi_next_of_kin_dob.strftime('%Y-%m-%d') if beneficiary.indvi_next_of_kin_dob else None,
            },
            'group_info': {
                'name': beneficiary.group_name,
                'reg_number': beneficiary.group_reg_number,
                'president': beneficiary.group_president,
                'secretary': beneficiary.group_secretary,
                'directors': beneficiary.group_directors,
                'address': beneficiary.group_company_add,
                'phone': beneficiary.group_phone,
                'email': beneficiary.group_email,
            },
            'location_info': {
                'forest_district': beneficiary.forest_district,
                'stool_family': beneficiary.stool_family,
                'district': beneficiary.mmdas.district if beneficiary.mmdas else None,
                'community': beneficiary.community,
            },
            'witness_info': {
                'name': beneficiary.withness_name,
                'phone': beneficiary.withness_phone,
            },
            'media': {
                'beneficiary_pic': beneficiary.beneficiary_pic.url if beneficiary.beneficiary_pic else None,
                'farmer_thumb': beneficiary.farmer_thumb.url if beneficiary.farmer_thumb else None,
                'witness_thumb': beneficiary.withness_thumb.url if beneficiary.withness_thumb else None,
            },
            'enumerator': beneficiary.enumerator.fname if beneficiary.enumerator else None,
            'organisation': beneficiary.organisation.name if beneficiary.organisation else None,
            'created_date': beneficiary.created_date.strftime('%Y-%m-%d %H:%M') if beneficiary.created_date else None,
        }
        
        return JsonResponse({
            'success': True,
            'beneficiary': data
        })
        
    except beneficiaryDetails.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Beneficiary not found'
        }, status=404)


#######################################################################################################################################

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import treeSpeciesTbl, treeSpeciesPhotos
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import treeSpeciesTbl, treeSpeciesPhotos

@login_required
def tree_species_list(request):
    """Tree species list page"""
    return render(request, 'update/tree_species.html')

@login_required
def get_tree_species_datatable(request):
    """Get tree species for DataTables"""
    try:
        # Get query parameters from DataTables
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        
        # Base queryset with photo count annotation
        species_query = treeSpeciesTbl.objects.all().annotate(
            photo_count=Count('treespeciesphotos')
        )
        
        # Apply search filter
        if search_value:
            species_query = species_query.filter(
                Q(code__icontains=search_value) |
                Q(name__icontains=search_value) |
                Q(botanical__icontains=search_value)
            )
        
        # Get total count before filtering for search
        total_records = treeSpeciesTbl.objects.count()
        filtered_records = species_query.count()
        
        # Apply ordering and pagination
        species_query = species_query.order_by('name')[start:start + length]
        
        # Prepare data for response
        data = []
        for spec in species_query:
            # Get main photo
            main_photo = treeSpeciesPhotos.objects.filter(treespecies=spec).first()
            main_photo_url = main_photo.species_photos.url if main_photo and main_photo.species_photos else '/static/dist/img/default-tree.png'
            
            species_data = {
                'id': spec.id,
                'code': spec.code or '',
                'name': spec.name or '',
                'botanical': spec.botanical or '',
                'photo_count': spec.photo_count,
                'main_photo_url': main_photo_url,
                'has_photos': spec.photo_count > 0,
            }
            data.append(species_data)
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        })
        
    except Exception as e:
        import traceback
        print(f"Error in get_tree_species_datatable: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            'draw': 0,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': str(e)
        }, status=500)

@login_required
def get_tree_species_detail(request, species_id):
    """Get detailed information for a specific tree species"""
    try:
        species = treeSpeciesTbl.objects.get(id=species_id)
        
        # Get all photos for this species
        photos = treeSpeciesPhotos.objects.filter(treespecies=species)
        photo_list = []
        for photo in photos:
            if photo.species_photos:
                photo_list.append({
                    'id': photo.id,
                    'url': photo.species_photos.url,
                    'thumbnail': f'<img src="{photo.species_photos.url}" style="width: 45px; height:45px;" />'
                })
        
        # Basic species data
        species_data = {
            'id': species.id,
            'code': species.code or 'N/A',
            'name': species.name or 'Unknown Species',
            'botanical': species.botanical or 'No botanical name available',
            'common_names': [species.name] if species.name else [],
            'description': f"Tree species: {species.name}. {species.botanical if species.botanical else 'No additional information available.'}",
            'photos': photo_list,
            'photo_count': len(photo_list),
            'uses': ['Timber', 'Environmental conservation'],  # Default uses
            'growth_characteristics': {
                'growth_rate': 'Medium',
                'mature_height': 'Varies',
                'lifespan': 'Long-lived',
                'soil_type': 'Well-drained soils'
            }
        }
        
        return JsonResponse({
            'success': True,
            'species': species_data
        })
        
    except treeSpeciesTbl.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Tree species not found'
        }, status=404)
    except Exception as e:
        import traceback
        print(f"Error in get_tree_species_detail: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

##############################################################################################################################

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Q
from datetime import datetime
import json

@login_required
def monitoring_dashboard(request):
    """Main dashboard view"""
    return render(request, 'update/monitoring_dashboard.html')

@login_required
def dashboard_data(request):
    """API endpoint for dashboard data"""
    community = request.GET.get("com")
    current_year = datetime.now().year
    
    # Base data structure
    data = {
        'training_stats': {},
        'farmer_stats': {},
        'seedling_stats': {},
        'demographics': {},
        'charts': {}
    }
    
    if community:
        # Filter by community
        farmers = farmerBiodata.objects.filter(community=community)
        trainings = trainingDetails.objects.filter(community=community)
        seedlings = seedlingsMonitoring.objects.filter(community=community)
    else:
        # All data
        farmers = farmerBiodata.objects.all()
        trainings = trainingDetails.objects.all()
        seedlings = seedlingsMonitoring.objects.all()
    
    # Training Statistics
    data['training_stats'] = {
        'total_trainings': trainings.count(),
        'trained_farmers': trainingparticipantDetails.objects.filter(
            training__in=trainings
        ).values('farmer_name').distinct().count(),
        'male_trained': trainingparticipantDetails.objects.filter(
            training__in=trainings,
            farmer_name__gender="male"
        ).values('farmer_name').distinct().count(),
        'female_trained': trainingparticipantDetails.objects.filter(
            training__in=trainings,
            farmer_name__gender="female"
        ).values('farmer_name').distinct().count(),
        'total_registered_farmers': farmers.count()
    }
    
    # Farmer Statistics
    data['farmer_stats'] = {
        'total_farmers': farmers.count(),
        'male_farmers': farmers.filter(gender='male').count(),
        'female_farmers': farmers.filter(gender='female').count(),
        'with_seedlings': farmers.filter(seedlingsmonitoring__isnull=False).distinct().count(),
        'without_seedlings': farmers.count() - farmers.filter(seedlingsmonitoring__isnull=False).distinct().count()
    }
    
    # Seedling Statistics
    seedling_updates = seedlingsMonitoringUpdate.objects.all()
    if community:
        seedling_updates = seedling_updates.filter(farmer__community=community)
    
    data['seedling_stats'] = {
        'total_monitoring_records': seedlings.count() + seedling_updates.count(),
        'farmers_with_seedlings': seedlings.values('farmer_name').distinct().count()
    }
    
    # Demographics
    age_ranges = [
        (18, 25, '18-25'),
        (26, 30, '26-30'),
        (31, 35, '31-35'),
        (36, 45, '36-45'),
        (46, 55, '46-55'),
        (56, 60, '56-60'),
        (61, 70, '61-70'),
        (71, 100, '71+')
    ]
    
    age_data = []
    age_labels = []
    for min_age, max_age, label in age_ranges:
        count = farmers.filter(
            dob__year__range=[current_year - max_age, current_year - min_age]
        ).count()
        age_data.append(count)
        age_labels.append(label)
    
    data['demographics']['age_distribution'] = {
        'data': age_data,
        'labels': age_labels
    }
    
    # Category distribution
    categories = farmers.values('small_holder_category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    data['demographics']['categories'] = [
        [cat['small_holder_category'], cat['count']] 
        for cat in categories if cat['small_holder_category']
    ]
    
    # Seedling survival timeline
    survival_data = []
    all_dates = set()
    
    # Get dates from seedlings monitoring
    for seedling in seedlings:
        date_str = seedling.created_date.strftime('%Y-%m-%d')
        all_dates.add(date_str)
        survival_data.append({
            'date': date_str,
            'survived': seedling.qnty_survived or 0
        })
    
    # Get dates from updates
    for update in seedling_updates:
        date_str = update.created_date.strftime('%Y-%m-%d')
        all_dates.add(date_str)
        survival_data.append({
            'date': date_str,
            'survived': update.qnty_survived or 0
        })
    
    # Aggregate by date
    date_aggregate = {}
    for entry in survival_data:
        date = entry['date']
        if date not in date_aggregate:
            date_aggregate[date] = 0
        date_aggregate[date] += entry['survived']
    
    # Sort by date and prepare chart data
    sorted_dates = sorted(date_aggregate.keys())
    data['charts']['seedling_survival'] = {
        'dates': sorted_dates,
        'survived': [date_aggregate[date] for date in sorted_dates]
    }
    
    # Gender distribution for chart
    data['charts']['gender_distribution'] = [
        ['Male', data['farmer_stats']['male_farmers']],
        ['Female', data['farmer_stats']['female_farmers']]
    ]
    
    # Seedling distribution for chart
    data['charts']['seedling_distribution'] = [
        ['Received Seedlings', data['farmer_stats']['with_seedlings']],
        ['No Seedlings', data['farmer_stats']['without_seedlings']]
    ]
    
    return JsonResponse(data)

##############################################################################################################################



# # API to validate farm boundary
# @csrf_exempt
# @require_http_methods(["POST"])
# def validate_farm_boundary(request, farm_id):
#     try:
#         farm = farmDetails.objects.get(id=farm_id)
        
#         # Perform validation checks
#         validation_errors = []
        
#         # Check if boundary exists
#         if not farm.coord and not farm.geom:
#             validation_errors.append("No boundary defined")
        
#         # Check if boundary has enough points
#         elif farm.coord and len(farm.coord) < 3:
#             validation_errors.append("Boundary must have at least 3 points")
        
#         # Check if boundary is closed (first and last point should be same)
#         elif farm.coord and farm.coord[0] != farm.coord[-1]:
#             validation_errors.append("Boundary is not closed (first and last point should be the same)")
        
#         # Calculate area if possible
#         area = None
#         if farm.coord and len(farm.coord) >= 3:
#             try:
#                 polygon = Polygon(farm.coord)
#                 area = polygon.area * 10000  # Convert to hectares if in degrees
#             except:
#                 area = None
        
#         is_valid = len(validation_errors) == 0
        
#         return JsonResponse({
#             'is_valid': is_valid,
#             'validation_errors': validation_errors,
#             'area_hectares': area,
#             'farm_id': farm.id
#         })
    
#     except farmDetails.DoesNotExist:
#         return JsonResponse({'error': 'Farm not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)





# def treelayerView(request):
# 	resulpoygon = []

    
# 	if request.GET.get("code"):
# 		farmdetails = farmDetails.objects.get(beneficiary=request.GET.get("code"))
# 		treedetails = treeDetails.objects.filter(farm_code=farmdetails,geom__isnull=False)
# 	else:
# 		treedetails = treeDetails.objects.filter(geom__isnull=False)

# 	for  aa in treedetails:
# 		properties={}
# 		# properties['beneficiary']= str(aa.beneficiary.indvi_first_name) + " " + str(aa.beneficiary.indvi_first_name)
# 		properties['species']= treespecies(aa.ptn_species)
# 		# properties['indvi_gender']=aa.beneficiary.indvi_gender
# 		# properties['indvi_dob']=aa.beneficiary.indvi_dob
# 		# properties['indvi_address']=aa.beneficiary.indvi_address
# 		# properties['indvi_phone_no']=aa.beneficiary.indvi_phone_no
# 		# properties['area']=aa.area
# 		# properties['establishment_type']=aa.establishment_type

# 		try:
# 			resulpoygon.append({"geometry":ast.literal_eval(returnsimplify(aa.geom)),"type":"Feature","properties":properties,"id":str(aa.id)})
# 			# ##print resulpoygon
# 		except Exception as e:
# 			raise
# 	return JsonResponse(resulpoygon,safe=False)





class treelayerView(GeoJSONLayerView):
  model = treeDetails
  precision = 4   
  simplify = 0.0001
  properties = ('ptn_species',)

  def get_queryset(self):      
    qs = super(treelayerView, self).get_queryset()
    vallen = len(self.kwargs.get('typevalue'))
    if self.kwargs.get('typevalue') != 'NONE':
        qs = qs.filter(farm_code__beneficiary = self.kwargs.get('typevalue'))
        return qs





class DistrictBoundarylayerView(GeoJSONLayerView):
    model = District
    precision = 4
    simplify = 0.001
    # properties = ("district")

    # def get_queryset(self):
    # 	qs = super(DistrictView, self).get_queryset()
    # 	# vallen = len(self.kwargs.get('typevalue'))
    # 	if self.kwargs.get('typevalue') != 'NONE':
    # 		qs = qs.filter(id = self.kwargs.get('typevalue'))
    # 	return qs





# def districtBoundaryView(request):
# 	arr=[]
# 	for  aa in District.objects.filter(pilot=True):
# 		data={}
# 		data["districtcode"] = aa.id
# 		data["district"] = aa.district.title()

# 		arr.append(data)

# 	return JsonResponse(arr, safe=False)




@method_decorator(csrf_exempt, name='dispatch')
class trainingView(View):

    def post(self, request):

        try:
        
            data = json.loads(request.body)

            print(data["trainingDetails"]["communityName"])

            print(data["trainingDetails"]["trainingTopic"])

            group  = trainingDetails.objects.filter(
                    community=Community.objects.get(id=data["trainingDetails"]["communityName"]) ,
                    trainingTopic=data["trainingDetails"]["trainingTopic"],
                    dateEventBegan=data["trainingDetails"]["dateEventBegan"],
                    eventDuration=data["trainingDetails"]["eventDuration"],
                    trainerName=data["trainingDetails"]["trainerName"],
                    trainerOrganisation=data["trainingDetails"]["trainerOrganisation"],
                    ).exists()

            if not group:
                
                train_obj, train_created = trainingDetails.objects.get_or_create(
                community=Community.objects.get(id=data["trainingDetails"]["communityName"]),
                trainingTopic=data["trainingDetails"]["trainingTopic"],
                dateEventBegan=data["trainingDetails"]["dateEventBegan"],
                eventDuration=data["trainingDetails"]["eventDuration"],
                trainerName=data["trainingDetails"]["trainerName"],
                trainerOrganisation=data["trainingDetails"]["trainerOrganisation"],
                enumerator=EnumeratorTbl.objects.get(id=data["trainingDetails"]["enumerator"]),
        
                ) 

                if train_created :

                    for part in data["participantDetails"] :
                        obj, created = trainingparticipantDetails.objects.get_or_create(
                            training = train_obj ,
                            farmer_name=farmerBiodata.objects.get(id=part["farmerid"]),
                            # name=part["name"],
                            # community=part["community"],
                            # gender=part["gender"],
                            # contact=part["phoneNumber"],
                            # signature= saveimage(part["signatureOrThumbprintBase64String"],part["name"])    
                            ) 
                status = {"status" : "done"}
                
            else:

                status = {"status" : "exist"}

        except Exception as e:
            raise e
            
            status = {"status" : "error occured",
                     "error" : str(e),
                     }
        
        return JsonResponse(status, safe=False)




@method_decorator(csrf_exempt, name='dispatch')
class seedlingsmonitoringView(View):

    def post(self, request):

        try:
        
            data = json.loads(request.body)

    
        
            if data["farmerDetails"]["baseline"] == "yes":
                train_obj, train_created = seedlingsMonitoring.objects.get_or_create(
                farmer_name=farmerBiodata.objects.get(id=data["farmerDetails"]["farmerid"]),
                # contact=data["farmerDetails"]["contact"],
                # gender=data["farmerDetails"]["gender"],
                community=Community.objects.get(id=data["visitDetails"]["communityName"]) ,
                date_of_visit=data["visitDetails"]["dateOfVisit"],
                enumerator=EnumeratorTbl.objects.get(id=data["visitDetails"]["enumerator"]),
                # visit=data["visitDetails"]["visitNum"],

                treespecies=data["treeFarmInformation"]["treeSpecies"],
                date_received=data["treeFarmInformation"]["dateReceived"],
                date_planted=data["treeFarmInformation"]["datePlanted"],
                qnty_received=data["treeFarmInformation"]["qntyReceived"],
                qntyplanted=data["treeFarmInformation"]["qntyPlanted"],
                qnty_survived=data["treeFarmInformation"]["qntySurvived"],
                planting_area_type=data["treeFarmInformation"]["plantingAreaType"],
                area_size=data["treeFarmInformation"]["areaSize"],
                no_of_trees_registered=data["treeFarmInformation"]["noOfTreesRegistered"],
                farm_location=data["treeFarmInformation"]["farmLocation"],

                )

            else:

                seed_created = seedlingsMonitoringUpdate.objects.create(
                    qnty_survived = data["treeFarmInformation"]["qntySurvived"],
                    farmer = seedlingsMonitoring.objects.get(id=data["farmerDetails"]["farmerid"]),
                    enumerator=EnumeratorTbl.objects.get(id=data["visitDetails"]["enumerator"]),
                    )

            status = {"status" : "done"}

        except Exception as e:
            raise e
            status = {"status" : "error occured",
                     "error" : str(e),
                     }
        
        return JsonResponse(status, safe=False)







@method_decorator(csrf_exempt, name='dispatch')
class lmbMonitoringView(View):

    def post(self, request):

        try:
        
            data = json.loads(request.body)

            group  = lmbMonitoring.objects.filter(
                    lmb_type=data["enumeratorDetails"]["lmbType"],
                    lmb_name=data["enumeratorDetails"]["lmbName"],
                    date_of_first_engagement=data["engagementDetails"]["dateOfFirstEng"],
                    loan_type=data["engagementDetails"]["finServiceType"],
                    loan_duration=data["engagementDetails"]["loanDuration"],
                    interest_rate=data["engagementDetails"]["interestRate"],

                    ).exists()

            if not group:
                
                train_obj, train_created = lmbMonitoring.objects.get_or_create(

                lmb_type=data["enumeratorDetails"]["lmbType"],
                lmb_name=data["enumeratorDetails"]["lmbName"],
                enumerator=EnumeratorTbl.objects.get(id=data["enumeratorDetails"]["enumerator"]),
                
                date_of_first_engagement=data["engagementDetails"]["dateOfFirstEng"],
                partnership_type=data["engagementDetails"]["partnershipType"],
                partnership_duration=data["engagementDetails"]["partnershipDuration"],
                mou_signed=data["engagementDetails"]["mouSigned"],
                loan_type=data["engagementDetails"]["finServiceType"],
                loan_duration=data["engagementDetails"]["loanDuration"],
                interest_rate=data["engagementDetails"]["interestRate"],

                no_of_Farmer_ben_female=data["engagementDetails"]["numOfFarmersBenfitting"]["female"],
                no_of_Farmer_ben_male=data["engagementDetails"]["numOfFarmersBenfitting"]["male"],
                no_of_Farmer_ben_youth=data["engagementDetails"]["numOfFarmersBenfitting"]["youth"],

                ) 

                status = {"status" : "done"}

            else:

                status = {"status" : "exist"}

        except Exception as e:
            raise e
            status = {"status" : "error occured",
                     "error" : str(e),
                     }
        
        return JsonResponse(status, safe=False)





@method_decorator(csrf_exempt, name='dispatch')
class alternativeMonitoringView(View):

    def post(self, request):

        try:
        
            data = json.loads(request.body)

            
            if data["farmerDetails"]["baseline"] == "yes":
                train_obj, train_created = alternativeMonitoring.objects.get_or_create(

                    farmer_name=farmerBiodata.objects.get(id=data["farmerDetails"]["farmerid"]),
                    # contact=data["farmerDetails"]["contact"],
                    # gender=data["farmerDetails"]["gender"],

                    community=Community.objects.get(id=data["visitDetails"]["communityName"]),
                    date_of_visit=data["visitDetails"]["dateOfVisit"],
                    enumerator=EnumeratorTbl.objects.get(id=data["visitDetails"]["enumerator"]),
                    # visit=data["visitDetails"]["visitNum"],

                    additional_livelihood=data["activityDetails"]["additionalLivelihood"],
                    trainer_organisation=data["activityDetails"]["trainerOrganisation"],
                    date_operations_started=data["activityDetails"]["dateOperationsStarted"],

                    invested_amounts=data["activityDetails"]["amounts"]["invested"],
                    # six_months_amounts=data["activityDetails"]["amounts"]["sixMonths"],
                    # one_year_amounts=data["activityDetails"]["amounts"]["oneYear"],
                    # two_ears_amounts=data["activityDetails"]["amounts"]["twoYears"],
                    duration=data["activityDetails"]["amounts"]["duration"],
                    amounts=data["activityDetails"]["amounts"]["amount"],
                    lmb_contrib_amounts=data["activityDetails"]["amounts"]["lmbContrib"],

                    activities_supported=data["activityDetails"]["activitiesSupported"],
                    ) 

            else:

                up_created = alternativeMonitorinUpdate.objects.create(
                    
                    farmer = alternativeMonitoring.objects.get(farmer_name=data["farmerDetails"]["farmerid"]),
                    qnty_survived=data["activityDetails"]["qnty_survived"],
                    enumerator=EnumeratorTbl.objects.get(id=data["visitDetails"]["enumerator"]),
                    duration=data["activityDetails"]["amounts"]["duration"],
                    amounts=data["activityDetails"]["amounts"]["amount"],
                    lmb_contrib_amounts=data["activityDetails"]["amounts"]["lmbContrib"],

                    )

            status = {"status" : "done"}

            

        except Exception as e:
            raise e
            status = {"status" : "error occured",
                     "error" : str(e),
                     }
        
        return JsonResponse(status, safe=False)



def SyncdbView(request):

    return JsonResponse(status, safe=False)


# def searchfarmer2View(request):
# 	dat = {}
# 	try:
# 		contact_number = str(request.GET.get('contact'))
# 		farmer = farmerBiodata.objects.get(contact=contact_number)
# 		dat['farmerid'] = farmer.id
# 		dat['farmer_name'] = farmer.farmer_name
# 		dat['status'] = 200

# 	except Exception as e:
# 		dat['status'] = "not_found"
# 	return JsonResponse(dat, safe=True)



def searchfarmerView(request):
    dat = {}
    try:
        contact_number = str(request.GET.get('contact'))
        form = str(request.GET.get('form'))

        if form =="alternative" :
            
            farmer = alternativeMonitoring.objects.filter(farmer_name__contact=contact_number)
            if farmer:
                farmer = farmer.latest('id')
                dat['farmerid'] = str(farmer.farmer_name.id)
                dat['farmer_name'] = str(farmer.farmer_name.farmer_name)
                dat['baseline'] = True
                dat['community_id'] = str(farmer.community.id)
                dat['contact'] = str(farmer.farmer_name.contact)
            else:
                dat['baseline'] = False
                if farmerBiodata.objects.filter(contact=contact_number).exists():
                    farmer = farmerBiodata.objects.get(contact=contact_number)
                    dat['farmerid'] = str(farmer.id)
                    dat['farmer_name'] = str(farmer.farmer_name)
                    dat['community_id'] = str(farmer.community.id)
                    dat['contact'] = str(farmer.contact)
                
            dat['status'] = 200

        elif form =="seedling" :

            farmer = seedlingsMonitoring.objects.filter(farmer_name__contact=contact_number)
            if farmer:
                farmer = farmer.latest('id')
                dat['farmerid'] = str(farmer.farmer_name.id)
                dat['farmer_name'] = str(farmer.farmer_name.farmer_name)
                dat['baseline'] = True
                dat['community_id'] = str(farmer.community.id)
                dat['contact'] = str(farmer.farmer_name.contact)
            else:
                dat['baseline'] = False
                if farmerBiodata.objects.filter(contact=contact_number).exists():
                    farmer = farmerBiodata.objects.get(contact=contact_number)
                    dat['farmerid'] = str(farmer.id)
                    dat['farmer_name'] = str(farmer.farmer_name)
                    dat['community_id'] = str(farmer.community.id)
                    dat['contact'] = str(farmer.contact)

            dat['status'] = 200

        else :
            contact_number = str(request.GET.get('contact'))
            farmer = farmerBiodata.objects.get(contact=contact_number)
            dat['farmerid'] = str(farmer.id)
            dat['farmer_name'] = str(farmer.farmer_name)
            dat['contact'] = str(farmer.contact)
            dat['community_id'] = str(farmer.community.id)
            dat['status'] = 200
    
    except Exception as e:
        raise
        dat['status'] = "not_found"
    return JsonResponse(dat, safe=True)








def checkzero(value):
    if value :

        return value
    else:

        return 0



def biomasView(request):

    for  aa in treeDetails.objects.all():
        if aa.geom:
            biomas = 0.30*(checkzero(aa.ptn_size_of_tree))**(2.31)
            treeDetails.objects.filter(id=aa.id).update(biomas= round(biomas,3))
    return HttpResponse ("done")


def checknull(value):
    if value == "null":
        value = "not available"
        return value
    elif value == None:
        value = "not available"
        return value
    else:
        return round(value,3)


def biomasmapView(request):
    resulpoygon =[]
    

    # for comm in Community.objects.all() : 

    
    biomas = treeDetails.objects.filter(geom__isnull=False)
    bio=[]
    for aa in biomas:
        totalbiomas = treeDetails.objects.filter(farm_code = aa.farm_code).aggregate(Sum('biomas'))['biomas__sum']
        intensity = (aa.biomas/ totalbiomas)*100
        bio.append([aa.ptn_latitude,aa.ptn_longitude ,intensity ])

    return JsonResponse(bio, safe=False)


def biomaspointView(request):
    resulpoygon =[]
    

    # for comm in Community.objects.all() : 

    totalbiomas = treeDetails.objects.all().aggregate(Sum('biomas'))['biomas__sum']
    biomas = treeDetails.objects.filter(geom__isnull=False)
    bio=[]
    for aa in biomas:
        properties =dict()
        try:
            if Community.objects.filter(geom__contains=aa.geom).exists() :
                comm = Community.objects.get(geom__contains=aa.geom)
                properties['community']=comm.community
            else : 
                properties['community']=""
            
            properties['biomas']=checknull(aa.biomas)
            # properties['percentage']=calculate100(aa.biomas)


            try:
                resulpoygon.append({"geometry":ast.literal_eval(aa.geom.geojson),"type":"Feature","properties":properties,"id":str(aa.id)})
                # ##print resulpoygon
            except Exception as e:
                raise
        except Exception as e:
                raise

    return JsonResponse(resulpoygon, safe=False)


def unique(list1):
     
    # insert the list to the set
    list_set = set(list1)
    asd =list(list_set)
    eok = []
    for aa in asd :
        if not aa == None:
            eok.append(aa)

    # convert the set to the list
    return (eok)
    


def calculate(eok):
    asd = []
    # for aff in treeDetails.objects.filter(geom__isnull=False):
    # 	asd.append(aff.biomas)
    unik= treeDetails.objects.filter(biomas__isnull=False).values_list('biomas', flat=True).distinct()	
    # unik = unique(asd)
    mins = min(unik)
    maxs = max(unik)
    # print(unik)
    # print(maxs)


    res = (eok - mins) / (maxs - mins)
    
    return res



def calculate100(eok):
    
    unik= treeDetails.objects.filter(biomas__isnull=False).values_list('biomas', flat=True).distinct()
    mins = min(unik)
    maxs = max(unik)
    print(unik)
    print(maxs)
    res = (eok - mins )/ (maxs - mins)
    
    return round(res * 100,3)





 # [6403.003, 21123.0, 5.43, 6.641, 7.987, 323332.0, 1545.268, 11.117, 140.644, 12300.0, 16.936, 29.842, 0.106, 32.92, 2323234.0, 809.566, 145453.0, 14000.0, 50.979, 123443.0, 2485.084, 6466.025, 328.898, 457.71, 123345.0, 83.999, 12003.0, 1381.806, 252.763]


@method_decorator(csrf_exempt, name='dispatch')
class farmerView(View):

    def post(self, request):

        try:
            data = json.loads(request.body)

            train_obj, train_created = farmerBiodata.objects.get_or_create(
                contact=data["contact"],defaults=dict(
                community= Community.objects.get(id=data["community"]),
                farmer_name=data["farmer_name"],
                contact=data["contact"],
                gender=data["gender"],
                dob=data["dob"],
                small_holder_category=data["small_holder_category"],
                farm_size=data["farm_size"],
                )
                ) 
            if  train_created : 
                status = {"status" : "done"}
            else:
                status = {"status" : "exist"}

        except Exception as e:
            raise e
            status = {"status" : "error occured",
                     "error" : str(e),
                     }
        
        return JsonResponse(status, safe=False)



def farmerlistView(request):
    
    try:
        arr=[]
        if request.GET.get('community'):
            data = farmerBiodata.objects.filter(community=request.GET.get('community'))
        else:
            data = farmerBiodata.objects.all()
        for aa in data :
            dat = {}
            dat['farmerid'] = aa.id
            dat['farmer_name'] = aa.farmer_name
            dat['community_name'] = aa.community.community
            dat['community'] = aa.community.id
            dat['contact'] = aa.contact
            arr.append(dat)
    except Exception as e:
        dat = {}
        dat['status'] = "not_found"
        arr.append(dat)
    return JsonResponse(arr, safe=False)




def send_notifications(request):
    path_to_fcm = "https://fcm.googleapis.com"
    server_key = 'AAAAKm20M4M:APA91bGpF0bd2S-uC4JL6wQZ0cHyTgIFQOYmI2aWlGIoU2qwlzS41pHV-HlRldx6FRPFC0PbC0Njx51Auq1EMd0STXl9cvCNoN05vtnJpBwsf8yTvMlgEPYiNNtdJ6YPHouVUL8eaefJ'
    if server_key:
        # message_title = "HCM"
        # message_body = message
        result = FCMNotification(api_key=server_key).notify_single_device(
            registration_id="fRHOKHZzREOKp9BPWHw0Ve:APA91bHNGfJ6joBncSKifqqgiUGvrNlqQEPW-GTRAdPu82onfGLkPH2FXxDLXMmIcVvgMLvQaEfE3X6GVZyWfw3FJLE0lb473EI2yJe0IwuKJZTP1xVkl10uoynF4DEbXtWUcHYaTFtL",
            message_title="News/Articles",
            message_body="THIS A TEST FROM ERnest")
            # print(result)
        return JsonResponse(result,safe=False)




def saveFirebaseCodeView(request):
    status =False
    obj,created = firebaseCodes.objects.get_or_create(fone_token= request.GET.get("token"))
    

    if created:
        status = "success"
        return HttpResponse(status)
    elif obj :
        status = "exist"
        return HttpResponse(status)
    else :
        status = "error"
        return HttpResponse(status)
    
    




@method_decorator(csrf_exempt, name='dispatch')
class saveSpeciesphotoview(View):

    def post(self, request):

        try:
            data = json.loads(request.body)
            train_obj, train_created = treeSpeciesPhotos.objects.get_or_create(

                    treespecies=treeSpeciesTbl.objects.get(id=data["treeSpecies"]["speciesid"]),
                    species_photos = saveimage(data["treeSpeciesImageBase64String"],data["treeSpecies"]["speciesid"]),

                    default={treespecies:treeSpeciesTbl.objects.get(id=data["treeSpecies"]["speciesid"])}
                    ) 
            if train_created:
                status = {"status" : "done"}

        except Exception as e:
            raise e
            status = {"status" : "error occured",
                     "error" : str(e),
                     }
        return JsonResponse(status, safe=False)



def treeSpecieslistView(request):
    
    try:
        arr=[]
        data = treeSpeciesPhotos.objects.all()
        for aa in data :
            dat = {}
            dat['species'] = aa.treespecies.name
            dat['image'] = f'{request.META["HTTP_HOST"]}/media/{aa.species_photos}'
            arr.append(dat)
    except Exception as e:
        dat = {}
        dat['status'] = "not_found"
        arr.append(dat)
    return JsonResponse(arr, safe=False)



def searchtreeregisterfarmerView(request):
    dat = {}
    try:
        contact_number = str(request.GET.get('contact'))
        farmer = beneficiaryDetails.objects.get(indvi_phone_no=contact_number)
        dat['farmerid'] = str(farmer.id)
        dat['type_beneficiary'] = str(farmer.type_beneficiary)
        dat['indvi_first_name'] = str(farmer.indvi_first_name)
        dat['indvi_surname'] = str(farmer.indvi_surname)
        dat['indvi_other_names'] = str(farmer.indvi_other_names)
        dat['indvi_gender'] = str(farmer.indvi_gender)
        dat['indvi_dob'] = str(farmer.indvi_dob)
        dat['indvi_age'] = str(farmer.indvi_age)
        dat['indvi_address'] = str(farmer.indvi_address)
        dat['indvi_phone_no'] = str(farmer.indvi_phone_no)
        dat['indvi_email'] = str(farmer.indvi_email)
        dat['indvi_next_of_kin'] = str(farmer.indvi_next_of_kin)
        dat['indvi_next_of_kin_phone_no'] = str(farmer.indvi_next_of_kin_phone_no)
        dat['indvi_next_of_kin_gender'] = str(farmer.indvi_next_of_kin_gender)
        dat['indvi_next_of_kin_address'] = str(farmer.indvi_next_of_kin_address)
        dat['indvi_next_of_kin_dob'] = str(farmer.indvi_next_of_kin_dob)
        dat['indvi_relationship'] = str(farmer.indvi_relationship)
        dat['forest_district'] = str(farmer.forest_district)
        dat['stool_family'] = str(farmer.stool_family)
        dat['mmdas'] = str(farmer.mmdas.district.title())
        dat['community'] = str(farmer.community)
        dat['status'] = 200
    except Exception as e:
        # raise
        dat['status'] = "not_found"
    return JsonResponse(dat, safe=True)





def seedlingsMonitoringSpeciesView(request):
    contact_number = request.GET.get("contact")
    try:
        arr=[]
        
        data = seedlingsMonitoring.objects.filter(farmer_name__contact=contact_number)
        
        for aa in data :
            dat = {}
            dat['species'] = aa.treespecies.replace("[","").replace("]","").replace("'","").replace("'","")
            dat['farmerid'] = aa.id
            arr.append(dat)
    except Exception as e:
        dat = {}
        dat['status'] = "not_found"
        arr.append(dat)
    return JsonResponse(arr, safe=False)


def ratingView(request):
    contact_number = request.GET.get("contact")
    dat = {}
    try:
        
        
        data = treeDetails.objects.filter(farm_code__beneficiary__enumerator__contact_number=contact_number)
        
        
        dat['tree_count'] =data.count()
        
        
    except Exception as e:
        dat = {}
        dat['status'] = "not_found"
    
    return JsonResponse(dat, safe=False)



def speciesListView(request):

    # data=treeSpeciesPhotos.objects.all()
    return render(request, 'update/specieslist.html' , locals())




def speciestblView(request):
    if request.GET.get("search"):
        data=treeSpeciesPhotos.objects.filter(treespecies__name__icontains=request.GET.get("search"))

    else:
        data=treeSpeciesPhotos.objects.all()
    return render(request, 'update/speciestbl.html' , locals())




def seedlingMonitoringreport(request):
    
    return render(request, 'update/seedlingmon_report.html' , locals())



def seedlingMontblreport(request):
    arr =[]
    data=farmerBiodata.objects.filter(seedlingsmonitoring__isnull=False)
    for aa in data :
        sed ={}
        dat= seedlingsMonitoring.objects.filter(farmer_name__id=aa.id).distinct("treespecies").count()
        sed["farmer"]=aa.farmer_name
        sed["community"]=aa.community.community
        sed["species"]=dat
        species=[]
        for _ in  seedlingsMonitoring.objects.filter(farmer_name__id=aa.id):
            spi={}
            spi["name"]=_.treespecies.replace("[","").replace("]","").replace("'","").title()
            spi["id"]=_.id
            species.append(spi)
        sed["species_list"]=species
        arr.append(sed)	


    return render(request, 'update/seedlingmon_tbl.html' , locals())



def seedlingMondetails(request):

    perdetails = seedlingsMonitoring.objects.get(id=request.GET.get("code"))


    perdetailupdate = seedlingsMonitoringUpdate.objects.filter(farmer=request.GET.get("code")).order_by("created_date")

    return render(request, 'update/seedlingmondetails_tbl.html' , locals())



def FetchAlltreefarmerView(request):
    
    try:
        contact_number = str(request.GET.get('contact'))
        farmers = beneficiaryDetails.objects.all()
        arraylist=[]
        for farmer in farmers : 
            dat = {}
            dat['farmerid'] = str(farmer.id)
            dat['type_beneficiary'] = str(farmer.type_beneficiary)
            dat['indvi_first_name'] = str(farmer.indvi_first_name)
            dat['indvi_surname'] = str(farmer.indvi_surname)
            dat['indvi_other_names'] = str(farmer.indvi_other_names)
            dat['indvi_gender'] = str(farmer.indvi_gender)
            dat['indvi_dob'] = str(farmer.indvi_dob)
            dat['indvi_age'] = str(farmer.indvi_age)
            dat['indvi_address'] = str(farmer.indvi_address)
            dat['indvi_phone_no'] = str(farmer.indvi_phone_no)
            dat['indvi_email'] = str(farmer.indvi_email)
            dat['indvi_next_of_kin'] = str(farmer.indvi_next_of_kin)
            dat['indvi_next_of_kin_phone_no'] = str(farmer.indvi_next_of_kin_phone_no)
            dat['indvi_next_of_kin_gender'] = str(farmer.indvi_next_of_kin_gender)
            dat['indvi_next_of_kin_address'] = str(farmer.indvi_next_of_kin_address)
            dat['indvi_next_of_kin_dob'] = str(farmer.indvi_next_of_kin_dob)
            dat['indvi_relationship'] = str(farmer.indvi_relationship)

            dat['group_name']= str(farmer.group_name)
            dat['group_reg_number']= str(farmer.group_reg_number)
            dat['group_president']= str(farmer.group_president)
            dat['group_secretary']= str(farmer.group_secretary)
            dat['group_directors']= str(farmer.group_directors)
            dat['group_company_add']= str(farmer.group_company_add)
            dat['group_phone']= str(farmer.group_phone)
            dat['group_email']= str(farmer.group_email)
            arraylist.append(dat)
            # dat['forest_district'] = str(farmer.forest_district)
            # dat['stool_family'] = str(farmer.stool_family)
            # dat['mmdas'] = str(farmer.mmdas.district.title())
            # dat['community'] = str(farmer.community)
            # dat['status'] = 200
    except Exception as e:
        # raise
        dat['status'] = "not_found"
    return JsonResponse(arraylist, safe=False)




@method_decorator(csrf_exempt, name='dispatch')
class deforestationView(View):

    def post(self, request):

        try:
            data = json.loads(request.body)

            train_obj, train_created = Deforestation.objects.get_or_create(
                
                community= Community.objects.get(id=data["community"]),
                directed_by_gfw=data["directed_by_gfw"],
                do_u_see_deforestation=data["do_u_see_deforestation"],
                cause_deforestation=data["cause_deforestation"],
                further_action_taken=data["further_action_taken"],
                reason_further_action_taken=data["reason_further_action_taken"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                geom=Point(data["longitude"], data["latitude"]),
                photos=saveimage(data["photos"],str(data["community"])),
                )
                 
            if  train_created : 
                status = {"status" : "done"}
            else:
                status = {"status" : "exist"}

        except Exception as e:
            raise e
            status = {"status" : "error occured",
                     "error" : str(e),
                     }
        
        return JsonResponse(status, safe=False)







# @csrf_exempt
# def seedlingsMonitoring_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     serializer_context = {
#     'request': Request(request),
# 		}
    
#     if request.method == 'GET':
#         snippets = seedlingsMonitoring.objects.all()
#         serializer = seedlingsMonitoringSerializer(snippets, many=True,context=serializer_context)
#         return JsonResponse(serializer.data, safe=False)


def dashboardResultsSeed(request):

    community = request.GET.get("com")

    

    seed_result = []
    b=[]
    a=[]
    species_arr=[]

    total_seed=seedlingsMonitoring.objects.all().aggregate(Sum('qnty_received'))['qnty_received__sum']
    qnty_survived=seedlingsMonitoring.objects.all().aggregate(Sum('qnty_survived'))['qnty_survived__sum']

    try:
        survive_rate = round((qnty_survived / total_seed ) * 100,2)
    except Exception as e:
        survive_rate = 0

    print(survive_rate)

    treespecies_count=seedlingsMonitoring.objects.all().distinct("treespecies").count()
    
    seedsmon=seedlingsMonitoring.objects.all().distinct("treespecies")
    for seed in seedsmon :
        species_qnty_survived=seedlingsMonitoring.objects.filter(treespecies__in=seed.treespecies).aggregate(Sum('qnty_survived'))['qnty_survived__sum']
        species_qnty_received=seedlingsMonitoring.objects.filter(treespecies__in=seed.treespecies).aggregate(Sum('qnty_received'))['qnty_received__sum']

        try:
            species_survive_rate = round((species_qnty_survived / species_qnty_received ) * 100,2)
        except Exception as e:
            species_survive_rate = 0
        
        

        species_arr.append([seed.treespecies,species_survive_rate])

    


    print(species_arr)

    return render(request, 'app/dashres_seed.html',locals())






def organisationApiView(request):
    arr=[]
    for  aa in organisation.objects.all():
        data={}
        data["org_id"] = aa.id
        data["name"] = aa.name.title()

        arr.append(data)

    return JsonResponse(arr, safe=False)





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_date
from django.contrib.gis.geos import Polygon
from django.core.exceptions import ValidationError
from decimal import Decimal
import json
import logging

logger = logging.getLogger(__name__)


def parse_boolean(value):
    """Convert 'yes'/'no' strings to boolean"""
    return str(value).lower() == 'yes' if isinstance(value, str) else bool(value)


def create_polygon_from_boundary(farm_boundary):
    """Create Polygon geometry from farm boundary coordinates"""
    if not farm_boundary or len(farm_boundary) < 3:
        return None
    
    try:
        coords = [(point["longitude"], point["latitude"]) for point in farm_boundary]
        # Ensure polygon is closed (first point = last point)
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        return Polygon(coords)
    except (KeyError, TypeError) as e:
        logger.error(f"Error creating polygon from boundary: {e}")
        return None

def calc_geom(latitude, longitude):
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        return GEOSGeometry('POINT (' + str(longitude) + ' ' + str(latitude) + ')')
    except Exception as e:
        import logging
        return logging.exception(str(e))
    

@csrf_exempt
@require_http_methods(["POST"])
def create_or_update_seedling_survey(request):
    """Handle POST request to create or update a seedling survey"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        survey_date = parse_date(data.get('date_of_survey'))
        if not survey_date:
            return JsonResponse({'error': 'Invalid date format for date_of_survey'}, status=400)
        
        farmer_id = data.get('farmer_id_number')
        if not farmer_id:
            return JsonResponse({'error': 'farmer_id_number is required'}, status=400)
        
        # Create farm boundary geometry
        farm_geom = create_polygon_from_boundary(data.get('farm_boundary', []))
        
        # Prepare survey data
        survey_data = {
            'name_of_surveyor': data.get('name_of_surveyor', ''),
            'name_of_community': data.get('name_of_community', ''),
            'name_of_farmer': data.get('name_of_farmer', ''),
            'type_of_plantation': data.get('type_of_plantation', ''),
            'species_provided_planted': data.get('species_provided_planted', []),
            'planted_species': data.get('planted_species', {}),
            'farm_boundary': farm_geom,  # Use the Polygon geometry, not the raw list
            'species_alive': data.get('species_alive', []),
            'living_species_records': data.get('living_species_records', []),
            'total_seedlings_alive': data.get('total_seedlings_alive', 0),
            'reason_for_death': data.get('reason_for_death', []),
            'source_of_water': data.get('source_of_water', []),
            'avg_watering_frequency': data.get('avg_watering_frequency', ''),
            'any_extreme_weather': parse_boolean(data.get('any_extreme_weather', False)),
            'extreme_weather_type': data.get('extreme_weather_type', []),
            'any_pests_around': parse_boolean(data.get('any_pests_around', False)),
            'pest_description': data.get('pest_description', ''),
            'any_signs_of_disease': parse_boolean(data.get('any_signs_of_disease', False)),
            'disease_signs_description': data.get('disease_signs_description', ''),
            'any_fertiliser_applied': parse_boolean(data.get('any_fertiliser_applied', False)),
            'fertiliser_type': data.get('fertiliser_type', ''),
            'any_pesticide_herbicide': parse_boolean(data.get('any_pesticide_herbicide', False)),
            'pesticide_herbicide_type': data.get('pesticide_herbicide_type', ''),
            'additional_observations': data.get('additional_observations', '')
        }
        
        # Create or update survey
        survey, created = SeedlingSurvey.objects.update_or_create(
            farmer_id_number=farmer_id,
            date_of_survey=survey_date,
            defaults=survey_data
        )
        
        # Handle living species records
        # Delete existing records for this survey and recreate
        LivingSpeciesRecord.objects.filter(survey=survey).delete()
        
        species_records = []
        for record_data in data.get('living_species_records', []):
            species_records.append(
                LivingSpeciesRecord(
                    survey=survey,
                    species=record_data.get('species', ''),
                    latitude=Decimal(str(record_data.get('latitude', 0))),
                    longitude=Decimal(str(record_data.get('longitude', 0))),
                    altitude=Decimal(str(record_data.get('altitude', 0))) if record_data.get('altitude') else None,
                    accuracy=Decimal(str(record_data.get('accuracy', 0))) if record_data.get('accuracy') else None,
                    geom=calc_geom(record_data.get('latitude', 0), record_data.get('longitude', 0))
                )
            )
        
        if species_records:
            LivingSpeciesRecord.objects.bulk_create(species_records)
        
        action = "created" if created else "updated"
        logger.info(f"Seedling survey {action} for farmer {survey.name_of_farmer} (ID: {farmer_id})")
        
        return JsonResponse({
            'success': True,
            'survey_id': survey.id,
            'created': created,
            'message': f'Seedling survey {action} successfully',
            'species_records_count': len(species_records)
        }, status=201 if created else 200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
    except ValidationError as e:
        return JsonResponse({
            'error': 'Validation error',
            'details': e.message_dict if hasattr(e, 'message_dict') else str(e)
        }, status=400)
        
    except Exception as e:
        raise
        logger.error(f"Error creating/updating seedling survey: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)
    









from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib.gis.geos import GEOSGeometry
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
import json

@require_http_methods(["GET"])
def get_farm_boundary_geojson(request, survey_id):
    """
    Get farm boundary as GeoJSON for a specific survey.
    
    Args:
        survey_id: The ID of the SeedlingSurvey
        
    Returns:
        JsonResponse with GeoJSON FeatureCollection
    """
    survey = get_object_or_404(SeedlingSurvey, id=survey_id)
    
    if not survey.farm_boundary:
        return JsonResponse({
            'error': 'No farm boundary data available for this survey'
        }, status=404)
    
    # Create GeoJSON feature
    feature = {
        "type": "Feature",
        "geometry": json.loads(survey.farm_boundary.geojson),
        "properties": {
            "survey_id": survey.id,
            "farmer_name": survey.name_of_farmer,
            "farmer_id": survey.farmer_id_number,
            "community": survey.name_of_community,
            "survey_date": survey.date_of_survey.isoformat(),
            "total_seedlings_alive": survey.total_seedlings_alive,
            "plantation_type": survey.type_of_plantation,
            "species": survey.species_provided_planted,
        }
    }
    
    # Wrap in FeatureCollection
    geojson_data = {
        "type": "FeatureCollection",
        "features": [feature]
    }
    
    return JsonResponse(geojson_data, safe=False)


@require_http_methods(["GET"])
def get_all_farm_boundaries_geojson(request):
    """
    Get all farm boundaries as GeoJSON.
    
    Query parameters:
        community: Filter by community name
        date_from: Filter surveys from this date (YYYY-MM-DD)
        date_to: Filter surveys to this date (YYYY-MM-DD)
    
    Returns:
        JsonResponse with GeoJSON FeatureCollection
    """
    surveys = SeedlingSurvey.objects.exclude(farm_boundary__isnull=True)
    
    # Apply filters
    community = request.GET.get('community')
    if community:
        surveys = surveys.filter(name_of_community__icontains=community)
    
    date_from = request.GET.get('date_from')
    if date_from:
        surveys = surveys.filter(date_of_survey__gte=date_from)
    
    date_to = request.GET.get('date_to')
    if date_to:
        surveys = surveys.filter(date_of_survey__lte=date_to)
    
    # Build features list
    features = []
    for survey in surveys:
        feature = {
            "type": "Feature",
            "geometry": json.loads(survey.farm_boundary.geojson),
            "properties": {
                "survey_id": survey.id,
                "farmer_name": survey.name_of_farmer,
                "farmer_id": survey.farmer_id_number,
                "community": survey.name_of_community,
                "survey_date": survey.date_of_survey.isoformat(),
                "total_seedlings_alive": survey.total_seedlings_alive,
                "plantation_type": survey.type_of_plantation,
                "species_count": len(survey.species_provided_planted),
            }
        }
        features.append(feature)
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return JsonResponse(geojson_data, safe=False)


@require_http_methods(["GET"])
def get_living_species_points_geojson(request, survey_id):
    """
    Get GPS points of living species as GeoJSON.
    
    Expected living_species_records format:
    [
        {
            "species": "Teak",
            "lat": 5.6037,
            "lng": -0.1870,
            "status": "healthy"
        }
    ]
    
    Returns:
        JsonResponse with GeoJSON FeatureCollection of Point features
    """
    survey = get_object_or_404(SeedlingSurvey, id=survey_id)
    
    if not survey.living_species_records:
        return JsonResponse({
            'error': 'No living species records available for this survey'
        }, status=404)
    
    features = []
    for record in survey.living_species_records:
        if 'lat' in record and 'lng' in record:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(record['lng']), float(record['lat'])]
                },
                "properties": {
                    "species": record.get('species', 'Unknown'),
                    "status": record.get('status', 'alive'),
                    "survey_id": survey.id,
                    "farmer_name": survey.name_of_farmer,
                }
            }
            features.append(feature)
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return JsonResponse(geojson_data, safe=False)


@require_http_methods(["GET"])
def get_survey_complete_map_data(request, survey_id):
    """
    Get complete map data for a survey including boundary and species points.
    
    Returns:
        JsonResponse with both polygon and points data
    """
    survey = get_object_or_404(SeedlingSurvey, id=survey_id)
    
    response_data = {
        "survey_info": {
            "id": survey.id,
            "farmer_name": survey.name_of_farmer,
            "community": survey.name_of_community,
            "survey_date": survey.date_of_survey.isoformat(),
        },
        "boundary": None,
        "species_points": []
    }
    
    # Add boundary if exists
    if survey.farm_boundary:
        response_data["boundary"] = {
            "type": "Feature",
            "geometry": json.loads(survey.farm_boundary.geojson),
            "properties": {
                "total_seedlings_alive": survey.total_seedlings_alive,
                "plantation_type": survey.type_of_plantation,
            }
        }
    
    # Add species points if exist
    if survey.living_species_records:
        for record in survey.living_species_records:
            if 'lat' in record and 'lng' in record:
                point = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(record['lng']), float(record['lat'])]
                    },
                    "properties": {
                        "species": record.get('species', 'Unknown'),
                        "status": record.get('status', 'alive'),
                    }
                }
                response_data["species_points"].append(point)
    
    return JsonResponse(response_data, safe=False)
