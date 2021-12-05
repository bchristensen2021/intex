from django import http
from django.shortcuts import render
from django.http import HttpResponse
from .models import Drug, Prescriber, State, DrugPrescriber
from django.db.models import Sum, Avg


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
    context = {}
    if(request.method == "POST"):
        drugName = request.POST.get("drug_name")
        isOpioid = request.POST.get("is_opioid")
        search_results = Drug.objects.filter(drug_name__contains=drugName)
        if(isOpioid == "True"):
            search_results = search_results.filter(is_opioid=True)
        elif(isOpioid == "False"):
            search_results = search_results.filter(is_opioid=False)
        context = {
            "search_results" : search_results
        }
    return render(request, 'opioidID/searchDrugs.html', context)

def detailsDrugPageView(request, drug_name):
    details_drug = Drug.objects.get(drug_name = drug_name)
    top_prescribers = DrugPrescriber.objects.values('prescriber').filter(drug = drug_name).annotate(total=Sum('quantity')).order_by('-total')[:10]
    data = []
    for p in top_prescribers:
        data.append({
            "prescriber": Prescriber.objects.get(pk=p["prescriber"]),
            "total": p["total"]
        })
    context = {
        "drug": details_drug,
        "top_prescribers": data
    }
    print(top_prescribers)
    return render(request, 'opioidID/detailsDrug.html',context)

def detailsPrescriberPageView(request, npi):

    prescriber = Prescriber.objects.get(npi=npi)
    prescriptions = DrugPrescriber.objects.filter(prescriber=npi).order_by('-quantity')
    averagePresc = DrugPrescriber.objects.values('drug').filter(drug__in=prescriptions.values('drug')).annotate(average=Avg('quantity'))
    totalPresc = prescriptions.aggregate(total=Sum('quantity'))

    data = []
    for p in prescriptions:
        data.append({
            "drug": p.drug,
            "average": round(averagePresc.get(drug=p.drug)["average"]),
            "quantity": p.quantity,
            "diff": int(round(p.quantity / round(averagePresc.get(drug=p.drug)["average"]) - 1, 2) * 100)
        })

    context = {
        'prescriber' : prescriber,
        'prescriptions' : data,
        'totalPresc' : totalPresc,
        'averagePresc' : averagePresc
    }    

    return render(request, 'opioidID/detailsPrescriber.html', context)

def editPageView(request, npi):
    prescriber = Prescriber.objects.get(npi=npi)
    prescriptions = DrugPrescriber.objects.filter(prescriber=npi).order_by('-quantity')
    averagePresc = DrugPrescriber.objects.values('drug').filter(drug__in=prescriptions.values('drug')).annotate(average=Avg('quantity'))
    totalPresc = prescriptions.aggregate(total=Sum('quantity'))

    data = []
    for p in prescriptions:
        data.append({
            "drug": p.drug,
            "quantity": p.quantity,
            "average": round(averagePresc.get(drug=p.drug)["average"]),
            "diff": int(round(p.quantity / round(averagePresc.get(drug=p.drug)["average"]) - 1, 2) * 100)
        })
    
    context = {
        "states": State.objects.all().order_by('state_name'),
        "specialties": Prescriber.objects.all().values('specialty').distinct().order_by('specialty'),
        "genders": Prescriber.objects.all().values('gender').distinct(),
        "prescriber": prescriber,
        'prescriptions' : data,
    }
    if(request.method=="POST"):
        prescriber.first_name=request.POST['fname']
        prescriber.last_name=request.POST['lname']
        prescriber.gender=request.POST.get('gender')
        prescriber.specialty=request.POST.get('specialty')
        prescriber.state_id=request.POST.get('state')
        
        prescriber.save()

        quantity = request.POST.getlist('quantity')
        for p, q in zip(prescriptions, quantity):
            p.quantity=int(q)
            p.save()

    return render(request,'opioidID/editPrescriber.html', context)
