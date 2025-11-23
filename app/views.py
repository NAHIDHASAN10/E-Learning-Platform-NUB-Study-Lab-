from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def homePage(request):

    return render(request, 'home.html')


def signupPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        full_name = request.POST.get('full_name')
        user_type = request.POST.get('user_type')
        
        user_exists = UserInfoModel.objects.filter(username=username, email= email).exists()
        if user_exists:
            messages.error(request, 'Username or Email already exists.')
            return redirect('signup')
            
        if password == password:
            user = UserInfoModel.objects.create_superuser(
                username=username,
                email=email,
                password=confirm_password,
                full_name=full_name,
                user_type=user_type,
            )
            ProfileModel.objects.create(user=user)
            
            subject = 'Account Info Mail'
            message = 'Your account created successfully.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
        
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )

            messages.success(request, "Account Created Successfully!")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

    return render(request, 'signup.html')



def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password")
            return redirect('login')

    return render(request, 'login.html')



def logoutPage(request):
    logout(request)
    return redirect('login')


def changepassword(request):
    current_user = request.user

    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        if check_password(current_password, current_user.password):
            if new_password == confirm_password:
                current_user.set_password(new_password)
                current_user.save()
                update_session_auth_hash(request,current_user)
                return redirect('login')

    return render(request, 'changepassword.html')


#------Profile---------

def updateProfilePage(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        profile_image = request.FILES.get('profile_image')

        current_user = request.user
        profile_user = ProfileModel.objects.get(user=current_user)
        profile_user.full_name = full_name
        profile_user.phone = phone
        profile_user.bio = bio
        if profile_image:
            profile_user.profile_image = profile_image
        profile_user.save()
        return redirect('profile_list')
    
    return render(request, 'update_profile.html')



def profileListPage(request):
    profiles = ProfileModel.objects.all()
    return render(request, 'profile_list.html', {'profiles': profiles})




#--------Department--------

def department_ListPage(request):
    department = DepartmentModel.objects.all()
    return render(request, 'department_list.html', {'department': department})





#---------Course-----------

def course_ListPage(request):
    course = CourseRegistrationModel.objects.all()
    return render(request, 'course_list.html', {'course': course})



def add_coursePage(request):
    if request.method == 'POST':
        course_form = CourseRegistrationForm(request.POST)
        if course_form.is_valid():
            course_form.save()
            return redirect('course_list')
    else:
        course_form = CourseRegistrationForm()

    context = {
        'course_form': course_form,
    }
    return render(request, 'add_course.html', context)




def update_coursePage(request, id):
    course_data = CourseRegistrationModel.objects.get(id=id)
    
    if request.method == 'POST':
        course_form = CourseRegistrationForm(request.POST, instance=course_data)
        if course_form.is_valid():
            course_form.save()
            return redirect('course_list')
    else:
        course_form = CourseRegistrationForm(instance=course_data)

    context = {
        'course_form': course_form,
    }
    return render(request, 'update_course.html', context)



def delete_coursePage(request, id):
    CourseRegistrationModel.objects.get(id=id).delete()
    return redirect('course_list')


#-----Teacher-------

def teacher_infoPage(request):
    # Get all faculty members ordered by display order
    faculty_members = TeacherModel.objects.all().order_by("display_order")

    context = {
        "faculty_members": faculty_members
    }
    return render(request, "teacher_info.html", context)



def about_nub_redirect(request):
    return redirect("https://nub.ac.bd/")


def e_library(request):
    search = request.GET.get("search", "")
    category = request.GET.get("category", "")

    books = Ebook.objects.all()

    if search:
        books = books.filter(title__icontains=search)

    if category:
        books = books.filter(category__icontains=category)

    context = {
        "books": books,
        "search": search,
        "category": category,
    }
    return render(request, "e_library.html", context)




    
def online_modules(request):
    modules = Module.objects.all()
    return render(request, "online_modules.html", {
        "modules": modules,
        "year": 2025,
    })


def index(request):
    search = request.GET.get("search", "")
    category = request.GET.get("category", "")

    books = Book.objects.all()

    if search:
        books = books.filter(title__icontains=search) | books.filter(author__icontains=search)
    if category:
        books = books.filter(category__iexact=category)

    context = {
        "books": books,
        "search": search,
        "category": category,
    }
    return render(request, "e_library.html", context)

def lessons_view(request):
    return render(request, "lessons.html")


def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == "POST":
        score = 0
        for question in questions:
            selected = request.POST.get(str(question.id))
            is_correct = selected == question.correct_answer
            UserAnswer.objects.create(
                user=request.user,
                question=question,
                selected_answer=selected,
                is_correct=is_correct
            )
            if is_correct:
                score += 1
        return render(request, 'quiz_result.html', {'score': score, 'total': questions.count()})

    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})


