import os
import json
from openai import OpenAI
from django.conf import settings


# 学習プランの作成
def generate_learning_plan(title, current_level, description):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""
<ユーザーの入力情報>と<作成ルール>に基づいて学習プランを作成してください。
<ユーザーの入力情報>
テーマ: {title}
学習経験: {current_level}
補足: {description}
<作成ルール>
1,(最重要)各topicは学習時間が長くならないようにできるだけ細かく設定してください。
2,学習プランは<例>のようにJSON形式で作成してください。
<例>[
    {{'topic':'python基本文法(変数)'}},
    {{'topic':'python基本文法(データ型)'}},
]
3,ユーザー入力はテーマのみ入力必須としています。それ以外は未入力(空文字)でも無視してください。
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
    raw_content = response.choices[0].message.content.strip()

    try:
        parsed_data = json.loads(raw_content)
        if '学習プラン' in parsed_data:
            generated_plan = parsed_data['学習プラン']
        else:
            generated_plan = parsed_data
    except json.JSONDecodeError as e:
        print(f'JSONでコードエラー: {e}')
        print(f'AIの出力内容:\n{raw_content}')
        generated_plan = []

    return generated_plan


if __name__ == '__main__':
    print(generate_learning_plan('Jave', '未経験', ''))
