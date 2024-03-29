
# 1 install virtualenv in the terminal
pip install virtualenv

# 2 to create vertual environment called "venv" 
python -m virtualenv venv

# 3 activate venv
venv\Scripts\activate

for deactivate venv\Scripts\deactivate

# 4 install django
pip install django

# show all packages
pip list

# 5 create django project with the name "pdfams"
django-admin startproject pdfams


# 6 change interpeter to venv folder to make sure you don't face errors of packages
ctrl+shift+p
python select interpeter
enter interpeter path , and past the venv folder path


# 7 to run the server
cd to the project folder cd pdfams
run -> python manage.py runserver

ctrl+c to use terminal again

# 8 create django app inside project folder with the name "webapp"
django-admin startapp webapp

# add the webapp to the INSTALLED_APPS list in the 
projectFolder -> settings.py
then run server again

# 10 run migrations
python manage.py migrate

# 11 create superuser
python manage.py createsuperuser


# pages views will be in webapp views.py


# urls.py in projects is the urls to any page, is better to leave it holding only admin url and create new urls.py script in webapp for rest of the use, like dashboard, log in etc..
then we need to link the urls in webapp to the main one in the project
- add include library to urls.py of pdfams
- add the following to the urlpatterns -> path('', include('webapp.urls')),

# 12 to get the home page
- make views.py in the webapp look like this:

from django.shortcuts import render
from django.http import HttpResponse
def home(request):
    return HttpResponse("hello world")

- then make urls.py look like 

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=''),
]


# 13 setup static pages, css/js
- add static folder side by side to the folders webapp and pdfams
- add subfolders of css, and js
- link static to the settings in the pdfams
- add under STATIC_URL = 'static/' the following

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# 14 adding the HTML templates
- add templates folder inside webapp
- add to it subfolder called same as the app name, in our case is "webapp"
- add inside it index.html file
- now go to the views.py and change 
def home(request):
    return HttpResponse("hello world")

to ->
def home(request):
return render(request, 'webapp/index.html')

# 15 add base.html file to inhert it over all pages

inside webapp/templates/webapp create base.html
- in this file at the begaing add {% load static %} to load all  static js/css
and then add the html template

{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>AMS</title>
    <link rel="stylesheet" type="text/css" href="https://bootswatch.com/5/flatly/bootstrap.min.css">

    <link rel="stylesheet" type="text/css" href="{% static 'css/styles.css' %}">
</head>
<body>
    <!-- Create Navbar here-->
    <div class="container">
        <br>
        <!-- Create Notification Message -->


        <!-- Create block to hold any content -->
        {%  block content %}

        {% endblock %}
    </div>

    <script src="{% static 'js/app.js' %}"></script>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js" crossorigin="anonymous"></script>
    
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js" integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy" crossorigin="anonymous"></script>

</body>
</html>

css style from
https://bootswatch.com
js script of bootstrap from
https://getbootstrap.com/docs/5.3/getting-started/introduction/



# 16 create forms of the register and login 
- creat forms.py inside webapp
and should look like:

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AuthenticationForm

from django import forms
from django.forms.widgets import PasswordInput, TextInput, EmailInput

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


# 17 to inhert base.html over index.html for example and make index.html as content block
- make index.html looks like:
{% extends "webapp/base.html" %}
{% block content %}
<h1> Hello</h1> // here add whatever you wish
{% endblock %}

- if css changes not shown up, try to clean the cache of the browser


# show specific content for user or not user 
{% if user.is_authenticated %}
<a> Show to the user</a>
{% else %}
<a> Show to the non user</a>
{% endif %}


# to create any forms, like user, record // inside webapp
- first create your form class in the forms.py
- go to views.py and import the class of the form then create function to return the request form


# to add any page you need
- add function in views.py to return the page
def home(request):
    return render(request, 'webapp/index.html')

- add path of the page in urls.py inside urlpatterns
path('name of the function from views.py', views.name of the function from views.py, name='name of the function from views.py'),
like path('register', views.register, name='register'),


# Create Model to sotre Records in the database
- go to models.py, and make Class of the record and it's properties
class Record(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    Full_name = models.CharField(max_length=256)

- Then go to admin.py and import the model and register it 
from .models import Record 
admin.site.register(Record)

- make magrition to have new migration
python manage.py makemigrations

- Migrate everything
python manage.py migrate

Now you can see the records in the admin dashboard

-- to show it into page, go to views and import the model
from .models import Record
-- Then add the variable of all records in the function that have the page, example dashboard
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records': my_records}
    return render(request, 'webapp/dashboard.html' , context=context)

