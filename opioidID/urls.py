from django.urls import path
from .views import indexPageView, searchPrescriberPageView, searchDrugPageView, detailsDrugPageView, detailsPrescriberPageView

urlpatterns = [
    path('prescribers/detail/<int:npi>' , detailsPrescriberPageView, name="detailsPrescriber"),
    path('drugs/detail/<str:drug_name>/' , detailsDrugPageView, name="detailsDrug"),
    path('drugs/search/' , searchDrugPageView, name="searchDrug" ),
    path('prescribers/search/' , searchPrescriberPageView, name="searchPrescriber" ),
    path("", indexPageView, name="index"),
]


