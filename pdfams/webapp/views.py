from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import Record

from django.contrib import messages

# Home page view
def home(request):

    return render(request, 'webapp/index.html')


# Register a user page view
def register(request):
    form = CreateUserForm()
    if request.method == 'POST': # check if the reqeust is POST
        form = CreateUserForm(request.POST)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect("my-login")
    context = {'form': form}

    return render(request, 'webapp/register.html', context=context)

# Login a user page view
def my_login(request):
    form = LoginForm()
    if request.method == 'POST': # check if the reqeust is POST
        form = LoginForm(request.POST, data=request.POST)
        if form.is_valid(): 
            # username = request.POST.get('username')
            username = request.POST.get('username')
            password = request.POST.get('password')

            # check if the user is authenticated for email and password
            user = authenticate(request, username=username, password=password) 
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard") # redirect to the home page
            else:
                messages.error(request, 'Invalid credentials')
                return redirect("my-login")
    context = {'loginForm': form}

    return render(request, 'webapp/my-login.html', context=context)


# Logout a user page view
def user_logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out')
    return redirect("my-login") # redirect to the login page



# Dashboard page view

@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()

    context = {'records': my_records}
    return render(request, 'webapp/dashboard.html' , context=context)


# Create a Record
@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == 'POST': # check if the reqeust is POST
        form = CreateRecordForm(request.POST)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'Record created successfully')
            return redirect("dashboard")
        
    context = {'createForm': form}

    return render(request, 'webapp/create-record.html', context=context)


@login_required(login_url='my-login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST': # check if the reqeust is POST
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'Record updated successfully')
            return redirect("dashboard")
        
    context = {'UpdateForm': form}

    return render(request, 'webapp/update-record.html', context=context)


# Read/ View a single record
@login_required(login_url='my-login')
def singular_record(request, pk):
    all_record = Record.objects.get(id=pk)
    context = {'record': all_record}
    return render(request, 'webapp/view-record.html', context=context)

# Delete a record
@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect("dashboard")


# print a record

import os
import pdfrw
import pandas as pd

@login_required(login_url='my-login')
def print_record(request, pk):
    record = Record.objects.get(id=pk)
    
    
    pdf_template = "./pdf_templates/Employees_Information_Template.pdf" # PDF file path
    pdf_outPut_path = './pdf_templates/' # output folder path
    
    
    try:
        # data = {"SIN": record.SIN, "Full_name": record.Full_name, "Date_of_birth": record.Date_of_birth, 
        #          "Date_of_hire": record.Date_of_hire, "Address": record.Address, "City": record.City, 
        #          "Zip": record.Zip, "State": record.State, "Home_phone": record.Home_phone, 
        #          "Cell_phone": record.Cell_phone, "Spouse_name": record.Spouse_name, 
        #          "Em_name": record.Em_name, "Em_relationship": record.Em_relationship, "Date": record.Date}
        data = {"Full_name": record.Full_name,"Address": record.Address,}
        
        print(type(record.SIN))
        
        run = get_data_from_dictionary(pdf_template,pdf_outPut_path, data)
        messages.success(request, 'Record printed successfully') 
        print("Finish\n{} files has been created successfully".format(run))
                
    except PermissionError as pr:
        print("Please close this file \" {} \" \nand try again".format(pr.filename))
    except NameError as nerr:
        print()
    except OSError as orr:
        print("Please check of the following directory \" {} \" \nmaybe it has typo error".format(orr.filename))
    except FileNotFoundError as ferr:
        print("Problem with the following directory,\n{} \ncheck if this right directory for your rawdata and pdf template".format(ferr.filename))
    except KeyError as msg :
        m1 = "The field name {} it has error, please check these scenarios\n".format(msg)
        m2 = "1- Probably it has typo error in pdf form\n"
        m3 = "2- If this field name is not same as the excel's column name, then you should add it manually in the \'dictionary\'"
        print(m1,m2,m3)
    except AttributeError as atterr:
        print("You are using \"{}\" function incorrectly the error statement is\n{}".format(atterr.name,atterr.args))
    except Exception as e:
        print("The error is\n{}".format(e))
    finally:
        print("The program has been terminated")
        return redirect("dashboard")


def write_new_pdf(pdf_template, output_pdf_path, columnName):
    ANNOT_KEY = '/Annots'           # key for all annotations within a page
    ANNOT_FIELD_KEY = '/T'          # Name of field. i.e. given ID of field
    ANNOT_FORM_type = '/FT'         # Form type (e.g. text/button)
    ANNOT_FORM_button = '/Btn'      # ID for buttons, i.e. a checkbox
    ANNOT_FORM_text = '/Tx'         # ID for textbox
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'
    pdfin = os.path.normpath(os.path.join(os.getcwd(),'in',pdf_template)) # full directory of pdf output file
    template_pdf = pdfrw.PdfReader(open(pdfin, "rb"))  # make new pdf file and hold it

    dictionary = columnName  # Use provided dictionary directly
  
    ## the next for loop will fill the dictionary with all data required to fill the pdf form
    for Page in template_pdf.pages:
        if Page[ANNOT_KEY]:
            for annotation in Page[ANNOT_KEY]:
                if annotation[ANNOT_FIELD_KEY] and annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY :
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in dictionary:
                        continue
                    elif annotation[ANNOT_FORM_type] == ANNOT_FORM_button:
                        # button field i.e. a checkbox
                        dictionary[key] = columnName[key]
                        annotation.update(pdfrw.PdfDict(V=pdfrw.PdfName(dictionary[key]) , AS=pdfrw.PdfName(dictionary[key]) ))
                    elif annotation[ANNOT_FORM_type] == ANNOT_FORM_text:
                        # regular text field
                        dictionary[key] = columnName[key]
                        annotation.update( pdfrw.PdfDict( V=dictionary[key], AP=dictionary[key]) )
                    
                    annotation.update(pdfrw.PdfDict(Ff=1)) # this line to make the file fields none editable
                    
    # this will fill the pdf form field with the data
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))

    # this line will release the final version of the filled pdf form to the output path
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

def get_data_from_dictionary(pdf_template,pdf_outPut_path, data):
    i = 0 
    for key, columnName in data.items(): # Use .items() to iterate through dictionary
        i += 1
        ## the output file name
        outPutFileName = columnName['Full_name'] + "_information"
        ######################
        temp_out_dir = os.path.normpath(os.path.join(pdf_outPut_path,outPutFileName +'.pdf'))
        write_new_pdf(pdf_template, temp_out_dir, columnName)
        print(i, "...please wait...")
    return i