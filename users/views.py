from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from resumes.models import Resume
from jobs.models import Job


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords don't match!")
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'users/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('/users/dashboard/')

    return render(request, 'users/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/users/dashboard/')
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    return redirect('/users/login/')


@login_required(login_url='/users/login/')
def dashboard(request):
    user_resumes = Resume.objects.filter(user=request.user).order_by('-id')
    jobs = Job.objects.all()

    resume_data = []
    for resume in user_resumes:
        resume_data.append({
            'id': resume.id,
            'skills': resume.skills,
            'experience': resume.experience[:100] + '...' if len(resume.experience) > 100 else resume.experience,
            'created': resume.id,
        })

    return render(request, 'users/dashboard.html', {
        'resumes': resume_data,
        'total_resumes': len(resume_data),
        'total_jobs': jobs.count(),
    })


@login_required(login_url='/users/login/')
def delete_resume(request, resume_id):
    Resume.objects.filter(id=resume_id, user=request.user).delete()
    return redirect('/users/dashboard/')