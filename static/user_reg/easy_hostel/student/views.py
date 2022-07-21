from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from _datetime import datetime
from .models import Login, Hreg, Sreg,payment, room,feedback
from warden.models import attendance
from warden.models import book
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Create your views here.
def log(request):
        if request.method == "POST":
            uname = request.POST.get("username")
            password = request.POST.get("password")
            print(uname,password)
            ob=Login.objects.all()
            print(ob)
            print("*************************************")
            if (Login.objects.filter(username=uname, password=password)):
                l = Login.objects.filter(username=uname, password=password)
                for i in l:
                    utype = i.utype
                if (utype == "admin"):
                    context = {}
                    template = loader.get_template("a_home.html")
                    return HttpResponse(template.render(context, request))
                elif (utype == "warden"):
                    t = Hreg.objects.get(uname=uname)
                    print(t.status,"****************************************************")
                    if (t.status == "pending" or t.status=='block'):
                        return HttpResponse(
                            "<script>alert('NoT Approved By Admin');window.location='/log';</script>")
                    else:
                        request.session["uname"] = uname
                        request.session['lid']=t.id
                        context = {}
                        template = loader.get_template("warden_home.html")
                        return HttpResponse(template.render(context, request))
                elif (utype == "student"):
                    u = Sreg.objects.get(uname=uname)
                    if (u.status == "pending"):
                        return HttpResponse(
                            "<script>alert('NoT Approved By Admin');window.location='/log';</script>")
                    else:
                        request.session["uname"] = uname
                        request.session["lid"] = u.id
                        request.session["g"] = u.gender+"S"
                        request.session["email"] = u.pemail



                        context = {}
                        template = loader.get_template("s_home.html")
                        return HttpResponse(template.render(context, request))

                else:
                    return HttpResponse("<script>alert('Invalid User!!!');window.location='/log';</script>")
            else:
                return HttpResponse("<script>alert('Invalid !!!');window.location='/log';</script>")
        else:
            context = {}
            template = loader.get_template("log.html")
            return HttpResponse(template.render(context, request))
def reg(request):
    if (request.method == "POST"):
        r = Sreg()
        r.admnno = request.POST.get("Adms")
        r.sfname = request.POST.get("first name")
        r.slname = request.POST.get("last name")
        r.stream = request.POST.get("stream")
        r.yoj = request.POST.get("year")
        r.duration = request.POST.get("duration")
        r.semail = request.POST.get("Email")
        r.con = request.POST.get("Number")
        r.housename = request.POST.get("house name")
        r.location = request.POST.get("location")
        r.pin=request.POST.get("pin")
        r.gender=request.POST.get("g")
        r.district = request.POST.get("district")
        r.pname = request.POST.get("p_name")
        r.pemail = request.POST.get("pEmail")
        r.img = request.FILES['img']
        r.aadhar = request.FILES['imgadhar']
        r.uname = request.POST.get("uname")
        r.status = 'pending'
        r.save()
        l = Login()
        l.username = request.POST.get("uname")
        l.password = request.POST.get("pass")
        l.utype = 'student'
        l.save()
        return HttpResponse("<script>alert('registration successfull');window.location='/log'</script>")
    else:
         template = loader.get_template("reg.html")
         context={}
         return HttpResponse(template.render(context,request))

def paymentfn(request):
    r = payment.objects.filter(stid=request.session['lid'])
    template = loader.get_template("spayment.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))
def paymentfn1(request):
    template=loader.get_template("payment.html")
    context={}
    return HttpResponse(template.render(context,request))


def paymentfn2(request):
    amt=request.POST['amt']
    cn=request.POST['amt']
    ifsc=request.POST['amt']
    q = book.objects.raw("select * from warden_book where Sid=%s and (status='approve' or status='pending') ", [request.session['lid']])
    if q:
        hid=q[0].Hid
        ob=payment()
        ob.stid=request.session['lid']
        ob.htid=hid
        ob.amt=amt
        ob.accno=cn
        ob.ifsc=ifsc
        ob.date=datetime.today()
        ob.save()

        return HttpResponse("<script>alert('payment successful!!!');window.location='/s_home';</script>")

    else:
        return HttpResponse("<script>alert('No payment!!!');window.location='/s_home';</script>")


def checkin(request):
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('ajaykv3@gmail.com', 'Appukannan')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Your son/daughter has chech-in the hostel just now")
    print(msg)
    msg['Subject'] = 'Check-in notification'
    msg['To'] = request.session["email"]
    msg['From'] = 'ajaykv3@gmail.com'
    try:
        gmail.send_message(msg)


    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))

    return HttpResponse("<script>alert('Check-in notification sended!!!');window.location='/s_home';</script>")


def checkout(request):
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('ajaykv3@gmail.com', 'Appukannan')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Your son/daughter has check-out the hostel just now")
    print(msg)
    msg['Subject'] = 'Check-out notification'
    msg['To'] = request.session["email"]
    msg['From'] = 'ajaykv3@gmail.com'
    try:
        gmail.send_message(msg)


    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))

    return HttpResponse("<script>alert('Check-out notification sended!!!');window.location='/s_home';</script>")


def s_home(request):
    template=loader.get_template("s_home.html")
    context={}
    return HttpResponse(template.render(context,request))
def s_pending(request):

    r = Sreg.objects.raw("select * from student_sreg where status = 'pending' ")
    template = loader.get_template("s_pending.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))
def approve_student(request,id):
    r = Sreg.objects.get(id=id)
    r.status ='approve'
    r.save()
    r = Sreg.objects.raw("select * from student_sreg where status = 'pending' ")
    template = loader.get_template("s_pending.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))
def reject_student(request,id):
    r = Sreg.objects.get(id=id)
    r.status='reject'
    r.save()
    r = Sreg.objects.raw("select * from student_sreg where status = 'pending' ")
    template = loader.get_template("s_pending.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))
def approve_list_student(request):
    r = Sreg.objects.raw("select * from student_sreg where status = 'approve' ")
    template = loader.get_template("student_approve.html")
    context = {'k': r}
    return HttpResponse(template.render(context, request))
def h_view(request):
    ob = Hreg.objects.all()
    print("*********************")
    for i in ob:
        print("====================")
        print(i.type)
    print("*************************")
    r=Hreg.objects.raw("select * from student_hreg where status = 'approve' and type='"+request.session['g']+"' ")
    template = loader.get_template("hostel_view.html")
    context = {'k': r}
    print("===================")
    print(r)
    for i in r:
        print(i)
    print("===================")
    return HttpResponse(template.render(context, request))
def h_book(request,id):
    uname = request.session['uname']
    data = Sreg.objects.get(uname=uname)
    uid = data.id
    un = data.sfname
    ul = data.slname
    q=book.objects.raw("select * from warden_book where Sid=%s and hid=%s and status!='VACATE'",[uid,id])
    if q:
        return HttpResponse("<script>alert('please choose another hostel');window.location='/h_view'</script>")
    else:
        q = book.objects.raw("select * from warden_book where Sid=%s and (status='approve' or status='pending') ", [uid])
        if q:
            return HttpResponse("<script>alert('Vacate Room');window.location='/h_view'</script>")
        today=datetime.today()
        r = book()
        r.Sid = uid
        r.Hid = id
        r.sfn = un
        r.sln = ul
        r.bdate = today
        r.status = 'pending'
        r.save()
        return HttpResponse("<script>alert('Hostel Booked successfully');window.location='/h_view'</script>")
def attendance1(request):
    r = attendance.objects.raw("select * from warden_attendance where stid = '"+str(request.session['lid'])+"' ")

    context = {'k': r}
    for i in r:
        print(i.date,i.status)


    template=loader.get_template("attendance.html")

    return HttpResponse(template.render(context,request))


def VACATE(request):

    context = {}
    template = loader.get_template("s_vacate.html")
    return HttpResponse(template.render(context, request))
def myhstl(request):
    uname = request.session['uname']
    data = Sreg.objects.get(uname=uname)
    uid = data.id
    un = data.sfname
    ul = data.slname
    q = book.objects.raw("select warden_book.*,student_Hreg.hname,student_Hreg.location,student_Hreg.con from warden_book,student_Hreg where student_Hreg.id=warden_book.Hid and  warden_book.Sid=%s order by warden_book.id desc ", [uid])
    print(len(q))
    context = {"t":"0"}
    if len(q)>0:
        context = {"kk":q,"t":"1"}
    template = loader.get_template("myhsl.html")
    return HttpResponse(template.render(context, request))


def VACATE1(request):
    r = book.objects.raw("select * from warden_book where Sid = '"+str(request.session['lid'])+"' and (status='approve' or status='pending' ) ")

    print(r)
    for i in r:
        print(i.Sid,i.status)
        print("+++++++++++++++++++++++++++")

    fbk=request.POST['f']
    # Hid = models.IntegerField(default=0)
    # Sid = models.IntegerField(default=0)
    # feedback = models.CharField(max_length=50, default='')
    # date = models.CharField(max_length=50, default='')
    rr = r[0]#book.objects.get(Sid=request.session['lid'], status='approve')

    fbob=feedback()

    fbob.feedback=fbk
    fbob.Hid=rr.Hid
    fbob.Sid=request.session['lid']
    fbob.date=datetime.today()

    fbob.save()

    rr.status = 'VACATE'
    rr.save()
    context = {}
    template = loader.get_template("s_home.html")
    return HttpResponse(template.render(context, request))


