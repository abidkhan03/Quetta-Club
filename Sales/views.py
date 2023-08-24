
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
from django.contrib import messages
from .models import Sales, Bill, dummyTable
from Customers.models import Customers
import pandas as pd
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import SalesSerializer, BillSerializer
from django.db.models import Sum, Count
import datetime
import re
import os
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q


def long_process(df):
    try:
        # rename
        # print('dsafasdf', df.columns)
        rename = {
            "Bill No": 'bill_no',
            "Rank": 'rank',
            "POS No": 'PoS_no',
            "Name": 'cname',
            "Address": 'address',
            "On Account of": 'account_of',
            "Dated": 'date',
            "Month": 'month',
            "Amount": 'amount',
            "Discount": 'discount',
            "Net Amount": 'net_amount'
        }
        df.rename(columns=rename, inplace=True)
        # print(df.columns)
        for index, row in df.iterrows():
            try:
                # print(row['cname'])
                if Customers.objects.filter(
                    customer_name=row['cname'],
                    customer_rank=row['rank'], 
                    customer_address=row['address']).exists():
                    
                    dummyTable.objects.create(
                        bill_no=row['bill_no'],
                        rank=row['rank'],
                        pos_no=row['PoS_no'],
                        cname=row['cname'],
                        address=row['address'],
                        account_of=row['account_of'],
                        # date=datetime.datetime.strptime(
                        #     row['date'], "%d-%m-%Y").date(),
                        date=row['date'],
                        month=row['month'],
                        amount=row['amount'],
                        discount=row['discount'],
                        net_amount=row['net_amount'],
                        status="already exists"

                    ).save()
                else:
                    dummyTable.objects.create(
                        bill_no=row['bill_no'],
                        rank=row['rank'],
                        pos_no=row['PoS_no'],
                        cname=row['cname'],
                        address=row['address'],
                        account_of=row['account_of'],
                        # date=datetime.datetime.strptime(
                        #     row['date'], "%d-%b-%Y").date(),
                        date=row['date'],
                        month=row['month'],
                        amount=row['amount'],
                        discount=row['discount'],
                        net_amount=row['net_amount'],
                        status="new"

                    ).save()
            except Exception as e:
                print(e)
                continue
        return True
    except Exception as e:
        print(
            type(e).__name__,          # TypeError
            __file__,                  # /tmp/example.py
            e.__traceback__.tb_lineno  # 2
        )
        return False


@login_required
def sales(request):
    print("###############################################", request.method)
    print("dummy date ", dummyTable.objects.values().last())
    if request.method == 'POST':
        try:
            if request.POST.get('Save'):
                # print(request.POST.get('customer_name'))

                customer = Customers.objects.filter(customer_name=request.POST.get(
                    'customer_name'), customer_rank=request.POST.get('customer_rank'))
                # print(customer)
                dummyTable.objects.create(
                    bill_no=request.POST.get('bill_no'),
                    rank=request.POST.get('customer_rank'),
                    pos_no=request.POST.get('PoS_no'),
                    cname=request.POST.get('customer_name'),
                    address=request.POST.get('address'),
                    account_of=request.POST.get('account_of'),
                    date=request.POST.get('date'),
                    month=request.POST.get('month'),
                    amount=request.POST.get('amount'),
                    discount=request.POST.get('discount'),
                    net_amount=request.POST.get('net_amount'),
                    remarks=request.POST.get('remarks'),
                    status="new" if not customer else "already exists"
                ).save()
                # print('dummy date ', dummyTable.date)
                messages.success(request, 'Sales Added Successful')
                return HttpResponseRedirect(reverse("Sales:sales"))

            elif request.POST.get('upload_bills'):

                messages.success(request, 'Sales Added Successful')
                return HttpResponseRedirect(reverse("Sales:sales"))

            elif request.POST.get('delete_all'):
                dummyTable.objects.all().delete()
                messages.success(
                    request, "All today's Bills have been deleted successfully")
                return redirect('Sales:sales')

            elif request.POST.get('sale_file_submit'):
                print("customer_file_submit")
                csv = request.FILES['sale_file']
                if not csv.name.split('.')[1] in ['csv', 'xlsx', 'xls']:
                    messages.error(
                        request, 'This is not a correct format file')
                else:
                    myfile = request.FILES["sale_file"]
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name, myfile)
                    uploaded_file_url = fs.url(filename)
                    excel_file = uploaded_file_url
                    # print("."+excel_file)
                    # print(csv.name.split('.')[-1])
                    if csv.name.split('.')[-1] in ['csv', 'CSV']:
                        print("csv")
                        df = pd.read_csv("." + excel_file)
                        for file in os.listdir("media/"):
                            print(os.path.join("media/", file))
                            os.remove(os.path.join("media/", file))
                        if long_process(df):
                            messages.success(
                                request, 'Sales csv Added Successful')
                            return HttpResponseRedirect(reverse("Sales:sales"))
                    elif csv.name.split('.')[-1] in ['xlsx', 'XLSX', 'xls', 'XLS']:
                        print("excel")
                        df = pd.read_excel("." + excel_file)
                        for file in os.listdir("media/"):
                            print(os.path.join("media/", file))
                            os.remove(os.path.join("media/", file))
                        if long_process(df):
                            messages.success(
                                request, 'Sales excel Added Successful')
                            return HttpResponseRedirect(reverse("Sales:sales"))
                raise Exception("File not found")
        except Exception as e:  # Exception as e:
            messages.error(request, 'Sales Added Failed', e)
            return HttpResponse("Please fill the required fields! Back to Sales page {}".format(e), status=400)

    else:
        print(dummyTable.objects.all())
        return render(request, "Sales/sales.html", {
            'customers': Customers.objects.all(),
            'sales': Sales.objects.all(),
            'dummy': dummyTable.objects.all().order_by('-id'),
        })


@login_required
def delete_items(request, pk):
    queryset = dummyTable.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Sales Deleted Successful')
        return HttpResponseRedirect(reverse("Sales:sales"))
    return render(request, 'Sales/delete_items.html', {
        'queryset': queryset
    })


def delete_sale(request, pk):
    querysale = Sales.objects.get(id=pk)
    if request.method == 'POST':
        querysale.delete()
        messages.success(request, 'Sales Deleted Successful')
        return HttpResponseRedirect(reverse("Sales:view_sales"))
    return render(request, 'Sales/delete_sale.html', {
        'querysale': querysale
    })


@login_required
def view_sales(request):

    return render(request, "Sales/view_sales.html", {
        'sales_data': Sales.objects.filter(net_amount__gt=0).select_related('customer_id').order_by("-bill_no"),
        'total_bills': Sales.objects.filter(net_amount__gt=0).count(),
        'total_amount': Sales.objects.filter(net_amount__gt=0).aggregate(Sum('amount'))['amount__sum'],
        'total_discount': Sales.objects.filter(net_amount__gt=0).aggregate(Sum('discount'))['discount__sum'],
        'total_net_amount': Sales.objects.filter(net_amount__gt=0).aggregate(Sum('net_amount'))['net_amount__sum'],
    })


@login_required
def update_sales(request):
    if request.method == "POST":
        try:
            if request.POST.get('update_bill'):
                customer = Customers.objects.filter(customer_name=request.POST.get('customer_name'),
                                                    customer_rank=request.POST.get('customer_rank'))

                dummyTable.objects.filter(id=request.POST.get('edit_id')).update(
                    bill_no=request.POST.get('bill_no'),
                    pos_no=request.POST.get('PoS_no'),
                    month=request.POST.get('month'),
                    date=request.POST.get('date'),
                    address=request.POST.get('address'),
                    account_of=request.POST.get('account_of'),
                    amount=request.POST.get('amount'),
                    discount=request.POST.get('discount'),
                    net_amount=request.POST.get('net_amount'),
                    remarks=request.POST.get('remarks'),
                    status="new" if not customer else "already exists",
                    cname=request.POST.get('customer_name'),
                    rank=request.POST.get('customer_rank'),
                )

                return HttpResponseRedirect(reverse("Sales:sales"))

            elif request.POST.get('cancel'):
                return HttpResponseRedirect(reverse("Sales:sales"))
        except Exception as e:
            messages.error(request, f'Sales Update Failed {e}')
            return HttpResponseRedirect(reverse("Sales:view_sales"))

    else:
        return render(request, "Sales/update_sales.html", {
            'dummy_data': dummyTable.objects.filter(id=request.GET.get('id')).first(),
            'customers': Customers.objects.all(),
            'sales': Sales.objects.all(),
        })


@login_required
def update_view_sale(request):
    if request.method != "POST":
        return render(request, "Sales/update_view_sale.html", {
            'sales_data': Sales.objects.filter(id=request.GET.get('id')).first(),
            'customers': Customers.objects.all(),
            'sales': Sales.objects.all(),
        })
    try:
        if request.POST.get("update_sale"):
            customer = Customers.objects.get(
                customer_name=request.POST.get('customer_name'), 
                customer_rank=request.POST.get('customer_rank'))
            # print("customer... ",customer.count())
            # print("sale id ",Sales.objects.filter(id=request.POST.get('saleId')).count())

            Sales.objects.filter(
                id=request.POST.get('saleId')).update(
                bill_no=request.POST.get('bill_no'),
                PoS_no=request.POST.get('PoS_no'),
                month=request.POST.get('month'),
                created_date=request.POST.get('date'),
                address=request.POST.get('address'),
                account_of=request.POST.get('account_of'),
                amount=request.POST.get('amount'),
                discount=request.POST.get('discount'),
                net_amount=request.POST.get('net_amount'),
                remarks=request.POST.get('remarks'),
                customer_id=customer
            )
            messages.success(request, "sale bill updated successfully")
            return HttpResponseRedirect(reverse("Sales:view_sales"))

        elif request.POST.get('cancel'):
            return HttpResponseRedirect(reverse("Sales:view_sales"))
    except Exception as e:
        messages.error(request, f"Sales update failed {e}")
        return HttpResponse(f"Error: {e}", status=400)


@login_required
def reports(request):
    # print(Sales.objects.filter(customer_id__id=request.GET.get(
    #     "id")).select_related('customer_id').order_by("-id"))
    if request.method == "POST":
        from_date=request.POST.get('from-date')
        to_date=request.POST.get('to-date')
        status=request.POST.get('check')
        print(from_date,to_date,status)
        if status:
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            return render(request, 'Sales/reports.html', {
                    'record': Bill.objects.select_related('sale_id').filter(status=status,date__range=[from_date,to_date] ).order_by('-id')
                })
        else:
                return render(request, 'Sales/reports.html', {
                    'record': Bill.objects.select_related('sale_id').filter(date__range=[from_date,to_date]).order_by('-id')
                })
    else:
        return render(request, 'Sales/reports.html', {
        'record': Bill.objects.all().select_related('sale_id').order_by('-id'),
        'total_paid': Bill.objects.filter(
            status__startswith="Paid").annotate(
                total_paid=Count('status')).count(),
        'total_complementary': Bill.objects.filter(
            status__startswith="Complementery").annotate(
                total_comp=Count('status')).count(),
        'total_cancelled': Bill.objects.filter(
            status__startswith="Cancelled").annotate(
                total_cancelled=Count('status')).count(),
        'total_paid_amount': Bill.objects.filter(
            status__startswith="Paid").aggregate(
                Sum('amount'))['amount__sum'],
        'total_comp_amount': Bill.objects.filter(
            status__startswith="Complementery").aggregate(
                Sum('amount'))['amount__sum'],
        'total_cancel_amount': Bill.objects.filter(
            status__startswith="Cancelled").aggregate(
                Sum('amount'))['amount__sum'],
        'total_amount': Bill.objects.aggregate(
            Sum('amount'))['amount__sum'],
    })


@api_view(['GET'])
def SearchbyName(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    rank=request.GET.get('rank')
    # print(SalesSerializer(Sales.objects.filter(query).order_by('-id'), many=True).data)
    try:
        lookup = f"{field}__icontains"
        if rank:
            print(field)
            if field=='customer_name':
                # field=
                lookup=f'customer_id__{field}__icontains'
                query=Q(**{lookup:value})
                return Response(SalesSerializer(Sales.objects.filter(customer_id__customer_rank=rank).filter(query).order_by('-id'), many=True).data)
            else:
                query=Q(**{lookup: value})
                return Response(SalesSerializer(Sales.objects.select_related('customer_id').filter(customer_id__customer_rank=rank).filter(query).order_by('-id'), many=True).data)
        else:
            if field=='customer_name':
                lookup=f'customer_id__{field}__icontains'
                query = Q(**{lookup: value})
                return Response(SalesSerializer(Sales.objects.filter(query).order_by('-id'), many=True).data)
            else:
                query=Q(**{lookup: value})
                return Response(SalesSerializer(Sales.objects.select_related('customer_id').filter(query).order_by('-id'), many=True).data)
    except Exception as e:
        lookup = f"customer_id__{field}__icontains"
        query=Q(**{lookup: value})
        return Response(SalesSerializer(Sales.objects.select_related('customer_id').filter(customer_id__customer_rank=rank).filter(query).order_by('-id'), many=True).data)


@api_view(['GET'])
def SearchbyNameReport(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    rank = request.GET.get('rank')
    try:
        if rank:
            if field in ['rv_no','date']:
                print('in if')
                lookup = f"{field}__icontains"
                query=Q(**{lookup: value})
                return Response(BillSerializer(Bill.objects.filter(sale_id__customer_id__customer_rank__icontains=rank).filter(query).order_by('-id'), many=True).data)
            elif field in ['name']:
                return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(sale_id__customer_id__customer_rank__icontains=rank).filter(sale_id__customer_id__customer_name__icontains=value).order_by('-id'), many=True).data)
            else:
                lookup = f"sale_id__{field}__icontains"
                query=Q(**{lookup: value})
                return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(sale_id__customer_id__customer_rank=rank).filter(query).order_by('-id'), many=True).data)
        elif field in ['rv_no','date']:
            print('in if')
            lookup = f"{field}__icontains"
            query=Q(**{lookup: value})
            return Response(BillSerializer(Bill.objects.filter(query).order_by('-id'), many=True).data)
        elif field in ['name']:
            return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(sale_id__customer_id__customer_name__icontains=value).order_by('-id'), many=True).data)
        else:
            lookup = f"sale_id__{field}__icontains"
            query=Q(**{lookup: value})
            return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(query).order_by('-id'), many=True).data)
            
            # elif field == 'rank':
            #     # return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(sale_id__customer_id__customer_rank__icontains=value).order_by('-id'), many=True).data)
            # elif field == 'bill_no':
            #     return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(sale_id__bill_no__iexact=value).order_by('-id'), many=True).data)
            # elif field == 'pos_no':
            #     return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(sale_id__PoS_no__iexact=value).order_by('-id'), many=True).data)
            # elif field == 'month':
            #     return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(sale_id__month__icontains=value).order_by('-id'), many=True).data)
            # elif field == 'account_of':
            #     return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(sale_id__account_of__icontains=value).order_by('-id'), many=True).data)
            # # elif field == 'date':
            # #     return Response(BillSerializer(Bill.objects.filter(date__icontains=value).order_by('-id'), many=True).data)
            # elif field == 'address':
            #     return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(sale_id__address__icontains=value).order_by('-id'), many=True).data)
    except Exception as e:
        return Response({"message": f"No data found {e}"})


@api_view(['GET', 'POST'])
def sales_pay_bill(request):  # sourcery skip: avoid-builtin-shadow
    if request.method == "POST":
        id = request.POST.get('id')
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
def sales_comp_bill(request):
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
def sales_cancel_bill(request):

    if request.method == "POST":
        id = request.POST.get('id')
        date = request.POST.get('cancel_date')
        reason = request.POST.get('reason')
        remaining_amount = request.POST.get('remaining_amount')
        amount = request.POST.get('amount')
        Bill.objects.create(date=date, reason=reason, amount=amount,
                            status='Cancelled', sale_id=Sales.objects.get(id=id))
        remaining_amount = 0
        amount = 0
        Sales.objects.filter(id=id).update(
            amount=amount, net_amount=remaining_amount)
        messages.success(request, "Bill Cancelled Successfully")
        return redirect('sales:view_sales')


@api_view(['POST'])
@login_required
# @permission_required('Sales.sales', raise_exception=True)
def sales_upload(request):
    if request.method == "POST":
        jsons = request.data
        print(jsons['myrows'][0])
        for obj in jsons['myrows']:
            if (Customers.objects.filter(customer_name=obj['Name'], customer_address=obj['Address'],customer_rank=obj['Rank']).exists()):
                print('already customer ')
                customer = Customers.objects.get(
                    customer_name=obj['Name'], customer_address=obj['Address'],customer_rank=obj['Rank'])
                Sales.objects.create(
                    bill_no=obj['Bill No'],
                    PoS_no=obj['POS NO'],
                    created_date=datetime.datetime.strptime(
                        obj['Dated'], "%d-%m-%Y").date(),
                    month=''.join(re.findall("[a-zA-Z]+", obj['Month'])),
                    account_of=obj['On Account Of'],
                    amount=obj['Amount'],
                    net_amount=obj['Net Amount'],
                    discount=obj['Discount'],
                    customer_id=customer
                ).save()
                # messages.success(request, "Sale Data Uploaded Successfully")
                # print('sale date: ', Sales.objects.values().last())
            else:
                print('create new customer')
                customer = Customers.objects.create(
                    customer_name=obj['Name'],
                    customer_address=obj['Address'],
                    customer_rank=obj['Rank']
                )
                customer.save()
                # messages.success(request, "Sale Data Uploaded Successfully")
                Sales.objects.create(
                    bill_no=obj['Bill No'],
                    PoS_no=obj['POS NO'],
                    created_date=datetime.datetime.strptime(
                        obj['Dated'], "%d-%m-%Y").date(),
                    month=''.join(re.findall("[a-zA-Z]+", obj['Month'])),
                    account_of=obj['On Account Of'],
                    amount=obj['Amount'],
                    net_amount=obj['Net Amount'],
                    discount=obj['Discount'],
                    customer_id=customer
                ).save()
        dummyTable.objects.all().delete()
        messages.success(request, "Sale Data Uploaded Successfully")
        return Response({"message": "Sales Data Uploaded Successfully"})
    else:
        return Response({"message": "Sales Data Not Uploaded"})
    
@api_view(['GET'])
def SearchByRank(request):
    rank=request.GET.get('rank')
    if rank in ['Staff','Army','Members','Other']:
        return Response(SalesSerializer(Sales.objects.select_related('customer_id').filter(customer_id__customer_rank=rank).order_by('-id'), many=True).data)
    else:
        return Response(SalesSerializer(Sales.objects.select_related('customer_id').order_by('-id'), many=True).data)

@api_view(['GET'])
def SearchByRankReport(request):
    rank=request.GET.get('rank')
    if rank in ['Staff','Army','Members','other']:
        return Response(BillSerializer(Bill.objects.select_related('sale_id').filter(sale_id__customer_id__customer_rank__icontains=rank).order_by('-id'), many=True).data)
    else:
        return Response(BillSerializer(Bill.objects.select_related('sale_id').order_by('-id'), many=True).data)

@api_view(['GET'])
def GetTotal(request):
    rank=request.GET.get('rank')
    print("dsafdddddd##########################",rank)
    return Response(
        {
        'total_bills': Sales.objects.select_related('customer_id').filter(net_amount__gt=0).filter(customer_id__customer_rank=rank).count(),
        'total_amount': Sales.objects.select_related('customer_id').filter(net_amount__gt=0).filter(customer_id__customer_rank=rank).aggregate(Sum('amount'))['amount__sum'],
        'total_discount': Sales.objects.select_related('customer_id').filter(net_amount__gt=0).filter(customer_id__customer_rank=rank).aggregate(Sum('discount'))['discount__sum'],
        'total_net_amount': Sales.objects.select_related('customer_id').filter(net_amount__gt=0).filter(customer_id__customer_rank=rank).aggregate(Sum('net_amount'))['net_amount__sum'],
            }
    )

sales_templates = [
    path('sales/', sales, name='sales'),
    path('view_sales/', view_sales, name='view_sales'),
    path('reports/', reports, name='reports'),
    path('update_sales/', update_sales, name='update_sales'),
    path('update_view_sale/', update_view_sale, name='update_view_sale'),
    path('delete_items/<int:pk>/', delete_items, name="delete_items"),
    path('delete_sale/<int:pk>/', delete_sale, name="delete_sale"),
    # api urls
    path('api/SearchbyName/', SearchbyName, name='SearchbyName'),
    path('api/sales/SearchByRank/', SearchByRank, name='SearchByRank'),
    path('api/SearchbyNameReport/', SearchbyNameReport, name='SearchbyNameReport'),
    path('api/sales/pay_bill/', sales_pay_bill, name='sales_pay_bill'),
    path('api/sales/comp_bill/', sales_comp_bill, name='sales_comp_bill'),
    path('api/sales/cancel_bill/', sales_cancel_bill, name='sales_cancel_bill'),
    path('api/sales/sales_upload/', sales_upload, name='sales_upload'),
    path('api/sales/SearchByRankReport/', SearchByRankReport, name='SearchByRankReport'),
    path('api/sales/GetTotal/', GetTotal, name='GetTotal'),

]
