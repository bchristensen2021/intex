from django.urls import path
from .views import indexPageView, searchPrescriberPageView, searchDrugPageView, detailsDrugPageView, detailsPrescriberPageView

urlpatterns = [
    path('detailsPrescriber/' , detailsPrescriberPageView, name="detailsPrescriber"),
    path('detailsDrug/' , detailsDrugPageView, name="detailsDrug"),
    path('searchDrugs/' , searchDrugPageView, name="searchDrug" ),
    path('searchPrescribers/' , searchPrescriberPageView, name="searchPrescriber" ),
    path("", indexPageView, name="index"),
]


