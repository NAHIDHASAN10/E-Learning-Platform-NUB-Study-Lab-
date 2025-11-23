from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserInfoModel(AbstractUser):
    User_Type = [
        ('Admin','Admin'),
        ('User','User'),
    ]

    full_name=models.CharField(max_length=100, null=True)
    user_type=models.CharField(max_length=100, choices=User_Type, null=True)

    def __str__(self):
        return f'{self.username}'
    
class DepartmentModel(models.Model):
    Faculty_Type = [
        ('Science','Science'),
        ('Business','Business'),
        ('Arts','Arts'),
    ]

    department_name=models.CharField(max_length=100, null=True)
    description=models.TextField(null=True)
    faculty_type=models.CharField(max_length=100, choices=Faculty_Type, null=True)

    def __str__(self):
        return f'{self.department_name}'    
    
class ProfileModel(models.Model):
    user = models.OneToOneField(UserInfoModel, on_delete=models.CASCADE,  related_name='profile_info', null=True)
    full_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='media/profile_image/', null=True, blank=True)

    def __str__(self):
        return self.full_name or self.user.username

    
class CourseRegistrationModel(models.Model):

    student_name = models.CharField(max_length=100, null=True)
    student_id = models.CharField(max_length=100, null=True)
    semester = models.IntegerField(null=True)
    section = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    subject = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return f'{self.student_name}'


class TeacherModel(models.Model):
    # Basic Information
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    department = models.CharField(max_length=100, default="Department of CSE")

    # Contact
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Profile Image
    profile_image = models.URLField(
        max_length=500,
        help_text="URL of profile image from university website"
    )

    # Qualifications
    qualification_1 = models.CharField(max_length=255, blank=True, null=True)
    qualification_2 = models.CharField(max_length=255, blank=True, null=True)
    qualification_3 = models.CharField(max_length=255, blank=True, null=True)

    # Optional field for ordering
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Ebook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=100, blank=True)
    cover_image = models.URLField(max_length=500)  # Book cover / thumbnail
    file_url = models.URLField(max_length=500)     # PDF or external link

    def __str__(self):
        return self.title    


class TutorialModel(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, default="W3Schools")
    category = models.CharField(max_length=50, choices=[
        ('Programming', 'Programming'),
        ('Web', 'Web Development'),
        ('Database', 'Database')
    ])
    file_url = models.URLField()
    cover_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    # library/models.py

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover_image = models.URLField(blank=True)  # or ImageField if you upload images
    file_url = models.URLField()  # link to download/open book
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


from django.db import models

class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='modules/')  # if using images
    slug = models.SlugField()

    def __str__(self):
        return self.title


# ---------------- ADVANCED QUIZ SYSTEM ----------------

class Quiz(models.Model):
    title = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', null=True)
    question_text = models.CharField(max_length=255, null=True)
    option1 = models.CharField(max_length=255, null=True)
    option2 = models.CharField(max_length=255, null=True)
    option3 = models.CharField(max_length=255, null=True)
    option4 = models.CharField(max_length=255, null=True)
    correct_answer = models.CharField(max_length=255, null=True, blank=True)



    def __str__(self):
        return self.question_text

class UserAnswer(models.Model):
    user = models.ForeignKey(UserInfoModel, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    selected_answer = models.CharField(max_length=255, null=True)
    is_correct = models.BooleanField()

