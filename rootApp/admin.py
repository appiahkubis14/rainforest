from django.contrib import admin
from .models import*
# Register your models here.


# class LectureInline(admin.TabularInline):
#     model = Lecture
#     #readonly_fields = ('id',)
#     extra = 5


# class CourseAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('coursetitle',)}
#     inlines = [LectureInline]


# admin.site.register(Course, CourseAdmin)
# admin.site.register(Lecture)


# clients
# assignuserstoClients
# clientView

class trainingdataAdmin(admin.ModelAdmin):
    fields = ('lng', 'lat', 'name','value')
    list_display =['lng', 'lat', 'name','value']

admin.site.register(trainingdata, trainingdataAdmin)