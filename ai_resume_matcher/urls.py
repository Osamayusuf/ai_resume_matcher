from django.contrib import admin
from django.urls import path, include
from resumes.views import home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/resumes/', include('resumes.urls')),
]