from django.contrib import admin

from .models import CustomUser
from ascension.models import InterestCategory, LearningGoal, LearningPlan, UserInterest, Category
from analytics.models import Progress

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(InterestCategory)
admin.site.register(LearningGoal)
admin.site.register(LearningPlan)
admin.site.register(Progress)
admin.site.register(UserInterest)
admin.site.register(Category)
