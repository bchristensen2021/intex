from django import http
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def indexPageView(request):
    return render(request, 'opioidID/index.html',)

def searchPrescriberPageView(request):
    return render(request, 'opioidID/searchPrescribers.html',)

def searchDrugPageView(request):
    return render(request, 'opioidID/searchDrugs.html',)

def detailsDrugPageView(request):
    return render(request, 'opioidID/detailsDrug.html',)

def detailsPrescriberPageView(request):
    return render(request, 'opioidID/detailsPrescriber.html',)

