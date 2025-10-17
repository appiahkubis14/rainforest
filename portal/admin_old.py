from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

from import_export import resources
from import_export.admin import ImportExportModelAdmin

# treeDetails


class treeDetailsAdmin(admin.TabularInline ):
	model = treeDetails
	extra = 0
	

class farmDetailsAdmin(admin.ModelAdmin):

	inlines = (treeDetailsAdmin,)
	list_display = ('beneficiary', 'farm_code' , 'establishment_type', 'species_planted', 'no_of_trees', 'no_of_corners')
	search_fields = ("beneficiary__indvi_first_name","beneficiary__indvi_surname","beneficiary__group_name", )


admin.site.register(farmDetails, farmDetailsAdmin)
# \\/[class beneficiaryDetailsAdmin(admin.ModelAdmin):

# 	model = beneficiaryDetails
# 	pass

class farmDetailsInline(admin.StackedInline):
	model = farmDetails
	extra = 0
	inlines = (treeDetailsAdmin,)


class beneficiaryDetailsAdmin(admin.ModelAdmin):
	search_fields = ('indvi_first_name', 'indvi_surname', 'group_name', )

	# list_display = ('fname','sname','designation', 'email_address' , 'contact_number', 'password','verified')
	# readonly_fields = ["beneficiary_pic"]
	# def beneficiary_pic(self, obj):
	# 	return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
	# 		url = obj.beneficiary_pic.url,
	# 		width=obj.beneficiary_pic.width,
	# 		height=obj.beneficiary_pic.height,
	# 		)
	# )
	# pass
	# inlines = (farmDetailsInline,)


admin.site.register(beneficiaryDetails, beneficiaryDetailsAdmin)


class EnumeratorTblAdmin(admin.ModelAdmin):
	search_fields = ('fname', 'sname', )
	
	list_display = ('fname','sname','designation', 'email_address' , 'contact_number', 'password','verified')

admin.site.register(EnumeratorTbl, EnumeratorTblAdmin)



class DistrictTblAdmin(admin.ModelAdmin):
	
	list_display = ('region','district','pilot')
	search_fields = ('district',  )

admin.site.register(District, DistrictTblAdmin)






class stoolResource(resources.ModelResource):

	class Meta:

		model = stoolTbl
		fields = ('name',)
		list_display = ['name',]
		ordering = ('name',)

class stoolAdmin(ImportExportModelAdmin):
	resource_class = stoolResource
	search_fields = ('name', )

admin.site.register(stoolTbl, stoolAdmin)
# class communityTblAdmin(admin.ModelAdmin):
# 	search_fields = ('name', )
# 	list_display = ('name',)

# admin.site.register(communityTbl, communityTblAdmin)


# class TreespeciesTblAdmin(admin.ModelAdmin):
	
# 	list_display = ('code','name','botanical')


class communityResource(resources.ModelResource):

	class Meta:

		model = communityTbl
		fields = ('name',)
		list_display = ['name',]
		ordering = ('name',)

class communityAdmin(ImportExportModelAdmin):
	resource_class = communityResource
	search_fields = ('name', )

admin.site.register(communityTbl, communityAdmin)



# admin.site.register(treeSpeciesTbl, TreespeciesTblAdmin)
# class forestDistrictAdmin(admin.ModelAdmin):
# 	search_fields = ('name', )
# 	list_display = ('name',)

# admin.site.register(forestDistrictTbl, forestDistrictAdmin)

class forestDistrictResource(resources.ModelResource):

	class Meta:

		model = forestDistrictTbl
		fields = ('name',)
		list_display = ['name',]
		ordering = ('name',)

class forestDistrictAdmin(ImportExportModelAdmin):
	resource_class = forestDistrictResource
	search_fields = ('name', )

admin.site.register(forestDistrictTbl, forestDistrictAdmin)




class treeSpeciesResource(resources.ModelResource):

	class Meta:

		model = treeSpeciesTbl
		fields = ('code','name','botanical')
		list_display = ['code','name','botanical']

class treeSpeciesAdmin(ImportExportModelAdmin):
	resource_class = treeSpeciesResource
	search_fields = ('name', 'botanical', )

admin.site.register(treeSpeciesTbl, treeSpeciesAdmin)
# class FriendshipInline(admin.TabularInline):
#     model = Friendship
#     fk_name = "to_person"

# class PersonAdmin(admin.ModelAdmin):
#     inlines = [
#         FriendshipInline,
#     ]





class farmerBiodataResource(resources.ModelResource):

	class Meta:

		model = farmerBiodata
		fields = ('code','name','botanical')
		# list_display = list_display = ['community','farmer_name','contact', 'gender' , 'dob', 'small_holder_category','farm_size']


class farmerBiodataAdmin(ImportExportModelAdmin):
	resource_class = farmerBiodataResource
	search_fields = ('farmer_name', 'contact', )
	list_display = ('community','farmer_name','contact', 'gender' , 'dob', 'small_holder_category','farm_size')

admin.site.register(farmerBiodata, farmerBiodataAdmin)




class trainingparticipantDetailsAdmin(admin.TabularInline ):
	model = trainingparticipantDetails
	extra = 0
	

class trainingDetailsResource(resources.ModelResource):

	class Meta:

		model = trainingDetails
		fields = list_display = ('community', 'trainingTopic' , 'dateEventBegan', 'eventDuration', 'trainerName', 'trainerOrganisation','enumerator','created_date')



class trainingDetailsAdmin(ImportExportModelAdmin):
	resource_class = trainingDetailsResource
	inlines = (trainingparticipantDetailsAdmin,)
	list_display = ('community', 'trainingTopic' , 'dateEventBegan', 'eventDuration', 'trainerName', 'trainerOrganisation','enumerator','created_date')
	search_fields = ("trainingTopic","trainingparticipantDetails__farmer_name__farmer_name")


admin.site.register(trainingDetails, trainingDetailsAdmin)





class seedlingsMonitoringUpdateAdmin(admin.TabularInline ):
	model = seedlingsMonitoringUpdate
	extra = 0

	
class seedlingsMonitoringResource(resources.ModelResource):

	class Meta:

		model = seedlingsMonitoring
		fields =('treespecies', 'date_received' , 'date_planted', 'qnty_received', 'qntyplanted', 'qnty_survived','planting_area_type','no_of_trees_registered','farm_location','created_date')
		search_fields = ("treespecies","farmer_name__farmer_name", )



class seedlingsMonitoringAdmin(ImportExportModelAdmin):
	resource_class = seedlingsMonitoringResource
	inlines = (seedlingsMonitoringUpdateAdmin,)
	list_display = ('treespecies', 'date_received' , 'date_planted', 'qnty_received', 'qntyplanted', 'qnty_survived','planting_area_type','no_of_trees_registered','farm_location','created_date')
	search_fields = ("treespecies","farmer_name__farmer_name", )


admin.site.register(seedlingsMonitoring, seedlingsMonitoringAdmin)





class lmbMonitoringResource(resources.ModelResource):

	class Meta:

		model = lmbMonitoring
		fields = ('lmb_type', 'lmb_name' , 'date_of_first_engagement', 'partnership_type', 'partnership_duration', 'mou_signed','loan_type')
		search_fields = ("treespecies","farmer_name__farmer_name", )


class lmbMonitoringAdmin(ImportExportModelAdmin):
	resource_class = lmbMonitoringResource
	list_display = ('lmb_type', 'lmb_name' , 'date_of_first_engagement', 'partnership_type', 'partnership_duration', 'mou_signed','loan_type')
	search_fields = ("treespecies","farmer_name__farmer_name", )


admin.site.register(lmbMonitoring, lmbMonitoringAdmin)




class alternativeMonitorinResource(resources.ModelResource):

	class Meta:

		model = alternativeMonitoring
		fields = ('farmer_name', 'community' , 'date_of_visit', 'invested_amounts', 'duration', 'amounts', 'lmb_contrib_amounts', 'activities_supported')
		search_fields = ("farmer_name","community", )

class alternativeMonitorinUpdateAdmin(admin.TabularInline ):
	model = alternativeMonitorinUpdate
	extra = 0
	

class alternativeMonitoringAdmin(ImportExportModelAdmin):
	resource_class = alternativeMonitorinResource
	inlines = (alternativeMonitorinUpdateAdmin,)
	list_display = ('farmer_name', 'community' , 'date_of_visit', 'invested_amounts', 'duration', 'amounts', 'lmb_contrib_amounts', 'activities_supported')
	search_fields = ("farmer_name","community", )


admin.site.register(alternativeMonitoring, alternativeMonitoringAdmin)




