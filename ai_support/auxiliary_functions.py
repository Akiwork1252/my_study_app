# aiの出力を改行付きにする
def format_question_output(ai_output):
    lines = ai_output.split(' ')
    formatted_output = []
    buffer = []

    for word in lines:
        buffer.append(word)
        if word.endswith(':') or word.endswith(')'):
            formatted_output.append(' '.join(buffer))
            buffer = []

    if buffer:
        formatted_output.append(' '.join(buffer))

    return '\n'.join(formatted_output)
