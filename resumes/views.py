from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resume
from .utils import calculate_match, get_missing_skills
from jobs.models import Job
from django.contrib.auth.models import User


def generate_feedback(resume):
    feedback = []

    if len(resume.skills.split(",")) < 3:
        feedback.append("Add more skills to your resume")

    if len(resume.experience) < 20:
        feedback.append("Add more details to your experience")

    return feedback


def get_resume_score(resume):
    score = 50

    if len(resume.skills.split(",")) >= 3:
        score += 25

    if len(resume.experience) > 20:
        score += 25

    return score


@api_view(['GET'])
def match_jobs(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    jobs = Job.objects.all()

    results = []

    for job in jobs:
        score = calculate_match(resume.skills, job.required_skills)
        missing = get_missing_skills(resume.skills, job.required_skills)
        feedback = generate_feedback(resume)

        results.append({
            "job_title": job.title,
            "company": job.company,
            "match_score": score,
            "missing_skills": missing,
            "feedback": feedback,
            "resume_score": get_resume_score(resume)
        })

    results = sorted(results, key=lambda x: x['match_score'], reverse=True)

    return Response(results)


@api_view(['GET'])
def resume_list(request):
    resumes = Resume.objects.all().values()
    return Response(resumes)


def home_page(request):
    first_resume = Resume.objects.order_by("id").first()

    if first_resume:
        return redirect("match-page", resume_id=first_resume.id)

    return render(request, "resumes/match.html", {"jobs": []})


def match_page(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    jobs = Job.objects.all()

    results = []

    for job in jobs:
        score = calculate_match(resume.skills, job.required_skills)
        missing = get_missing_skills(resume.skills, job.required_skills)
        feedback = generate_feedback(resume)

        results.append({
            "job_title": job.title,
            "company": job.company,
            "match_score": score,
            "missing_skills": missing,
            "feedback": feedback,
            "resume_score": get_resume_score(resume)
        })

    results = sorted(results, key=lambda x: x['match_score'], reverse=True)

    return render(request, 'resumes/match.html', {"jobs": results})


def create_resume(request):
    if request.method == "POST":
        skills = request.POST.get("skills")
        experience = request.POST.get("experience")

        user = User.objects.first()

        resume = Resume.objects.create(
            user=user,
            skills=skills,
            experience=experience
        )

        return redirect('match-page', resume_id=resume.id)

    return render(request, "resumes/form.html")