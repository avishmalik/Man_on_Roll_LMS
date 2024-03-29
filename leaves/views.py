from django.shortcuts import render
from .models import leavesDatabase, holidayList, todays_attendance2, cumulativeLeavesDatabase, appliedLeavesDatabase
from django.shortcuts import render
import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q

from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.
def searchLeavesData(request):
    date_check = datetime.date.today() + datetime.timedelta(days=1)
    Ticket_No = request.user.Ticket_No
    # key = open(r'C:\Users\CMS\Desktop\27072020\django_crud\static\encrypter\pass.key', 'rb').read()
    # decrypter = Fernet(key)
    # q = request.GET.get('q')
    # leavesDatabase.objects.all().update(Ticket_No='625297')
    # cumulativeLeavesDatabase.objects.all().update(Ticket_No='625297')
    # appliedLeavesDatabase.objects.all().update(Ticket_No='625297')
    # if q:
    #     card_no = decrypter.decrypt(bytes(q[1:], 'utf8')).decode()
    # Ticket_No = 625297
    try:
        queryset = leavesDatabase.objects.filter(Ticket_No = Ticket_No).values()[0]
        percentPlAvailable = queryset['total_available_pl'] * 100 / queryset['total_assigned_pl']
        percentClAvailable = queryset['total_available_cl'] * 100 / queryset['total_assigned_cl']
        percentSlAvailable = queryset['total_available_sl'] * 100 / queryset['total_assigned_sl']
    except:
        queryset = []
        percentPlAvailable = 0
        percentClAvailable = 0
        percentSlAvailable = 0
    labels = []
    count = [1, 10]
    date_list = []
    i = 0
    weekly_list = []
    months = {
        1: "JANUARY",
        2: "FEBRUARY",
        3: "MARCH",
        4: "APRIL",
        5: "MAY",
        6: "JUNE",
        7: "JULY",
        8: "AUGUST",
        9: "SEPTEMBER",
        10: "OCTOBER",
        11: "NOVEMBER",
        12: "DECEMBER"
    }
    m = 0
    month_list = []
    start_date = datetime.date.today()
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    holidays = holidayList.objects.all().order_by('date_today').reverse()
    start_date = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)
    end_date = start_date + relativedelta(day=31)
    leave_list = cumulativeLeavesDatabase.objects.filter(Ticket_No = Ticket_No).filter(
        Q(from_date__gte=start_date, from_date__lte=end_date) | Q(
            Q(to_date__gte=start_date, to_date__lte=end_date))).order_by('from_date').values()
    min_month = datetime.date(datetime.date.today().year - 1, 1, 1).strftime('%Y-%m')
    max_month = datetime.date(datetime.date.today().year, 12, 1).strftime('%Y-%m')
    name = request.user.Complete_Name
    shop = request.user.Current_Shop
    line = request.user.Cost_Center_Name
    data = {
        'date_list': date_list,
        'month_list': month_list,
        'min_month': min_month,
        'max_month': max_month,
        'current_month_name': datetime.date.today().strftime('%Y-%m'),
        'leave_list': leave_list,
        'data_list': queryset,
        'date_check': date_check,
        "Ticket_No": Ticket_No,
        'holidays' : holidays,
        "name":name,
        "shop":shop,
        "line":line,
        'labels': labels,
        'count': count,
        'percentPlAvailable': int(percentPlAvailable),
        'percentClAvailable': int(percentClAvailable),
        'percentSlAvailable': int(percentSlAvailable)
    }
    return render(request, 'leaveDataDisplay.html', data)

def leaveDataDisplay(request):
    date_check = datetime.date.today() + datetime.timedelta(days=1)
    # Ticket_No = request.GET.get('Ticket_No')
    # # if Ticket_No:
    # #     # last_transaction_done.objects.all().update(lastScannedTicketNo=Ticket_No)
    # #     if Person.objects.filter(username=Ticket_No):
    # #         return redirect('/loginEmployeePage/')
    # #     else:
    # #         return redirect('/registerEmployee/')
    data = {
        "date_check": date_check
    }
    return render(request, 'searchDataDisplay.html',data)


def validateLeaves(request):
    # Ticket_No = 625297
    Ticket_No = request.user.Ticket_No
    employeeData = leavesDatabase.objects.filter(Ticket_No=Ticket_No).values()[0]
    leaveType = request.GET.get('leaveType')
    leaveDuration = request.GET.get('leaveDuration')
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    from_date_ = datetime.datetime.strptime(fromDate, '%Y-%m-%d')
    to_date_ = datetime.datetime.strptime(toDate, '%Y-%m-%d')
    planned = "0"
    if cumulativeLeavesDatabase.objects.filter(Ticket_No=Ticket_No, from_date__gte=fromDate,
                                               to_date__lte=toDate) or cumulativeLeavesDatabase.objects.filter(
        Ticket_No=Ticket_No, from_date__lte=fromDate,
        to_date__gte=fromDate) or cumulativeLeavesDatabase.objects.filter(Ticket_No=Ticket_No,
                                                                          from_date__lte=toDate,
                                                                          to_date__gte=toDate):
        planned = "1"
    availableQuota = "0"
    if leaveType == "PL( Privilege Leave )" and employeeData['total_available_pl'] < (to_date_ - from_date_).days:
        availableQuota = "1"
    elif leaveType == "CL( Casual Leave )" and employeeData['total_available_cl'] < (to_date_ - from_date_).days:
        availableQuota = "1"
    elif leaveType == "SL( Sick Leave )" and employeeData['total_available_sl'] < (to_date_ - from_date_).days:
        availableQuota = "1"
    date_list = []
    while from_date_ < to_date_:
        info = {
            "date": from_date_.date(),
            "status": "3/5",
            "waiting": "5",
            "highlight": "1"
        }
        date_list.append(info)
        from_date_ = from_date_ + datetime.timedelta(days=1)
    info = {
        "date": to_date_.date(),
        "status": "0/5",
        "waiting": "2",
        "highlight": "0"
    }
    date_list.append(info)
    data = {
        "planned": planned,
        "availableQuota": availableQuota,
        "date_list": date_list
    }
    return JsonResponse(data)


def applyLeavesData(request):
    # Ticket_No = 625297
    Ticket_No = request.user.Ticket_No
    Complete_Name = request.user.Complete_Name
    employeeData = leavesDatabase.objects.filter(Ticket_No=Ticket_No).values()[0]
    leaveType = request.GET.get('leaveType')
    leaveDuration = request.GET.get('leaveDuration')
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    cumulativeLeavesDatabase.objects.create(
        Ticket_No=Ticket_No,
        Complete_Name = Complete_Name,
        leave_type=leaveType,
        leave_duration=leaveDuration,
        from_date=fromDate,
        to_date=toDate,
        status="0",
        Current_Shop=employeeData['Current_Shop'],
        Cost_Center_Name=employeeData['Cost_Center_Name'],
        applied_on_date=datetime.date.today()
    )
    start_date = datetime.datetime.strptime(fromDate, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(toDate, '%Y-%m-%d').date()
    while start_date <= end_date:
        appliedLeavesDatabase.objects.get_or_create(
            Ticket_No=Ticket_No,
            Current_Shop=employeeData['Current_Shop'],
            Cost_Center_Name=employeeData['Cost_Center_Name'],
            leave_duration = leaveDuration,
            leave_type = leaveType,
            on_date=start_date,
            applied_on_date_time=timezone.now()
        )
        start_date = start_date + datetime.timedelta(days=1)
    data = {}
    return JsonResponse(data)


def monthDataFilter(request):
    status = request.GET.get('status')
    leaveType = request.GET.get('leaveType')
    month = request.GET.get('month')
    # Ticket_No = 625297
    Ticket_No = request.user.Ticket_No
    start_date = datetime.date(int(month.split('-')[0]), int(month.split('-')[1]), 1)
    end_date = start_date + relativedelta(day=31)
    leave_list = cumulativeLeavesDatabase.objects.filter(Ticket_No=Ticket_No)
    if leaveType != "All":
        leave_list = cumulativeLeavesDatabase.objects.filter(Ticket_No=Ticket_No, leave_type=leaveType)
    if status != "All":
        leave_list = leave_list.filter(status=status)
    leave_list = leave_list.filter(
        Q(from_date__gte=start_date, from_date__lte=end_date) | Q(
            Q(to_date__gte=start_date, to_date__lte=end_date))).values()
    data = {
        'data_list': list(leave_list)
    }
    return JsonResponse(data)


def statusSelect(request):
    status = request.GET.get('status')
    leaveType = request.GET.get('leaveType')
    month = request.GET.get('month')
    # Ticket_No = 625297
    Ticket_No = request.user.Ticket_No
    start_date = datetime.date(int(month.split('-')[0]), int(month.split('-')[1]), 1)
    end_date = start_date + relativedelta(day=31)
    leave_list = cumulativeLeavesDatabase.objects.filter(Ticket_No=Ticket_No)
    if leaveType != "All":
        leave_list = cumulativeLeavesDatabase.objects.filter(Ticket_No=Ticket_No, leave_type=leaveType)
    if status != "All":
        leave_list = leave_list.filter(status=status)
    leave_list = leave_list.filter(
        Q(from_date__gte=start_date, from_date__lte=end_date) | Q(
            Q(to_date__gte=start_date, to_date__lte=end_date))).values()
    data = {
        'data_list': list(leave_list)
    }
    return JsonResponse(data)


def leaveTypeSelect(request):
    status = request.GET.get('status')
    leaveType = request.GET.get('leaveType')
    month = request.GET.get('month')
    # Ticket_No = 625297
    Ticket_No = request.user.Ticket_No
    start_date = datetime.date(int(month.split('-')[0]), int(month.split('-')[1]), 1)
    end_date = start_date + relativedelta(day=31)
    leave_list = cumulativeLeavesDatabase.objects.filter(Ticket_No=Ticket_No)
    if leaveType != "All":
        leave_list = cumulativeLeavesDatabase.objects.filter(Ticket_No=Ticket_No, leave_type=leaveType)
    if status != "All":
        leave_list = leave_list.filter(status=status)
    leave_list = leave_list.filter(
        Q(from_date__gte=start_date, from_date__lte=end_date) | Q(
            Q(to_date__gte=start_date, to_date__lte=end_date))).values()
    data = {
        'data_list': list(leave_list)
    }
    return JsonResponse(data)
