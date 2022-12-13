from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
# from employee.forms import EmployeeCreateForm
from leaves.models import *
from LMS.models import *
# from leave.forms import LeaveCreationForm
from django.http import JsonResponse



# -------------------------------Dashboard Requirements--------------------------------

def dashboard(request):
	if not request.user.is_authenticated:
		return redirect('LMS:login_view')

	dataset = dict()
	Current_Shop = request.user.Current_Shop
	Cost_Center_Name = request.user.Cost_Center_Name
	num = 0
	approved_list = []
	total_list = []
	date_list = []
	mp1 = []
	mp2 = []
	if request.user.is_supervisor:
		employees = CustomUser.objects.filter(Current_Shop = Current_Shop,Cost_Center_Name = Cost_Center_Name,is_supervisor = False,is_shop_incharge = False)
		num = employees.count()
		for i in range(1,8):
			date_list.append((datetime.date.today() + datetime.timedelta(days=i)))
			x = holidayList.objects.filter(date_today = (datetime.date.today() + datetime.timedelta(days=i)))
			if x.count():
				total_list.append('HOLIDAY')
				approved_list.append('HOLIDAY')
				mp1.append('HOLIDAY')
				mp2.append(x[0].type_of_holiday)
			else:
				mp1.append('')
				mp2.append('')
				temp1 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'First Half',Current_Shop = Current_Shop,Cost_Center_Name= Cost_Center_Name)
				temp2 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'Second Half',Current_Shop = Current_Shop,Cost_Center_Name= Cost_Center_Name)
				temp3 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'Full Day',Current_Shop = Current_Shop,Cost_Center_Name= Cost_Center_Name)
				k = (temp1.count()*0.5) + (temp2.count()*0.5) + (temp3.count())
				approved_list.append(k)
				if num != 0:
					total_list.append(round((k/num) * 100,2))
				else:
					total_list.append(0)
    
		dataset['employees'] = employees
  
	elif request.user.is_shop_incharge:
		employees = CustomUser.objects.filter(Current_Shop = Current_Shop,is_supervisor = False,is_shop_incharge = False)
		num = employees.count()
		for i in range(1,8):
			date_list.append((datetime.date.today() + datetime.timedelta(days=i)))
			x = holidayList.objects.filter(date_today = (datetime.date.today() + datetime.timedelta(days=i)))
			if x.count():
				total_list.append('HOLIDAY')
				approved_list.append('HOLIDAY')
				mp1.append('HOLIDAY')
				mp2.append(x[0].type_of_holiday)
			else:
				mp1.append('')
				mp2.append('')
				temp1 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'First Half',Current_Shop = Current_Shop)
				temp2 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'Second Half',Current_Shop = Current_Shop)
				temp3 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'Full Day',Current_Shop = Current_Shop)
				k = (temp1.count()*0.5) + (temp2.count()*0.5) + (temp3.count())
				approved_list.append(k)
				if num != 0:
					total_list.append(round((k/num) * 100,2))
				else:
					total_list.append(0)
    
		dataset['lines'] = CustomUser.objects.filter(Current_Shop = Current_Shop).order_by('Cost_Center_Name').distinct('Cost_Center_Name')
		dataset['line'] = 'x'
		dataset['employees'] = employees
	
	dataset['mp1'] = mp1
	dataset['mp2'] = mp2
	dataset['approved_list'] = approved_list
	dataset['day1'] = total_list[0]
	dataset['day2'] = total_list[1]
	dataset['day3'] = total_list[2]
	dataset['day4'] = total_list[3]
	dataset['day5'] = total_list[4]
	dataset['day6'] = total_list[5]
	dataset['day7'] = total_list[6]
	dataset['date_list'] = date_list
	dataset['num'] = num
 
	return render(request,'dashboard/dashboard_index.html',dataset)



def linedashboard(request,id):
	if not request.user.is_authenticated:
		return redirect('LMS:login_view')
	
	dataset = dict()
	Current_Shop = request.user.Current_Shop
	Cost_Center_Name = get_object_or_404(CustomUser,Ticket_No = id).Cost_Center_Name
	employees = CustomUser.objects.filter(Current_Shop = Current_Shop,Cost_Center_Name = Cost_Center_Name,is_supervisor = False,is_shop_incharge = False)
	num = employees.count()
	approved_list = []
	total_list = []
	date_list = []
	mp1 = []
	mp2 = []
	for i in range(1,8):
		date_list.append((datetime.date.today() + datetime.timedelta(days=i)))
		x = holidayList.objects.filter(date_today = (datetime.date.today() + datetime.timedelta(days=i)))
		if x.count():
			total_list.append('HOLIDAY')
			approved_list.append('HOLIDAY')
			mp1.append('HOLIDAY')
			mp2.append(x[0].type_of_holiday)
		else:
			mp1.append('')
			mp2.append('')
			temp1 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'First Half',Current_Shop = Current_Shop,Cost_Center_Name= Cost_Center_Name)
			temp2 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'Second Half',Current_Shop = Current_Shop,Cost_Center_Name= Cost_Center_Name)
			temp3 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'Full Day',Current_Shop = Current_Shop,Cost_Center_Name= Cost_Center_Name)
			k = (temp1.count()*0.5) + (temp2.count()*0.5) + (temp3.count())
			approved_list.append(k)
			if num != 0:
				total_list.append(round((k/num) * 100,2))
			else:
				total_list.append(0)
   
	dataset['mp1'] = mp1
	dataset['mp2'] = mp2
	dataset['lines'] = CustomUser.objects.filter(Current_Shop = Current_Shop).order_by('Cost_Center_Name').distinct('Cost_Center_Name')
	dataset['employees'] = employees
	dataset['line'] = Cost_Center_Name
	dataset['approved_list'] = approved_list
	dataset['day1'] = total_list[0]
	dataset['day2'] = total_list[1]
	dataset['day3'] = total_list[2]
	dataset['day4'] = total_list[3]
	dataset['day5'] = total_list[4]
	dataset['day6'] = total_list[5]
	dataset['day7'] = total_list[6]
	dataset['date_list'] = date_list
	dataset['num'] = num
 
	return render(request,'dashboard/dashboard_index.html',dataset)





# --------------------------------------Employee Listing-----------------------------------

def dashboard_employees(request):
	if not (request.user.is_authenticated):
		return redirect('/logout')

	dataset = dict()
	Current_Shop = request.user.Current_Shop
	dataset['shop'] = Current_Shop
	if request.user.is_supervisor:
		Cost_Center_Name = request.user.Cost_Center_Name
		dataset['line'] = Cost_Center_Name
		dataset['employee_list'] = CustomUser.objects.filter(Current_Shop = Current_Shop,Cost_Center_Name = Cost_Center_Name,is_supervisor = False,is_shop_incharge = False).order_by('Complete_Name')

	elif request.user.is_shop_incharge:
		dataset['employee_list'] = CustomUser.objects.filter(Current_Shop = Current_Shop,is_supervisor = False,is_shop_incharge = False).order_by('Cost_Center_Name','Complete_Name')
		dataset['lines'] = CustomUser.objects.filter(Current_Shop = Current_Shop).order_by('Cost_Center_Name').distinct('Cost_Center_Name')
		dataset['line'] = 'x'
	dataset['title'] = "Men_On_Roll"
	
	return render(request,'dashboard/employee_app.html',dataset)


def employeesfilter(request,id):
	if not (request.user.is_authenticated and request.user.is_shop_incharge):
		return redirect('/logout')

	dataset = dict()
	Current_Shop = request.user.Current_Shop
	Cost_Center_Name = get_object_or_404(CustomUser,Ticket_No = id).Cost_Center_Name
	dataset['shop'] = Current_Shop
	
	dataset['employee_list'] = CustomUser.objects.filter(Current_Shop = Current_Shop,Cost_Center_Name=Cost_Center_Name,is_supervisor = False,is_shop_incharge = False).order_by('Complete_Name')
		
	dataset['title'] = "Men_On_Roll"
	dataset['lines'] = CustomUser.objects.filter(Current_Shop = Current_Shop).order_by('Cost_Center_Name').distinct('Cost_Center_Name')
	dataset['line'] = Cost_Center_Name
		
	return render(request,'dashboard/employee_app.html',dataset)



# -----------------------------Dashboard And Leave View----------------------------------

def dashboard_employee_info(request,id):
	if not request.user.is_authenticated:
		return redirect('/logout')
	
	employee = get_object_or_404(CustomUser, Ticket_No = id)
	quota = get_object_or_404(leavesDatabase,Ticket_No = id)
	
	Ticket_No = id
	leaves = cumulativeLeavesDatabase.objects.all_leaves()
	leaves = leaves.filter(Ticket_No = Ticket_No,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1)))
	name = get_object_or_404(CustomUser,Ticket_No = Ticket_No).Complete_Name
 
	dataset = dict()
	dataset['employee'] = employee
	dataset['quota'] = quota
	dataset['title'] = 'profile - {0}'.format(employee.Complete_Name)
	dataset['leave_list'] = leaves
	dataset['name'] = name
	dataset['ticket'] = Ticket_No
 
	return render(request,'dashboard/employee_detail.html',dataset)



def leaves_view(request,id):
	if not (request.user.is_authenticated):
		return redirect('/login')

	leave = get_object_or_404(cumulativeLeavesDatabase, id = id)
	Ticket_No = leave.Ticket_No
	employee = get_object_or_404(CustomUser,Ticket_No = Ticket_No)
	quota = get_object_or_404(leavesDatabase,Ticket_No = Ticket_No)
	x = ""
	if leave.status == 0:
		x = 'Waiting'
	elif leave.status == 1:
		x = 'Approved'
	else:
		x = 'Rejected'
  
	return render(request,'dashboard/leave_detail_view.html',{'leave':leave,'quota':quota,'employee':employee,'title':'{0}-{1} leave'.format(leave.Complete_Name,x)})





# # ---------------------LEAVES LISTING-------------------------------------------


def leaves_list(request):
	if not (request.user.is_authenticated):
		return redirect('/logout')

	dataset = dict()
	Current_Shop = request.user.Current_Shop
	if request.user.is_supervisor:
		Cost_Center_Name = request.user.Cost_Center_Name
		leaves = cumulativeLeavesDatabase.objects.all_leaves()
		dataset['leave_list'] = leaves.filter(Current_Shop = Current_Shop,Cost_Center_Name = Cost_Center_Name,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	
	elif request.user.is_shop_incharge:
		leaves = cumulativeLeavesDatabase.objects.all_leaves()
		dataset['leave_list'] = leaves.filter(Current_Shop = Current_Shop,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	
	dataset['title'] = 'All_Leaves'
	return render(request,'dashboard/leaves_recent.html',dataset)



def pending_leaves_list(request):
	if not (request.user.is_authenticated):
		return redirect('/login')

	dataset = dict()
	Current_Shop = request.user.Current_Shop
	if request.user.is_supervisor:
		Cost_Center_Name = request.user.Cost_Center_Name
		leaves = cumulativeLeavesDatabase.objects.all_pending_leaves()
		dataset['leave_list'] = leaves.filter(Current_Shop = Current_Shop,Cost_Center_Name = Cost_Center_Name,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
		
	elif request.user.is_shop_incharge:
		leaves = cumulativeLeavesDatabase.objects.all_pending_leaves()
		dataset['leave_list'] = leaves.filter(Current_Shop = Current_Shop,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
 
	dataset['title'] = 'Waiting_Leaves'
	return render(request,'dashboard/leaves_pending.html',dataset)



def leaves_approved_list(request):
	if not (request.user.is_authenticated):
		return redirect('/logout')

	dataset = dict()
	leaves = cumulativeLeavesDatabase.objects.all_approved_leaves()
	Current_Shop = request.user.Current_Shop
 
	if request.user.is_supervisor:
		Cost_Center_Name = request.user.Cost_Center_Name
		dataset['leave_list'] = leaves.filter(Current_Shop = Current_Shop,Cost_Center_Name = Cost_Center_Name,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	elif request.user.is_shop_incharge:
		dataset['leave_list'] = leaves.filter(Current_Shop = Current_Shop,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')

	dataset['title'] = 'Approved_Leaves'
	return render(request,'dashboard/leaves_approved.html',dataset)



def leave_rejected_list(request):
	if not (request.user.is_authenticated):
		return redirect('/logout')
	dataset = dict()
	Current_Shop = request.user.Current_Shop
	leaves = cumulativeLeavesDatabase.objects.all_rejected_leaves()
 
	if request.user.is_supervisor:
		Cost_Center_Name = request.user.Cost_Center_Name
		dataset['leaves_list_rejected'] = leaves.filter(Current_Shop = Current_Shop,Cost_Center_Name = Cost_Center_Name,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	elif request.user.is_shop_incharge:
		leaves = leaves.filter(Current_Shop = Current_Shop,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
		dataset['leave_list_rejected'] = leaves
  
  
	dataset['title'] = 'Rejected_Leaves'
	return render(request,'dashboard/rejected_leaves_list.html',dataset)





# ----------------------------Personal Leaves Sorting----------------------------------


def sortedleaves(request,id):
	if not (request.user.is_supervisor or request.user.is_shop_incharge):
		return redirect('/logout')

	Ticket_No = id
	leaves = cumulativeLeavesDatabase.objects.all_leaves()
	leaves = leaves.filter(Ticket_No = Ticket_No,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	name = get_object_or_404(CustomUser,Ticket_No = Ticket_No).Complete_Name
 
	employee = get_object_or_404(CustomUser, Ticket_No = id)
	quota = get_object_or_404(leavesDatabase,Ticket_No = id)
 
	dataset = dict()
	dataset['employee'] = employee
	dataset['quota'] = quota
	dataset['title'] = 'profile - {0}'.format(employee.Complete_Name)
	dataset['leave_list'] = leaves
	dataset['name'] = name
	dataset['ticket'] = Ticket_No
 
	return render(request,'dashboard/employee_detail.html',dataset)



def personalapproved(request,id):
	if not (request.user.is_supervisor or request.user.is_shop_incharge):
		return redirect('/login')

	Ticket_No = id
	leaves = cumulativeLeavesDatabase.objects.all_leaves()
	leaves = leaves.filter(Ticket_No = Ticket_No,status = 1,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	name = get_object_or_404(CustomUser,Ticket_No = Ticket_No).Complete_Name
	employee = get_object_or_404(CustomUser, Ticket_No = id)
	quota = get_object_or_404(leavesDatabase,Ticket_No = id)
 
	dataset = dict()
	dataset['employee'] = employee
	dataset['quota'] = quota
	dataset['title'] = 'profile - {0}'.format(employee.Complete_Name)
	dataset['leave_list'] = leaves
	dataset['name'] = name
	dataset['ticket'] = Ticket_No

	return render(request,'dashboard/employee_detail.html',dataset)


def personalwaiting(request,id):
	if not (request.user.is_supervisor or request.user.is_shop_incharge):
		return redirect('/login')

	Ticket_No = id
	leaves = cumulativeLeavesDatabase.objects.all_leaves()
	leaves = leaves.filter(Ticket_No = Ticket_No,status = 0,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	name = get_object_or_404(CustomUser,Ticket_No = Ticket_No).Complete_Name
	employee = get_object_or_404(CustomUser, Ticket_No = id)
	quota = get_object_or_404(leavesDatabase,Ticket_No = id)
 
	dataset = dict()
	dataset['employee'] = employee
	dataset['quota'] = quota
	dataset['title'] = 'profile - {0}'.format(employee.Complete_Name)
	dataset['leave_list'] = leaves
	dataset['name'] = name
	dataset['ticket'] = Ticket_No
 
	return render(request,'dashboard/employee_detail.html',dataset)

def personalrejected(request,id):
	if not (request.user.is_supervisor or request.user.is_shop_incharge):
		return redirect('/login')

	Ticket_No = id
	leaves = cumulativeLeavesDatabase.objects.all_leaves()
	leaves = leaves.filter(Ticket_No = Ticket_No,status = 2,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	name = get_object_or_404(CustomUser,Ticket_No = Ticket_No).Complete_Name
	employee = get_object_or_404(CustomUser, Ticket_No = id)
	quota = get_object_or_404(leavesDatabase,Ticket_No = id)
 
	dataset = dict()
	dataset['employee'] = employee
	dataset['quota'] = quota
	dataset['title'] = 'profile - {0}'.format(employee.Complete_Name)
	dataset['leave_list'] = leaves
	dataset['name'] = name
	dataset['ticket'] = Ticket_No

	return render(request,'dashboard/employee_detail.html',dataset)







# ------------------------------------Action on Leaves--------------------------------------

def unapprove_leave(request,id):
	if not (request.user.is_authenticated and (request.user.is_supervisor or request.user.is_shop_incharge)):
		return redirect('/login')

	leave = get_object_or_404(cumulativeLeavesDatabase, id = id)
	Ticket_No = leave.Ticket_No
	
	validate = get_object_or_404(leavesDatabase,Ticket_No = Ticket_No)
	leaveType = leave.leave_type
	duration = leave.leave_duration
	fromDate = str(leave.from_date)
	toDate = str(leave.to_date)
	start_date = datetime.datetime.strptime(fromDate, '%Y-%m-%d').date()
	end_date = datetime.datetime.strptime(toDate, '%Y-%m-%d').date()
	holidays = holidayList.objects.filter(Q(date_today__gte=start_date,date_today__lte=end_date)).count()
	if (duration == 'Second Half' or duration == 'First Half') and holidays:
		holidays = 0.5
	if(leaveType == 'CL( Casual Leave )'):				
		validate.total_available_cl = validate.total_available_cl + leave.leave_days - holidays
		validate.save()
	elif(leaveType == 'PL( Privilege Leave )'):
		validate.total_available_pl = validate.total_available_pl + leave.leave_days - holidays
		validate.save()
	else:
		validate.total_available_sl = validate.total_available_sl + leave.leave_days - holidays
		validate.save()
	leave.reason = ''
	leave.action_by = request.user.Complete_Name
	leave.unapprove_leave
 
	line = leave.Cost_Center_Name

	while start_date <= end_date:
		holi = holidayList.objects.filter(date_today = start_date)
		if holi.count():
			delapprovedLeavesDatabase.objects.filter(Ticket_No = Ticket_No,Cost_Center_Name = line,on_date = start_date).delete()
		else:
			approvedLeavesDatabase.objects.filter(Ticket_No = Ticket_No,Cost_Center_Name = line,on_date = start_date).delete()
		start_date = start_date + datetime.timedelta(days=1)
 
	messages.warning(request,'Leave is now in Waiting list',extra_tags = 'alert alert-warning alert-dismissible fade show')
	
	return redirect('dashboard:leaveslist') 



def approve_leave(request,id):
	if not ((request.user.is_supervisor or request.user.is_shop_incharge) and request.user.is_authenticated):
		return redirect('/login')
	leave = get_object_or_404(cumulativeLeavesDatabase, id = id)
	Ticket_No = leave.Ticket_No

	validate = get_object_or_404(leavesDatabase,Ticket_No = Ticket_No)
	leaveType = leave.leave_type
	leave_duration = leave.leave_duration
	
	fromDate = str(leave.from_date)
	toDate = str(leave.to_date)
	start_date = datetime.datetime.strptime(fromDate, '%Y-%m-%d').date()
	end_date = datetime.datetime.strptime(toDate, '%Y-%m-%d').date()
	holidays = holidayList.objects.filter(Q(date_today__gte=start_date,date_today__lte=end_date)).count()
	if (leave_duration == 'Second Half' or leave_duration == 'First Half') and holidays:
		holidays = 0.5
	if(leaveType == 'CL( Casual Leave )'):
		if(leave.leave_days > validate.total_available_cl):
			messages.warning(request,'Insufficient Leave Quota',extra_tags = 'alert alert-warning alert-dismissible fade show')
			return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
		else:
			validate.total_available_cl = validate.total_available_cl - leave.leave_days + holidays
			validate.save()
	elif(leaveType == 'PL( Privilege Leave )'):
		if(leave.leave_days > validate.total_available_pl):
			messages.warning(request,'Insufficient Leave Quota',extra_tags = 'alert alert-warning alert-dismissible fade show')
			return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
		else:
			validate.total_available_pl = validate.total_available_pl - leave.leave_days + holidays
			validate.save()
	else: 
		if(leave.leave_days > validate.total_available_sl):
			messages.warning(request,'Insufficient Leave Quota',extra_tags = 'alert alert-warning alert-dismissible fade show')
			return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
		else:
			validate.total_available_sl = validate.total_available_sl - leave.leave_days + holidays
			validate.save()
      
	employee = get_object_or_404(CustomUser,Ticket_No = Ticket_No)
	leave.reason = ''
	Complete_Name = request.user.Complete_Name
	leave.action_by = Complete_Name
	leave.approve_leave
	

	while start_date <= end_date:
		holi = holidayList.objects.filter(date_today = start_date)
		if holi.count():
			delapprovedLeavesDatabase.objects.get_or_create(
                Ticket_No = Ticket_No,
                Current_Shop = leave.Current_Shop,
                Cost_Center_Name = leave.Cost_Center_Name,
                leave_duration = leave.leave_duration,
                leave_type = leave.leave_type,
                on_date = start_date,
                approved_on_date_time = timezone.now(),
                approved_by = request.user.Complete_Name
            )
		else:
			approvedLeavesDatabase.objects.get_or_create(
				Ticket_No = Ticket_No,
				Current_Shop = leave.Current_Shop,
				Cost_Center_Name = leave.Cost_Center_Name,
				leave_duration = leave_duration,
				leave_type = leaveType,
				on_date = start_date,
				approved_on_date_time = timezone.now(),
				approved_by = Complete_Name
			)
		start_date = start_date + datetime.timedelta(days=1)
 
 
 
	messages.success(request,'Leave successfully approved for {0}'.format(employee.Complete_Name),extra_tags = 'alert alert-success alert-dismissible fade show')

	return redirect('dashboard:leaveslist')


def reject_leave(request,id):
	dataset = dict()
	leave = get_object_or_404(cumulativeLeavesDatabase, id = id)
	Ticket_No = leave.Ticket_No
	reason = request.GET.get('reason')
	validate = get_object_or_404(leavesDatabase,Ticket_No = Ticket_No)
	leaveType = leave.leave_type
	leave.reason = reason
	leave.action_by = request.user.Complete_Name
	duration = leave.leave_duration
	fromDate = str(leave.from_date)
	toDate = str(leave.to_date)
	start_date = datetime.datetime.strptime(fromDate, '%Y-%m-%d').date()
	end_date = datetime.datetime.strptime(toDate, '%Y-%m-%d').date()
 
	holidays = holidayList.objects.filter(Q(date_today__gte=start_date,date_today__lte=end_date)).count()
	if (duration == 'Second Half' or duration == 'First Half') and holidays:
		holidays = 0.5
	if leave.status == 1 and leaveType == 'CL( Casual Leave )':	
		validate.total_available_cl = validate.total_available_cl + leave.leave_days - holidays
		validate.save()
	elif leave.status == 1 and leaveType == 'PL( Privilege Leave )' :
		validate.total_available_pl = validate.total_available_pl + leave.leave_days - holidays
		validate.save()
	elif leave.status == 1 and leaveType == 'SL( Sick Leave )' :
		validate.total_available_sl = validate.total_available_sl + leave.leave_days - holidays
		validate.save()
	leave.reject_leave
 

	line = leave.Cost_Center_Name
	
	while start_date <= end_date:
		holi = holidayList.objects.filter(date_today = start_date)
		if holi.count():
			delapprovedLeavesDatabase.objects.filter(Ticket_No = Ticket_No,Cost_Center_Name = line,on_date = start_date).delete()
		else:
			approvedLeavesDatabase.objects.filter(Ticket_No = Ticket_No,Cost_Center_Name = line,on_date = start_date).delete()
		start_date = start_date + datetime.timedelta(days=1)
	
	messages.warning(request,'Leave is rejected',extra_tags = 'alert alert-warning alert-dismissible fade show')
	if request.user.is_shop_incharge:
		x = 1
	else:
		x = 2
	data = {'x': x}
 
	return JsonResponse(data)


def unreject_leave(request,id):
	if not (request.user.is_supervisor or request.user.is_shop_incharge):
		return redirect('/logout')
	leave = get_object_or_404(cumulativeLeavesDatabase, id = id)
	leave.reason = ''
	leave.action_by = request.user.Complete_Name
	leave.unreject_leave
	messages.success(request,'Leave is now in Pending list ',extra_tags = 'alert alert-success alert-dismissible show')
 
	return redirect('dashboard:leaveslist')




