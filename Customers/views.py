'''
    Authors: Abid Khan and Ehtisham
    
    Repository: https://github.com/abidkhan03,
                https://github.com/CodeWithEhtisham
'''

from multiprocessing.sharedctypes import Value
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from Sales.models import Sales, Bill
from Sales.serializer import SalesSerializer
from .models import Customers
import pandas as pd
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CustomersSerializer
from django.utils import timezone
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from rest_framework import viewsets



def long_process(df):
    try:
        rename = {
            'ID': 'customer_id',
            'Address': 'customer_address',
            'Name': 'customer_name',
            'Rank': 'customer_rank',
        }
        df.rename(columns=rename, inplace=True)
        print(df.columns)
        for index, row in df.iterrows():
            print(row)
            if (Customers.objects.filter(
                customer_rank=row['customer_rank'],
                customer_address=row['customer_address'],
                    customer_name=row['customer_name']).exists()):
                continue
                # messages.error("Customer id already exists")
            # else:
            Customers.objects.create(
                customer_id=row['customer_id'],
                customer_name=row['customer_name'],
                customer_address=row['customer_address'],
                customer_rank=row['customer_rank'],
            ).save()
        return True

    except Exception as e:
        print("failed", e)
        return False

##################################### Add & details Customer Functions ###


def signin(request):
    if request.method == 'POST':
        try:
            if request.POST.get('login_button'):
                username = request.POST.get('username')
                password = request.POST.get('password')
                # user = authenticate(username=username, password=password)
                # print('user: ', user)
                # if user is not None and user.is_active and user.is_authenticated:
                #     login(request, user)
                #     messages.success(request, f"You are now logged in as {username}")
                #     return redirect('index')
                # else:
                #     messages.error(request, "Invalid Credentials")
                #     return redirect('Customers:signin')
                if User.objects.get(username=username):
                    user = User.objects.get(username=username)
                    auth = authenticate(
                        username=user.username, password=password)
                    print('user: ', user)
                # if user is not None and user.is_authenticated:
                    if auth:
                        print('auth')
                        login(request, user)
                        messages.success(
                            request, f"You are now logged in as {username}")
                        return HttpResponseRedirect(reverse('Customers:index'))
                    else:
                        print('user login failed')
                        messages.error(request, "Invalid username or password")
                        return HttpResponseRedirect(reverse('Customers:signin'))
                else:
                    print('user login failed')
                    messages.error(request, "Invalid user")
                    return HttpResponseRedirect(reverse('Customers:signin'))
        except Exception as e:
            print('login error', e)
            messages.error(request, "Invalid user")
            return HttpResponseRedirect(reverse('Customers:signin'))
    else:
        return render(request, 'Customers/signin.html')


@login_required
def index(request):
    if User.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'Customers/signin.html')
    # return render(request, "index.html")


def logout_user(request):
    logout(request)
    return render(request, 'Customers/signin.html')


@login_required
def customers(request):
    if request.method == 'POST':
        try:
            if request.POST.get('Save'):
                if Customers.objects.filter(
                        customer_address=request.POST.get('customer_address'),
                        customer_name=request.POST.get("customer_name"),
                        customer_rank=request.POST.get('customer_rank')).exists():
                    messages.error(request, 'Customer is Already Exists')
                    return redirect('Customers:customers')
                if Customers.objects.filter(customer_id=request.POST.get('customer_id')).exists():
                    messages.error(request, 'Customer ID is Already Exists')
                    return redirect('Customers:customers')
                else:
                    Customers(customer_name=request.POST.get('customer_name'),
                              customer_rank=request.POST.get('customer_rank'),
                              customer_id=request.POST.get('customer_id'),
                              customer_address=request.POST.get(
                                  'customer_address'),
                              customer_file=request.FILES.get('customer_file')).save()
                    messages.success(request, 'Customer Added Successfully')
                    return HttpResponseRedirect(reverse('Customers:customers'))

            elif request.POST.get('customer_file_submit'):
                # print("customer_file_submit")
                csv = request.FILES['customer_file']
                if not csv.name.split('.')[1] in ['csv', 'xlsx', 'xls']:
                    messages.error(
                        request, 'This is not a correct formate file')
                    return HttpResponseRedirect(reverse('Customers:customers'))
                else:
                    myfile = request.FILES["customer_file"]
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name, myfile)
                    uploaded_file_url = fs.url(filename)
                    excel_file = uploaded_file_url
                    print("." + excel_file)
                    print(csv.name.split('.')[-1])
                    if csv.name.split('.')[-1] in ['csv', 'CSV']:
                        df = pd.read_csv("." + excel_file)
                        if long_process(df):
                            messages.success(request, 'csv added to database')
                            return HttpResponseRedirect(reverse('Customers:customers'))
                    elif csv.name.split('.')[-1] in ['xlsx', 'XLSX', 'xls', 'XLS']:
                        print("excel")
                        df = pd.read_excel("." + excel_file)
                        if long_process(df):
                            messages.success(
                                request, 'excel added to database')
                            return HttpResponseRedirect(reverse('Customers:customers'))

                    raise Exception("File not found")
            # if request.POST.get('edit_customer'):
            # return render(request, "Customers/customer_update.html",
            # {'customer_data':
            # Customers.objects.filter(id=request.POST.get("cid"))[0]})

        except Exception as e:  # Exception as e:
            messages.error(request, 'Customer Added Failed {}'.format(e))
            return HttpResponseRedirect(reverse('Customers:customers'))
    else:
        # every customer net amount sales

        ids = Sales.objects.values_list('customer_id', flat=True).distinct()
        ids = [i for i in ids]
        customer = Customers.objects.exclude(id__in=ids).order_by('-id')
        sales=[]
        for i in list(set(ids)):
            c=Customers.objects.filter(id=i).first()
            sales.append(
                {
                    'total_amount':Sales.objects.filter(customer_id=c).aggregate(Sum('net_amount'))['net_amount__sum'] ,
                    'customer_id':c.customer_id,
                    'customer_name':c.customer_name,
                    'customer_rank':c.customer_rank,
                    'customer_address':c.customer_address,
                    'id':c.id
                },
            )
        print(customer)
        return render(request, 'Customers/customers.html',
                      {
                          'customer_table': customer,
                          'customers_table': sales,
                          'all_customers': Customers.objects.all().count(),
                          'all_staffs': Customers.objects.all().filter(customer_rank__in=['Army', 'Staff', 'Members']).values('customer_rank').annotate(count=Count('pk', distinct=True))

                      })


@login_required
def customer_update(request):
    if request.method == 'POST':
        try:
            if request.POST.get('update_customer'):
                Customers.objects.filter(id=request.POST.get('cid')).update(
                    customer_name=request.POST.get('customer_name'),
                    customer_rank=request.POST.get('customer_rank'),
                    customer_id=request.POST.get('customer_id'),
                    customer_address=request.POST.get('customer_address'))
                messages.success(request, 'Customer Updated Successfully')
                return HttpResponseRedirect(reverse('Customers:customers'))
        except Exception as e:
            messages.error(request, 'Customer Update Failed {}'.format(e))
            return HttpResponseRedirect(reverse('Customers:customers'))
    else:
        return render(request, "Customers/customer_update.html",
                      {'customer_data': Customers.objects.filter(id=request.GET.get("id")).first()})

@login_required
def delete_customer(request, pk):
    query = Customers.objects.get(id=pk)
    if request.method == 'POST':
        query.delete()
        messages.success(request, 'Customer Deleted Successful')
        return HttpResponseRedirect(reverse("Customers:customers"))
    return render(request, 'Customers/delete_customer.html', {
        'querysale': query
    })

@login_required
def customer_details(request):
    return render(request, "Customers/customer_details.html", {
        'sale_id': request.GET.get("id"),
        'Sales_data': Sales.objects.filter(customer_id__id=request.GET.get("id")).select_related('customer_id').order_by("-id"),
        'all_bills': Sales.objects.filter(customer_id__id=request.GET.get("id")).select_related('bill_no').count(),
        'total_amount': Sales.objects.filter(customer_id__id=request.GET.get("id")).select_related('bill_no').aggregate(Sum('amount'))['amount__sum'],
        'total_discount': Sales.objects.filter(customer_id__id=request.GET.get("id")).select_related('bill_no').aggregate(Sum('discount'))['discount__sum'],
        'total_net_amount': Sales.objects.filter(customer_id__id=request.GET.get("id")).select_related('bill_no').aggregate(Sum('net_amount'))['net_amount__sum'],
    })


@login_required
def customer_bill(request):
    if request.method == 'POST':
        if request.POST.get('save_bill'):
            if Bill.objects.filter(sale_id__id=request.POST.get('sale_id')).exists():
                messages.error(request, 'This Bill No is Already Exists')
                return redirect('Customers:customer_bill')
            customer = Customers.objects.filter(
                customer_name=request.POST.get('customer_name'),
                customer_rank=request.POST.get('customer_rank')).first()

            Sales(bill_no=request.POST.get('bill_no'),
                  PoS_no=request.POST.get('PoS_no'),
                  month=request.POST.get('month'),
                  created_date=request.POST.get('date'),
                  created_on=request.POST.get('created_on'),
                  address=request.POST.get('address'),
                  account_of=request.POST.get('account_of'),
                  amount=request.POST.get('amount'),
                  discount=request.POST.get('discount'),
                  net_amount=request.POST.get('net_amount'),
                  remarks=request.POST.get('remarks'),
                  customer_id=customer
                  ).save()
            messages.success(request, 'Sales Added Successful')
            return redirect("Customers:customers")
    else:
        return render(request, 'Customers/customer_bill.html', {
        'customer_data': Customers.objects.filter(id=request.GET.get("id")).first(),
        'sales': Sales.objects.all()
    })


        

# @api_view(['GET'])
# def SearchCustomer(request):
#     field = request.GET.get('field')
#     value = request.GET.get('value')

#     try:
#         if field == 'Name':
#             return Response(Customers.objects.all())
#         elif field == 'Rank':
#             return Response(CustomersSerializer(Customers.objects.filter(customer_rank__icontains=value).order_by('-id'), many=True).data)
#         elif field == 'ID':
#             # return Response(SalesSerializer(Sales.objects.select_related('customer_id').filter(customer_id__customer_id__icontains=value).annotate(total_amount=Sum('net_amount')),many=True).data)
            
#             return Response(CustomersSerializer(Customers.objects.filter(customer_id__exact=value).order_by('-id'), many=True).data)
#         elif field == 'Address':
#             return Response(CustomersSerializer(Customers.objects.filter(customer_address__icontains=value).order_by('-id'), many=True).data)

#     except Exception as e:
#         return Response({"message": "No data found {}".format(e)})


@api_view(['GET', 'POST'])
def pay_bill(request):

    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        rv_no = request.POST.get('rv_no')
        paid_date = request.POST.get('paid_date')
        amount = request.POST.get('amount')
        remaining_amount = request.POST.get('remaining_amount')
        print("remaining amount ", remaining_amount)

        Bill.objects.create(rv_no=rv_no, date=paid_date, amount=amount,
                            status="Paid", sale_id=Sales.objects.get(id=id))

        Sales.objects.filter(id=id).update(net_amount=remaining_amount)

        print("sale net amount ", Sales.objects.filter(id=id).first())
        return Response({"message": "Bill Paid Successfully"})


@api_view(['GET', 'POST'])
def pay_all_bills(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print('dasfjaskdfj ', id)
        rv_no = request.POST.get('rv_no')
        print('#################################',request.POST.get('paid_date'))
        paid_date = timezone.datetime.strptime((request.POST.get('paid_date')),'%d-%m-%Y')
        amount = request.POST.get('amount')
        remaining_amount = request.POST.get('remaining_amount')
        print("remaining amount ", remaining_amount)

        Bill.objects.create(rv_no=rv_no, date=paid_date, amount=amount,
                            status="Paid", sale_id=Sales.objects.get(id=id))

        Sales.objects.filter(id=id).update(net_amount=remaining_amount)

        print("sale net amount ", Sales.objects.filter(id=id).first())
        return Response({"message": "Bill Paid Successfully"})


@api_view(['GET', 'POST'])
def comp_bill(request):
    if request.method == "POST":
        id = request.POST.get('id')
        date = request.POST.get('comp_date')
        amount = request.POST.get('comp_amount')
        remarks = request.POST.get('comp_remarks')
        remaining_amount = request.POST.get('remaining_amount')

        Bill.objects.create(amount=amount, date=date, bill_remarks=remarks,
                            status="Complementery", sale_id=Sales.objects.get(id=id))

        Sales.objects.filter(id=id).update(net_amount=remaining_amount)
        return Response({"message": "Complement Bill Added Successfully"})


@api_view(['GET', 'POST'])
def cancel_bill(request):

    if request.method == "POST":
        id = request.POST.get('id')
        date = request.POST.get('cancel_date')
        reason = request.POST.get('reason')
        remaining_amount = request.POST.get('remaining_amount')
        amount = request.POST.get('amount')
        Bill.objects.create(date=date, reason=reason,
                            status='Cancel', sale_id=Sales.objects.get(id=id))

        remaining_amount = 0
        amount = 0
        Sales.objects.filter(id=id).update(
            amount=amount, net_amount=remaining_amount)
        messages.success(request, "Bill Cancelled Successfully")
        return HttpResponse({"message": "Cancel Bill Added Successfully"})


@api_view(['POST'])
@login_required
def bills_upload(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        jsons = request.data
        print(jsons['myrows'][0])
        for obj in jsons['myrows']:
            print(obj)
            Bill.objects.create(
                # rv_no=obj['rv_no'],
                date=timezone.now(),
                amount=obj['Net Amount'],
                status="Paid",
                sale_id=Sales.objects.get(id=id)
            ).save()
        print(Bill.objects.values().last())
        return Response({"message": "Bills Uploaded Successfully"})


# urls paths and apis
index_template = [
    path('', signin, name='signin'),
    path('signin/', signin, name='signin'),
    path('index/', index, name='index'),
    path('customers/', customers, name='customers'),
    path('customer_details/', customer_details, name='customer_details'),
    path('customer_update/', customer_update, name='customer_update'),
    path('customer_bill/', customer_bill, name='customer_bill'),
    path('logout', logout_user, name='logout'),
    path('delete_customer/<int:pk>/', delete_customer, name="delete_customer"),
    # api url paths
    # path('api/SearchCustomer/', SearchCustomer, name='SearchCustomer'),
    path('api/customer/pay_bill/', pay_bill, name='pay_bill'),
    path('api/customer/comp_bill/', comp_bill, name='comp_bill'),
    path('api/customer/cancel_bill/', cancel_bill, name='cancel_bill'),
    path('api/customer/bills_upload/', bills_upload, name='bills_upload'),
    path('api/customer/pay_all_bills/', pay_all_bills, name='pay_all_bills'),
]
