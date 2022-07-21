from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from student.models import Login, Hreg, Sreg, room, payment,feedback
# Create your views here.
def a_home(request):
    template=loader.get_template("a_home.html")
    context={}
    return HttpResponse(template.render(context,request))
def admin_pending_view(request):
    r = Hreg.objects.raw("select * from student_hreg where status = 'pending' ")
    template = loader.get_template("admin_pending_view.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))
def approve_warden(request,id):
    r = Hreg.objects.get(id=id)
    r.status='approve'
    r.save()
    r = Hreg.objects.raw("select * from student_hreg where status = 'pending' ")
    template = loader.get_template("admin_pending_view.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))
def reject_warden(request,id):
    r = Hreg.objects.get(id=id)
    r.status='reject'
    r.save()
    r = Hreg.objects.raw("select * from student_hreg where status = 'pending' ")
    template = loader.get_template("admin_pending_view.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))
def block_warden(request,id):
    r = Hreg.objects.get(id=id)
    r.status='block'
    r.save()
    r = Hreg.objects.raw("select * from student_hreg where status = 'approve'")
    template = loader.get_template("admin_approve.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))


def approve_list_warden(request):
    r = Hreg.objects.raw("select * from student_hreg where status = 'approve' ")
    template = loader.get_template("admin_approve.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))



def view_feedback(request):
    ob=feedback.objects.all()
    print(ob)
    print("==================")
    r = feedback.objects.raw(
        "select student_Sreg.id,student_Sreg.sfname,student_Sreg.slname,student_feedback.feedback,student_feedback.date,student_Hreg.hname from student_feedback,student_Hreg,student_Sreg where student_Sreg.id=student_feedback.Sid and student_Hreg.id=student_feedback.Hid ")

    template = loader.get_template("admin_feedback.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))