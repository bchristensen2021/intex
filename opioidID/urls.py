from django.urls import path
from .views import indexPageView, searchPrescriberPageView, searchDrugPageView, detailsDrugPageView, detailsPrescriberPageView

urlpatterns = [
<<<<<<< HEAD
    path('detailsPrescriber/' , detailsPrescriberPageView, name="detailsPrescriber"),
=======
    path('detailsprescriber/' , detailsPrescriberPageView, name="detailsPerscriber"),
>>>>>>> 7b11286 (changed urls)
    path('detailsDrug/' , detailsDrugPageView, name="detailsDrug"),
    path('searchDrugs/' , searchDrugPageView, name="searchDrug" ),
    path('searchPrescribers/' , searchPrescriberPageView, name="searchPrescriber" ),
    path("", indexPageView, name="index"),
]


