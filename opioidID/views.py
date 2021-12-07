from io import SEEK_CUR
from django import http
from django.shortcuts import render
from django.http import HttpResponse
from .models import Drug, Prescriber, State, DrugPrescriber, Credential
from django.db.models import Sum, Avg
import json
from django.conf import settings
import os
import urllib.request


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

        # limit to 100 results
        search_results = search_results[:100]

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
    total_prescriptions = DrugPrescriber.objects.filter(drug=drug_name).aggregate(total_presc=Sum('quantity'))['total_presc']

    
    data = []
    for p in top_prescribers:
        data.append({
            "prescriber": Prescriber.objects.get(pk=p["prescriber"]),
            "total": '{:,}'.format(p["total"])
        })
    context = {
        "drug": details_drug,
        "top_prescribers": data,
        "total_prescriptions": '{:,}'.format(total_prescriptions)
    }

    return render(request, 'opioidID/detailsDrug.html',context)

def detailsPrescriberPageView(request, npi):

    prescriber = Prescriber.objects.get(npi=npi)
    prescriptions = DrugPrescriber.objects.filter(prescriber=npi).order_by('-quantity')
    averagePresc = DrugPrescriber.objects.values('drug').filter(drug__in=prescriptions.values('drug')).annotate(average=Avg('quantity'))
    totalPresc = prescriptions.aggregate(total=Sum('quantity'))
    credentials = Credential.objects.filter(prescriber=npi)

    data = []
    for p in prescriptions:
        data.append({
            "drug": p.drug,
            "average": '{:,}'.format(round(averagePresc.get(drug=p.drug)["average"])),
            "quantity": '{:,}'.format(p.quantity),
            "diff": int(round(p.quantity / round(averagePresc.get(drug=p.drug)["average"]) - 1, 2) * 100)
        })

    context = {
        'prescriber' : prescriber,
        'prescriptions' : data,
        'totalPresc' : totalPresc,
        'averagePresc' : averagePresc,
        'credentials' : credentials
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
        return detailsPrescriberPageView(request, npi)

    return render(request,'opioidID/editPrescriber.html', context)

def createPrescriberPageView(request):
    
    context={
        "states": State.objects.all().order_by('state_name'),
        "specialties": Prescriber.objects.all().values('specialty').distinct().order_by('specialty'),
    }

    if (request.method=="POST"):
        prescriber = Prescriber()
        state = State.objects.get(state_abbrev=request.POST.get('state'))

        prescriber.npi = request.POST["npi"]
        prescriber.first_name = request.POST["fname"].capitalize()
        prescriber.last_name = request.POST["lname"].capitalize()
        prescriber.gender = request.POST.get("gender")
        prescriber.specialty = request.POST.get("specialty")
        prescriber.state = state

        prescriber.save()
        return detailsPrescriberPageView(request, prescriber.npi)

    return render(request, "opioidID/createPrescriber.html", context)

def deletePrescriberPageView(request,npi):
    data=Prescriber.objects.get(npi=npi)
    data.delete()

    return searchPrescriberPageView(request)

def analyticsPageView(request):
    return render(request, 'opioidID/analytics.html')

def deathsByStatePageView(request):
    # get all 50 states (doesn't include things like Puerto rico with no statistics)
    states = [{
        "state_name": s.state_name,
        "population": '{:,}'.format(s.population),
        "deaths": '{:,}'.format(s.deaths),
        "deaths_per_hundred_thousand": s.deaths_per_hundred_thousand()
    } for s in State.objects.filter(population__gt=0)]
    print(type(states))
    print((states[0]))
    states = sorted(states, key=lambda s: -s["deaths_per_hundred_thousand"])
    context = {
        "states": states
    }

    return render(request, 'opioidID/deathsByState.html', context)

def opioidQuantitiesPageView(request):
    opioids = Drug.objects.filter(is_opioid=True)
    data = {
        "drugs": []
    }
    totalQuantity = 0
    for o in opioids:
        quantity = DrugPrescriber.objects.filter(drug=o.drug_name).aggregate(total=Sum('quantity'))['total']
        data["drugs"].append({
            "drug_name": o.drug_name,
            "quantity": quantity
        })
        totalQuantity += quantity

    # sort drugs by quantity
    data["drugs"] = sorted(data["drugs"], key=lambda d: -d["quantity"])

    # convert all the quantities to strings with commas
    for d in data["drugs"]:
        d["quantity"] = '{:,}'.format(d["quantity"])

    data["total_quantity"] = '{:,}'.format(totalQuantity)
    
    return render(request, 'opioidID/opioidQuantities.html', data)

def prescribersOnlyOpioidsPageView(request):
    # get all prescribers who have ever prescribed something not an opioid
    opioids = [(d.drug_name) for d in Drug.objects.filter(is_opioid=True)]
    havePrescribedNotOpioids = [(p["prescriber"]) for p in DrugPrescriber.objects.all().exclude(drug__in=opioids).values("prescriber").distinct()]
    # get all prescribers who HAVE prescribed an opioid
    # and remove all the ones that are in the previous list
    # this variable only has NPIs in it
    prescribedOnlyOpioids = [(p["prescriber"]) for p in DrugPrescriber.objects.filter(drug__in=opioids).exclude(prescriber__in=havePrescribedNotOpioids).values('prescriber').distinct()]

    finalData = Prescriber.objects.filter(npi__in=prescribedOnlyOpioids)

    context = {
        "prescribedOnlyOpioids": finalData
    }

    return render(request, 'opioidID/onlyOpioids.html', context)

def highOpioidRatioPageView(request):
    highOpioidRatioPrescribers = Prescriber.objects.raw("""
    select *,
    (select sum(dp.quantity) from drug_prescriber dp inner join drug d on dp.drugname = d.drugname
                where prescribernpi = p.npi and isopioid = TRUE group by prescribernpi) AS opioid_presc_total,
    (select sum(dp.quantity) from drug_prescriber dp
                where prescribernpi = p.npi group by prescribernpi) AS presc_total,
    (ROUND(CAST(CAST((select sum(dp.quantity) from drug_prescriber dp inner join drug d on dp.drugname = d.drugname
                where prescribernpi = p.npi and isopioid = TRUE group by prescribernpi) AS NUMERIC) /
    CAST((select sum(dp.quantity) from drug_prescriber dp
                where prescribernpi = p.npi group by prescribernpi) AS NUMERIC) AS NUMERIC),2) * 100)::INTEGER AS percent_opioid
    from prescriber p
    where (select sum(dp.quantity) from drug_prescriber dp inner join drug d on dp.drugname = d.drugname
                where prescribernpi = p.npi and isopioid = TRUE group by prescribernpi) IS NOT NULL
    order by percent_opioid DESC;
    """)

    # arbitrarily limit to the first 200 results
    context = {
        "highOpioidRatioPrescribers": highOpioidRatioPrescribers[:200]
    }

    return render(request, "opioidID/highOpioidRatio.html", context)

def machineLearningPredictorPageView(request):

    context = {
        "states": State.objects.all().order_by('state_name'),
        "specialties": Prescriber.objects.all().values('specialty').distinct().order_by('specialty'),
    }

    if(request.method == "POST"):
        print(request.POST)
        # send the form data to Azure endpoint
        data = {
            "Inputs": {
                "WebServiceInput0":
                [
                    {
                        'state': request.POST.get('state'),
                        'specialty': request.POST.get('specialty'),
                        'totalprescriptions': request.POST.get('total-prescriptions'),
                        'md': bool(request.POST.get('is_md')),
                        'pa': bool(request.POST.get('is_pa')),
                        'od': bool(request.POST.get('is_od')),
                        'rn': bool(request.POST.get('is_rn')),
                    },
                ],
            },
            "GlobalParameters": {
            }
        }

        body = str.encode(json.dumps(data))

        url = 'http://2fab4e09-9e05-455e-a0de-a9be72b734fa.westus.azurecontainer.io/score'
        api_key = '8EMUPfu1TfN8A7c25bU0e0gnuaaTyl8L' # Replace this with the API key for the web service
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            result = json.loads(result)
            result = result["Results"]["WebServiceOutput0"][0]
            context["prediction"] = result["Scored Labels"]
            context["probability"] = round(result["Scored Probabilities"] * 100)
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(json.loads(error.read().decode("utf8", 'ignore')))

    return render(request, "opioidID/machineLearningPredictor.html", context)

def machineLearningRecommenderPageView(request):
    opioids = Drug.objects.filter(is_opioid=True)
    other_drugs = Drug.objects.filter(is_opioid=False)
    file = open(os.path.join(settings.STATIC_ROOT, 'js/recommendations.json'))
    recommendations = json.load(file)

    context = {
        "opioids": opioids,
        "other_drugs": other_drugs,
    }
    
    prescribers = []
    if(request.method == "POST"):
        selected_drug = request.POST.get('drug')
        for result in recommendations[selected_drug]:
            prescribers.append(Prescriber.objects.get(npi=recommendations[selected_drug][result]))
        context["results"] = prescribers
        context["selected_drug"] = selected_drug
    return render(request, "opioidID/machineLearningRecommender.html", context)

def editDrugQuantityPageView(request, npi):
    prescriber = Prescriber.objects.get(npi=npi)
    context = {
        "prescriber": prescriber,
        "drugs": Drug.objects.all()
    }
    if(request.method == "POST"):
        print(request.POST)
        drug = request.POST.get('drug')
        qty = int(request.POST.get('qty'))
        print(drug, npi, qty)
        try:
            record = DrugPrescriber.objects.get(drug=drug, prescriber=npi)
        except DrugPrescriber.DoesNotExist:
            record = DrugPrescriber()
            record.prescriber = prescriber
            record.drug = Drug.objects.get(drug_name=drug)
        record.quantity = qty
        record.save()
        return detailsPrescriberPageView(request, prescriber.npi)

    return render(request, "opioidID/editDrugQuantity.html", context)
