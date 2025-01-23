import os
import json
import logging
import re
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from django.conf import settings
# from .auxiliary_functions import format_question_output

logger = logging.getLogger(__name__)


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
1,(重要)各topicは学習時間が長くならないようにできるだけ細かく設定してください。
2,(必須)学習プランは<例>のようにJSON形式で作成してください。また文字列は""で囲む等厳密なJSON形式に従うこと、出力はJSON形式のデータのみにしてください。
<例>[
    {{'topic':'python基本文法(変数)'}},
    {{'topic':'python基本文法(データ型)'}},
]
3,ユーザー入力はテーマのみ入力必須としています。それ以外は未入力(空文字)でも無視してください。
"""
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'あなたはユーザーに最適な学習プランを提案するAIアシスタントです。'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    raw_content = response.choices[0].message.content.strip()
    if not raw_content:  # 空のレスポンスを確認
        print("AIから空のレスポンスが返されました。")
        print(f"Raw API Response:\n{response}")
        return []
    print(f"Debug: Raw Response Content:\n{raw_content}")
    # 不要なバッククォートを削除
    raw_content = raw_content.replace('```json', '').replace('```', '').strip()
    json_match = re.search(r'\[.*\]', raw_content, re.DOTALL)
    if not json_match:
        print('JSONデータが見つかりませんでした。')
        return []
    json_data = json_match.group()

    try:
        generated_plan = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f'JSONでコードエラー: {e}')
        print(f'AIの出力内容:\n{raw_content}')
        generated_plan = []

    return generated_plan


# ハンズオン講義
def generate_lecture_content(topic, user_input):
    if not user_input:
        return f'"{topic}" に関する講義を始めます。何か質問があれば教えてください。'
    
    # print(f"Generating lecture content for topic: {topic}, user input: {user_input}")
    llm = ChatOpenAI(temperature=0.7)
    prompt_template = ChatPromptTemplate.from_template(
        'あなたは教師であり、ユーザーはあなたの生徒です。以下のトピックに基づいてハンズオン形式で講義を行ってください。\n'
        'トピック:{topic}\n'
        'ユーザーの応答:{user_input}\n'
        '次の講義内容を出力してください。\n'
        # '{topic}に関する講義内容が全て終了した場合は、以下の終了コメントを出力してください。\n'
        # '終了コメント:講義は以上です。質問があれば入力してください。「終了」ボタンで講義を終了します。'
    )

    prompt = prompt_template.format_prompt(topic=topic, user_input=user_input)
    # print(f"Generated prompt: {prompt.to_string()}")
    response = llm.invoke(prompt.to_string())
    # print(f"Response received: {response.content}")
    if not response.content.strip():
        return 'トピックに基づくテスト問題生成中に問題が発生しました。'
    return response.content


# テスト採点(選択問題用)
def choice_test_scoring(question, user_answer):
    print(f'Debug:Question: {question}, User Answer: {user_answer}')
    llm = ChatOpenAI(temperature=0.2)
    prompt_template = ChatPromptTemplate.from_template(
        '以下はテスト問題とユーザーの回答です。\n'
        'テスト問題:{question}\n'
        'ユーザーの回答:{user_answer}\n'
        '10点満点で採点し、スコアと解説を以下の例のように辞書型(重要)で出力してください。\n'
        '例:{{"score": スコア, "explanation": 解説}}'
    )

    print(f"Debug: Prompt Template: {prompt_template}")
    try:
        prompt = prompt_template.format_prompt(
            question=question, 
            user_answer=user_answer
        )
        print(f'Debug: prompt: {prompt}')

        response = llm.invoke(prompt.to_string())
        print(f'AI Response: {response.content}')

        result = json.loads(response.content)
        if not isinstance(result, dict):
            raise ValueError(f'AI response is not a directory: {result}')
        missing_keys = [key for key in ['score', 'explanation'] if key not in result]
        if missing_keys:
            raise KeyError(f'Missing Keys in AI response: {missing_keys}, Response: {result}')
    except json.JSONDecodeError as e:
        print(f'JSON Decode Error: {response.content}')
        raise e
    except Exception as e:
        print(f'Unexpected Error: {e}')
        raise e
    return result


# テスト採点(記述問題用)
def written_test_scoring(question, user_answer):
    print(f'Debug:Question: {question}, User Answer: {user_answer}')
    llm = ChatOpenAI(temperature=0.2)
    prompt_template = ChatPromptTemplate.from_template(
        '以下はテスト問題とユーザーの回答です。\n'
        'テスト問題:{question}\n'
        'ユーザーの回答:{user_answer}\n'
        '以下の採点基準を元に採点を行い、スコア(合計点数)と解説を出力例のように辞書型(重要)で出力してください。\n'
        '採点基準:正確性(/40点)、設計(/20点)、読みやすさ(/20点)、ベストプラクティス(/20点)'
        '出力例:{{"score": 合計点数, "explanation": 解説}}'
    )

    print(f"Debug: Prompt Template: {prompt_template}")
    try:
        prompt = prompt_template.format_prompt(
            question=question, 
            user_answer=user_answer
        )
        print(f'Debug: prompt: {prompt}')

        response = llm.invoke(prompt.to_string())
        print(f'AI Response: {response.content}')

        result = json.loads(response.content)
        if not isinstance(result, dict):
            raise ValueError(f'AI response is not a directory: {result}')
        missing_keys = [key for key in ['score', 'explanation'] if key not in result]
        if missing_keys:
            raise KeyError(f'Missing Keys in AI response: {missing_keys}, Response: {result}')
    except json.JSONDecodeError as e:
        print(f'JSON Decode Error: {response.content}')
        raise e
    except Exception as e:
        print(f'Unexpected Error: {e}')
        raise e
    return result


# 選択問題を生成
def generate_multiple_choice_questions(topic, previous_question=''):
    llm = ChatOpenAI(temperature=0.7)
    if previous_question:
        prompt_text = (
            'あなたは教師です。以下のトピックから1問の選択問題を生成してください。\n'
            '前回の問題と内容が重複しないように注意してください。\n'
            'トピック:{topic}\n'
            '前回の問題:{previous_question}\n'
            '<例>\n'
            '問題: 生成した問題\n'
            'a): 選択肢1\n'
        )
    else:
        prompt_text = (
            'あなたは教師です。以下のトピックから1問の選択問題を生成してください。\n'
            'トピック:{topic}\n'
             '以下の<例>のように**改行を必ず適用**して出力してください。\n'
             '<例>\n'
             '問題: 生成した問題\n'
             'a): 選択肢1\n'
        )

    prompt_template = ChatPromptTemplate.from_template(prompt_text)
    prompt = prompt_template.format_prompt(topic=topic, previous_question=previous_question)
    response = llm.invoke(prompt.to_string())
    # formatted_output = format_question_output(response.content)
    return response.content


# 入力問題を生成
def generate_written_questions(topic):
    llm = ChatOpenAI(temperature=0.7)
    prompt_text = (
        'あなたは教師です。以下のトピックから1問のコーディング問題を生成してください。'
        'トピック内容がプログラミングでなければ、記述式の問題を生成してください。'
        'トピック:{topic}\n'
        '<例>\n'
        '問題: 生成した問題\n'
    )
    prompt_template = ChatPromptTemplate.from_template(prompt_text)
    prompt = prompt_template.format_prompt(topic=topic)
    response = llm.invoke(prompt.to_string())
    return response.content


if __name__ == '__main__':
    # print(generate_learning_plan('Jave', '未経験', ''))
    # lecture = generate_lecture_content('python基礎構文(データ型)', '')
    # print(lecture)
    # topics = ['python基礎構文(データ型)', 'python基礎構文(変数)']
    # test= generate_multiple_choice_questions(topics)
    # print(test)
    # question = "Pythonで整数を表すデータ型は何ですか？"
    # user_answer = 'int'
    # score = scoding(question, user_answer)
    # print(score)
    # question = '''
# 問題: Pythonでファイルを書き込む際に使用するメソッドはどれか？
# a): write()
# b): read()
# c): append()
# d): close()
# '''
#     answer = 'a'
#     result = choice_test_scoring(question=question, user_answer=answer)
#     print(result)
    title = 'python'
    level = '未経験'
    description = '株価予測ができるようになりたい'
    response = generate_learning_plan(title, level, description)
    print(response)
