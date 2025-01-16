from django.db import models

from accounts.models import CustomUser
from ascension.models import LearningPlan


# 学習進捗管理
class Progress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    learning_plan = models.ForeignKey(LearningPlan, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[
                                  ('not_started', '未完了'),
                                  ('in_progress', '進行中'),
                                  ('compleated', '完了'),
                              ],
                              default='not_started',
                              )
    score = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
