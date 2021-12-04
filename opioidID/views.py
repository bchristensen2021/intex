from django import http
from django.shortcuts import render
from django.http import HttpResponse
from .models import Drug, Prescriber, State


# Create your views here.
def indexPageView(request):
    return render(request, 'opioidID/index.html',)

def searchPrescriberPageView(request):
    context = {
        "states": State.objects.all().order_by('state_name'),
        "specialties": Prescriber.objects.all().values('specialty').distinct().order_by('specialty'),
        "genders": Prescriber.objects.all().values('gender').distinct()
    }

    # if this page is showing search results
    if(request.method == "POST"):

        name = request.POST.get("name")
        gender = request.POST.get("gender")
        state = request.POST.get("state")
        specialty = request.POST.get("specialty")
        search_results = Prescriber.objects.all()
        # only filter if the value isn't empty
        if(gender):
            search_results = search_results.filter(gender__contains=gender)
        if(state):
            search_results = search_results.filter(state__state_name=state)
        if(specialty):
            search_results = search_results.filter(specialty=specialty)

        search_results = search_results.order_by('first_name','last_name','specialty','state')

        # filter the results further by first and last name (can't do this in the filter)
        search_results = [result for result in search_results if name.lower() in result.full_name.lower()]
        context["search_results"] = search_results


    return render(request, 'opioidID/searchPrescribers.html', context)

def searchDrugPageView(request):
    return render(request, 'opioidID/searchDrugs.html')

def detailsDrugPageView(request, drug_name):
    details_drug = Drug.objects.get(drug_name = drug_name)
    context = {
        "drug": details_drug
    }
    return render(request, 'opioidID/detailsDrug.html',context)

def detailsPrescriberPageView(request, npi):

    prescriber = Prescriber.objects.get(npi=npi)

    context = {
        'prescriber' : prescriber,
    }    

    return render(request, 'opioidID/detailsPrescriber.html', context)

