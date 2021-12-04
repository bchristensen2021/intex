from django.urls import path
from .views import *

urlpatterns = [
    path('prescribers/detail/<int:npi>' , detailsPrescriberPageView, name="detailsPrescriber"),
    path('drugs/detail/<str:drug_name>/' , detailsDrugPageView, name="detailsDrug"),
    path('drugs/search/' , searchDrugPageView, name="searchDrug" ),
    path('prescribers/search/' , searchPrescriberPageView, name="searchPrescriber" ),
    path('analytics/', analyticsPageView, name="analytics"),
    path('analytics/deaths-by-state', deathsByStatePageView, name="deathsByState"),
    path('analytics/opioid-quantities', opioidQuantitiesPageView, name="opioidQuantities"),
    path('analytics/prescribers-only-opioids', prescribersOnlyOpioidsPageView, name="onlyOpioids"),
    path("", indexPageView, name="index"),
]


