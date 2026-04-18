from django.urls import path
from .views import create_resume, match_page, home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('create/', create_resume, name='create-resume'),
    path('view/<int:resume_id>/', match_page, name='match-page'),
]