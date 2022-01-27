from django.urls import path
from .views import *

urlpatterns = [
    path('', Index, name='home'),
    path('history/', History, name='history'),
    path('statistics/', Statistics, name='statistics'),
    path('receptionDesk/', receptionDeskQueue, name='receptionDesk'),
    path('insurance/', insuranceQueue, name='insurance'),
    path('legalQueue/', legalQueue, name='legalqueue'),
    path('techDocQueue/', techDocQueue, name='techdocqueue'),
    path('referencesQueue/', referencesQueue, name='referencesqueue'),
    path('readyDocQueue', readyDocQueue, name='readydocqueue'),
    path('techInvetory/', techInventory, name='techinventory'),
    path('stateRegistr/', stateRegistr, name='stateregistr'),
    path('allqueue/', allQueue, name='allqueue'),
]
