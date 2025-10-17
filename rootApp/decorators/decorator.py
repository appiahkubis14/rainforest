from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from rootApp.models import *

def usergroup (function):
	@login_required
	@wraps(function)
	def wrap(request, *args, **kwargs):
		if request.user.is_authenticated():
			profile=usergroupTbl.objects.get(userTbl_foreignkey__user=request.user)
			if profile:
				try:
					group = groupTbl.objects.get(id=profile.groupTbl_foreignkey.id, delete_field="no")
				except Exception as identifier:
					errorlog("Errors/generic/decorator-error.txt", request, identifier)
					return redirect('/404/')
				return function(request, group, **kwargs)
		else:
			return redirect('/login/')
	return wrap

def errorlog(path, request, error):
	error_log = open(path, "a+")
	error=str(str(request.user)+": "+str(identifier))
	error_log.write(error)
	error_log.write("\n")
	error_log.close()
	return