from django.urls import path
from .views import indexPageView, searchPrescriberPageView, searchDrugPageView, detailsDrugPageView, detailsPrescriberPageView

urlpatterns = [
    path('prescribers/detail/' , detailsPrescriberPageView, name="detailsPrescriber"),
    path('drugs/detail/' , detailsDrugPageView, name="detailsDrug"),
    path('drugs/search/' , searchDrugPageView, name="searchDrug" ),
    path('prescribers/search/' , searchPrescriberPageView, name="searchPrescriber" ),
    path("", indexPageView, name="index"),
]


