# admin.py
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.utils.html import format_html
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export.formats.base_formats import XLSX, CSV, JSON
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.utils.html import format_html
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import XLSX, CSV, JSON
from .models import *
import json

# ========== CUSTOM WIDGETS ==========
class JSONWidget(widgets.Widget):
    """Widget for handling JSON fields"""
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return {}
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return {}
        return value
    
    def render(self, value, obj=None, **kwargs):  # Add **kwargs here
        if not value:
            return ''
        return json.dumps(value, ensure_ascii=False)


    
    # def render(self, value, obj=None):
    #     if not value:
    #         return ''
    #     return json.dumps(value, ensure_ascii=False)

class ArrayWidget(widgets.Widget):
    """Widget for handling ArrayFields"""
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return []
        if isinstance(value, str):
            if value.startswith('['):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return []
            return [item.strip() for item in value.split(',') if item.strip()]
        return value
    
    def render(self, value, obj=None, **kwargs):  # Add **kwargs to accept any additional arguments
        if not value:
            return ''
        if isinstance(value, list):
            return ', '.join(str(v) for v in value)
        return str(value)

# ========== RESOURCE CLASSES FOR ALL MODELS ==========

class RegionResource(resources.ModelResource):
    class Meta:
        model = Region
        import_id_fields = ['id']
        fields = ('id', 'region', 'reg_code', 'pilot', 'geom')
        skip_unchanged = True
        report_skipped = True

class DistrictResource(resources.ModelResource):
    class Meta:
        model = District
        fields = ('id', 'region', 'district', 'district_code', 'reg_code', 'pilot', 'geom')
        skip_unchanged = True
        report_skipped = True

class CommunityResource(resources.ModelResource):
    class Meta:
        model = Community
        fields = ('id', 'community', 'lat', 'long', 'elevation')
        skip_unchanged = True
        report_skipped = True

class EnumeratorTblResource(resources.ModelResource):
    class Meta:
        model = EnumeratorTbl
        fields = ('id', 'fname', 'sname', 'designation', 'email_address', 'contact_number', 'password', 'verified', 'created_date')
        skip_unchanged = True
        report_skipped = True

class OrganisationResource(resources.ModelResource):
    class Meta:
        model = organisation
        fields = ('id', 'name')
        skip_unchanged = True
        report_skipped = True

class BeneficiaryDetailsResource(resources.ModelResource):
    mmdas = fields.Field(
        attribute='mmdas',
        widget=widgets.ForeignKeyWidget(District, 'district')
    )
    enumerator = fields.Field(
        attribute='enumerator', 
        widget=widgets.ForeignKeyWidget(EnumeratorTbl, 'fname')
    )
    organisation = fields.Field(
        attribute='organisation',
        widget=widgets.ForeignKeyWidget(organisation, 'name')
    )
    
    class Meta:
        model = beneficiaryDetails
        fields = (
            'id', 'farmercode', 'type_beneficiary', 'indvi_first_name', 'indvi_surname',
            'indvi_other_names', 'indvi_gender', 'indvi_dob', 'indvi_age', 'indvi_address',
            'indvi_phone_no', 'indvi_email', 'mmdas', 'community', 'forest_district',
            'stool_family', 'created_date'
        )
        skip_unchanged = True
        report_skipped = True

class FarmDetailsResource(resources.ModelResource):
    beneficiary = fields.Field(
        attribute='beneficiary',
        widget=widgets.ForeignKeyWidget(beneficiaryDetails, 'farmercode')
    )
    establishment_type = fields.Field(
        attribute='establishment_type',
        widget=ArrayWidget()
    )
    coord = fields.Field(
        attribute='coord',
        widget=JSONWidget()
    )
    
    class Meta:
        model = farmDetails
        fields = (
            'id', 'farm_code', 'beneficiary', 'establishment_type', 'area', 
            'coord', 'waypoint_id', 'species_planted', 'no_of_trees', 
            'no_of_corners', 'created_date'
        )
        skip_unchanged = True
        report_skipped = True

class TreeDetailsResource(resources.ModelResource):
    farm_code = fields.Field(
        attribute='farm_code',
        widget=widgets.ForeignKeyWidget(farmDetails, 'farm_code')
    )
    
    class Meta:
        model = treeDetails
        fields = (
            'id', 'farm_code', 'wcp_species_planted', 'wcp_no_of_trees', 
            'wcp_planting_distance', 'wcp_establishment_year', 'ptn_tree_no',
            'ptn_p_n', 'ptn_species', 'ptn_size_of_tree', 'ptn_year_planted',
            'ptn_year_nurturing', 'ptn_latitude', 'ptn_longitude', 'biomas', 'created_date'
        )
        skip_unchanged = True
        report_skipped = True

class TreeSpeciesTblResource(resources.ModelResource):
    class Meta:
        model = treeSpeciesTbl
        fields = ('id', 'code', 'name', 'botanical')
        skip_unchanged = True
        report_skipped = True

class ForestDistrictTblResource(resources.ModelResource):
    class Meta:
        model = forestDistrictTbl
        fields = ('id', 'name')
        skip_unchanged = True
        report_skipped = True

class CommunityTblResource(resources.ModelResource):
    class Meta:
        model = communityTbl
        fields = ('id', 'name')
        skip_unchanged = True
        report_skipped = True

class StoolTblResource(resources.ModelResource):
    class Meta:
        model = stoolTbl
        fields = ('id', 'name')
        skip_unchanged = True
        report_skipped = True

class FarmerBiodataResource(resources.ModelResource):
    community = fields.Field(
        attribute='community',
        widget=widgets.ForeignKeyWidget(Community, 'community')
    )
    
    class Meta:
        model = farmerBiodata
        fields = (
            'id', 'farmer_name', 'community', 'contact', 'gender', 'dob',
            'small_holder_category', 'farm_size', 'created_date'
        )
        skip_unchanged = True
        report_skipped = True

class TrainingDetailsResource(resources.ModelResource):
    community = fields.Field(
        attribute='community',
        widget=widgets.ForeignKeyWidget(Community, 'community')
    )
    enumerator = fields.Field(
        attribute='enumerator',
        widget=widgets.ForeignKeyWidget(EnumeratorTbl, 'fname')
    )
    
    class Meta:
        model = trainingDetails
        fields = (
            'id', 'trainingTopic', 'community', 'dateEventBegan', 'eventDuration',
            'trainerName', 'trainerOrganisation', 'enumerator', 'created_date'
        )
        skip_unchanged = True
        report_skipped = True

class TrainingParticipantDetailsResource(resources.ModelResource):
    training = fields.Field(
        attribute='training',
        widget=widgets.ForeignKeyWidget(trainingDetails, 'trainingTopic')
    )
    farmer_name = fields.Field(
        attribute='farmer_name',
        widget=widgets.ForeignKeyWidget(farmerBiodata, 'farmer_name')
    )
    
    class Meta:
        model = trainingparticipantDetails
        fields = ('id', 'training', 'farmer_name', 'created_date')
        skip_unchanged = True
        report_skipped = True

class SeedlingsMonitoringResource(resources.ModelResource):
    farmer_name = fields.Field(
        attribute='farmer_name',
        widget=widgets.ForeignKeyWidget(farmerBiodata, 'farmer_name')
    )
    community = fields.Field(
        attribute='community',
        widget=widgets.ForeignKeyWidget(Community, 'community')
    )
    enumerator = fields.Field(
        attribute='enumerator',
        widget=widgets.ForeignKeyWidget(EnumeratorTbl, 'fname')
    )
    
    class Meta:
        model = seedlingsMonitoring
        fields = (
            'id', 'farmer_name', 'community', 'date_of_visit', 'enumerator',
            'treespecies', 'date_received', 'date_planted', 'qnty_received',
            'qntyplanted', 'qnty_survived', 'planting_area_type', 'area_size',
            'no_of_trees_registered', 'farm_location', 'created_date'
        )
        skip_unchanged = True
        report_skipped = True

class SeedlingsMonitoringUpdateResource(resources.ModelResource):
    farmer = fields.Field(
        attribute='farmer',
        widget=widgets.ForeignKeyWidget(seedlingsMonitoring, 'id')
    )
    enumerator = fields.Field(
        attribute='enumerator',
        widget=widgets.ForeignKeyWidget(EnumeratorTbl, 'fname')
    )
    
    class Meta:
        model = seedlingsMonitoringUpdate
        fields = ('id', 'farmer', 'qnty_survived', 'enumerator', 'created_date')
        skip_unchanged = True
        report_skipped = True

class DeforestationResource(resources.ModelResource):
    community = fields.Field(
        attribute='community',
        widget=widgets.ForeignKeyWidget(Community, 'community')
    )
    
    class Meta:
        model = Deforestation
        fields = (
            'id', 'community', 'directed_by_gfw', 'do_u_see_deforestation',
            'cause_deforestation', 'further_action_taken', 'reason_further_action_taken',
            'latitude', 'longitude', 'publish', 'created_date'
        )
        skip_unchanged = True
        report_skipped = True

class LMBMonitoringResource(resources.ModelResource):
    enumerator = fields.Field(
        attribute='enumerator',
        widget=widgets.ForeignKeyWidget(EnumeratorTbl, 'fname')
    )
    
    class Meta:
        model = lmbMonitoring
        fields = (
            'id', 'lmb_type', 'lmb_name', 'enumerator', 'date_of_first_engagement',
            'partnership_type', 'partnership_duration', 'mou_signed', 'loan_type',
            'loan_duration', 'interest_rate', 'no_of_Farmer_ben_female',
            'no_of_Farmer_ben_male', 'no_of_Farmer_ben_youth', 'created_date'
        )
        skip_unchanged = True
        report_skipped = True

class AlternativeMonitoringResource(resources.ModelResource):
    farmer_name = fields.Field(
        attribute='farmer_name',
        widget=widgets.ForeignKeyWidget(farmerBiodata, 'farmer_name')
    )
    community = fields.Field(
        attribute='community',
        widget=widgets.ForeignKeyWidget(Community, 'community')
    )
    enumerator = fields.Field(
        attribute='enumerator',
        widget=widgets.ForeignKeyWidget(EnumeratorTbl, 'fname')
    )
    
    class Meta:
        model = alternativeMonitoring
        fields = (
            'id', 'farmer_name', 'community', 'date_of_visit', 'enumerator',
            'additional_livelihood', 'trainer_organisation', 'date_operations_started',
            'invested_amounts', 'duration', 'amounts', 'lmb_contrib_amounts',
            'activities_supported'
        )
        skip_unchanged = True
        report_skipped = True

class AlternativeMonitoringUpdateResource(resources.ModelResource):
    farmer = fields.Field(
        attribute='farmer',
        widget=widgets.ForeignKeyWidget(alternativeMonitoring, 'id')
    )
    enumerator = fields.Field(
        attribute='enumerator',
        widget=widgets.ForeignKeyWidget(EnumeratorTbl, 'fname')
    )
    
    class Meta:
        model = alternativeMonitorinUpdate
        fields = (
            'id', 'farmer', 'visit', 'qnty_survived', 'enumerator', 'duration',
            'amounts', 'lmb_contrib_amounts'
        )
        skip_unchanged = True
        report_skipped = True

class FirebaseCodesResource(resources.ModelResource):
    class Meta:
        model = firebaseCodes
        fields = ('id', 'fone_token', 'created_date')
        skip_unchanged = True
        report_skipped = True

class NoticeBoardResource(resources.ModelResource):
    class Meta:
        model = noticeBoard
        fields = ('id', 'category', 'text', 'publish', 'created_date')
        skip_unchanged = True
        report_skipped = True

class TreeSpeciesPhotosResource(resources.ModelResource):
    treespecies = fields.Field(
        attribute='treespecies',
        widget=widgets.ForeignKeyWidget(treeSpeciesTbl, 'name')
    )
    
    class Meta:
        model = treeSpeciesPhotos
        fields = ('id', 'treespecies', 'species_photos')
        skip_unchanged = True
        report_skipped = True

class TestFarmsResource(resources.ModelResource):
    coord = fields.Field(
        attribute='coord',
        widget=ArrayWidget()
    )
    
    class Meta:
        model = testFarms
        fields = ('id', 'coord')
        skip_unchanged = True
        report_skipped = True

# ========== CUSTOM ADMIN CLASSES ==========

class CustomGISModelAdmin(GISModelAdmin, ImportExportModelAdmin):
    """Combines GIS admin with import/export functionality"""
    list_per_page = 50
    save_on_top = True

class CustomImportExportAdmin(ImportExportModelAdmin):
    """Custom admin with import/export for non-GIS models"""
    list_per_page = 50
    save_on_top = True

# ========== ADMIN REGISTRATIONS ==========

@admin.register(Region)
class RegionAdmin(CustomGISModelAdmin):
    resource_class = RegionResource
    list_display = ['id', 'region', 'reg_code', 'pilot']
    list_filter = ['pilot', 'region']
    search_fields = ['region', 'reg_code']
    readonly_fields = ['id']

@admin.register(District)
class DistrictAdmin(CustomGISModelAdmin):
    resource_class = DistrictResource
    list_display = ['id', 'district', 'region', 'district_code', 'pilot']
    list_filter = ['pilot', 'region']
    search_fields = ['district', 'region', 'district_code']
    list_select_related = True

@admin.register(Community)
class CommunityAdmin(CustomGISModelAdmin):
    resource_class = CommunityResource
    list_display = ['id', 'community', 'lat', 'long', 'elevation']
    search_fields = ['community']
    list_filter = ['community']

@admin.register(EnumeratorTbl)
class EnumeratorTblAdmin(CustomImportExportAdmin):
    resource_class = EnumeratorTblResource
    list_display = ['id', 'fname', 'sname', 'designation', 'email_address', 'verified', 'created_date']
    list_filter = ['verified', 'designation', 'created_date']
    search_fields = ['fname', 'sname', 'email_address']
    readonly_fields = ['created_date']

@admin.register(organisation)
class OrganisationAdmin(CustomImportExportAdmin):
    resource_class = OrganisationResource
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(beneficiaryDetails)
class BeneficiaryDetailsAdmin(CustomImportExportAdmin):
    resource_class = BeneficiaryDetailsResource
    list_display = ['id', 'farmercode', 'get_full_name', 'type_beneficiary', 'indvi_gender', 'mmdas', 'created_date']
    list_filter = ['type_beneficiary', 'indvi_gender', 'mmdas', 'created_date']
    search_fields = ['farmercode', 'indvi_first_name', 'indvi_surname', 'indvi_phone_no']
    readonly_fields = ['created_date', 'display_photos']
    list_select_related = ['mmdas', 'enumerator', 'organisation']
    
    def get_full_name(self, obj):
        if obj.indvi_surname and obj.indvi_first_name:
            return f"{obj.indvi_surname} {obj.indvi_first_name}"
        return obj.group_name or "No Name"
    get_full_name.short_description = 'Full Name'
    
    def display_photos(self, obj):
        if obj.beneficiary_pic:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.beneficiary_pic.url)
        return "No Image"
    display_photos.short_description = 'Profile Photo Preview'

@admin.register(farmDetails)
class FarmDetailsAdmin(CustomGISModelAdmin):
    resource_class = FarmDetailsResource
    list_display = ['id', 'farm_code', 'get_beneficiary_name', 'area', 'no_of_trees', 'created_date']
    list_filter = ['created_date', 'beneficiary__mmdas']
    search_fields = ['farm_code', 'beneficiary__indvi_first_name', 'beneficiary__indvi_surname']
    readonly_fields = ['created_date']
    list_select_related = ['beneficiary']
    
    def get_beneficiary_name(self, obj):
        return str(obj.beneficiary)
    get_beneficiary_name.short_description = 'Beneficiary'

@admin.register(treeDetails)
class TreeDetailsAdmin(CustomGISModelAdmin):
    resource_class = TreeDetailsResource
    list_display = ['id', 'get_farm_code', 'wcp_species_planted', 'wcp_no_of_trees', 'biomas', 'created_date']
    list_filter = ['wcp_species_planted', 'created_date']
    search_fields = ['farm_code__farm_code', 'wcp_species_planted']
    readonly_fields = ['created_date', 'biomas']
    list_select_related = ['farm_code']
    
    def get_farm_code(self, obj):
        return obj.farm_code.farm_code
    get_farm_code.short_description = 'Farm Code'

@admin.register(treeSpeciesTbl)
class TreeSpeciesTblAdmin(CustomImportExportAdmin):
    resource_class = TreeSpeciesTblResource
    list_display = ['id', 'code', 'name', 'botanical']
    search_fields = ['code', 'name', 'botanical']
    list_filter = ['code']

@admin.register(forestDistrictTbl)
class ForestDistrictTblAdmin(CustomImportExportAdmin):
    resource_class = ForestDistrictTblResource
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(communityTbl)
class CommunityTblAdmin(CustomImportExportAdmin):
    resource_class = CommunityTblResource
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(stoolTbl)
class StoolTblAdmin(CustomImportExportAdmin):
    resource_class = StoolTblResource
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(farmerBiodata)
class FarmerBiodataAdmin(CustomImportExportAdmin):
    resource_class = FarmerBiodataResource
    list_display = ['id', 'farmer_name', 'contact', 'gender', 'community', 'created_date']
    list_filter = ['gender', 'small_holder_category', 'created_date']
    search_fields = ['farmer_name', 'contact']
    readonly_fields = ['created_date']
    list_select_related = ['community']

@admin.register(trainingDetails)
class TrainingDetailsAdmin(CustomImportExportAdmin):
    resource_class = TrainingDetailsResource
    list_display = ['id', 'trainingTopic', 'community', 'trainerName', 'dateEventBegan', 'created_date']
    list_filter = ['dateEventBegan', 'created_date']
    search_fields = ['trainingTopic', 'trainerName', 'community__community']
    readonly_fields = ['created_date']
    list_select_related = ['community', 'enumerator']

@admin.register(trainingparticipantDetails)
class TrainingParticipantDetailsAdmin(CustomImportExportAdmin):
    resource_class = TrainingParticipantDetailsResource
    list_display = ['id', 'training', 'farmer_name', 'created_date']
    list_filter = ['created_date']
    search_fields = ['training__trainingTopic', 'farmer_name__farmer_name']
    readonly_fields = ['created_date']
    list_select_related = ['training', 'farmer_name']

@admin.register(seedlingsMonitoring)
class SeedlingsMonitoringAdmin(CustomImportExportAdmin):
    resource_class = SeedlingsMonitoringResource
    list_display = ['id', 'get_farmer_name', 'community', 'treespecies', 'qnty_received', 'qnty_survived', 'created_date']
    list_filter = ['planting_area_type', 'created_date']
    search_fields = ['farmer_name__farmer_name', 'treespecies', 'community__community']
    readonly_fields = ['created_date']
    list_select_related = ['farmer_name', 'community', 'enumerator']
    
    def get_farmer_name(self, obj):
        return obj.farmer_name.farmer_name
    get_farmer_name.short_description = 'Farmer Name'

@admin.register(seedlingsMonitoringUpdate)
class SeedlingsMonitoringUpdateAdmin(CustomImportExportAdmin):
    resource_class = SeedlingsMonitoringUpdateResource
    list_display = ['id', 'farmer', 'qnty_survived', 'enumerator', 'created_date']
    list_filter = ['created_date']
    search_fields = ['farmer__farmer_name__farmer_name']
    readonly_fields = ['created_date']
    list_select_related = ['farmer', 'enumerator']

@admin.register(Deforestation)
class DeforestationAdmin(CustomGISModelAdmin):
    resource_class = DeforestationResource
    list_display = ['id', 'community', 'do_u_see_deforestation', 'publish', 'created_date']
    list_filter = ['publish', 'do_u_see_deforestation', 'created_date']
    search_fields = ['community__community', 'cause_deforestation']
    readonly_fields = ['created_date']
    list_select_related = ['community']

@admin.register(lmbMonitoring)
class LMBMonitoringAdmin(CustomImportExportAdmin):
    resource_class = LMBMonitoringResource
    list_display = ['id', 'lmb_name', 'lmb_type', 'enumerator', 'date_of_first_engagement', 'created_date']
    list_filter = ['lmb_type', 'mou_signed', 'created_date']
    search_fields = ['lmb_name', 'enumerator__fname']
    readonly_fields = ['created_date']
    list_select_related = ['enumerator']

@admin.register(alternativeMonitoring)
class AlternativeMonitoringAdmin(CustomImportExportAdmin):
    resource_class = AlternativeMonitoringResource
    list_display = ['id', 'get_farmer_name', 'community', 'additional_livelihood', ]
    list_filter = ['additional_livelihood', ]
    search_fields = ['farmer_name__farmer_name', 'community__community']
    readonly_fields = []
    list_select_related = ['farmer_name', 'community', 'enumerator']
    
    def get_farmer_name(self, obj):
        return obj.farmer_name.farmer_name
    get_farmer_name.short_description = 'Farmer Name'

@admin.register(alternativeMonitorinUpdate)
class AlternativeMonitoringUpdateAdmin(CustomImportExportAdmin):
    resource_class = AlternativeMonitoringUpdateResource
    list_display = ['id', 'farmer', 'visit', 'amounts', 'enumerator', ]
    list_filter = ['visit', ]
    search_fields = ['farmer__farmer_name__farmer_name']
    readonly_fields = []
    list_select_related = ['farmer', 'enumerator']

@admin.register(firebaseCodes)
class FirebaseCodesAdmin(CustomImportExportAdmin):
    resource_class = FirebaseCodesResource
    list_display = ['id', 'fone_token', 'created_date']
    list_filter = ['created_date']
    search_fields = ['fone_token']
    readonly_fields = ['created_date']

@admin.register(noticeBoard)
class NoticeBoardAdmin(CustomImportExportAdmin):
    resource_class = NoticeBoardResource
    list_display = ['id', 'category', 'text', 'publish', 'created_date']
    list_filter = ['category', 'publish', 'created_date']
    search_fields = ['text', 'category']
    readonly_fields = ['created_date']
    actions = ['make_published', 'make_unpublished']
    
    def make_published(self, request, queryset):
        queryset.update(publish=True)
    make_published.short_description = "Mark selected notices as published"
    
    def make_unpublished(self, request, queryset):
        queryset.update(publish=False)
    make_unpublished.short_description = "Mark selected notices as unpublished"

@admin.register(treeSpeciesPhotos)
class TreeSpeciesPhotosAdmin(CustomImportExportAdmin):
    resource_class = TreeSpeciesPhotosResource
    list_display = ['id', 'treespecies', 'image_tag']
    list_filter = ['treespecies']
    search_fields = ['treespecies__name']
    readonly_fields = ['image_tag']
    list_select_related = ['treespecies']
    
    def image_tag(self, obj):
        if obj.species_photos:
            return format_html('<img src="{}" style="width: 45px; height:45px;" />', obj.species_photos.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'

@admin.register(testFarms)
class TestFarmsAdmin(CustomGISModelAdmin):
    resource_class = TestFarmsResource
    list_display = ['id']
    search_fields = ['id']

# ========== KEEP YOUR EXISTING SEEDLING SURVEY ADMIN CODE ==========

# [Your existing SeedlingSurvey and LivingSpeciesRecord admin code remains exactly the same]
# This includes all the custom widgets, resources, and admin classes for these models
# that you already have in your current admin.py

# LivingSpeciesRecordResource (keep your existing one)
class LivingSpeciesRecordResource(resources.ModelResource):
    """Resource for Living Species Records"""
    survey_id = fields.Field(
        column_name='survey_id',
        attribute='survey',
        widget=widgets.ForeignKeyWidget(SeedlingSurvey, 'id')
    )
    farmer_name = fields.Field(
        column_name='farmer_name',
        attribute='survey__name_of_farmer',
        readonly=True
    )
    
    class Meta:
        model = LivingSpeciesRecord
        fields = (
            'id',
            'survey_id',
            'farmer_name',
            'species',
            'latitude',
            'longitude',
            'altitude',
            'accuracy',
            'geom',
        )
        export_order = fields
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True
    
    def dehydrate_geom(self, record):
        """Export geometry as WKT"""
        if record.geom:
            return record.geom.wkt
        return ''
    
    def before_import_row(self, row, **kwargs):
        """Auto-generate geometry from lat/lon on import"""
        lat = row.get('latitude')
        lon = row.get('longitude')
        
        if lat and lon:
            try:
                from django.contrib.gis.geos import Point
                row['geom'] = Point(float(lon), float(lat))
            except (ValueError, TypeError):
                pass

# PlantedSpeciesResource (keep your existing one)
class PlantedSpeciesResource(resources.ModelResource):
    """Resource for Planted Species - separate sheet export"""
    survey_id = fields.Field(column_name='survey_id')
    farmer_id_number = fields.Field(column_name='farmer_id_number')
    farmer_name = fields.Field(column_name='farmer_name')
    date_of_survey = fields.Field(column_name='date_of_survey')
    species_name = fields.Field(column_name='species_name')
    quantity_received = fields.Field(column_name='quantity_received')
    quantity_planted = fields.Field(column_name='quantity_planted')
    date_of_planting = fields.Field(column_name='date_of_planting')
    
    class Meta:
        model = SeedlingSurvey
        fields = ()
        export_order = (
            'survey_id',
            'farmer_id_number',
            'farmer_name',
            'date_of_survey',
            'species_name',
            'quantity_received',
            'quantity_planted',
            'date_of_planting',
        )
        skip_unchanged = True
    
    def get_queryset(self):
        return SeedlingSurvey.objects.all()
    
    def export(self, queryset=None, *args, **kwargs):
        """Custom export to flatten planted_species data"""
        if queryset is None:
            queryset = self.get_queryset()
        
        from tablib import Dataset
        
        dataset = Dataset()
        dataset.headers = list(self.Meta.export_order)
        
        for survey in queryset:
            planted_species = getattr(survey, 'planted_species', None)
            
            if not planted_species:
                continue
            
            if isinstance(planted_species, bytes):
                try:
                    planted_species = json.loads(planted_species.decode('utf-8'))
                except Exception:
                    continue
            
            if isinstance(planted_species, dict):
                for species_name, data in planted_species.items():
                    if not isinstance(data, dict):
                        continue
                    
                    row = [
                        survey.id,
                        survey.farmer_id_number,
                        survey.name_of_farmer,
                        str(survey.date_of_survey) if survey.date_of_survey else '',
                        str(species_name),
                        data.get('quantity_received', ''),
                        data.get('quantity_planted', ''),
                        str(data.get('date_of_planting', '')),
                    ]
                    dataset.append(row)
            
            elif isinstance(planted_species, list):
                for item in planted_species:
                    if not isinstance(item, dict):
                        continue
                    
                    row = [
                        survey.id,
                        survey.farmer_id_number,
                        survey.name_of_farmer,
                        str(survey.date_of_survey) if survey.date_of_survey else '',
                        item.get('species', item.get('species_name', '')),
                        item.get('quantity_received', ''),
                        item.get('quantity_planted', ''),
                        str(item.get('date_of_planting', '')),
                    ]
                    dataset.append(row)
        
        return dataset

# SeedlingSurveyResource (keep your existing one)
class SeedlingSurveyResource(resources.ModelResource):
    """Resource for Seedling Surveys"""
    
    species_provided_planted = fields.Field(
        column_name='species_provided_planted',
        attribute='species_provided_planted',
        widget=ArrayWidget()
    )
    
    species_alive = fields.Field(
        column_name='species_alive',
        attribute='species_alive',
        widget=ArrayWidget()
    )
    
    reason_for_death = fields.Field(
        column_name='reason_for_death',
        attribute='reason_for_death',
        widget=ArrayWidget()
    )
    
    source_of_water = fields.Field(
        column_name='source_of_water',
        attribute='source_of_water',
        widget=ArrayWidget()
    )
    
    extreme_weather_type = fields.Field(
        column_name='extreme_weather_type',
        attribute='extreme_weather_type',
        widget=ArrayWidget()
    )
    
    living_species_records = fields.Field(
        column_name='living_species_records',
        attribute='living_species_records',
        widget=JSONWidget()
    )
    
    farm_boundary_coords = fields.Field(
        column_name='farm_boundary_coords',
        attribute='farm_boundary_coords',
        widget=JSONWidget()
    )
    
    farm_boundary_wkt = fields.Field(
        column_name='farm_boundary_wkt',
        readonly=True
    )
    
    survival_rate = fields.Field(
        column_name='survival_rate',
        readonly=True
    )
    
    class Meta:
        model = SeedlingSurvey
        fields = (
            'id',
            'farmer_id_number',
            'name_of_farmer',
            'name_of_surveyor',
            'date_of_survey',
            'name_of_community',
            'type_of_plantation',
            'species_provided_planted',
            'planted_species',
            'species_alive',
            'living_species_records',
            'total_seedlings_alive',
            'survival_rate',
            'reason_for_death',
            'source_of_water',
            'avg_watering_frequency',
            'any_extreme_weather',
            'extreme_weather_type',
            'any_pests_around',
            'pest_description',
            'any_signs_of_disease',
            'disease_signs_description',
            'any_fertiliser_applied',
            'fertiliser_type',
            'any_pesticide_herbicide',
            'pesticide_herbicide_type',
            'additional_observations',
            'farm_boundary_coords',
            'farm_boundary_wkt',
            'created_at',
            'updated_at',
        )
        export_order = fields
        import_id_fields = ['farmer_id_number']
        skip_unchanged = True
        report_skipped = True
    
    def dehydrate_survival_rate(self, survey):
        """Calculate survival rate for export"""
        if not isinstance(survey, SeedlingSurvey):
            return 0
            
        if not survey.planted_species:
            return 0
        
        total_planted = 0
        if isinstance(survey.planted_species, dict):
            total_planted = sum(
                data.get('quantity_planted', 0) 
                for data in survey.planted_species.values()
            )
        elif isinstance(survey.planted_species, list):
            total_planted = sum(
                item.get('quantity_planted', 0) 
                for item in survey.planted_species
                if isinstance(item, dict)
            )
        
        if total_planted == 0:
            return 0
        
        return round((survey.total_seedlings_alive / total_planted) * 100, 2)
    
    def dehydrate_farm_boundary_wkt(self, survey):
        """Export farm boundary as WKT"""
        if survey.farm_boundary:
            return survey.farm_boundary.wkt
        return ''


# LivingSpeciesRecordResource
class LivingSpeciesRecordResource(resources.ModelResource):
    """Resource for Living Species Records"""
    
    survey_id = fields.Field(
        column_name='survey_id',
        attribute='survey__id'
    )
    
    farmer_id_number = fields.Field(
        column_name='farmer_id_number',
        attribute='survey__farmer_id_number'
    )
    
    farmer_name = fields.Field(
        column_name='farmer_name',
        attribute='survey__name_of_farmer'
    )
    
    class Meta:
        model = LivingSpeciesRecord
        fields = (
            'id',
            'survey_id',
            'farmer_id_number',
            'farmer_name',
            'species',
            'latitude',
            'longitude',
            'altitude',
            'accuracy',
            'geom',
        )
        export_order = fields


# PlantedSpeciesResource for multi-sheet export
class PlantedSpeciesResource(resources.ModelResource):
    """Resource for planted species data in multi-sheet export"""
    
    farmer_id_number = fields.Field(
        column_name='farmer_id_number',
        attribute='farmer_id_number'
    )
    
    farmer_name = fields.Field(
        column_name='farmer_name',
        attribute='name_of_farmer'
    )
    
    species_name = fields.Field(
        column_name='species_name',
        readonly=True
    )
    
    quantity_received = fields.Field(
        column_name='quantity_received',
        readonly=True
    )
    
    quantity_planted = fields.Field(
        column_name='quantity_planted',
        readonly=True
    )
    
    date_of_planting = fields.Field(
        column_name='date_of_planting',
        readonly=True
    )
    
    class Meta:
        model = SeedlingSurvey
        fields = (
            'farmer_id_number',
            'farmer_name',
            'species_name',
            'quantity_received',
            'quantity_planted',
            'date_of_planting',
        )
    
    def dehydrate_species_name(self, survey):
        """Extract species names from planted_species JSON"""
        if not survey.planted_species:
            return ''
        
        if isinstance(survey.planted_species, dict):
            return ', '.join(survey.planted_species.keys())
        elif isinstance(survey.planted_species, list):
            return ', '.join([item.get('species', '') for item in survey.planted_species if isinstance(item, dict)])
        return ''
    
    def dehydrate_quantity_received(self, survey):
        """Extract quantity received from planted_species"""
        if not survey.planted_species:
            return 0
        
        total = 0
        if isinstance(survey.planted_species, dict):
            total = sum(data.get('quantity_received', 0) for data in survey.planted_species.values())
        elif isinstance(survey.planted_species, list):
            total = sum(item.get('quantity_received', 0) for item in survey.planted_species if isinstance(item, dict))
        return total
    
    def dehydrate_quantity_planted(self, survey):
        """Extract quantity planted from planted_species"""
        if not survey.planted_species:
            return 0
        
        total = 0
        if isinstance(survey.planted_species, dict):
            total = sum(data.get('quantity_planted', 0) for data in survey.planted_species.values())
        elif isinstance(survey.planted_species, list):
            total = sum(item.get('quantity_planted', 0) for item in survey.planted_species if isinstance(item, dict))
        return total
    
    def dehydrate_date_of_planting(self, survey):
        """Extract planting dates from planted_species"""
        if not survey.planted_species:
            return ''
        
        dates = []
        if isinstance(survey.planted_species, dict):
            dates = [data.get('date_of_planting', '') for data in survey.planted_species.values()]
        elif isinstance(survey.planted_species, list):
            dates = [item.get('date_of_planting', '') for item in survey.planted_species if isinstance(item, dict)]
        
        return ', '.join(filter(None, dates))


# LivingSpeciesRecordInline
class LivingSpeciesRecordInline(admin.TabularInline):
    """Inline admin for living species records"""
    model = LivingSpeciesRecord
    extra = 1
    fields = (
        'species', 
        'latitude', 
        'longitude', 
        'altitude', 
        'accuracy', 
        'geom',
        'geom_preview'
    )
    readonly_fields = ('geom_preview',)
    
    @admin.display(description='Location Preview')
    def geom_preview(self, obj):
        """Display a preview of the point location"""
        if obj.geom:
            lat = f"{obj.geom.y:.6f}"
            lon = f"{obj.geom.x:.6f}"
            return format_html(
                '<div style="background: #f0f0f0; padding: 5px; border-radius: 3px; font-size: 12px;">'
                '📍 Point at ({}, {})</div>',
                lat, lon
            )
        return 'No location set'


# SeedlingSurveyAdmin - COMPLETE with ALL fields
@admin.register(SeedlingSurvey)
class SeedlingSurveyAdmin(ImportExportModelAdmin, GISModelAdmin):
    """Admin interface for Seedling Surveys with Import/Export - ALL FIELDS INCLUDED"""
    
    resource_class = SeedlingSurveyResource
    formats = [XLSX, CSV, JSON]
    import_template_name = 'admin/import_export/import.html'
    export_template_name = 'admin/import_export/export.html'
    skip_admin_log = False
    
    def get_export_data(self, file_format, queryset=None, *args, **kwargs):
        """Override to create multi-sheet Excel export"""
        actual_queryset = queryset
        
        if hasattr(queryset, 'method'):
            actual_queryset = self.get_export_queryset(queryset)
        elif queryset is None:
            request = kwargs.get('request')
            if request:
                actual_queryset = self.get_export_queryset(request)
            else:
                actual_queryset = self.get_queryset()
        
        if file_format.get_title() == 'xlsx':
            from tablib import Databook
            
            databook = Databook()
            
            # Sheet 1: Main Survey Data
            main_resource = self.resource_class()
            main_dataset = main_resource.export(actual_queryset)
            main_dataset.title = 'Survey Data'
            databook.add_sheet(main_dataset)
            
            # Sheet 2: Planted Species Details
            if actual_queryset.exists():
                planted_resource = PlantedSpeciesResource()
                planted_dataset = planted_resource.export(actual_queryset)
                planted_dataset.title = 'Planted Species'
                databook.add_sheet(planted_dataset)
            
            # Sheet 3: Living Species Records
            living_queryset = LivingSpeciesRecord.objects.filter(survey__in=actual_queryset)
            if living_queryset.exists():
                living_resource = LivingSpeciesRecordResource()
                living_dataset = living_resource.export(living_queryset)
                living_dataset.title = 'Living Species GPS'
                databook.add_sheet(living_dataset)
            
            return file_format.export_data(databook)
        else:
            return super().get_export_data(file_format, actual_queryset, *args, **kwargs)
    
    def get_export_queryset(self, request):
        """Get the queryset for export based on the request"""
        changelist = self.get_changelist_instance(request)
        queryset = changelist.get_queryset(request)
        return queryset
    
    inlines = [LivingSpeciesRecordInline]
    
    list_display = (
        'farmer_id_number',
        'name_of_farmer',
        'name_of_community',
        'date_of_survey',
        'type_of_plantation',
        'total_seedlings_alive',
        'survival_rate_display',
        'has_pests',
        'has_disease',
        'has_extreme_weather',
        'farm_boundary_preview',
        'created_at_display',
    )
    
    list_filter = (
        'date_of_survey',
        'name_of_community',
        'type_of_plantation',
        'any_extreme_weather',
        'any_pests_around',
        'any_signs_of_disease',
        'any_fertiliser_applied',
        'any_pesticide_herbicide',
        'created_at',
        'updated_at',
    )
    
    search_fields = (
        'name_of_farmer',
        'farmer_id_number',
        'name_of_community',
        'name_of_surveyor',
        'type_of_plantation',
    )
    
    readonly_fields = (
        'created_at_display',
        'updated_at_display',
        'survival_rate_display',
        'species_count',
        'farm_boundary_preview',
        'farm_area_display',
        'planted_species_preview',
        'living_species_records_preview',
        'environmental_factors_preview',
        'treatments_preview',
    )
    
    date_hierarchy = 'date_of_survey'
    
    # COMPREHENSIVE FIELDSETS - ALL FIELDS INCLUDED
    fieldsets = (
        ('Survey Information', {
            'fields': (
                'name_of_surveyor',
                'date_of_survey',
                'name_of_community',
            )
        }),
        ('Farmer Details', {
            'fields': (
                'name_of_farmer',
                'farmer_id_number',
                'type_of_plantation',
            )
        }),
        ('Species & Planting Data', {
            'fields': (
                'species_provided_planted',
                'planted_species',
                'planted_species_preview',
                'species_alive',
                'total_seedlings_alive',
                'survival_rate_display',
                'species_count',
            )
        }),
        ('Living Species Records', {
            'fields': (
                'living_species_records',
                'living_species_records_preview',
            ),
            'classes': ('collapse',),
        }),
        ('Farm Location & Boundary', {
            'fields': (
                'farm_boundary_coords',
                'farm_boundary',
                'farm_boundary_preview',
                'farm_area_display',
            ),
            'classes': ('wide',),
        }),
        ('Environmental Factors', {
            'fields': (
                'reason_for_death',
                'source_of_water',
                'avg_watering_frequency',
                'environmental_factors_preview',
            )
        }),
        ('Weather Conditions', {
            'fields': (
                'any_extreme_weather',
                'extreme_weather_type',
            )
        }),
        ('Pests & Diseases', {
            'fields': (
                'any_pests_around',
                'pest_description',
                'any_signs_of_disease',
                'disease_signs_description',
            )
        }),
        ('Treatments Applied', {
            'fields': (
                'any_fertiliser_applied',
                'fertiliser_type',
                'any_pesticide_herbicide',
                'pesticide_herbicide_type',
                'treatments_preview',
            )
        }),
        ('Additional Information', {
            'fields': (
                'additional_observations',
            )
        }),
        ('System Information', {
            'fields': (
                'created_at_display',
                'updated_at_display',
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ('-date_of_survey', '-created_at')
    
    @admin.display(description='Survival Rate', ordering='total_seedlings_alive')
    def survival_rate_display(self, obj):
        if not obj.planted_species:
            return '-'
        
        total_planted = 0
        
        if isinstance(obj.planted_species, dict):
            total_planted = sum(
                data.get('quantity_planted', 0) 
                for data in obj.planted_species.values()
            )
        elif isinstance(obj.planted_species, list):
            total_planted = sum(
                item.get('quantity_planted', 0) 
                for item in obj.planted_species
                if isinstance(item, dict)
            )
        
        if total_planted == 0:
            return '0%'
        
        rate = (obj.total_seedlings_alive / total_planted) * 100
        
        if rate >= 80:
            color = 'green'
        elif rate >= 50:
            color = 'orange'
        else:
            color = 'red'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}%</span>',
            color,
            round(rate, 1)
        )
    
    @admin.display(boolean=True, description='Pests')
    def has_pests(self, obj):
        return obj.any_pests_around
    
    @admin.display(boolean=True, description='Disease')
    def has_disease(self, obj):
        return obj.any_signs_of_disease
    
    @admin.display(boolean=True, description='Extreme Weather')
    def has_extreme_weather(self, obj):
        return obj.any_extreme_weather
    
    @admin.display(description='Species Count')
    def species_count(self, obj):
        return len(obj.species_provided_planted) if obj.species_provided_planted else 0
    
    @admin.display(description='Farm Boundary')
    def farm_boundary_preview(self, obj):
        if obj.farm_boundary:
            centroid = obj.farm_boundary.centroid
            lat = f"{centroid.y:.6f}"
            lon = f"{centroid.x:.6f}"
            num_points = len(obj.farm_boundary.coords[0]) if obj.farm_boundary.coords else 0
            area = f"{obj.farm_boundary.area:.2f}"
            
            return format_html(
                '<div style="background: #e8f4fd; padding: 8px; border-radius: 4px; border-left: 4px solid #2196F3;">'
                '🗺️ <strong>Farm Boundary</strong><br>'
                '📍 Center: ({}, {})<br>'
                '📐 Points: {}<br>'
                '📏 Area: {} sq meters'
                '</div>',
                lat, lon, num_points, area
            )
        elif obj.farm_boundary_coords:
            return format_html(
                '<div style="background: #fff3cd; padding: 8px; border-radius: 4px; border-left: 4px solid #ffc107;">'
                '📋 Coordinates available (click edit to view on map)'
                '</div>'
            )
        return format_html(
            '<div style="background: #f8d7da; padding: 8px; border-radius: 4px; border-left: 4px solid #dc3545;">'
            '❌ No boundary set'
            '</div>'
        )
    
    @admin.display(description='Farm Area')
    def farm_area_display(self, obj):
        if obj.farm_boundary:
            area_hectares = obj.farm_boundary.area / 10000
            area_str = f"{area_hectares:.2f}"
            return format_html(
                '<span style="font-weight: bold; color: #2e7d32;">{} hectares</span>',
                area_str
            )
        return 'Not available'
    
    @admin.display(description='Planted Species Preview')
    def planted_species_preview(self, obj):
        if obj.planted_species:
            if isinstance(obj.planted_species, dict):
                preview = '<br>'.join([f"• {species}: {data}" for species, data in obj.planted_species.items()])
            elif isinstance(obj.planted_species, list):
                preview = '<br>'.join([f"• {item}" for item in obj.planted_species])
            else:
                preview = str(obj.planted_species)
            
            return format_html(
                '<div style="background: #f0f8f0; padding: 8px; border-radius: 4px; border-left: 4px solid #4caf50;">'
                '<strong>🌱 Planted Species Data</strong><br>{}'
                '</div>',
                preview
            )
        return 'No planted species data'
    
    @admin.display(description='Living Species Records Preview')
    def living_species_records_preview(self, obj):
        if obj.living_species_records:
            return format_html(
                '<div style="background: #fff3e0; padding: 8px; border-radius: 4px; border-left: 4px solid #ff9800;">'
                '<strong>📍 Living Species GPS Records</strong><br>'
                '{} record(s) available'
                '</div>',
                len(obj.living_species_records) if isinstance(obj.living_species_records, list) else 1
            )
        return 'No living species records'
    
    @admin.display(description='Environmental Factors')
    def environmental_factors_preview(self, obj):
        factors = []
        if obj.reason_for_death:
            factors.append(f"Death reasons: {', '.join(obj.reason_for_death)}")
        if obj.source_of_water:
            factors.append(f"Water sources: {', '.join(obj.source_of_water)}")
        if obj.avg_watering_frequency:
            factors.append(f"Watering: {obj.avg_watering_frequency}")
        
        if factors:
            return format_html(
                '<div style="background: #e3f2fd; padding: 8px; border-radius: 4px;">'
                '<strong>🌍 Environmental Factors</strong><br>{}'
                '</div>',
                '<br>'.join(factors)
            )
        return 'No environmental factors recorded'
    
    @admin.display(description='Treatments Summary')
    def treatments_preview(self, obj):
        treatments = []
        if obj.any_fertiliser_applied:
            treatments.append(f"Fertilizer: {obj.fertiliser_type or 'Yes'}")
        if obj.any_pesticide_herbicide:
            treatments.append(f"Pesticide/Herbicide: {obj.pesticide_herbicide_type or 'Yes'}")
        
        if treatments:
            return format_html(
                '<div style="background: #f3e5f5; padding: 8px; border-radius: 4px;">'
                '<strong>💊 Treatments Applied</strong><br>{}'
                '</div>',
                '<br>'.join(treatments)
            )
        return 'No treatments applied'
    
    @admin.display(description='Created At')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else '-'
    
    @admin.display(description='Updated At')
    def updated_at_display(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S') if obj.updated_at else '-'
    
    default_lon = -0.1870
    default_lat = 5.6037
    default_zoom = 14
    map_width = 800
    map_height = 600
    map_template = 'gis/admin/openlayers.html'
    openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/4.6.5/ol.js'
    modifiable = True
    scrollable = False
    
    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/openlayers/4.6.5/ol.js',
        )
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/openlayers/4.6.5/ol.css',
            )
        }


# LivingSpeciesRecordAdmin - COMPLETE with ALL fields
@admin.register(LivingSpeciesRecord)
class LivingSpeciesRecordAdmin(ImportExportModelAdmin, GISModelAdmin):
    """Admin interface for Living Species Records with Import/Export - ALL FIELDS INCLUDED"""
    
    resource_class = LivingSpeciesRecordResource
    
    list_display = (
        'survey',
        'species',
        'latitude_display',
        'longitude_display',
        'altitude',
        'accuracy',
        'location_preview',
        # 'created_at_display',
    )
    
    list_filter = (
        'species',
        'survey__name_of_community',
        'survey__date_of_survey',
        
    )
    
    search_fields = (
        'species',
        'survey__name_of_farmer',
        'survey__farmer_id_number',
        'survey__name_of_community',
        'survey__name_of_surveyor',
    )
    
    readonly_fields = (
        'geom_preview',
        # 'created_at_display',
        # 'updated_at_display',
        'latitude_display',
        'longitude_display',
        'survey_info',
    )
    
    # COMPREHENSIVE FIELDSETS - ALL FIELDS INCLUDED
    fieldsets = (
        ('Survey Reference', {
            'fields': (
                'survey',
                'survey_info',
            )
        }),
        ('Species Information', {
            'fields': ('species',)
        }),
        ('GPS Coordinates & Location', {
            'fields': (
                'latitude',
                'longitude',
                'latitude_display',
                'longitude_display',
                'altitude',
                'accuracy',
                'geom',
                'geom_preview',
            )
        }),
    #     ('System Information', {
    #         'fields': (
    #             'created_at_display',
    #             'updated_at_display',
    #         ),
    #         'classes': ('collapse',),
    #     }),
    )
    
    @admin.display(description='Latitude')
    def latitude_display(self, obj):
        if obj.latitude:
            return f"{obj.latitude:.6f}"
        return '-'
    
    @admin.display(description='Longitude')
    def longitude_display(self, obj):
        if obj.longitude:
            return f"{obj.longitude:.6f}"
        return '-'
    
    @admin.display(description='Location')
    def location_preview(self, obj):
        if obj.geom:
            lat = f"{obj.geom.y:.6f}"
            lon = f"{obj.geom.x:.6f}"
            return format_html(
                '<div style="background: #e8f5e8; padding: 4px 8px; border-radius: 12px; '
                'border: 1px solid #4caf50; display: inline-block; font-size: 12px;">'
                '📍 ({}, {})</div>',
                lat, lon
            )
        return '-'
    
    @admin.display(description='Location Preview')
    def geom_preview(self, obj):
        if obj.geom:
            lat = f"{obj.geom.y:.6f}"
            lon = f"{obj.geom.x:.6f}"
            altitude_str = f"{obj.altitude}" if obj.altitude else 'N/A'
            accuracy_str = f"{obj.accuracy}" if obj.accuracy else 'N/A'
            
            return format_html(
                '<div style="background: #f8f9fa; padding: 12px; border-radius: 6px; border-left: 4px solid #4caf50;">'
                '<strong>📍 GPS Location Details</strong><br>'
                '<table style="width: 100%; margin-top: 8px;">'
                '<tr><td style="padding: 4px;"><strong>Latitude:</strong></td><td style="padding: 4px;">{}</td></tr>'
                '<tr><td style="padding: 4px;"><strong>Longitude:</strong></td><td style="padding: 4px;">{}</td></tr>'
                '<tr><td style="padding: 4px;"><strong>Altitude:</strong></td><td style="padding: 4px;">{} m</td></tr>'
                '<tr><td style="padding: 4px;"><strong>Accuracy:</strong></td><td style="padding: 4px;">{} m</td></tr>'
                '</table>'
                '</div>',
                lat, lon, altitude_str, accuracy_str
            )
        return format_html(
            '<div style="background: #fff3cd; padding: 12px; border-radius: 6px; border-left: 4px solid #ffc107;">'
            'No GPS location data available. Set latitude and longitude to generate point.'
            '</div>'
        )
    
    @admin.display(description='Survey Information')
    def survey_info(self, obj):
        if obj.survey:
            return format_html(
                '<div style="background: #e3f2fd; padding: 8px; border-radius: 4px;">'
                '<strong>📋 Survey Details</strong><br>'
                '<strong>Farmer:</strong> {}<br>'
                '<strong>Community:</strong> {}<br>'
                '<strong>Survey Date:</strong> {}'
                '</div>',
                obj.survey.name_of_farmer,
                obj.survey.name_of_community,
                obj.survey.date_of_survey
            )
        return 'No survey associated'
    
    # @admin.display(description='Created At')
    # def created_at_display(self, obj):
    #     return obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else '-'
    
    # @admin.display(description='Updated At')
    # def updated_at_display(self, obj):
    #     return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S') if obj.updated_at else '-'
    
    default_lon = -0.1870
    default_lat = 5.6037
    default_zoom = 16
    map_width = 800
    map_height = 500
    point_zoom = 18
    modifiable = True
    scrollable = False
    
    def save_model(self, request, obj, form, change):
        if obj.latitude is not None and obj.longitude is not None:
            from django.contrib.gis.geos import Point
            obj.geom = Point(float(obj.longitude), float(obj.latitude))
        super().save_model(request, obj, form, change)
    
    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/openlayers/4.6.5/ol.js',
        )
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/openlayers/4.6.5/ol.css',
            )

        }

# Admin site configuration
admin.site.site_header = "Forest Management System Administration"
admin.site.site_title = "Forest Management System"
admin.site.index_title = "Welcome to Forest Management System Admin"