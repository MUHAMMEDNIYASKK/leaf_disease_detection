from django.shortcuts import render
from django.template import loader
from student.models import Login
from django.http import HttpResponse
def home(request):

    template=loader.get_template("home.html")
    context={}
    return HttpResponse(template.render(context,request))