from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from .models import Sub, Subscriber, Search
from .forms import SearchModelForm, SubModelForm, SubscriberForm, SubscriberModelForm,SearchForm, SubForm, PopForm
import csv
import pandas as pd
import numpy as np
import os
import glob
from IPython.display import HTML
from django.views import View
from django.views.generic.edit import FormView
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template
import xlsxwriter
from openpyxl import load_workbook
from functools import reduce
import re
import time
import datetime
# Create your views here.

def home(request):
    template_name = 'core/home.html'
    return render(request, template_name)



def tables(request):
    extension = 'xlsx'
    documents = Sub.objects.all()
    form = SearchModelForm(request.POST or None,  request.FILES or None)
    #form = SubModelForm(request.POST or None, request.FILES or None)
    all_filenames = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
    csv_list = [pd.read_excel(f) for f in all_filenames]

    #LOCATE BASE FILE
    fileLocation = r"media/zz/base.xlsx"
    year = 2017
    month = 11
    day = 5
    hour = 19
    minute = 50
    second = 0
    #SET THE MODIFIED BASE FILE TO THE TIME ABOVE
    date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    modTime = time.mktime(date.timetuple())
    try:
        os.utime(fileLocation, (modTime, modTime))
    except FileNotFoundError:
        return render(request, 'core/non-tables.html')

    if csv_list:
        if form.is_valid():
                x_word = form.cleaned_data['s_word'] #GET DATA FROM FORM
                obj = form.save(commit=False)
                obj.save()
                extension = 'xlsx'                      #SAVE DATA
                files = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
                files.sort(key=os.path.getmtime) #GET FILES BASED ON TIME CREATED


                csv_list = [pd.read_excel(f) for f in files]

                base = pd.read_excel('media/zz/base.xlsx')

                #GET ALL DF IN CSV LIST, MERGE ON ID USING LEFT DF AS INDEX
                tab = reduce(lambda left, right: pd.merge(left,right[['AMOUNT','ID']], on=["ID"], how='left'), csv_list)
                tab['TOTAL'] = tab.drop(['PAYABLE AMOUNT','NUMBER OF PLOT','PHONE NUMBER'], axis=1).sum(axis=1)
                tab['BALANCE'] = tab['PAYABLE AMOUNT'] - tab['TOTAL']

                #STATUS UPDATE
                tab.loc[tab["TOTAL"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'COMPLETED'
                tab.loc[tab["TOTAL"] > tab["PAYABLE AMOUNT"], 'STATUS'] = 'COMPLETED'
                tab.loc[tab["TOTAL"] < tab ["PAYABLE AMOUNT"], 'STATUS'] = 'OUTSTANDING'

                tab = tab.drop(columns=['id']).fillna('0')

                #GET FILES IN A LIST
                res = [sub[9 :-5] for sub in files]
                months = res[::-1]#READ IT BACKWARDS

                #SET THE TABLES COLUMN
                tab.columns =["ID","SUBSCRIBER'S NAME","PHONE NUMBER", "NUMBER OF PLOT", "PAYABLE AMOUNT", "PAYMENT STARTING DATE",
                    "SUPPOSED END DATE", "STATUS"]+ months + ["TOTAL AMOUNT","BALANCE"]
                pd.options.display.float_format = '{:.2f}'.format #SET DIGITS TO TWO DECIMAL PLACES
                s = tab.loc[tab["ID"] == str(x_word)] #SEARCH BY ID
                ss = (len(s.index)) #NUMBER OF SUBSCRIBER IN SEARCH BY ID

                f = tab[tab["SUBSCRIBER'S NAME"].str.contains(str(x_word))]  #match or contains
                x = (len(f.index)) #NUMBER OF SUBSCRIBER IN SEARCH BY NAME
                pd.options.display.float_format = '{:.2f}'.format

                #CONVERTING PANDAS TABLE TO HTML
                s = s.to_html(classes='table table-striped table-hover')
                f = f.to_html(classes='table table-striped table-hover')
                ht = tab.to_html(classes='table table-striped table-hover')

                return render(request, 'core/search-tables.html', {'html_table': ht,'f':f, 'x': x, 's': s,'ss':ss})

        else:

            extension = 'xlsx'
            files = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
            files.sort(key=os.path.getmtime)



            extension = 'xlsx'


            csv_list = [pd.read_excel(f) for f in files]

            base = pd.read_excel('media/zz/base.xlsx')


            tab = reduce(lambda left, right: pd.merge(left,right[['AMOUNT','ID']], on=["ID"], how='left'), csv_list)#.fillna('0.0')


            tab['TOTAL'] = tab.drop(['PAYABLE AMOUNT','NUMBER OF PLOT','PHONE NUMBER'], axis=1).sum(axis=1)

            tab['BALANCE'] = tab['PAYABLE AMOUNT'] - tab['TOTAL']

            tab.loc[tab["TOTAL"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'COMPLETED'
            tab.loc[tab["TOTAL"] > tab["PAYABLE AMOUNT"], 'STATUS'] = 'COMPLETED'
            tab.loc[tab["TOTAL"] < tab ["PAYABLE AMOUNT"], 'STATUS'] = 'OUTSTANDING'

            tab = tab.drop(columns=['id']).fillna('0')
            res = [sub[9 :-5] for sub in files]
            months = res[::-1]
            tab.columns =["ID","SUBSCRIBER'S NAME","PHONE NUMBER", "NUMBER OF PLOT", "PAYABLE AMOUNT", "PAYMENT STARTING DATE",
                "SUPPOSED END DATE", "STATUS"]+ months + ["TOTAL AMOUNT","BALANCE"]
            length = (len(tab.index))
            pd.options.display.float_format = '{:.2f}'.format


            ht =tab.to_html(classes='table table-striped table-hover')
            return render(request, 'core/tables.html', {'html_table': ht,'documents': documents,"length":length})#, 'x': x})
    else:
        return render(request, 'core/non-tables.html')


def registration(request):
    form = SubscriberModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        #GET DATA FROM FORM
        sub_id = form.cleaned_data['id_no']
        sub_name= form.cleaned_data['sub_name']
        phone_no = form.cleaned_data['phone_no']
        no_of_plot = form.cleaned_data['no_of_plot']
        payable_amount = form.cleaned_data['payable_amount']
        payment_starting_date = form.cleaned_data['payment_starting_date']
        supposed_end_date = form.cleaned_data['supposed_end_date']
        amount_paid = form.cleaned_data['amount_paid']

        #PRESENT DATA AS STRING IN A LIST
        new_row_data = [ str(sub_id), str(sub_name), str(phone_no), str(no_of_plot),
                str(payable_amount), str(payment_starting_date), str(supposed_end_date),'','',str(amount_paid)]

        #GET FILE AND LOAD IT
        wb = load_workbook("media/zz/base.xlsx")
        # Select First Worksheet
        ws = wb.worksheets[0]

        # Append Row Values
        ws.append(new_row_data)

        wb.save("media/zz/base.xlsx")
        return redirect('/tables/')
        form = SubscriberModelForm()
    template_name = 'core/registration.html'
    context = {'form': form}
    return render(request, template_name, context)


def upload(request, *args, **kwargs):
    form = SubModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        doc = form.cleaned_data['doc']
        try:
            base = pd.read_excel('media/zz/base.xlsx')
            other = pd.read_excel(doc)


            differences = other[~other['ID'].isin(base['ID'])]
            differences2 = other[~other["SUBSCRIBER’S NAME"].isin(base["SUBSCRIBER'S NAME"])]


            s = differences.to_html(classes='table table-striped table-hover')
            s2 = differences2.to_html(classes='table table-striped table-hover')

            context = {'form': form, 's':s,'s2':s2}
            template_name = 'core/upload.html'
            return render(request, template_name, context)
        except FileNotFoundError:
            obj = form.save(commit=False)
            obj.save()
            return redirect('/tables')
        #else:
        #    obj = form.save(commit=False)
        #    obj.save()
        #    return redirect('/tables')
    else:
        messages.success(request,"File nOT successfully uploaded")
    context = {'form': form}
    template_name = 'core/upload.html'
    return render(request, template_name, context)



class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        extension = 'xlsx'
        documents = Sub.objects.all()
        form = SearchModelForm(request.POST or None,  request.FILES or None)

        files = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
        files.sort(key=os.path.getmtime)


        search = Search.objects.last()#GET THE LAST FIELDS IN THE DB
        extension = 'xlsx'

        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
        csv_list = [pd.read_excel(f) for f in files]

        base = pd.read_excel('media/zz/base.xlsx')


        tab = reduce(lambda left, right: pd.merge(left,right[['AMOUNT','ID']], on=["ID"], how='left'), csv_list)
        tab['TOTAL'] = tab.drop(['PAYABLE AMOUNT','NUMBER OF PLOT','PHONE NUMBER'], axis=1).sum(axis=1)
        tab['BALANCE'] = tab['PAYABLE AMOUNT'] - tab['TOTAL']

        tab.loc[tab["TOTAL"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'COMPLETED'
        tab.loc[tab["TOTAL"] > tab["PAYABLE AMOUNT"], 'STATUS'] = 'COMPLETED'
        tab.loc[tab["TOTAL"] < tab ["PAYABLE AMOUNT"], 'STATUS'] = 'OUTSTANDING'
        #tab=tab.T.drop_duplicates().T
        tab = tab.drop(columns=['id']).fillna('0')
        res = [sub[9 :-5] for sub in files]
        months = res[::-1]
        tab.columns =["ID","SUBSCRIBER'S NAME","PHONE NUMBER", "NUMBER OF PLOT", "PAYABLE AMOUNT", "PAYMENT STARTING DATE",
            "SUPPOSED END DATE", "STATUS"]+ months + ["TOTAL AMOUNT","BALANCE"]
        length = (len(tab.index))
        pd.options.display.float_format = '{:.2f}'.format
        #m = m.drop(m.index[0])
        f = tab.loc[tab["ID"] == str(search.s_word)]


        #SET ALL DATA FROM SEARCH TO STRING NEGLECTING THEIR INDICES
        sub_name = f["SUBSCRIBER'S NAME"].to_string(index=False)
        phone_no = f["PHONE NUMBER"].to_string(index=False)
        payment_status = f["STATUS"].to_string(index=False)
        no_of_plot = f["NUMBER OF PLOT"].to_string(index=False)
        payable_amount = f["PAYABLE AMOUNT"].to_string(index=False)
        initial_payment = f["base"].to_string(index=False)
        total_amount = f["TOTAL AMOUNT"].to_string(index=False)
        balance = f["BALANCE"].to_string(index=False)
        f = f.loc[:, f.columns != 'PHONE NUMBER']
        f = f.loc[:, f.columns != "SUBSCRIBER'S NAME"]
        f = f.loc[:, f.columns != 'PAYABLE AMOUNT']
        f = f.loc[:, f.columns != 'PAYMENT STARTING DATE']
        f = f.loc[:, f.columns != 'SUPPOSED END DATE']
        f = f.loc[:, f.columns != 'NUMBER OF PLOT']
        f = f.loc[:, f.columns != 'BALANCE']
        f = f.loc[:, f.columns != 'STATUS']
        f = f.loc[:, f.columns != 'TOTAL AMOUNT']
        f = f.loc[:, f.columns != 'ID']
        #f.stack()

        f = f.fillna('0')
        f = f.T
        pd.options.display.float_format = '{:.2f}'.format



        f =f.to_html()


        template = get_template('core/pdf.html')
        context = {
        "sub_id": search.s_word,
        'sub_name': sub_name,
        'phone_no': phone_no,
        'payment_status': payment_status,
        'no_of_plot': no_of_plot,
        'payable_amount': payable_amount,
        'initial_payment': initial_payment,
        'total_amount': total_amount,
        'balance': balance,
        'f': f
            }
        html = template.render(context)
        pdf = render_to_pdf('core/pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s details.pdf" %(sub_name)
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")





def download(request):
    extension = 'xlsx'
    documents = Sub.objects.all()
    form = SearchModelForm(request.POST or None,  request.FILES or None)
    fileLocation = r"media/zz/base.xlsx"
    year = 2017
    month = 11
    day = 5
    hour = 19
    minute = 50
    second = 0

    date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    modTime = time.mktime(date.timetuple())

    os.utime(fileLocation, (modTime, modTime))
    #form = SubModelForm(request.POST or None, request.FILES or None)
    all_filenames = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
    csv_list = [pd.read_excel(f) for f in all_filenames]
    csv_names = [pd.DataFrame(f).set_index("ID") for f in csv_list]
    files = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
    files.sort(key=os.path.getmtime)
    print(files)


    extension = 'xlsx'

    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    csv_list = [pd.read_excel(f) for f in files]

    base = pd.read_excel('media/zz/base.xlsx')


    tab = reduce(lambda left, right: pd.merge(left,right[['AMOUNT','ID']], on=["ID"], how='left'), csv_list)#.fillna('0.0')
    tab['TOTAL'] = tab.drop(['PAYABLE AMOUNT','NUMBER OF PLOT','PHONE NUMBER'], axis=1).sum(axis=1)
    tab['BALANCE'] = tab['PAYABLE AMOUNT'] - tab['TOTAL']

    tab.loc[tab["TOTAL"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'COMPLETED'
    tab.loc[tab["TOTAL"] > tab["PAYABLE AMOUNT"], 'STATUS'] = 'COMPLETED'
    tab.loc[tab["TOTAL"] < tab ["PAYABLE AMOUNT"], 'STATUS'] = 'OUTSTANDING'
    #tab=tab.T.drop_duplicates().T
    tab = tab.drop(columns=['id']).fillna('0')
    res = [sub[9 :-5] for sub in files]
    months = res[::-1]
    tab.columns =["ID","SUBSCRIBER'S NAME","PHONE NUMBER", "NUMBER OF PLOT", "PAYABLE AMOUNT", "PAYMENT STARTING DATE",
        "SUPPOSED END DATE", "STATUS"] + months + ["TOTAL AMOUNT","BALANCE"]
    length = (len(tab.index))
    pd.options.display.float_format = '{:.2f}'.format


    k = tab.to_csv()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="coop.xlsx"'
    writer = csv.writer(response)
    writer.writerow([k])
    return response





def file_delete(request):
    form = PopForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        filename = form.cleaned_data['name']
        dig = "media/zz/{}".format(filename)
        try:
            os.remove(dig)
            return redirect("/tables")
        except FileNotFoundError:
            template_name = 'core/file-delete-except.html'
            context = {'form': form}
            return render(request, template_name, context)
    else:
        template_name = 'core/file-delete.html'
        context = {'form': form}
        return render(request, template_name, context)
