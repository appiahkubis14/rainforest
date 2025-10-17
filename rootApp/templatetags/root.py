from django.forms.models import model_to_dict
from django import template

register = template.Library()


@register.filter
def subtract(firstnumber, secondnumber):
    """
		Finds the differences between two value and compare with the last value
    """
    diff_total = firstnumber - secondnumber

    return diff_total



@register.inclusion_tag('rootApp/table/html_pagination.html')
def html_paginator(paginator, tableheader):
	"""
	for pagination of a page
	"""
	return {'paginator':paginator, 'tableheader': tableheader}


@register.filter
def extractdict(dictname, dictkey):
	"""
		Extract value usind dick key
	"""
	return dictname[dictkey]

@register.filter
def model_dict(modelname):
	"""
		Convert model to dict
	"""
	return modelname.__dict__

	
    