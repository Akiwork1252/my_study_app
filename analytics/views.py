import matplotlib
matplotlib.use('Agg')  # 非インタラクティブモード

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Progress, LearningGoal



def make_graph(request, learning_goal_id):
    user = request.user
    learning_goal = get_object_or_404(LearningGoal, id=learning_goal_id, user=user)

    # データ取得
    progress_data = Progress.objects.filter(
        user=user,
        learning_goal=learning_goal,
        completed_at__isnull=False
    ).values('score', 'id')

    # データフレイム作成
    df = pd.DataFrame(progress_data)
    df = df.sort_values('id')

    # グラフ作成
    sns.lineplot(data=df, x='id', y='score')
    plt.title('Total Score')
    plt.ylabel('Score')
    plt.xticks(rotation=45)
    plt.xlim(0, 100)
    plt.ylim(0, 3000)
    plt.tight_layout()

    # 保存
    output_dir = 'static/graph/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, f'{user.username}-{learning_goal.title}_score.png')
    plt.savefig(output_path)
    plt.close()

    graph_path = f'/static/graph/{user.username}-{learning_goal.title}_score.png'
    return render(request, 'analytics/show_data.html', {
        'learning_goal': learning_goal,
        'graph_path': graph_path,
    })
