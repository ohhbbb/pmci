from django.urls import path
from .views import RoleBasedLoginView, admin_dashboard, finance_dashboard, reports, registrar_dashboard, user_management, docreq, studentrecord, add_user

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', RoleBasedLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('finance_dashboard/', finance_dashboard, name='finance_dashboard'),
    path('reports/', reports, name='reports'),
    path('registrar_dashboard/', registrar_dashboard, name='registrar_dashboard'),
    path('user_management/', user_management, name='user_management'),
    path('docreq/', docreq, name='docreq'),
    path('studentrecord/', studentrecord, name='studentrecord'),
    path('add_user/', add_user, name='add_user'),

]   
