from django.urls import path
from .views import create_resume, match_jobs, match_page, resume_list
urlpatterns = [
    path('', resume_list, name='resume-list'),
    path('match/<int:resume_id>/', match_jobs, name='match-jobs'),
    path('view/<int:resume_id>/', match_page, name='match-page-short'),
    path('view/<int:resume_id>/page/', match_page, name='match-page'),
    path('create/', create_resume),
]
