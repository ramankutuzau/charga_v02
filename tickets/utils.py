import json
from .models import Tickets
import os
from config.settings import BASE_DIR
from datetime import datetime,timedelta
from django.db.models import Q
from mysql.connector import connect,Error
import shutil
import warnings



def strToDate(str):
    str = datetime.strptime(str, "%d.%m.%Y %H:%M:%S")
    return str


def waitingTime(time):
    timeTemp = str(datetime.now().time()).split('.')
    time_1 = datetime.strptime(time, "%H:%M:%S")
    time_2 = datetime.strptime(timeTemp[0], "%H:%M:%S")
    time_interval = time_2 - time_1
    minutes = time_interval.seconds // 60
    return int(minutes)




def addRequest(data,nameBackup,lenBackup):
    i = 0
    try:
        while i < lenBackup:
            ticketID = data[nameBackup][i]["id"]  # add ID
            ticketNum = f'{data[nameBackup][i]["prefix"]}{data["backup"][i]["number"]}'  # add prefix
            status = f'{data[nameBackup][i]["state"]}'  # add status
            serviceID = f'{data[nameBackup][i]["to_service"]["id"]}'  # add service id
            serviceName = f'{data[nameBackup][i]["to_service"]["name"]}'  # add service name
            standTime = strToDate(f'{data[nameBackup][i]["stand_time"]}')  # add stand time

            startTime = None
            userName = None

            dateTime = data[nameBackup][i]["stand_time"].split()
            ticketDate = datetime.strptime(dateTime[0], "%d.%m.%Y")
            waiteTime = waitingTime(dateTime[1])

            if 'from_user' in data[nameBackup][i] and 'start_time' in data[nameBackup][i]:
                userName = f'{data[nameBackup][i]["from_user"]["name"]}'  # add username
                startTime = strToDate(f'{data[nameBackup][i]["start_time"]}') # add start time


            is_exists = Tickets.objects.filter(ticket_id=ticketID).exists()

            if not is_exists:
                t = Tickets(ticket_id=ticketID, ticket_num=ticketNum, status=status,
                            service_id=serviceID, service_name=serviceName,user_name=userName,ticket_date=ticketDate,waite_stand_time=waiteTime,
                            stand_time=standTime, start_time=startTime,is_active=True)
                t.save()
            else:
                ticketWithUser = Tickets.objects.filter(ticket_id=ticketID,user_name=None,ticket_date=datetime.now().date()).exists()
                if ticketWithUser:
                    dateTime = data[nameBackup][i]["stand_time"].split()
                    waiteTime = waitingTime(dateTime[1])
                    Tickets.objects.filter(ticket_id=ticketID,ticket_date=datetime.now().date()).update(start_time = startTime,user_name=userName,status=status,waite_stand_time=waiteTime)
                else:
                    try:
                        dateTime = data[nameBackup][i]["start_time"].split()
                        waiteTime = waitingTime(dateTime[1])
                        Tickets.objects.filter(ticket_id=ticketID,ticket_date=datetime.now().date()).update(start_time=startTime, user_name=userName,status=status, waite_start_time=waiteTime)
                    except Error:
                        print(Error)
                        pass

            i += 1
    except:
        pass


def parserJson():
    shutil.copyfile(os.getenv('JSON_PATH_TICKETS'), BASE_DIR+r'\temp1.json')
    # TODO change path/argument
    f = open(BASE_DIR+r'\temp1.json','r',encoding='UTF-8')
    data = json.load(f)
    f.close()
    os.remove(BASE_DIR+r'\temp1.json')

    lenBackup = len(data['backup'])
    lenParallelBackup = len(data['parallelBackup'])

    addRequest(data,'backup',lenBackup)
    # addRequest(data,'parallelBackup',lenParallelBackup)





def inWork():

    try:
        with connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
        ) as connection:
            tickets = Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT') | Q(status='STATE_WORK'),
                                             is_active=True,ticket_date=datetime.now().date())
            for el in tickets:
                query = f"SELECT EXISTS(SELECT * FROM {os.getenv('DB_NAME')}.clients WHERE id = {el.ticket_id})"
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    for db in cursor:
                        if db[0] == 1:
                            Tickets.objects.filter(ticket_id=el.ticket_id).update(is_active=False)

    except Error as e:
        print(e)

    return Tickets.objects.filter(status='STATE_WORK',is_active=True,ticket_date=datetime.now().date()).order_by('-start_time')


def inQueue(serviceID):
    ticketsInQueue = Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),
                                            service_id=serviceID,ticket_date=datetime.now().date(),is_active=True).order_by('stand_time')
    return ticketsInQueue

def allInQueue():
    return Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),is_active=True,ticket_date=datetime.now().date()).order_by('stand_time')



def getQueueCounts():

    queueCountsDict = {
        'receptionDesk': len(Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),
                                                    service_id=2,is_active=True,ticket_date=datetime.now().date())), # 1.Прием регистратора
        'legal': len(Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),
                                            service_id=1630344076627,is_active=True,ticket_date=datetime.now().date())), # 2 Прием юр лиц
        'insurance': len(Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),
                                                service_id=1630344092733,is_active=True,ticket_date=datetime.now().date())),# 3 Cтрахование
        'techDoc': len(Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),
                                              service_id=1630344113357,is_active=True,ticket_date=datetime.now().date())),# 4.Тех. документации
        'references': len(Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),
                                                 service_id=1630344125534,is_active=True,ticket_date=datetime.now().date())), # 5 Справки
        'readyDoc': len(Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),
                                               service_id=1630344147077,is_active=True,ticket_date=datetime.now().date())),# 6 Выдача готовых документов
        'techInvetory': len(Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),
                                                   service_id=1630331336539,is_active=True,ticket_date=datetime.now().date())),  # Техническая инвентаризация
        'stateRegistr': len(Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),
                                                   service_id=1630331318265,is_active=True,ticket_date=datetime.now().date())),  # Государственная регистрация
        'all':len(Tickets.objects.filter(Q(status='STATE_INVITED') | Q(status='STATE_WAIT'),is_active=True,
                                         ticket_date=datetime.now().date())), # вся очередь
    }
    return queueCountsDict






def getHistoryTickets(serviceID,date):

    try:
        with connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
        ) as connection:

            strQuery = ''
            if serviceID != 'all':
                strQuery =  f" AND statistic.service_id = {serviceID}"

            query = f"SELECT clients.service_prefix,number,users.name,services.name,client_stand_time,client_wait_period, " \
                    f" user_finish_time,user_work_period" \
                    f" FROM {os.getenv('DB_NAME')}.statistic " \
                    f"JOIN {os.getenv('DB_NAME')}.clients ON client_id = clients.id " \
                    f"JOIN {os.getenv('DB_NAME')}.services ON statistic.service_id = services.id " \
                    f"JOIN {os.getenv('DB_NAME')}.users ON statistic.user_id = users.id " \
                    f" WHERE client_stand_time >= '{date} 08:00:00' AND  client_stand_time <= '{date} 23:59:00'"+strQuery
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
            return rows

    except Error as e:
        print(e)


def getListServices():

    try:
        with connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
        ) as connection:

            query = f" SELECT services.id, services.name" \
                    f" FROM {os.getenv('DB_NAME')}.services ORDER BY services.name"

            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                new_rows = []
                for el in rows:
                    if not ('Оператор' in el[1] or 'Операторы' in el[1] or 'Прием юридических лиц' in el[1] ) and (el[1] != ''):
                        elTemp = [el[0],el[1]]
                        new_rows.append(elTemp)

        return new_rows
    except Error as e:
        print(e)



def getListWithTime(servicesList,dataList):
    newList = []
    i = 0

    while i < len(servicesList):
        newList.append(f"{servicesList[i]} ({dataList[i]})")
        i += 1
    return newList


def getListClients(date,listServices):

    try:
        with connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
        ) as connection:
            with connection.cursor() as cursor:
                new_rows = []
                for el in listServices:
                    query = f" SELECT COUNT(*) FROM {os.getenv('DB_NAME')}.statistic" \
                            f" JOIN {os.getenv('DB_NAME')}.services ON statistic.service_id = services.id " \
                            f" WHERE service_id = {el[0]} AND" \
                            f" client_stand_time >= '{date} 08:00:00' AND  client_stand_time <= '{date} 23:59:00' "

                    cursor.execute(query)
                    rows = cursor.fetchall()
                    for el in rows:
                        new_rows.append(el[0])
        return new_rows
    except Error as e:
        print(e)


def getAverageTimes(date,listServices):
    try:
        with connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
        ) as connection:
            with connection.cursor() as cursor:
                new_rows = []
                for el in listServices:
                    query = f" SELECT user_work_period FROM {os.getenv('DB_NAME')}.statistic" \
                            f" JOIN {os.getenv('DB_NAME')}.services ON statistic.service_id = services.id " \
                            f" WHERE service_id = {el[0]} AND " \
                            f" client_stand_time >= '{date} 08:00:00' AND  client_stand_time <= '{date} 23:59:00' "
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        sum = 0
                        for el in rows:
                            sum += el[0]
                        average = sum / len(rows)
                        new_rows.append(int(average))
                    else:
                        new_rows.append(0)

        return new_rows
    except Error as e:
        print(e)



def getClientsDuring(date):

    i = 0
    listDateTime = []

    dateTemp = datetime.strptime(str(date)+' 08:00:00', '%Y-%m-%d %H:%M:%S')
    while i < 13:
        listDateTime.append(dateTemp)
        dateTemp = dateTemp + timedelta(hours=1)
        i += 1
    try:
        with connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
        ) as connection:
            with connection.cursor() as cursor:
                new_rows = []
                i = 0
                while i < len(listDateTime) - 1:
                    query = f" SELECT COUNT(*) FROM {os.getenv('DB_NAME')}.clients WHERE " \
                            f" stand_time >= '{listDateTime[i]}' AND  stand_time <= '{listDateTime[i+1]}' "
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    for el in rows:
                        new_rows.append(el[0])
                    i += 1
        return new_rows
    except Error as e:
        print(e)


def getServicesList(servicesList):
    newList = []
    for el in servicesList:
        newList.append(f"{el[1]}")

    return newList


def getTimesList():
    newList = ["8:00 - 9:00","9:00 - 10:00","10:00 - 11:00","11:00 - 12:00",
               "12:00 - 13:00","13:00 - 14:00","14:00 - 15:00","15:00 - 16:00",
               "16:00 - 17:00","17:00 - 18:00","18:00 - 19:00","19:00 - 20:00"]
    return newList


def getPeriodWaiteTimes(dateFrom,dateTo,listServices):
    try:
        with connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
        ) as connection:
            with connection.cursor() as cursor:
                new_rows = []
                for el in listServices:
                    query = f" SELECT client_wait_period FROM {os.getenv('DB_NAME')}.statistic" \
                            f" JOIN {os.getenv('DB_NAME')}.services ON statistic.service_id = services.id " \
                            f" WHERE service_id = {el[0]} AND " \
                            f" client_stand_time >= '{dateFrom} 08:00:00' AND  client_stand_time <= '{dateTo} 23:59:00' "
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        sum = 0
                        for el in rows:
                            sum += el[0]
                        average = sum / len(rows)
                        new_rows.append(int(average))
                    else:
                        new_rows.append(0)
        return new_rows
    except Error as e:
        print(e)


def getPeriodWorkTimes(dateFrom,dateTo,listServices):
    try:
        with connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
        ) as connection:
            with connection.cursor() as cursor:
                new_rows = []
                for el in listServices:
                    query = f" SELECT user_work_period FROM {os.getenv('DB_NAME')}.statistic" \
                            f" JOIN {os.getenv('DB_NAME')}.services ON statistic.service_id = services.id " \
                            f" WHERE service_id = {el[0]} AND " \
                            f" client_stand_time >= '{dateFrom} 08:00:00' AND  client_stand_time <= '{dateTo} 23:59:00' "
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        sum = 0
                        for el in rows:
                            sum += el[0]
                        average = sum / len(rows)
                        new_rows.append(int(average))
                    else:
                        new_rows.append(0)
        return new_rows
    except Error as e:
        print(e)


def getPeriodListClients(dateFrom,dateTo,listServices):

    try:
        with connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
        ) as connection:
            with connection.cursor() as cursor:
                new_rows = []
                for el in listServices:
                    query = f" SELECT COUNT(*) FROM {os.getenv('DB_NAME')}.statistic" \
                            f" JOIN {os.getenv('DB_NAME')}.services ON statistic.service_id = services.id " \
                            f" WHERE service_id = {el[0]} AND" \
                            f" client_stand_time >= '{dateFrom} 08:00:00' AND  client_stand_time <= '{dateTo} 23:59:00' "

                    cursor.execute(query)
                    rows = cursor.fetchall()
                    for el in rows:
                        new_rows.append(el[0])
        return new_rows
    except Error as e:
        print(e)


def getPeriodClients(dateFrom,dateTo):

    dateTemp = datetime.strptime(str(dateFrom) + ' 08:00:00', '%Y-%m-%d %H:%M:%S')
    dateTo = datetime.strptime(str(dateTo) + ' 20:00:00', '%Y-%m-%d %H:%M:%S')

    out_rows = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    days = 0
    while dateTemp <= dateTo:
        listDateTime = []
        i = 0
        while i < 13:
            listDateTime.append(dateTemp)
            dateTemp = dateTemp + timedelta(hours=1)
            i += 1

        try:
            with connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
            ) as connection:
                with connection.cursor() as cursor:
                    new_rows = []
                    i = 0
                    j = 0
                    while i < len(listDateTime) - 1:
                        query = f" SELECT COUNT(*) FROM {os.getenv('DB_NAME')}.clients WHERE " \
                                f" stand_time >= '{listDateTime[i]}' AND  stand_time <= '{listDateTime[i+1]}' "
                        cursor.execute(query)
                        rows = cursor.fetchall()
                        for el in rows:
                            new_rows.append(el[0])
                        i += 1
        except Error as e:
            print(e)
        days += 1
        while j < len(new_rows):
            if not new_rows[0] == 0: # если не выходной
                out_rows[j] += new_rows[j]
            j += 1
        dateTemp = dateTemp + timedelta(hours=11)

    j = 0
    while j < len(out_rows):
        out_rows[j] = round(out_rows[j] / days)
        j += 1
    return out_rows


def getPeriodServices(dateFrom,dateTo,serviceID):

    dateTemp = datetime.strptime(str(dateFrom)+' 08:00:00', '%Y-%m-%d %H:%M:%S')
    dateTo = datetime.strptime(str(dateTo)+' 20:00:00', '%Y-%m-%d %H:%M:%S')
    out_rows = []
    while dateTemp <= dateTo:
        try:
            with connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
            ) as connection:
                with connection.cursor() as cursor:
                    strQuery = ''
                    if serviceID != 'all':
                        strQuery = f" AND statistic.service_id = {serviceID}"
                    dateTemp1 = dateTemp + timedelta(hours=12)
                    query = f" SELECT COUNT(*) FROM {os.getenv('DB_NAME')}.statistic" \
                            f" JOIN {os.getenv('DB_NAME')}.services ON statistic.service_id = services.id " \
                            f" WHERE client_stand_time >= '{dateTemp}'" \
                            f" AND  client_stand_time <= '{dateTemp1}' {strQuery} "


                    cursor.execute(query)
                    rows = cursor.fetchall()
                    for el in rows:
                        out_rows.append(el[0])

        except Error as e:
            print(e)

        dateTemp = dateTemp + timedelta(days=1)

    return out_rows


def getDateList(dateFrom,dateTo):
    new_rows = []

    dateFrom = datetime.strptime(str(dateFrom), '%Y-%m-%d')
    dateTo = datetime.strptime(str(dateTo), '%Y-%m-%d')
    while dateFrom <= dateTo:

        new_rows.append(str(dateFrom).split(' ')[0])

        dateFrom = dateFrom + timedelta(days=1)

    return new_rows

warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')