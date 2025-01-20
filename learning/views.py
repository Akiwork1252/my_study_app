from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View, generic
from django.utils import timezone

from analytics.models import Progress
from ascension.models import LearningPlan
from ai_support.services import generate_lecture_content


# Create your views here.
class LectureChatView(View):
    def get(self, request, learning_plan_id):
        learning_plan = get_object_or_404(LearningPlan, id=learning_plan_id, completed=False)
        initial_ai_message = generate_lecture_content(
            topic=learning_plan.topic,
            user_input=''
        )
        
        context = {
            'learning_plan': learning_plan,
            'initial_ai_message': initial_ai_message, # 初回メッセージ
        }
        
        return render(request, 'learning/lecture_chat.html', context)
    
    def post(self, request, learning_plan_id):
        # ユーザーから応答を受け取り、次の講義内容を生成
        user_input = request.POST.get('message', '')
        learning_plan = get_object_or_404(LearningPlan, id=learning_plan_id, completed=False)

        # AIによる応答
        lecture_response = generate_lecture_content(topic=learning_plan.topic, user_input=user_input)

        # チャット終了
        if user_input.lower() == '終了':
            # LearningPlanモデル.topicを完了状態に更新
            learning_plan.completed = True
            learning_plan.save()

            # Progressモデルにデータを保存
            progress, _ = Progress.objects.get_or_create(
                user=request.user,
                learning_plan=learning_plan
            )
            progress.status = 'completed'
            progress.completed_at = timezone.now()
            progress.save()

            # 学習プランページに戻る
            return JsonResponse({'redirect_url': redirect('ascension:learning_plan_list', learning_goal_id=learning_plan.learning_goal.id).url})
        
        return JsonResponse({'lecture_response': lecture_response})
    