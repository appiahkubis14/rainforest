
# Create your models here.
from django.db import models
from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db import models
from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.geos import GEOSGeometry,Point,Polygon
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from pyfcm import FCMNotification
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse

def checkzero(value):
    if value :

        return value
    else:

        return 0

# class TimeStampManager(models.Manager):
#     def __init__(self, *args, **kwargs):
#         self.alive_only = kwargs.pop('alive_only', True)
#         super(TimeStampManager, self).__init__(*args, **kwargs)

#     def get_queryset(self):
#         if self.alive_only:
#             return TimeStampQuerySet(self.model).filter(is_deleted=False)
#         return TimeStampQuerySet(self.model)

#     def hard_delete(self):
#         return self.get_queryset().hard_delete()

# class TimeStampQuerySet(models.QuerySet):
#     def delete(self):
#         return self.update(is_deleted=True)
    
#     def hard_delete(self):
#         return super(TimeStampQuerySet, self).delete()
    
#     def alive(self):
#         return self.filter(is_deleted=False)
    
#     def dead(self):
#         return self.filter(is_deleted=True)

# class TimeStampModel(models.Model):
#     """
#     Abstract base model with timestamp and soft delete functionality
#     """
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_deleted = models.BooleanField(default=False)
#     added_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_created')
#     modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_modified')
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_deleted')
    
#     objects = TimeStampManager()
#     all_objects = models.Manager()
    
#     class Meta:
#         abstract = True
    
#     def delete(self, *args, **kwargs):
#         self.is_deleted = True
#         self.save()
    
#     def hard_delete(self, *args, **kwargs):
#         super(TimeStampModel, self).delete(*args, **kwargs)

class versionTbl(models.Model):
 version = models.IntegerField(blank=True, null=True)

class Region(models.Model):
    id = models.BigIntegerField(primary_key=True)
    geom = models.GeometryField(blank=True, null=True, srid=4326)
    region = models.CharField(max_length=50, blank=True, null=True)
    reg_code = models.CharField(max_length=254, blank=True, null=True)
    pilot = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'region'


class District(models.Model):
    geom = models.GeometryField(blank=True, null=True, srid=4326)
    region = models.CharField(max_length=50, blank=True, null=True)
    region_foreignkey = models.ForeignKey(Region, on_delete=models.CASCADE,blank=True,null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    district_code = models.CharField(max_length=254, blank=True, null=True)
    reg_code = models.CharField(max_length=250,blank=True,null=True)
    pilot = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'district'
        ordering = ['district']


class Community(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE,blank=True,null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    elevation = models.BigIntegerField(blank=True, null=True)

    
    # def __str__(self):
    #     return self.community.community 


class testFarms(models.Model):
    geom = GeometryField(blank=True, null=True)
    coord = ArrayField(models.CharField( max_length=200), blank=True)


class EnumeratorTbl(models.Model):
    fname = models.CharField(max_length=250,blank=True,null=True,default="na")
    sname = models.CharField(max_length=250,blank=True,null=True,default="na")
    designation = models.CharField(max_length=250,blank=True,null=True,default="na")
    email_address = models.EmailField(max_length=250,blank=True,null=True)
    contact_number = models.CharField(max_length=250,blank=True,null=True)
    password = models.CharField(max_length=250,blank=True,null=True)
    verified=models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    class Meta:
        pass	
    def __str__(self):
        return  "{} {}".format(self.fname,self.sname)   

    class Meta:
        verbose_name = 'Enumerator'
        verbose_name_plural='Enumerators'


class organisation(models.Model):
    name = models.CharField( max_length=200,blank=True,null=True)

    def __str__(self):
        return self.name.title() 
    

class farmerBiodata(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    farmercode = models.CharField(default="na", max_length=200, blank=True, null=True) 
    farmer_name = models.CharField(default="na", max_length=200, blank=True, null=True)
    contact = models.CharField(default="na", max_length=200, blank=True, null=True)
    gender = models.CharField(default="na", max_length=200, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    small_holder_category = models.CharField(default="na", max_length=200, blank=True, null=True)
    farm_size = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.farmercode or self.farmercode == "na":
            # Get the district code through community -> district relationship
            district_code = self.community.district.district_code
            
            # Get the count of existing farmers in this district to generate sequential number
            farmers_in_district = farmerBiodata.objects.filter(
                community__district=self.community.district
            ).count()
            
            # Generate the sequential number (start from 1)
            sequential_number = farmers_in_district + 1
            
            # Format the farmer code
            self.farmercode = f"RA/{district_code}/{sequential_number:04d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.farmer_name 

    class Meta:
        verbose_name = 'Farmer Detail'
        verbose_name_plural = 'Farmer Details'


class beneficiaryDetails(models.Model):
    farmercode= models.CharField(default="na", max_length=200,blank=True,null=True) 
    farmerbiodata = models.ForeignKey(farmerBiodata, on_delete=models.CASCADE,blank=True,null=True)
    type_beneficiary= models.CharField(default="na",  max_length=200,blank=True,null=True) 
    indvi_first_name= models.CharField(default="na",  max_length=200,blank=True,null=True)
    indvi_surname= models.CharField(default="na",  max_length=200,blank=True,null=True)
    indvi_other_names= models.CharField(default="na",  max_length=200,blank=True,null=True)
    indvi_gender= models.CharField(default="na", max_length=200,blank=True,null=True)
    indvi_dob = models.DateField(blank=True, null=True)
    indvi_age = models.IntegerField(blank=True, null=True)
    indvi_address= models.CharField(default="na",  max_length=200,blank=True,null=True)
    indvi_phone_no = models.CharField(default="na", max_length=200,blank=True,null=True)
    indvi_email = models.CharField(default="na",  max_length=200,blank=True,null=True)
    indvi_next_of_kin= models.CharField(default="na",  max_length=200,blank=True,null=True)
    indvi_next_of_kin_phone_no= models.CharField(default="na", max_length=200,blank=True,null=True)
    indvi_relationship= models.CharField(default="na", max_length=200,blank=True,null=True)
    indvi_next_of_kin_gender= models.CharField(default="na", max_length=200,blank=True,null=True)
    indvi_next_of_kin_address= models.CharField(default="na", max_length=200,blank=True,null=True)
    indvi_next_of_kin_dob = models.DateField(blank=True, null=True)
    
    group_name= models.CharField(default="na", max_length=200,blank=True,null=True)
    group_reg_number = models.CharField(default="na",  max_length=200,blank=True,null=True)
    group_president = models.CharField(default="na",  max_length=200,blank=True,null=True)
    group_secretary= models.CharField(default="na",  max_length=200,blank=True,null=True)
    group_directors= models.CharField(default="na",  max_length=200,blank=True,null=True)
    group_company_add= models.CharField(default="na",  max_length=200,blank=True,null=True)
    group_phone= models.CharField(default="na",  max_length=200,blank=True,null=True)
    group_email = models.CharField(default="na",  max_length=200,blank=True,null=True)

    forest_district= models.CharField(default="na",  max_length=200,blank=True,null=True)
    stool_family= models.CharField(default="na",  max_length=200,blank=True,null=True)
    mmdas= models.ForeignKey(District, on_delete=models.CASCADE)
    community= models.CharField(default="na", max_length=200,blank=True,null=True)

    withness_name = models.CharField(default="na", max_length=200,blank=True,null=True)
    withness_phone = models.CharField(default="na", max_length=200,blank=True,null=True)

    beneficiary_pic = models.ImageField(upload_to="beneficiary_pic", null=True)
    farmer_thumb = models.ImageField(upload_to="farmer/thumbprint", null=True)
    withness_thumb = models.ImageField(upload_to="withness/thumb", null=True)
    created_date = models.DateTimeField(auto_now=True)

    enumerator= models.ForeignKey(EnumeratorTbl, on_delete=models.CASCADE)

    organisation=models.ForeignKey(organisation, on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Beneficiary Details"
        ordering = ['indvi_first_name']

    def __str__(self):
            if self.indvi_surname:
                return  "{} {}".format(self.indvi_surname,self.indvi_first_name)   
            else:
                return  "{}".format(self.group_name)

class farmDetails(models.Model):
    farm_code  = models.CharField(default="na", max_length=200,blank=True,null=True)
    beneficiary = models.ForeignKey(beneficiaryDetails, on_delete=models.CASCADE)
    establishment_type=ArrayField(models.CharField(max_length=200), blank=True, null=True)
    area = models.FloatField(blank=True, null=True)	
    coord = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
    waypoint_id= models.IntegerField(blank=True, null=True)
    geom = GeometryField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)
    species_planted= models.IntegerField(blank=True, null=True)
    no_of_trees = models.IntegerField(blank=True, null=True)
    no_of_corners = models.IntegerField(blank=True, null=True)	
    


    def __str__(self):
        return self.farm_code 
    
    def get_boundary_coordinates(self):
        """Get boundary coordinates in GeoJSON format"""
        if self.coord:
            # Convert coord array to GeoJSON coordinates format
            # Assuming coord is in format: [[lng, lat], [lng, lat], ...]
            return {
                "type": "Polygon",
                "coordinates": [self.coord]  # Wrap in array for Polygon
            }
        elif self.geom:
            # Convert geometry field to GeoJSON
            return json.loads(self.geom.geojson)
        return None
    
    def update_boundary(self, coordinates):
        """Update boundary coordinates"""
        try:
            # Update coord field
            self.coord = coordinates
            
            # Also update geom field if you want to maintain both
            if coordinates and len(coordinates) >= 3:
                # Ensure polygon is closed (first and last point same)
                if coordinates[0] != coordinates[-1]:
                    coordinates.append(coordinates[0])
                
                # Create polygon from coordinates
                polygon = Polygon(coordinates)
                self.geom = polygon
            
            self.save()
            return True
        except Exception as e:
            print(f"Error updating boundary: {e}")
            return False

    class Meta:
        verbose_name_plural = "Farm Details"
        ordering = ['beneficiary__indvi_first_name']

        

class treeDetails(models.Model):
    farm_code= models.ForeignKey(farmDetails, on_delete=models.CASCADE)
    wcp_species_planted= models.CharField(default="na", max_length=200,blank=True,null=True,)
    wcp_no_of_trees = models.IntegerField(blank=True, null=True)	
    wcp_planting_distance= models.IntegerField(blank=True, null=True)
    wcp_establishment_year= models.IntegerField(blank=True, null=True)

    speciesImage= models.ImageField(upload_to="treespecies", null=True)

    ptn_tree_no	= models.IntegerField(blank=True, null=True)
    ptn_p_n= models.CharField(default="na", max_length=200,blank=True,null=True,)
    ptn_species= models.CharField(default="na", max_length=200,blank=True,null=True, )
    ptn_size_of_tree = models.FloatField(blank=True, null=True)
    ptn_year_planted	= models.IntegerField(blank=True, null=True)
    ptn_year_nurturing = models.IntegerField(blank=True, null=True)
    ptn_latitude = models.FloatField(blank=True, null=True)	
    ptn_longitude = models.FloatField(blank=True, null=True)
    geom = GeometryField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)
    biomas = models.FloatField(blank=True, null=True)

    def save(self, force_insert=False, force_update=True, using=None, update_fields=None):
        if self.geom:
            biomas = 0.30*(checkzero(self.ptn_size_of_tree))**(2.31)
            self.biomas= round(biomas,3)
        return super(treeDetails, self).save()

    class Meta:
        verbose_name_plural = "Tree Details"
        ordering = ['-created_date']


class treeSpeciesTbl(models.Model):
    code = models.CharField(max_length=250,blank=True,null=True,default="na")
    name = models.CharField(max_length=250,blank=True,null=True,default="na")
    botanical = models.CharField(max_length=250,blank=True,null=True,default="na")
    def __str__(self):
        return self.name 


class forestDistrictTbl(models.Model):
    # code = models.CharField(, max_length=250,blank=True,null=True,default="na")
    name = models.CharField(max_length=250,blank=True,null=True,default="na")
    # botanical = models.CharField(, max_length=250,blank=True,null=True,default="na")

    class Meta:
        verbose_name_plural = "Forest District"
        ordering = ['name']
    def __str__(self):
        return self.name 


class communityTbl(models.Model):
    # code = models.CharField(, max_length=250,blank=True,null=True,default="na")
    name = models.CharField(max_length=250,blank=True,null=True,default="na")
    # botanical = models.CharField(, max_length=250,blank=True,null=True,default="na")

    class Meta:
        verbose_name_plural = "Community"
        ordering = ['name']
    def __str__(self):
        return self.name 
        


class stoolTbl(models.Model):
    # code = models.CharField(, max_length=250,blank=True,null=True,default="na")
    name = models.CharField(max_length=250,blank=True,null=True,default="na")
    # botanical = models.CharField(, max_length=250,blank=True,null=True,default="na")

    class Meta:
        verbose_name_plural = "Stools"
        ordering = ['name']
    def __str__(self):
        return self.name 




class trainingDetails(models.Model):
    community= models.ForeignKey(Community, on_delete=models.CASCADE)
    trainingTopic= models.CharField(default="na", max_length=200,blank=True,null=True)
    dateEventBegan= models.DateTimeField(blank="" , null="")
    eventDuration= models.CharField(default="na", max_length=200,blank=True,null=True)
    trainerName= models.CharField(default="na", max_length=200,blank=True,null=True)
    trainerOrganisation= models.CharField(default="na", max_length=200,blank=True,null=True)
    enumerator= models.ForeignKey(EnumeratorTbl, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.trainingTopic 

    class Meta:
        verbose_name = 'Training Detail'
        verbose_name_plural='Training Details'

class trainingparticipantDetails(models.Model):
    training = models.ForeignKey(trainingDetails, on_delete=models.CASCADE)
    farmer_name= models.ForeignKey(farmerBiodata, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)



class seedlingsMonitoring(models.Model):

    # farmerDetails
    farmer_name= models.ForeignKey(farmerBiodata, on_delete=models.CASCADE)
    # farmer_name= models.CharField(default="na", max_length=200,blank=True,null=True)
    # contact= models.CharField(default="na", max_length=200,blank=True,null=True)
    # gender= models.CharField(default="na", max_length=200,blank=True,null=True)

    # visitDetails
    community= models.ForeignKey(Community, on_delete=models.CASCADE)
    date_of_visit= models.CharField(default="na", max_length=200,blank=True,null=True)
    enumerator= models.ForeignKey(EnumeratorTbl, on_delete=models.CASCADE)
    # visit= models.IntegerField(blank=True, null=True)
    
     # treeFarmInformation
    treespecies= models.CharField(default="na", max_length=200,blank=True,null=True)
    date_received = models.DateTimeField(blank="" , null="")
    date_planted =  models.DateTimeField(blank="" , null="")
    qnty_received= models.IntegerField(blank=True, null=True)
    qntyplanted= models.IntegerField(blank=True, null=True)
    qnty_survived= models.IntegerField(blank=True, null=True)
    planting_area_type= models.CharField(default="na", max_length=200,blank=True,null=True)
    area_size= models.CharField(default="na", max_length=200,blank=True,null=True)
    no_of_trees_registered= models.CharField(default="na", max_length=200,blank=True,null=True)
    farm_location= models.CharField(default="na", max_length=200,blank=True,null=True)
    # date_of_visit= models.CharField(default="na", max_length=200,blank=True,null=True)
    # enumerator= models.CharField(default="na", max_length=200,blank=True,null=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.farmer_name.farmer_name 

    class Meta:
        verbose_name = 'landscape Seedling Monitoring'
        verbose_name_plural='landscape Seedling Monitoring'

class seedlingsMonitoringUpdate(models.Model):
    farmer = models.ForeignKey(seedlingsMonitoring, on_delete=models.CASCADE)
    # visit= models.IntegerField(blank=True, null=True)
    qnty_survived= models.IntegerField(blank=True, null=True)
    enumerator= models.ForeignKey(EnumeratorTbl, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)




class Deforestation(models.Model):
    community= models.ForeignKey(Community, on_delete=models.CASCADE)
    directed_by_gfw= models.CharField(default="na", max_length=200,blank=True,null=True)
    do_u_see_deforestation= models.CharField(default="na", max_length=200,blank=True,null=True)
    cause_deforestation= models.CharField(default="na", max_length=200,blank=True,null=True)
    further_action_taken= models.CharField(default="na", max_length=200,blank=True,null=True)
    reason_further_action_taken= models.CharField(default="na", max_length=200,blank=True,null=True)
    latitude = models.FloatField(blank=True, null=True)	
    longitude = models.FloatField(blank=True, null=True)
    geom = GeometryField(blank=True, null=True)
    photos = models.ImageField(upload_to='deforestation', null=True)
    created_date = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)








class lmbMonitoring(models.Model):

    lmb_type = models.CharField(default="", max_length=200,blank=True,null=True)
    lmb_name = models.CharField(default="", max_length=200,blank=True,null=True)
    enumerator = models.ForeignKey(EnumeratorTbl, on_delete=models.CASCADE)

    # name = models.CharField(default="", max_length=200,blank=True,null=True)
    date_of_first_engagement =  models.DateTimeField(blank="" , null="")
    partnership_type = models.CharField(default="", max_length=200,blank=True,null=True)
    partnership_duration = models.CharField(default="", max_length=200,blank=True,null=True)
    mou_signed = models.CharField(default="", max_length=200,blank=True,null=True)


    loan_type = models.CharField(default="", max_length=200,blank=True,null=True)
    loan_duration = models.IntegerField(blank=True, null=True)
    interest_rate = models.IntegerField(blank=True, null=True)
    no_of_Farmer_ben_female = models.IntegerField(blank=True, null=True)
    no_of_Farmer_ben_male = models.IntegerField(blank=True, null=True)
    no_of_Farmer_ben_youth = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'landscape LMB Monitoring'
        verbose_name_plural='landscape LMB Monitoring'


class alternativeMonitoring(models.Model):
    # farmerDetails
    farmer_name= models.ForeignKey(farmerBiodata, on_delete=models.CASCADE)
    # contact= models.CharField(default="na", max_length=200,blank=True,null=True)
    # gender= models.CharField(default="na", max_length=200,blank=True,null=True)

    # visitDetails
    community= models.ForeignKey(Community, on_delete=models.CASCADE)
    date_of_visit= models.CharField(default="na", max_length=200,blank=True,null=True)
    enumerator= models.ForeignKey(EnumeratorTbl, on_delete=models.CASCADE)
    # visit= models.IntegerField(blank=True, null=True)

    additional_livelihood = models.CharField(default="na", max_length=200,blank=True,null=True)
    trainer_organisation = models.CharField(default="na", max_length=200,blank=True,null=True)
    date_operations_started =  models.DateTimeField(blank="" , null="")

    # activityDetails
    invested_amounts = models.FloatField(blank=True, null=True)
    # six_months_amounts = models.FloatField(blank=True, null=True)
    # one_year_amounts = models.FloatField(blank=True, null=True)
    # two_ears_amounts = models.FloatField(blank=True, null=True)
    duration = models.CharField(default="na", max_length=200,blank=True,null=True)
    amounts = models.FloatField(blank=True, null=True)
    lmb_contrib_amounts = models.FloatField(blank=True, null=True)
    activities_supported = models.CharField(default="na", max_length=200,blank=True,null=True)

    class Meta:
        verbose_name = 'landscape Alternative Monitoring'
        verbose_name_plural='landscape Alternative Monitoring'

class alternativeMonitorinUpdate(models.Model):
    farmer = models.ForeignKey(alternativeMonitoring, on_delete=models.CASCADE)
    visit= models.IntegerField(blank=True, null=True)
    qnty_survived= models.IntegerField(blank=True, null=True)
    enumerator= models.ForeignKey(EnumeratorTbl, on_delete=models.CASCADE)
    duration = models.CharField(default="na", max_length=200,blank=True,null=True)
    amounts = models.FloatField(blank=True, null=True)
    # one_year_amounts = models.FloatField(blank=True, null=True)
    # two_ears_amounts = models.FloatField(blank=True, null=True)
    lmb_contrib_amounts = models.FloatField(blank=True, null=True)

class firebaseCodes(models.Model):
    fone_token = models.CharField(default="na", max_length=200,blank=True,null=True)
    created_date = models.DateTimeField(auto_now=True)


def send_notifications(title,messgae):
    path_to_fcm = "https://fcm.googleapis.com"
    server_key = 'AAAAKm20M4M:APA91bGpF0bd2S-uC4JL6wQZ0cHyTgIFQOYmI2aWlGIoU2qwlzS41pHV-HlRldx6FRPFC0PbC0Njx51Auq1EMd0STXl9cvCNoN05vtnJpBwsf8yTvMlgEPYiNNtdJ6YPHouVUL8eaefJ'
    result = False
    if server_key:
        data = firebaseCodes.objects.all()
        for aa in data:
            result = FCMNotification(api_key=server_key).notify_single_device(
                registration_id=str(aa.fone_token),
                message_title=title,
                message_body=messgae)
        return JsonResponse(result,safe=False)



class noticeBoard(models.Model):
    category = models.CharField(choices=(
            ("News/Articles", "News/Articles"),
            ("Trainings/workshops", "Trainings/workshops"),
        ), max_length=200,blank=True,null=True)
    text = models.CharField(default="na", max_length=200,blank=True,null=True)
    publish = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.publish ==True:
            
            asd=send_notifications(str(self.category),str(self.category))
        
        return super(noticeBoard, self).save()




from django.utils.safestring import mark_safe

class treeSpeciesPhotos(models.Model):
    treespecies = models.ForeignKey(treeSpeciesTbl, on_delete=models.CASCADE)
    species_photos = models.ImageField(upload_to='species', null=True)
    

    def image_tag(self):
        if self.species_photos:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.species_photos.url)
        else:
            return 'No Image Found'
        image_tag.short_description = 'Image'
    
    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    # 	self.species_photos = f'species/{treeSpeciesTbl.objects.get(id=self.treespecies.id).code}'
    # 	return super(treeSpeciesPhotos, self).save()



from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
import json
from decimal import Decimal
from datetime import datetime


class SeedlingSurvey(models.Model):
    # Survey metadata
    name_of_surveyor = models.CharField(max_length=100)
    date_of_survey = models.DateField()
    name_of_community = models.CharField(max_length=100)
    name_of_farmer = models.CharField(max_length=100)
    farmer_id_number = models.CharField(max_length=20, unique=True)
    type_of_plantation = models.CharField(max_length=100)
    
    # Species data - using JSONField for flexible structure
    species_provided_planted = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        default=list,
        help_text="List of species provided/planted"
    )
    planted_species = models.JSONField(
        default=dict,
        help_text="Detailed planting data per species"
    )
    
    # Location

    # geom= models.GeometryField(blank=True, null=True)
    # farm_boundary= models.GeometryField(blank=True, null=True)
    # In your model, you could add a separate field for raw coordinates:
    farm_boundary_coords = models.JSONField(blank=True, null=True, help_text="Raw boundary coordinates")
    farm_boundary = models.GeometryField(blank=True, null=True)  # Polygon geometry

    # Survival data
    species_alive = ArrayField( models.CharField(max_length=50), blank=True, default=list
    )
    living_species_records = models.JSONField( default=list, help_text="GPS records of living species"
    )
    total_seedlings_alive = models.PositiveIntegerField()
    
    # Environmental factors
    reason_for_death = ArrayField(models.CharField(max_length=50),blank=True,default=list
    )
    source_of_water = ArrayField(models.CharField(max_length=50),blank=True,default=list
    )
    avg_watering_frequency = models.CharField(max_length=50, blank=True)
    
    # Weather and conditions
    any_extreme_weather = models.BooleanField(default=False)
    extreme_weather_type = ArrayField( models.CharField(max_length=50), blank=True, default=list
    )
    
    # Pests and diseases
    any_pests_around = models.BooleanField(default=False)
    pest_description = models.TextField(blank=True)
    any_signs_of_disease = models.BooleanField(default=False)
    disease_signs_description = models.TextField(blank=True)
    
    # Treatments
    any_fertiliser_applied = models.BooleanField(default=False)
    fertiliser_type = models.CharField(max_length=100, blank=True)
    any_pesticide_herbicide = models.BooleanField(default=False)
    pesticide_herbicide_type = models.CharField(max_length=100, blank=True)
    
    # Additional notes
    additional_observations = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'seedling_surveys'
        ordering = ['-date_of_survey']
        indexes = [
            models.Index(fields=['farmer_id_number']),
            models.Index(fields=['date_of_survey']),
            models.Index(fields=['name_of_community']),
        ]
    
    def __str__(self):
        return f"{self.name_of_farmer} - {self.name_of_community} ({self.date_of_survey})"
    
    def clean(self):
        """Custom validation"""
        if self.total_seedlings_alive < 0:
            raise ValidationError("Total seedlings alive cannot be negative")
        
        # # Validate JSON structures
        # if self.planted_species:
        #     for species, data in self.planted_species.items():
        #         required_fields = ['quantity_received', 'quantity_planted', 'date_of_planting']
        #         if not all(field in data for field in required_fields):
        #             raise ValidationError(f"Missing required fields for species {species}")


class LivingSpeciesRecord(models.Model):
    """Separate model for individual living species records if you prefer normalized approach"""
    survey = models.ForeignKey(SeedlingSurvey, on_delete=models.CASCADE, related_name='species_records')
    species = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    altitude = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    accuracy = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    geom= models.GeometryField(blank=True, null=True)
    class Meta:
        db_table = 'living_species_records'

