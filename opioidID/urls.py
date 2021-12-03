from django.urls import path
from .views import indexPageView, searchPrescriberPageView, searchDrugPageView, detailsDrugPageView, detailsPrescriberPageView

urlpatterns = [
    path('detailsPrescriber/' , detailsPrescriberPageView, name="detailsPerscriber"),
    path('detailsDrug/' , detailsDrugPageView, name="detailsDrug"),
    path('searchDrugs/' , searchDrugPageView, name="searchDrugs" ),
    path('searchPrescribers/' , searchPrescriberPageView, name="searchPerscriber" ),
    path("", indexPageView, name="index"),
]


