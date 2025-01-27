import matplotlib
matplotlib.use('Agg')  # 非インタラクティブモード

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from .models import Progress, LearningGoal
from my_study_app import settings_dev


# データトップ画面
class DataTopView(View):
    def get(self, request, learning_goal_id):
        learning_goal = get_object_or_404(LearningGoal, id=learning_goal_id)
        context = {
            'learning_goal': learning_goal
        }
        return render(request, 'analytics/data_top_menu.html', context)
    

# 学習目標のトータルスコア表示
def show_total_score_graph(request, learning_goal_id):
    user = request.user
    learning_goal = get_object_or_404(LearningGoal, id=learning_goal_id, user=user)

    # データ取得()
    progress_data = Progress.objects.filter(
        user=user,
        learning_goal=learning_goal,
    ).values('score', 'id')

    # データフレイム作成
    df = pd.DataFrame(progress_data)

    # スコアdf
    if not df.empty:
        df = df.sort_values('id').reset_index(drop=True)
        df['total_score'] = df['score'].cumsum()
        df['user_specific_id'] = range(1, (len(df)+1))

        # グラフ作成
        plt.plot(df['user_specific_id'], df['total_score'], marker='o', markersize=3, markerfacecolor='r')
        plt.title('Total-Score')
        plt.xlabel('Progress Order')
        plt.ylabel('Score')
        plt.xticks(rotation=45)
        plt.xlim(0, 100)
        plt.ylim(-50, 3000)
        plt.tight_layout()

        # 保存
        output_dir = os.path.join(settings_dev.MEDIA_ROOT, 'graph/')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, f'{user.username}-{learning_goal.title}_totalscore.png')
        plt.savefig(output_path)
        plt.close()

        graph_path = f'/static/graph/{user.username}-{learning_goal.title}_totalscore.png'
    else:
        graph_path = None


    return render(request, 'analytics/show_score_data.html', {
        'learning_goal': learning_goal,
        'graph_path': graph_path,
        'Error': '進捗データが存在しません。' if df.empty else None,
    })


# 学習目標のトピックスコア表示
def show_topic_score_graph(request, learning_goal_id):
    user = request.user
    learning_goal = get_object_or_404(LearningGoal, id=learning_goal_id, user=user)

    # データ取得()
    progress_data = Progress.objects.filter(
        user=user,
        learning_goal=learning_goal,
    ).values('score', 'id')

    # データフレイム作成
    df = pd.DataFrame(progress_data)

    # スコアdf
    if not df.empty:
        df = df.sort_values('id').reset_index(drop=True)
        df['user_specific_id'] = range(1, (len(df)+1))

        # グラフ作成
        plt.plot(df['user_specific_id'], df['score'], marker='o', markersize=3, markerfacecolor='r')
        plt.title('Topic-Test-Score')
        plt.xlabel('Progress Order')
        plt.ylabel('Score')
        plt.xticks(rotation=45)
        plt.ylim(-100, 200)
        plt.tight_layout()

        # 保存
        output_dir = os.path.join(settings_dev.MEDIA_ROOT, 'graph/')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, f'{user.username}-{learning_goal.title}_score.png')
        plt.savefig(output_path)
        plt.close()

        graph_path = f'/static/graph/{user.username}-{learning_goal.title}_score.png'
    else:
        graph_path = None


    return render(request, 'analytics/show_score_data.html', {
        'learning_goal': learning_goal,
        'graph_path': graph_path,
        'Error': '進捗データが存在しません。' if df.empty else None,
    })