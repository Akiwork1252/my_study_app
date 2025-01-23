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
    ).values('score', 'completed_at')

    # データフレイム作成
    df = pd.DataFrame(progress_data)
    df['completed_at'] = pd.to_datetime(df['completed_at'])
    df = df.sort_values('completed_at')

    # グラフ作成
    sns.lineplot(data=df, x='completed_at', y='socre')
    plt.title(f'スコア　〜{learning_goal.title}〜')
    plt.xlabel('completetion Date')
    plt.ylabel('Score')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存
    output_path = f'static/graph/{user.username}-{learning_goal.title}_score.png'
    plt.savefig(output_path)
    plt.close()

    return render(request, 'show_data.html', {
        'learning_goal': learning_goal,
        'graph_path': output_path,
    })


