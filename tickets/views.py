# import requests
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .utils import *

__all__ = ('Index','History','Statistics','receptionDeskQueue',
           'insuranceQueue','allQueue','legalQueue','techDocQueue',
           'referencesQueue','readyDocQueue','stateRegistr',
           'techInventory',)





def Index(request):
    parserJson()
    ticketsInWork = inWork()
    ticketsInQueue = allInQueue()  # вся очередь
    context = {
        'ticketsInWork': ticketsInWork,
        'ticketsInQueue': ticketsInQueue,
        'queueCounts': getQueueCounts,
    }
    return render(request, "tickets/index1.html", context)


def History(request):
    servicesList = getListServices()

    if request.method == "GET":
        date = request.GET.get('calendar')
        serviceID = request.GET.get('select')
        if date == None:
            date = datetime.now().date()
            serviceID = 'all'
        ticketsHistory = getHistoryTickets(serviceID,date)
        clientsList = getListClients(date, servicesList)
        clientsTimesList = getAverageTimes(date, servicesList)
        clientsDuring = getClientsDuring(date)
        timesList = getTimesList()

    serviceStatistic = getServicesList(servicesList)
    context = {
        'ticketsHistory': ticketsHistory,
        'servicesList': servicesList,
        'serviceStatistic': serviceStatistic,
        'clientsList': clientsList,
        'clientsTimesList': clientsTimesList,
        'date':date,
        'clientsDuring':clientsDuring,
        'timesList':timesList,
    }
    return render(request, "tickets/history.html",context)


def Statistics(request):

    servicesList = getListServices()

    if request.method == "GET":
        dateFrom = request.GET.get('calendarFrom')
        dateTo = request.GET.get('calendarTo')
        serviceID = request.GET.get('select')
        if dateFrom == None:
            dateFrom = datetime.now().date()
            dateTo = datetime.now().date()
            serviceID = 'all'


    clientsPeriodList = getPeriodListClients(dateFrom, dateTo, servicesList)
    periodWaiteTimes = getPeriodWaiteTimes(dateFrom, dateTo, servicesList)
    periodWorkTimes = getPeriodWorkTimes(dateFrom, dateTo, servicesList)
    serviceStatistic = getServicesList(servicesList)
    periodClients = getPeriodClients(dateFrom, dateTo)
    periodServices = getPeriodServices(dateFrom,dateTo,serviceID)
    dateList = getDateList(dateFrom,dateTo)
    timesList = getTimesList()
    context = {
        'serviceStatistic': serviceStatistic,

        'clientsPeriodList': clientsPeriodList,
        'periodWaiteTimes': periodWaiteTimes,
        'periodWorkTimes': periodWorkTimes,
        'periodClients': periodClients,
        'periodServices': periodServices,

        'servicesList': servicesList,
        'timesList': timesList,
        'dateList':dateList,
        'dateFrom': dateFrom,
        'dateTo': dateTo,
    }
    return render(request, "tickets/statistics.html",context)

def receptionDeskQueue(request):
    parserJson()
    ticketsInWork = inWork()
    ticketsInQueue = inQueue(2) # 1 прием регистратора
    context = {
        'ticketsInWork': ticketsInWork,
        'ticketsInQueue': ticketsInQueue,
        'queueCounts': getQueueCounts,
    }
    return render(request, "tickets/index1.html", context)



def legalQueue(request):
    parserJson()
    ticketsInWork = inWork()
    ticketsInQueue = inQueue(1630344076627) # 2 Прием юр лиц
    context = {
        'ticketsInWork': ticketsInWork,
        'ticketsInQueue': ticketsInQueue,
        'queueCounts': getQueueCounts,
    }
    return render(request,"tickets/index1.html",context)


def insuranceQueue(request):
    parserJson()
    ticketsInWork = inWork()
    ticketsInQueue = inQueue(1630344092733) # 3 Cтрахование
    context = {
        'ticketsInWork': ticketsInWork,
        'ticketsInQueue': ticketsInQueue,
        'queueCounts': getQueueCounts,
    }
    return render(request,"tickets/index1.html",context)




def techDocQueue(request):
    parserJson()
    ticketsInWork = inWork()
    ticketsInQueue = inQueue(1630344113357) # Тех. документации
    context = {
        'ticketsInWork': ticketsInWork,
        'ticketsInQueue': ticketsInQueue,
        'queueCounts': getQueueCounts,
    }
    return render(request,"tickets/index1.html",context)


def referencesQueue(request):
    parserJson()
    ticketsInWork = inWork()
    ticketsInQueue = inQueue(1630344125534) # Справки
    context = {
        'ticketsInWork': ticketsInWork,
        'ticketsInQueue': ticketsInQueue,
        'queueCounts': getQueueCounts,
    }
    return render(request,"tickets/index1.html",context)


def readyDocQueue(request):
    parserJson()
    ticketsInWork = inWork()
    ticketsInQueue = inQueue(1630344147077) # Выдача готовых документов
    context = {
        'ticketsInWork': ticketsInWork,
        'ticketsInQueue': ticketsInQueue,
        'queueCounts': getQueueCounts,
    }
    return render(request,"tickets/index1.html",context)


def techInventory(request):
    parserJson()
    ticketsInWork = inWork()
    ticketsInQueue = inQueue(1630331336539)  # 2 Техническая инвентаризация
    context = {
        'ticketsInWork': ticketsInWork,
        'ticketsInQueue': ticketsInQueue,
        'queueCounts': getQueueCounts,
    }
    return render(request, "tickets/index1.html", context)


def stateRegistr(request):
    parserJson()
    ticketsInWork = inWork()
    ticketsInQueue = inQueue(1630331318265)  # 2 Государственная регистрация
    context = {
        'ticketsInWork': ticketsInWork,
        'ticketsInQueue': ticketsInQueue,
        'queueCounts': getQueueCounts,
    }
    return render(request, "tickets/index1.html", context)


def allQueue(request):
    parserJson()
    ticketsInWork = inWork()
    ticketsInQueue = allInQueue() # вся очередь
    context = {
        'ticketsInWork': ticketsInWork,
        'ticketsInQueue': ticketsInQueue,
        'queueCounts': getQueueCounts,
    }
    return render(request,"tickets/index1.html",context)

