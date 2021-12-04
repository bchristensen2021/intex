from django import http
from django.shortcuts import render
from django.http import HttpResponse
from .models import Drug, Prescriber


# Create your views here.
def indexPageView(request):
    return render(request, 'opioidID/index.html',)

def searchPrescriberPageView(request):
    return render(request, 'opioidID/searchPrescribers.html',)

def searchDrugPageView(request):
    return render(request, 'opioidID/searchDrugs.html',)

def detailsDrugPageView(request, drug_name):
    details_drug = Drug.objects.get(drug_name = drug_name)
    context = {
        "drug": details_drug
    }
    return render(request, 'opioidID/detailsDrug.html',context)

def detailsPrescriberPageView(request):

    data = Prescriber.objects.all()

    context = {
        'data' : data,
    }    
    return render(request, 'opioidID/detailsPrescriber.html',)

