from django.db import models
from accounts.models import CustomUser


# 興味分野リスト
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# ユーザー興味分野
class InterestCategory(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# 中間モデル
class UserInterest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)


# ユーザー学習目標
class LearningGoal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    current_level = models.CharField(max_length=100, blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        # タスク完了でソート
        ordering = ['completed']

# ユーザー学習プラン
class LearningPlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    learning_goal = models.ForeignKey(LearningGoal, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
   
    def __str__(self):
        return self.topic
