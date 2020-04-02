def upload(request, *args, **kwargs):
    form = SubModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect('/tables')
    else:
        messages.success(request,"File nOT successfully uploaded")
    context = {'form': form}
    template_name = 'core/upload.html'
    return render(request, template_name, context)





csv_names = [pd.DataFrame(f).set_index("ID") for f in csv_list] #NEW FILES UPLOADED ON MONTHLY BASIS, INDEX THEM BY ID .set_index("ID")
ds = pd.concat(csv_list, axis=1)# use to be to csv_names   )#CONCATENATE ABOVE FILES
df = pd.concat(csv_list) #CONCATENATE EVERY FILE IN ZZ FOLDER

base = pd.read_excel('media/zz/base.xlsx')


new = df.groupby(["ID", "SUBSCRIBER'S NAME"],as_index = False).sum()
new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']

see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT', 'AMOUNT',
             'STATUS','NUMBER OF PLOT'])

tab = pd.merge(see,new, on=['ID'], how='inner')
tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'COMPLETED'
tab.loc[tab["AMOUNT"] > tab["PAYABLE AMOUNT"], 'STATUS'] = 'COMPLETED'
tab.loc[tab["AMOUNT"] < tab ["PAYABLE AMOUNT"], 'STATUS'] = 'OUTSTANDING'
ife = tab.drop(columns=['id'])
ife = ife.rename(columns ={'AMOUNT': 'TOTAL AMOUNT'}, inplace=False)
#ife = ife.drop(ife.index[0])
#m = ife.merge(ds["AMOUNT"], how='inner', on="ID")#ID #use to be merge on ID)
col_filt = ds['AMOUNT']
col_filt = col_filt.fillna('0')

m = pd.concat([ife,col_filt], axis=1)
m = m.fillna('0.0')

x = (len(m.index)-1) #NUMBER OF SUBSCRIBER REGISTERED
res = [sub[9 :-5] for sub in all_filenames]
m.columns =["ID",'PAYMENT STARTING DATE','SUPPOSED END DATE',"SUBSCRIBER'S NAME", 'TOTAL AMOUNT',
             'NUMBER OF PLOT','PAYABLE AMOUNT','PHONE NUMBER','STATUS','BALANCE'] + res

#m = m.drop(m.index[0])
m = m.dropna(thresh=9)
















def tables(request):
    extension = 'xlsx'
    documents = Sub.objects.all()
    form = SearchModelForm(request.POST or None,  request.FILES or None)
    #form = SubModelForm(request.POST or None, request.FILES or None)
    all_filenames = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
    csv_list = [pd.read_excel(f) for f in all_filenames]

    csv_names = [pd.DataFrame(f).set_index("SUBSCRIBER'S NAME") for f in csv_list] #USE TO BE SUBSCRIBER'S NAME

    #if csv_names:
    #    df = pd.concat(csv_names)
    #else:
    #    print('aa')
    print(all_filenames)
    if csv_list:
        if form.is_valid():
                x_word = form.cleaned_data['s_word'] #GET DATA FROM FORM
                obj = form.save(commit=False)
                obj.save()                          #SAVE DATA
                csv_names = [pd.DataFrame(f).set_index("ID") for f in csv_list] #NEW FILES UPLOADED ON MONTHLY BASIS, INDEX THEM BY ID
                ds = pd.concat(csv_list, axis=1) #CONCATENATE ABOVE FILES ON Y-AXIS
                df = pd.concat(csv_list)

                base = pd.read_excel('media/zz/base.xlsx')

                new = df.groupby(["ID","SUBSCRIBER'S NAME"],as_index = False).sum() #MATCH DATA IN ALL FILES BASED ON ID AND NAME
                new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']
                see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT','AMOUNT',
                             'STATUS','NUMBER OF PLOT'])
                tab = pd.merge(see,new, on=['ID'], how='inner')

                #TABLE STATUS
                tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Completed'
                tab.loc[tab["AMOUNT"] > tab["PAYABLE AMOUNT"], 'STATUS'] = 'Completed'
                tab.loc[tab["AMOUNT"]  < tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Outstanding'
                ife = tab.drop(columns=['id'])
                ife = ife.rename(columns ={'AMOUNT': 'TOTAL AMOUNT'}, inplace=False)
                ife = ife.drop(ife.index[0])

                #m = pd.concat([ife,ds["AMOUNT"]], axis=1)


                m = ife.merge(ds['AMOUNT'], how='inner', on='ID') #MERGE BASE FILE AND AMOUNT COLUMN ON EACH FILE
                m = m.fillna('0')


                res = [sub[9 :-5] for sub in all_filenames]
                m.columns =["ID",'PAYMENT STARTING DATE','SUPPOSED END DATE',"SUBSCRIBER'S NAME", 'TOTAL AMOUNT',
                             'NUMBER OF PLOT','PAYABLE AMOUNT','PHONE NUMBER','STATUS','BALANCE'] + res
                s = m.loc[m["ID"] == str(x_word)]
                ss = (len(s.index)) #NUMBER OF SUBSCRIBER IN SEARCH BY ID

                f = m[m["SUBSCRIBER'S NAME"].str.contains(str(x_word))]  #match or contains
                x = (len(f.index)) #NUMBER OF SUBSCRIBER IN SEARCH BY NAME

                #CONVERTING PANDAS TABLE TO HTML
                s = s.to_html(classes='table table-striped table-hover')
                f = f.to_html(classes='table table-striped table-hover')
                ht = m.to_html(classes='table table-striped table-hover')

                return render(request, 'core/search-tables.html', {'html_table': ht,'f':f, 'x': x, 's': s,'ss':ss})

        else:

            csv_names = [pd.DataFrame(f).set_index("ID") for f in csv_list] #NEW FILES UPLOADED ON MONTHLY BASIS, INDEX THEM BY ID .set_index("ID")
            ds = pd.concat(csv_names, axis=1)# use to be to csv_names   )#CONCATENATE ABOVE FILES

            df = pd.concat(csv_list) #CONCATENATE EVERY FILE IN ZZ FOLDER

            base = pd.read_excel('media/zz/base.xlsx')


            new = df.groupby(["ID","SUBSCRIBER'S NAME"],as_index = False).sum()
            new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']

            see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT', 'AMOUNT',
                         'STATUS','NUMBER OF PLOT'])

            tab = pd.merge(see,new, on=['ID'], how='inner')
            tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Completed'
            tab.loc[tab["AMOUNT"] > tab["PAYABLE AMOUNT"], 'STATUS'] = 'Completed'
            tab.loc[tab["AMOUNT"] < tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Outstanding'
            ife = tab.drop(columns=['id'])
            ife = ife.rename(columns ={'AMOUNT': 'TOTAL AMOUNT'}, inplace=False)
            ife = ife.drop(ife.index[0])
            m = ife.merge(ds["AMOUNT"], how='inner', on="ID")#ID #use to be merge on ID)
            #m = pd.concat([ife,ds['AMOUNT']], axis=1)
            m = m.fillna('0')

            x = (len(m.index)-1) #NUMBER OF SUBSCRIBER REGISTERED
            res = [sub[9 :-5] for sub in all_filenames]
            m.columns =["ID",'PAYMENT STARTING DATE','SUPPOSED END DATE',"SUBSCRIBER'S NAME", 'TOTAL AMOUNT',
                         'NUMBER OF PLOT','PAYABLE AMOUNT','PHONE NUMBER','STATUS','BALANCE'] + res

            m = m.drop(m.index[0])
            m = m.dropna(thresh=9) #removes na values if more than nine in a arow



            ht =m.to_html(classes='table table-striped table-hover')
            return render(request, 'core/tables.html', {'html_table': ht,'documents': documents, 'x': x})
    else:
        return render(request, 'core/non-tables.html')






def tables(request):
    extension = 'xlsx'
    documents = Sub.objects.all()
    form = SearchModelForm(request.POST or None,  request.FILES or None)
    #form = SubModelForm(request.POST or None, request.FILES or None)
    all_filenames = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
    csv_list = [pd.read_excel(f) for f in all_filenames]
    #csv_names = [pd.DataFrame(f).set_index("SUBSCRIBER'S NAME") for f in csv_list]
    #if csv_names:
    #    df = pd.concat(csv_names)
    #else:
    #    print('aa')
    print(all_filenames)
    if csv_list:
        if form.is_valid():
                x_word = form.cleaned_data['s_word'] #GET DATA FROM FORM
                obj = form.save(commit=False)
                obj.save()                          #SAVE DATA
                csv_names = [pd.DataFrame(f).set_index("ID") for f in csv_list] #NEW FILES UPLOADED ON MONTHLY BASIS, INDEX THEM BY ID
                ds = pd.concat(csv_list, axis=1) #CONCATENATE ABOVE FILES ON Y-AXIS
                df = pd.concat(csv_list)

                base = pd.read_excel('media/zz/base.xlsx')

                new = df.groupby(["ID","SUBSCRIBER'S NAME"],as_index = False).sum() #MATCH DATA IN ALL FILES BASED ON ID AND NAME
                new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']
                see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT','AMOUNT',
                             'STATUS','NUMBER OF PLOT'])
                tab = pd.merge(see,new, on=['ID'], how='inner')

                #TABLE STATUS
                tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Completed'
                tab.loc[tab["AMOUNT"] > tab["PAYABLE AMOUNT"], 'STATUS'] = 'Completed'
                tab.loc[tab["AMOUNT"]  < tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Outstanding'
                ife = tab.drop(columns=['id'])
                ife = ife.rename(columns ={'AMOUNT': 'TOTAL AMOUNT'}, inplace=False)
                ife = ife.drop(ife.index[0])

                m = pd.concat([ife,ds["AMOUNT"]], axis=1)
                m = m.fillna('0')
                #m = ife.merge(ds['AMOUNT'], how='inner', on='ID') #MERGE BASE FILE AND AMOUNT COLUMN ON EACH FILE

                res = [sub[9 :-5] for sub in all_filenames]
                m.columns =["ID",'PAYMENT STARTING DATE','SUPPOSED END DATE',"SUBSCRIBER'S NAME", 'TOTAL AMOUNT',
                             'NUMBER OF PLOT','PAYABLE AMOUNT','PHONE NUMBER','STATUS','BALANCE'] + res
                s = m.loc[m["ID"] == str(x_word)]
                ss = (len(s.index)) #NUMBER OF SUBSCRIBER IN SEARCH BY ID

                f = m[m["SUBSCRIBER'S NAME"].str.contains(str(x_word))]  #match or contains
                x = (len(f.index)) #NUMBER OF SUBSCRIBER IN SEARCH BY NAME

                #CONVERTING PANDAS TABLE TO HTML
                s = s.to_html(classes='table table-striped table-hover')
                f = f.to_html(classes='table table-striped table-hover')
                ht = m.to_html(classes='table table-striped table-hover')

                return render(request, 'core/search-tables.html', {'html_table': ht,'f':f, 'x': x, 's': s,'ss':ss})

        else:

            csv_names = [pd.DataFrame(f).set_index("ID") for f in csv_list] #NEW FILES UPLOADED ON MONTHLY BASIS, INDEX THEM BY ID .set_index("ID")
            ds = pd.concat(csv_list, axis=1)# use to be to csv_names   )#CONCATENATE ABOVE FILES
            df = pd.concat(csv_list) #CONCATENATE EVERY FILE IN ZZ FOLDER
            print(ds)
            base = pd.read_excel('media/zz/base.xlsx')


            new = df.groupby(["ID","SUBSCRIBER'S NAME"],as_index = False).sum()
            new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']

            see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT', 'AMOUNT',
                         'STATUS','NUMBER OF PLOT'])

            tab = pd.merge(see,new, on=['ID'], how='inner')
            tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Completed'
            tab.loc[tab["AMOUNT"] > tab["PAYABLE AMOUNT"], 'STATUS'] = 'Completed'
            tab.loc[tab["AMOUNT"] < tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Outstanding'
            ife = tab.drop(columns=['id'])
            ife = ife.rename(columns ={'AMOUNT': 'TOTAL AMOUNT'}, inplace=False)
            ife = ife.drop(ife.index[0])
            #m = ife.merge(ds["AMOUNT"], how='inner', on="ID")#ID #use to be merge on ID)
            m = pd.concat([ife,ds['AMOUNT']], axis=1)
            m = m.fillna('0')

            x = (len(m.index)-1) #NUMBER OF SUBSCRIBER REGISTERED
            res = [sub[9 :-5] for sub in all_filenames]
            m.columns =["ID",'PAYMENT STARTING DATE','SUPPOSED END DATE',"SUBSCRIBER'S NAME", 'TOTAL AMOUNT',
                         'NUMBER OF PLOT','PAYABLE AMOUNT','PHONE NUMBER','STATUS','BALANCE'] + res

            m = m.drop(m.index[0])
            m = m.dropna(thresh=9) #removes na values if more than nine in a arow



            ht =m.to_html(classes='table table-striped table-hover')
            return render(request, 'core/tables.html', {'html_table': ht,'documents': documents, 'x': x})
    else:
        return render(request, 'core/non-tables.html')




PHONE NUMBER	NUMBER OF PLOT	PAYABLE AMOUNT	PAYMENT STARTING DATE	SUPPOSED END DATE	STATUS	id	AMOUNT



from openpyxl import load_workbook

new_row_data = [
    ['odhgos', 'e/p', 'dromologio', 'ora'],
    ['odigosou', 'dromou', 'dromologio', 'ora']]

wb = load_workbook("base.xlsx")
# Select First Worksheet
ws = wb.worksheets[0]

# Append 2 new Rows - Columns A - D
for row_data in new_row_data:
    # Append Row Values
    ws.append(row_data)

wb.save("base.xlsx")



def registration(request):
    model_class = Subscriber

    meta = model_class._meta
    field_names = [field.name for field in meta.fields]
    try:
        sub = Subscriber.objects.latest('id_no')

    except AssertionError:
        pass
    except:
        pass

    form = SubscriberModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        with open('media/zz/base.xlsx', 'a') as csvfile:
            writer = csv.writer(csvfile)
            subs = Subscriber.objects.latest('id_no')
            row = writer.writerow([getattr(subs,field) for field in field_names])
            obj = form.save(commit=False)
            obj.save()
            return redirect('/tables')
        form = SubscriberModelForm()
    template_name = 'core/registration.html'
    context = {'form': form}
    return render(request, template_name, context)







        <style type="text/css">
            body {
                font-weight: 200;
                font-size: 14px;
            }
            .header {
                font-size: 20px;
                font-weight: 100;
                text-align: center;
                color: #007cae;
            }
            .title {
                font-size: 22px;
                font-weight: 100;
               /* text-align: right;*/
               padding: 10px 20px 0px 20px;
            }
            .title span {
                color: #007cae;
            }
            .details-left {
                padding: 10px 20px 0px 20px;
                text-align: left !important;
                float-left: 50%,
                /*margin-left: 40%;*/
            }

            .details-right {
                padding: 10px 20px 0px 20px;

                float: right;
                width: 30%;
                /*margin-left: 40%;*/
            }
            .hrItem {
                border: none;
                height: 1px;
                /* Set the hr color */
                color: #333; /* old IE */
                background-color: #fff; /* Modern Browsers */
            }
            h2{
                text-align: center;
            }
        </style>





template = get_template('core/invoice.html')
context = {
    "invoice_id": 123,
    "customer_name": "John Cooper",
    "amount": 1399.99,
    "today": "Today",
}
html = template.render(context)
pdf = render_to_pdf('core/invoice.html', context)
if pdf:
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Invoice_%s.pdf" %("12341231")
    content = "inline; filename='%s'" %(filename)
    download = request.GET.get("download")
    if download:
        content = "attachment; filename='%s'" %(filename)
    response['Content-Disposition'] = content
    return response
return HttpResponse("Not found")




def download(request):

    extension = 'xlsx'
    all_filenames = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
    csv_list = [pd.read_csv(f) for f in all_filenames]
    df = pd.concat(csv_list)
    base = pd.read_csv('media/zz/base.xlsx')
    new = df.groupby("ID",as_index = False).sum()
    new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']
    see = base.drop(columns=['id','PHONE NUMBER','PAYABLE AMOUNT', 'AMOUNT',
                         'STATUS','NUMBER OF PLOT'])
    tab = pd.merge(see,new, on=['ID'], how='inner')
    form = SearchModelForm(request.POST or None,  request.FILES or None)
    if form.is_valid():
        print('valid')
        x_word = form.cleaned_data['s_word']
        f = tab.loc[tab['ID'] == x_word]
        htf = f.to_html(classes='table table-striped table-hover')
        k = f.to_csv()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="coop-search.xlsx"'
        writer = csv.writer(response)
        writer.writerow([k])
        return response
    else:
        tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Balanced'
        tab.loc[tab["AMOUNT"] !=tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Not Balanced'
        ife = tab.drop(columns=['id'])
        k = ife.to_csv()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="coopsys.xlsx"'
        writer = csv.writer(response)
        writer.writerow([k])
        return response




class Table(FormView):
    def get(self,request):
        extension = 'xlsx'
        documents = Sub.objects.all()
        form = SearchModelForm(request.POST or None,  request.FILES or None)
        #form = SubModelForm(request.POST or None, request.FILES or None)
        all_filenames = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
        csv_list = [pd.read_csv(f) for f in all_filenames]
        csv_names = [pd.DataFrame(f).set_index("SUBSCRIBER'S NAME") for f in csv_list]
        if csv_names:
            df = pd.concat(csv_names)
        else:
            print('aa')
        print(all_filenames)
        if csv_list:
            if form.is_valid():
                #if form2.is_valid():
                    csv_names = [pd.DataFrame(f).set_index("SUBSCRIBER'S NAME") for f in csv_list]
                    ds = pd.concat(csv_names, axis=1)
                    #name = form.cleaned_data['name']
                    #print(name.strip('.xlsx'))
                    #dude = name.strip('.xlsx')
                    #x_word = form.cleaned_data['s_word']
                    df = pd.concat(csv_list)
                    dp = pd.concat(csv_list, axis=1)
                    #try:
                    base = pd.read_csv('media/zz/base.xlsx')

                    new = df.groupby(["ID","SUBSCRIBER'S NAME"],as_index = False).sum()
                    new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']
                    see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT',
                                 'STATUS','NUMBER OF PLOT'])
                    tab = pd.merge(see,new, on=['ID'], how='inner')
                    tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Balanced'
                    tab.loc[tab["AMOUNT"] !=tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Not Balanced'
                    ife = tab.drop(columns=['id'])
                    ht = ife.to_html(classes='table table-striped table-hover')
                    f = tab.loc[tab['ID'] == x_word]
                    m = pd.concat([ife,ds['AMOUNT']], axis=1)
                    m.rename(columns = {'AMOUNT': settings.COLUMN_NAME}, inplace = True)
                    print(m)
                    htf = m.to_html(classes='table table-striped table-hover')
                    k = f.to_csv()

                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="coop-search.xlsx"'
                    writer = csv.writer(response)
                    writer.writerow([k])
                    template_name = 'core/tables.html'
                    context = {'htf': htf, 'html_table':ht}
                    return render(request,template_name, context)
                #return response
            else:
                #name = form2.cleaned_data['name']
                #print(name.strip('.xlsx'))
                csv_names = [pd.DataFrame(f).set_index("ID") for f in csv_list]
                #csv_list = [pd.DataFrame(f).set_index("SUBSCRIBER'S NAME") for f in csv_list]
                ds = pd.concat(csv_names, axis=1)
                print('else2')
                df = pd.concat(csv_list)
                dp = pd.concat(csv_list, axis=1)
                #try:
                base = pd.read_csv('media/zz/base.xlsx')

                new = df.groupby(["ID","SUBSCRIBER'S NAME"],as_index = False).sum()
                new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']

                see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT', 'AMOUNT',
                             'STATUS','NUMBER OF PLOT'])
                tab = pd.merge(see,new, on=['ID'], how='inner')
                tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Balanced'
                tab.loc[tab["AMOUNT"] !=tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Not Balanced'
                ife = tab.drop(columns=['id'])
                ife = ife.rename(columns ={'AMOUNT': 'TOTAL AMOUNT'}, inplace=False)
                ife = ife.drop(ife.index[0])
                m = pd.concat([ife, ds['AMOUNT']], axis=1)
                y = 9
                res = [sub[y :-5] for sub in all_filenames]
                m.columns =["ID",'PAYMENT STARTING DATE','SUPPOSED END DATE',"SUBSCRIBER'S NAME", 'TOTAL AMOUNT',
                             'NUMBER OF PLOT','PAYABLE AMOUNT','PHONE NUMBER','STATUS','BALANCE'] + res
                x = (len(ife.index))
                m = m.drop(m.index[0])
                ht =m.to_html(classes='table table-striped table-hover')
                return render(request, 'core/tables.html', {'html_table': ht,'documents': documents, 'x': x})
        else:
            return render(request, 'core/non-tables.html')







def tables(request):
    extension = 'xlsx'
    documents = Sub.objects.all()
    #for each in Sub.objects.all():
    # d_name=each.name
    form = SearchModelForm(request.POST or None,  request.FILES or None)
    #form = SubModelForm(request.POST or None, request.FILES or None)
    all_filenames = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
    csv_list = [pd.read_csv(f) for f in all_filenames]
    csv_names = [pd.DataFrame(f).set_index("SUBSCRIBER'S NAME") for f in csv_list]
    df = pd.concat(csv_names)
    if csv_list:
        if form.is_valid():
            #if form2.is_valid():
                csv_names = [pd.DataFrame(f).set_index("SUBSCRIBER'S NAME") for f in csv_list]
                ds = pd.concat(csv_names, axis=1)
                #name = form.cleaned_data['name']
                #print(name.strip('.xlsx'))
                #dude = name.strip('.xlsx')
                #x_word = form.cleaned_data['s_word']
                df = pd.concat(csv_list)
                dp = pd.concat(csv_list, axis=1)
                #try:
                base = pd.read_csv('media/zz/base.xlsx')

                new = df.groupby(["ID","SUBSCRIBER'S NAME"],as_index = False).sum()
                new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']
                see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT',
                             'STATUS','NUMBER OF PLOT'])
                tab = pd.merge(see,new, on=['ID'], how='inner')
                tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Balanced'
                tab.loc[tab["AMOUNT"] !=tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Not Balanced'
                ife = tab.drop(columns=['id'])
                ht = ife.to_html(classes='table table-striped table-hover')
                f = tab.loc[tab['ID'] == x_word]
                m = pd.concat([ife,ds['AMOUNT']], axis=1)
                file_name = file_name_parser()
                m.rename(columns = {'AMOUNT': file_name}, inplace = True)
                print(m)
                htf = m.to_html(classes='table table-striped table-hover')
                k = f.to_csv()

                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="coop-search.xlsx"'
                writer = csv.writer(response)
                writer.writerow([k])
                template_name = 'core/tables.html'
                context = {'htf': htf, 'html_table':ht}
                return render(request,template_name, context)
            #return response
        else:
            #name = form2.cleaned_data['name']
            #print(name.strip('.xlsx'))
            csv_names = [pd.DataFrame(f).set_index("ID") for f in csv_list]
            #csv_list = [pd.DataFrame(f).set_index("SUBSCRIBER'S NAME") for f in csv_list]
            ds = pd.concat(csv_names, axis=1)
            print('else2')
            df = pd.concat(csv_list)
            dp = pd.concat(csv_list, axis=1)
            #try:
            base = pd.read_csv('media/zz/base.xlsx')

            new = df.groupby(["ID","SUBSCRIBER'S NAME"],as_index = False).sum()
            new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']

            see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT', 'AMOUNT',
                         'STATUS','NUMBER OF PLOT'])
            tab = pd.merge(see,new, on=['ID'], how='inner')
            tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Balanced'
            tab.loc[tab["AMOUNT"] !=tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Not Balanced'
            ife = tab.drop(columns=['id'])
            ife = ife.rename(columns ={'AMOUNT': 'TOTAL AMOUNT'}, inplace=False)
            #ds = ds.rename(columns = {'AMOUNT':documents}, inplace=True)
            m = pd.concat([ife, ds['AMOUNT']], axis=1)
            ds = ds.rename(columns = {'AMOUNT':documents}, inplace=True)
            file_name = file_name_parser()
            m.rename(columns = {'AMOUNT': documents}, inplace = True)
            x = (len(m.index))-1
            # m.rename(columns = {'AMOUNT':documents}, inplace = True)
            ht = m.to_html(classes='table table-striped table-hover')
            return render(request, 'core/tables.html', {'html_table': ht,'documents': documents, 'x': x})
    else:
        return render(request, 'core/non-tables.html')









def tables(request):
    extension = 'xlsx'
    #form = SearchModelForm(request.POST or None,  request.FILES or None)
    form = SubModelForm(request.POST or None, request.FILES or None)
    all_filenames = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
    csv_list = [pd.read_csv(f) for f in all_filenames]
    if csv_list:
        if form.is_valid():
            #if form2.is_valid():
                name = form2.cleaned_data['name']
                print(name.strip('.xlsx'))
                dude = name.strip('.xlsx')
                x_word = form.cleaned_data['s_word']
                df = pd.concat(csv_list)
                dp = pd.concat(csv_list, axis=1)
                #try:
                base = pd.read_csv('media/zz/base.xlsx')

                new = df.groupby(["ID","SUBSCRIBER'S NAME"],as_index = False).sum()
                new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']
                dude = new['AMOUNT PAID']
                see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT',
                             'STATUS','NUMBER OF PLOT'])
                tab = pd.merge(see,new, on=['ID'], how='inner')
                tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Balanced'
                tab.loc[tab["AMOUNT"] !=tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Not Balanced'
                ife = tab.drop(columns=['id'])
                ht = ife.to_html(classes='table table-striped table-hover')
                f = tab.loc[tab['ID'] == x_word]
                m = pd.concat([ife,dp['AMOUNT']], axis=1)
                m.rename(columns = {'AMOUNT':'amount'}, inplace = True)
                print(m)
                htf = m.to_html(classes='table table-striped table-hover')
                k = f.to_csv()

                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="coop-search.xlsx"'
                writer = csv.writer(response)
                writer.writerow([k])
                template_name = 'core/tables.html'
                context = {'htf': htf, 'html_table':ht}
                return render(request,template_name, context)
            #return response
        else:
            #name = form2.cleaned_data['name']
            #print(name.strip('.xlsx'))
            print('else2')
            df = pd.concat(csv_list)
            dp = pd.concat(csv_list, axis=1)
            #try:
            base = pd.read_csv('media/zz/base.xlsx')

            new = df.groupby(["ID","SUBSCRIBER'S NAME"],as_index = False).sum()
            new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT']

            see = base.drop(columns=["SUBSCRIBER'S NAME",'id','PHONE NUMBER','PAYABLE AMOUNT', 'AMOUNT',
                         'STATUS','NUMBER OF PLOT'])
            tab = pd.merge(see,new, on=['ID'], how='inner')
            tab.loc[tab["AMOUNT"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Balanced'
            tab.loc[tab["AMOUNT"] !=tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Not Balanced'
            ife = tab.drop(columns=['id'])
            m = pd.concat([ife, dp['AMOUNT']], axis=1)
            m.rename(columns = {'AMOUNT':'dud'}, inplace = True)
            ht = m.to_html(classes='table table-striped table-hover')
            return render(request, 'core/tables.html', {'html_table': ht})










def download(request):

    extension = 'xlsx'
    all_filenames = [i for i in glob.glob('media/zz/*.{}'.format(extension))]
    #all_filenames = Sub.objects.all()
    csv_list = [pd.read_csv(f) for f in all_filenames]
    df = pd.concat(csv_list)
    base = pd.read_csv('media/zz/base.xlsx')
    new = df.groupby("ID",as_index = False).sum()
    new['BALANCE'] = new['PAYABLE AMOUNT']-new['AMOUNT PAID']
    see = base.drop(columns=['id','PHONE NUMBER','PAYABLE AMOUNT', 'AMOUNT PAID',
                         'STATUS','NUMBER OF PLOT'])
    tab = pd.merge(see,new, on=['ID'], how='inner')
    tab.loc[tab["AMOUNT PAID"] == tab["PAYABLE AMOUNT"], 'STATUS'] = 'Balanced'
    tab.loc[tab["AMOUNT PAID"] !=tab ["PAYABLE AMOUNT"], 'STATUS'] = 'Not Balanced'
    ife = tab.drop(columns=['id'])
    k = ife.to_csv()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="coop.xlsx"'
    writer = csv.writer(response)
    writer.writerow([k])
    return response







def search(request):
    extension = 'csv'
    all_filenames = [i for i in glob.glob('zz/*.{}'.format(extension))]
    form = SearchModelForm(request.POST or None,  request.FILES or None)
    if form.is_valid():
        print('valid')
        x_word = form.cleaned_data['s_word']
        for i in range(0,len(all_filenames)):
            with open(all_filenames[i], "r") as csvfile:
                reader = csv.DictReader(csvfile)
                #items = []
                for row in reader:
                    if x_word is not None:
                        #for id in all_filenames:
                            if x_word == int(row.get("ID")):
                                print(row)
                                return HttpResponse(row)

    context = {'form': form}
    template_name = 'core/search.html'
    return render(request, template_name, context)


    storage = messages.get_messages(request)
messages.success(request,"File successfully uploaded")
        {% if messages %}
        {% for message in messages %}
              <div class="alert alert-success" role="alert">
                  {{ message }}
              </div>
        {% endfor %}
        {% endif %}


###SEARCH BY SUBSCRIBER'S ID
import pandas as pd
import glob
import csv
extension = 'csv'
all_filenames = [i for i in glob.glob('zz/*.{}'.format(extension))]
csv_list = [pd.read_csv(f) for f in all_filenames]
#for i in range(0,len(all_filenames)):
#    with open(all_filenames[i], "r") as csvfile:
#        reader = csv.reader(csvfile)
#        for row in reader:
#            print(row)
#def search(user_id=None):
user_id = input()
for i in range(0,len(all_filenames)):
    with open(all_filenames[i], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        items = []
        for row in reader:
            #print(row)
            if user_id is not None:
                #for id in all_filenames:
                    if int(user_id) == int(row.get("id")):
                        print(row)



###REGISTRATION
import pandas as pd
import glob
import csv
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
id = input('Enter id')
name = input('Enter name')
with open('january.csv', "a") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([id,name])







def registration(request):
    with open('zz/base.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        sub = Subscriber.objects.all()
        form = SubscriberModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            writer.writerow([])
            obj = form.save(commit=False)
            obj.save()
            return redirect('/tables')
        form = SubscriberModelForm()
    template_name = 'core/registration.html'
    context = {'form': form}
    return render(request, template_name, context)









def tables(request):
    extension = 'csv'
    all_filenames = [i for i in glob.glob('csv_files/*.{}'.format(extension))]
    csv_list = [pd.read_csv(f) for f in all_filenames]
    full = csv_list[-1]
    rev =reversed(csv_list)
    combined_csv = pd.concat(rev, axis=1, copy=False)
    overall = combined_csv['amount']
    ht = overall.to_html()
    return HttpResponse(ht)



def tables_two(request):
    extension = 'csv'
    all_filenames = [i for i in glob.glob('csv_files/*.{}'.format(extension))]
    csv_list = [pd.read_csv(f) for f in all_filenames]
    full = csv_list[-1]
    rev =reversed(csv_list)
    combined_csv = pd.concat(rev, axis=1, copy=False)
    overall = combined_csv['amount']
    print(overall)
    ht = overall.to_html()
    return HttpResponse(ht)




#os.chdir('/csv_files')

def tables_two(request):
    extension = 'csv'
    all_filenames = [i for i in glob.glob('csv_files/*.{}'.format(extension))]
    a = [pd.read_csv(f) for f in all_filenames]
    full = a[-1]
    dd =reversed(a)
    new = pd.DataFrame(reversed(a))
    #da = a.select_dtypes(include=['amount'], exclude=['email'])
    combined_cs = pd.concat(dd, axis=1,copy=False)
    combined_csv = combined_cs['amount']
    #for index, row in combined_csv.iterrows():
    #    summation= combined_csv.at[index] = sum(row['amount'])
    #    print(summation)
    ht = combined_csv.to_html()
    return HttpResponse(ht)



def tables(request):

    extension = 'csv'
    all_filenames = [i for i in glob.glob('zz\*.{}'.format(extension))]
    csv_list = [pd.read_csv(f) for f in all_filenames]
    month_names=[str(i).strip('zz\.csv') for i in all_filenames]
    csv_names = [pd.DataFrame(f).set_index('id') for f in csv_list]

    def dfSum(x,y):
        df = pd.DataFrame(columns=['id','name','email','payment starting date','supposed end date','payable_amount',str(month_names[x]),str(month_names[y]),'amount','balance'])
        for i in csv_names[x].index:
            for j in csv_names[y].index:
                if i == j:
                    df=df.append({'id': csv_names[x].index[i-1],'name':csv_names[x].name[i],'email':csv_names[x].email[i],
                                  'payment starting date':csv_names[x]['payment starting date'][i],'supposed end date':csv_names[x]['supposed end date'][i],
                                'payable_amount':csv_names[x]['payable_amount'][i],str(month_names[x]):csv_names[x]['amount'][i],
                                   str(month_names[y]):csv_names[y]['amount'][j],'amount': int(csv_names[x]['amount'][i]) + int(csv_names[y]['amount'][j]),
                                'balance':int(csv_names[x].payable_amount[i])-(int(csv_names[x]['amount'][i]) + int(csv_names[y]['amount'][j]))}, ignore_index = True)
                    k = df.set_index('id')
        return k

    for i in range(0,len(csv_names)):
        if len(csv_names) >= 2:
            p = dfSum(1,0)
            csv_names.pop(0)
            csv_names[0] = p

    #print(csv_names[1])
    ht = csv_names[1].to_html()
    return HttpResponse(ht)
