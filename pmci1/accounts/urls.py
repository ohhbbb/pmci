from django.urls import path
from .views import RoleBasedLoginView, admin_dashboard, finance_dashboard, registrar_dashboard
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', RoleBasedLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('finance_dashboard/', finance_dashboard, name='finance_dashboard'),
    path('registrar_dashboard/', registrar_dashboard, name='registrar_dashboard'),
]