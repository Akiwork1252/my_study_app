import re
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View, generic
from django.utils import timezone
from django.urls import reverse

from ai_support.services import choice_test_scoring, generate_multiple_choice_questions, written_test_scoring, generate_written_questions, generate_comprehesive_questions
from ascension.models import LearningPlan, LearningGoal
from analytics.models import Progress


# テストチャット(選択問題)
def choice_test_view(request, learning_goal_id):
    if request.method == 'GET':
        # クエリパラメータからtopicを取得
        topic = request.GET.get('topic')
        # セッションに保存(次の問題生成で利用)
        if topic:
            request.session['current_topic'] = topic  # トピックをセッションに保存
        # トピックが取得できなかった場合
        else:
            topic = request.session.get('current_topic', learning_goal.topic)

        # learning_planを取得してセッションに保存
        learning_plan = LearningPlan.objects.filter(user=request.user,
                                                    topic=topic,
                                                    learning_goal_id=learning_goal_id
                                                    ).first()
        print(f'learning_plan_id: {learning_plan.id}')
        if not learning_plan:
            return JsonResponse({'ERROR': '関連するLearningPlanが見つかりませんでした。'})
        request.session['learning_plan_id'] = learning_plan.id

        # topicに関する問題文を生成
        question = generate_multiple_choice_questions(topic)
        # 問題文をセッションに保存
        request.session['current_question'] = question

        return render(request, 'learning_test/choice_test_chat.html', {
            'learning_goal_id': learning_goal_id,
            'question': question
        })
    
    elif request.method == 'POST':
        user_answer = request.POST.get('message')

        # セッションからtopic、learning_plan_id、前回の問題を取り出す
        topic = request.session.get('current_topic')  
        learning_plan_id = request.session.get('learning_plan_id')
        previous_question = request.session.get('current_question', '')
        print(f"Debug: topic={topic}, learning_plan_id={learning_plan_id}")
        print(f"Debug: previous_question={previous_question}")

        if not topic or not learning_plan_id:
            print("Debug: セッションから必要なデータが見つかりません。")
            return JsonResponse({'ERROR': 'セッションから必要なデータが見つかりません。'})
        
        if not previous_question:
            print("Debug: 問題が見つかりません。")
            return JsonResponse({'ERROR': '問題が見つかりません。'})

        # 採点結果を取得
        result = choice_test_scoring(previous_question, user_answer)  # 戻り値:{'score': int float, 'explanation': str}
        score = result['score']
        print(f"Debug: result={result}")

        # 問題を生成してセッションに保存
        question = generate_multiple_choice_questions(topic, previous_question)
        print(f"Debug: next_question={question}")
        request.session['current_question'] = question

        # スコアと問題数を保持
        question_count = int(request.GET.get('question_count', 1))  # リクエストで追跡
        total_score = float(request.session.get('total_score', 0)) + score  # 合計スコアを計算
        request.session['total_score'] = total_score  # 更新された合計スコアを保存
        try:
            question_count = int(question_count)
        except ValueError:
            question_count = 1
        print(f"Debug: question_count={question_count}, total_score={total_score}")

        # テスト終了条件
        if question_count >= 5:
            print("Debug: テスト終了処理開始")
            # Progressモデルにテストデータ保存
            progress = Progress.objects.create(
                user=request.user,
                learning_goal_id=learning_goal_id,
                learning_plan_id = learning_plan_id,
                score=total_score,
                started_at=timezone.now()
            )
            # LearningGoalモデルのtotalスコアを更新
            learning_goal = LearningGoal.objects.get(id=learning_goal_id)
            learning_goal.total_score = (learning_goal.total_score or 0) + total_score
            learning_goal.save()

            return JsonResponse({
                'score': score,  # 回答のスコア
                'explanation': result['explanation'],  # 問題の解説
                'message': '確認テストは以上です。終了ボタンを押してください。',
                'total_score': total_score,  # テストの合計点数
                # 'redirect_url': reverse('ascension:learning_plan_list', args=[learning_goal_id]),
            })
        
        return JsonResponse({
            'score': score,  # 回答のスコア
            'explanation': result['explanation'],  # 問題の解説
            'next_question': question,  # 次の問題
            'question_score': question_count + 1,  # 次の問題数 
            'total_score': total_score,  # 合計スコア
        })
        

# テストチャット(入力問題)
def written_test_view(request, learning_goal_id):
    if request.method == 'GET':
        # クエリパラメータからtopicを取得
        topic = request.GET.get('topic')
        # セッションに保存(次の問題生成で利用)
        if topic:
            request.session['current_topic'] = topic  # トピックをセッションに保存
        # トピックが取得できなかった場合
        else:
            topic = request.session.get('current_topic', learning_goal.topic)

        # learning_planを取得してセッションに保存
        learning_plan  =LearningPlan.objects.filter(user=request.user,
                                                    topic=topic,
                                                    learning_goal_id=learning_goal_id
                                                    ).first()
        print(f'learning_plan_id: {learning_plan.id}')
        if not learning_plan:
            return JsonResponse({'ERROR': '関連するLearningPlanが見つかりませんでした。'})
        request.session['learning_plan_id'] = learning_plan.id

        # topicに関する問題文を生成
        question = generate_written_questions(topic)
        # 問題文をセッションに保存
        request.session['current_question'] = question

        return render(request, 'learning_test/written_test_chat.html', {
            'learning_goal_id': learning_goal_id,
            'question': question
        })
    

    elif request.method == 'POST':
        user_answer = request.POST.get('message')
        # セッションからtopicとlearning_plan_idを取り出す
        topic = request.session.get('current_topic')  
        learning_plan_id = request.session.get('learning_plan_id')
        print(f"Debug: topic={topic}, learning_plan_id={learning_plan_id}")

        if not topic or not learning_plan_id:
            print("Debug: セッションから必要なデータが見つかりません。")
            return JsonResponse({'ERROR': 'セッションから必要なデータが見つかりません。'})

        # 前回の問題をセッションから取得
        previous_question = request.session.get('current_question', '')
        print(f"Debug: previous_question={previous_question}")
        if not previous_question:
            print("Debug: 問題が見つかりません。")
            return JsonResponse({'ERROR': '問題が見つかりません。'})
        # print(f'Previous question: {previous_question}')

        # 採点結果を取得
        result = written_test_scoring(previous_question, user_answer)  # 戻り値:{'score': int float, 'explanation': str}
        print(f"Debug: result={result}")
        score = result['score']
        explanation = result['explanation']

        print("Debug: テスト終了処理開始")
        learning_plan_id = request.session.get('learning_plan_id')
        if learning_plan_id is None:
            return JsonResponse({'ERROR': 'セッションにlearning_plan_idがありません。'})
        # Progressモデルにテストデータ保存
        progress = Progress.objects.create(
            user=request.user,
            learning_goal_id=learning_goal_id,
            learning_plan_id = learning_plan_id,
            score=score,
            started_at=timezone.now()
        )

        # LearningGoalモデルのtotalスコアを更新
        learning_goal = LearningGoal.objects.get(id=learning_goal_id)
        learning_goal.total_score = (learning_goal.total_score or 0) + score
        learning_goal.save()

        return JsonResponse({
            'score': score,
            'explanation': explanation,
            'message': '記述テストは以上です。終了ボタンを押してください。',
        })
        

# テストチャット(学習目標総合問題)
def comprehensive_test_view(request, learning_goal_id):
    if request.method == 'GET':
        # 学習目標の全てのlearning planを取得
        learning_plans = LearningPlan.objects.filter(user=request.user, learning_goal_id=learning_goal_id)
        if not learning_plans.exists():
            return JsonResponse({'ERROR': '関連するLearningPlanが取得できませんでした。'})
        
        # 全てのトピックをリスト化してセッションに保存
        topics = [plan.topic for plan in learning_plans]
        print(f'DEBUG: topics={topics}')
        request.session['topics'] = topics

        # topicに関する総合問題文を生成してセッションに保存
        try:
            question = generate_comprehesive_questions(topics)
        except Exception as e:
            return JsonResponse({'ERROR': f'問題の生成に失敗しました。: {str(e)}'})
        request.session['current_question'] = question

        return render(request, 'learning_test/comprehensive_test_chat.html', {
            'learning_goal_id': learning_goal_id,
            'question': question
        })
    

    elif request.method == 'POST':
        user_answer = request.POST.get('message')

        # セッションからtopic一覧と問題を取り出す
        topics = request.session.get('topics', [])  
        previous_question = request.session.get('current_question', '')
        print(f"Debug: topic={topics}, previous_question={previous_question}")

        if not topics or not previous_question:
            return JsonResponse({'ERROR': 'セッションから必要なデータが見つかりません。'})


        # 採点結果を取得
        result = written_test_scoring(previous_question, user_answer)  # 戻り値:{'score': int float, 'explanation': str}
        print(f"Debug: result={result}")
        score = result['score']
        explanation = result['explanation']

        print("Debug: テスト終了処理開始")
        # Progressモデルにテストデータ保存
        progress = Progress.objects.create(
            user=request.user,
            learning_goal_id=learning_goal_id,
            learning_plan=None,
            score=score,
            started_at=timezone.now()
        )

        # LearningGoalモデルのtotalスコアを更新
        learning_goal = LearningGoal.objects.get(id=learning_goal_id)
        learning_goal.total_score = (learning_goal.total_score or 0) + score
        learning_goal.save()

        return JsonResponse({
            'score': score,
            'explanation': explanation,
            'message': '記述テストは以上です。終了ボタンを押してください。',
        })

