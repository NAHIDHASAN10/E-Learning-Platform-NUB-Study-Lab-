from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(UserInfoModel)
admin.site.register(ProfileModel)
for profile in ProfileModel.objects.all():
    print(profile.user.username, profile.user.email)

admin.site.register(CourseRegistrationModel)
admin.site.register(TeacherModel)
admin.site.register(DepartmentModel)
admin.site.register(Module)



class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Quiz, QuizAdmin)

