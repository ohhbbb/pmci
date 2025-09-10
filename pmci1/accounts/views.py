from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import CustomLoginForm, AddUserform , StudentRecordForm
from .models import CustomUser , StudentRecord


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
    form = AddUserform()

    if request.method == 'POST':
        form = AddUserform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')

    return render(request, 'AdminDB/user_management.html', {
        'users': users,
        'form': form
    })


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



@login_required
def studentrecord(request):
    students = StudentRecord.objects.all().order_by('last_name')

    if request.method == 'POST':
        if "add_student" in request.POST:
            form = StudentRecordForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Student record added successfully.")
                return redirect('studentrecord')

        elif "delete_student" in request.POST:
            student_id = request.POST.get("student_id")
            student = get_object_or_404(StudentRecord, id=student_id)
            student.delete()
            messages.error(request, "Student record deleted.")
            return redirect('studentrecord')

    else:
        form = StudentRecordForm()

    return render(request, 'RegistrarDB/studentrecord.html', {
        'form': form,
        'students': students,
    })

@login_required
def studentrecord(request):
    students = StudentRecord.objects.all().order_by("last_name")

    if request.method == "POST":
        # ADD STUDENT
        if "add_student" in request.POST:
            lrn = request.POST.get("lrn", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            first_name = request.POST.get("first_name", "").strip()
            middle_name = request.POST.get("middle_name", "").strip()

            # ✅ SERVER-SIDE VALIDATION
            if not lrn.isdigit():
                messages.error(request, "LRN must contain only numbers.")
            elif StudentRecord.objects.filter(lrn=lrn).exists():
                messages.error(request, "A student with this LRN already exists.")
            else:
                StudentRecord.objects.create(
                    lrn=lrn,
                    last_name=last_name,
                    first_name=first_name,
                    middle_name=middle_name
                )
                messages.success(request, "Student record added successfully.")
                return redirect("studentrecord")

        # EDIT STUDENT
        elif "edit_student" in request.POST:
            student_id = request.POST.get("student_id")
            student = get_object_or_404(StudentRecord, id=student_id)

            lrn = request.POST.get("lrn", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            first_name = request.POST.get("first_name", "").strip()
            middle_name = request.POST.get("middle_name", "").strip()

            if not lrn.isdigit():
                messages.error(request, "LRN must contain only numbers.")
            elif StudentRecord.objects.exclude(id=student.id).filter(lrn=lrn).exists():
                messages.error(request, "Another student already uses this LRN.")
            else:
                student.lrn = lrn
                student.last_name = last_name
                student.first_name = first_name
                student.middle_name = middle_name
                student.save()
                messages.success(request, "Student record updated successfully.")
                return redirect("studentrecord")

        # DELETE STUDENT
        elif "delete_student" in request.POST:
            student_id = request.POST.get("student_id")
            student = get_object_or_404(StudentRecord, id=student_id)
            student.delete()
            messages.error(request, " Student record deleted.")
            return redirect("studentrecord")

    # Always provide a blank form for the modal
    form = StudentRecordForm()
    return render(request, "RegistrarDB/studentrecord.html", {
        "form": form,
        "students": students,
    })
