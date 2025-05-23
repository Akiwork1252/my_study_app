from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
from ascension.models import LearningPlan, LearningGoal


# 学習進捗管理
class Progress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    learning_goal = models.ForeignKey(LearningGoal, on_delete=models.CASCADE, null=True, blank=True)
    learning_plan = models.ForeignKey(LearningPlan, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20,
                              choices=[
                                  ('not_started', '未完了'),
                                  ('in_progress', '進行中'),
                                  ('completed', '完了'),
                              ],
                              default='not_started',
                              )
    score = models.FloatField(null=True, blank=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.status == 'in_progress' and not self.started_at:
            self.started_at = timezone.now()
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.learning_plan:
            learning_plan_topic = self.learning_plan.topic 
        else:
            learning_plan_topic = self.learning_goal.title
        return f'{learning_plan_topic} - {self.get_status_display()}'
