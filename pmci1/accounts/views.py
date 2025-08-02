from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import CustomLoginForm, AddUserform
from .models import CustomUser

class RoleBasedLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        user = self.request.user
        if user.role == 'admin':
            return reverse_lazy('admin_dashboard')
        elif user.role == 'finance':
            return reverse_lazy('finance_dashboard')
        elif user.role == 'registrar':
            return reverse_lazy('registrar_dashboard')
        return reverse_lazy('login')

@login_required
def admin_dashboard(request):
    return render(request, 'AdminDB/admin_dashboard.html')

@login_required
def finance_dashboard(request):
    return render(request, 'FinanceDB/finance_dashboard.html')

@login_required
def registrar_dashboard(request):
    return render(request, 'RegistrarDB/registrar_dashboard.html')

@login_required
def user_management(request):
    users = CustomUser.objects.all()
    return render(request, 'AdminDB/user_management.html', {'users': users})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = AddUserform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = AddUserform()
    return render(request, 'AdminDB/add_user.html', {'form': form})

def docreq(request):
    return render(request, 'RegistrarDB/docreq.html')

def studentrecord(request):
    return render(request, 'RegistrarDB/studentrecord.html')