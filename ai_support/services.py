import os
from openai import OpenAI
from django.conf import settings


# 学習プランの作成
def generate_learning_plan(title, current_level, description):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""
以下の<作成ルール>と<ユーザー入力情報>に基づいて最適な学習プランを作成してください。
<作成ルール>
1、ユーザー入力はテーマのみ入力必須としています。それ以外は未入力(空文字)でも無視してください。
2、各タスクは1時間程度の学習量に設定してください。(例:python基本文法(変数とデータ型)、python基本文法(制御構文))
3、出力は以下のJSON形式で作成してください。
[
  {{"topic": "Python基本文法（変数とデータ型）"}},
  {{"topic": "Python基本文法（制御構文）"}}
]
<ユーザー入力情報>
テーマ: {title}
テーマに関するユーザーのレベル: {current_level}
補足: {description}
"""

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'あなたはユーザーに最適な学習プランを提案するAIアシスタントです。'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=400,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()