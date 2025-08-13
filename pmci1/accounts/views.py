from django.shortcuts import render, redirect, get_object_or_404
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
    context = {'users': users}
    if request.method == 'POST':
        form = AddUserform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    return render(request, 'AdminDB/user_management.html', context)

@login_required
def add_user(request):
    if request.method == 'POST':
        form = AddUserform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB yet
            if user.role == 'admin':
                user.is_staff = True
            else:
                user.is_staff = False
            user.save()
            return redirect('user_management')
    else:
        form = AddUserform()
    return render(request, 'AdminDB/add_user.html', {'form': form})


def docreq(request):
    return render(request, 'RegistrarDB/docreq.html')

def studentrecord(request):
    return render(request, 'RegistrarDB/studentrecord.html')

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = AddUserform(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = AddUserform(instance=user)

    return render(request, 'AdminDB/edit_user.html', {'form': form, 'user': user})


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('user_management')

    return render(request, 'AdminDB/delete_user.html', {'user': user})


