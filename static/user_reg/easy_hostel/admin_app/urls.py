from django.urls import path
import admin_app.views
urlpatterns = [
    path('a_home/', admin_app.views.a_home, name='a_home'),
    path('admin_pending_view/', admin_app.views.admin_pending_view, name='admin_pending_view'),
    path('approve_warden/<id>', admin_app.views.approve_warden, name='approve_warden'),
    path('reject_warden/<id>', admin_app.views.reject_warden, name='reject_warden'),
    path('block_warden/<id>', admin_app.views.block_warden, name='block_warden'),
    path('approve_list_warden/', admin_app.views.approve_list_warden, name='approve_list_warden'),
    path('view_feedback/', admin_app.views.view_feedback, name='view_feedback'),
]