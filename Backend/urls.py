"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homePage, name='home'),
    path('signup/', signupPage, name='signup'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    
    path('changepassword/', changepassword, name='changepassword'),

    # ✅ Password Reset URLs (fixed)
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
        name='password_reset'
    ),

    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'
    ),

    path('reset/<uidb64>/<token>/', 
     auth_views.PasswordResetConfirmView.as_view(
         template_name='password_reset_confirm.html'
     ), 
     name='password_reset_confirm'),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'
    ),
    
    # Profile
    path('update_profile/', updateProfilePage, name='update_profile'),
    path('profile_list/', profileListPage, name='profile_list'),
    
    # Departments
    path('department_list/', department_ListPage, name='department_list'),
    
    # Courses
    path('course_list/', course_ListPage, name='course_list'),
    path('add_course/', add_coursePage, name='add_course'),
    path('update_course/<int:id>/', update_coursePage, name='update_course'),
    path('delete_course/<int:id>/', delete_coursePage, name='delete_course'),
    
    # Teacher
    path('teacher_info/', teacher_infoPage, name='teacher_info'),
    path("about-nub/", about_nub_redirect, name="about_nub"),
    
    # Library
    path("e-library/", e_library, name="e_library"),
    path("modules/", online_modules, name="online_modules"),
    
    # Lessons
    path('lessons/', lessons_view, name='lessons'),
    
    # Quiz
    path('quiz_list/', quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', take_quiz, name='take_quiz'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
