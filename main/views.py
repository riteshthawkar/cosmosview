from django.shortcuts import render, redirect
from .get_data import get_info
from .models import Body, Model_3D
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.contrib import messages

import requests
from bs4 import BeautifulSoup


# Create your views here.
def index_view(request):
    return render(request, "index.html")


def discover_view(request):
    return render(request, "discover.html")

def view_3d(request):
    if request.method == "POST":
        name = request.POST["name"].title()
        model = Model_3D.objects.filter(name=name)
        return render(request, "viewer.html", {"model": model})
    models = Model_3D.objects.all()
    return render(request, "view.html", {"models": models})

def viewer(request, pk):
    model = Model_3D.objects.filter(id=pk)
    return render(request, "viewer.html", {"model": model})

def list_view(request, type):
    items = Body.objects.filter(category=type.lower())

    return render(request, "list.html", {"items": items, "type": type})


def data_view(request):
    if request.method == "POST":
        name = request.POST["name"]
        category = request.POST["category"]
        obj = Body.objects.filter(name=name.capitalize())
        if obj:
            context = get_info(keyword=obj[0].name, type=obj[0].category, url=obj[0].page_url, contenturl=obj[0].content_url, img_url=obj[0].img_url)
        else:
            context = get_info(keyword=name, type=category)

            if "table_data" in context:
                try:
                    page_url = context["page_url"]
                    image_url = context["img_url"]
                    content_url = context["content_url"]
                except:
                    page_url = ""
                    image_url = ""
                    content_url = ""
                obj = Body.objects.filter(name=name.capitalize())
                if not obj and page_url and image_url and content_url:
                    obj = Body.objects.create(name=name, category=category, page_url=page_url, img_url=image_url, content_url=content_url)
                    obj.save()
                else:
                    try:
                        context["img_url"] = obj[0].img_url
                    except:
                        pass
            else:
                context = {}
    else:
        context = {}
    return render(request, "data.html", context={"data": context})


def list_data_view(request, pk):
    obj = Body.objects.filter(id=pk)
    if obj:
        context = get_info(keyword=obj[0].name, type=obj[0].category, url=obj[0].page_url, contenturl=obj[0].content_url, img_url=obj[0].img_url)
    else:
        context = {}
    return render(request, "data.html", context={"data": context})

# def register_view(request):
#     if request.method =="POST":
#         print(request.POST)
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password1"]
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("index_view")
#     else:
#         print("Not Working")
#     return render(request, "registration.html")


# def login_view(request):
#     if request.method == "POST":
#         print(request.POST)
#         username = request.POST["username"]
#         password = request.POST["password1"]
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("index_view")
#         else:
#             messages.info(request, "You have successfully logged out.")
#     return render(request, "logIn.html")


# def logout_view(request):
#     logout(request)
#     return redirect("login_view")


from django.conf import settings
from django.core.mail import send_mail

def contact_view(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
        email_to = "riteshthawkar2003@gmail.com"

        subject = 'Hi, you have a new Email'
        message = f'Name: {name} \n Email: {email} \n Messsage: {message}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email_to,]
        send_mail( subject, message, email_from, recipient_list )

        return redirect("index_view")
    return render(request, "contact.html")

# import smtplib
# import ssl
# from email.message import EmailMessage

# email_sender = 'riteshthawkar2003@gmail.com'
# email_password = 'rbmduhbfdojjipud'
# email_receiver = 'fizzbuzz2000@gmail.com'
# subject = 'Check out my new video!'
# body = """
# I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg
# """

# def contact_view(request):
#     if request.method=="POST":
#         em = EmailMessage()
#         em['From'] = email_sender
#         em['To'] = email_receiver
#         em['Subject'] = subject
#         em.set_content(body)
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#             smtp.login(email_sender, email_password)
#             smtp.sendmail(email_sender, email_receiver, em.as_string())
        
#         return redirect("index_view")
#     return render(request, "contact.html")


# def add_model(request):
#     models = get_Models()
#     for model in models:
#         x = Model_3D.objects.create(name=model[0], model_url=model[1], caption=model[2])
#         x.save()
#     return render(request, "index.html")
