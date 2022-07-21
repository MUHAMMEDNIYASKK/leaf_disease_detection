from django.urls import path
import student.views
urlpatterns = [
    path('log/', student.views.log, name='log'),
    path('reg/', student.views.reg, name='reg'),
    path('payment/', student.views.paymentfn, name='payment'),
    path('payment1/', student.views.paymentfn1, name='payment1'),
    path('paymentfn2/', student.views.paymentfn2, name='paymentfn2'),
    path('s_home/', student.views.s_home, name='s_home'),
    path('s_pending/', student.views.s_pending, name='s_pending'),
    path('approve_student/<id>', student.views.approve_student, name='approve_student'),
    path('reject_student/<id>', student.views.reject_student, name='reject_student'),
    path('approve_list_student/', student.views.approve_list_student, name='approve_list_student'),
    path('h_view/', student.views.h_view, name='h_view'),
    path('h_book/<id>', student.views.h_book, name='h_book'),
    path('attendance/', student.views.attendance1, name='attendance'),
    path('VACATE/', student.views.VACATE, name='VACATE'),
    path('VACATE1/', student.views.VACATE1, name='VACATE1'),
    path('myhstl/', student.views.myhstl, name='myhstl'),
    path('checkout/', student.views.checkout, name='checkout'),
    path('checkin/', student.views.checkin, name='checkin'),

 ]