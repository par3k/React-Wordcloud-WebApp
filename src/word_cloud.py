from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# 플라스크 웹 서버 객체 생성
app = Flask(__name__)
CORS(app)

# 폰트 경로 설정
font_path = '/Users/alex/Documents/GitHub/React-Wordcloud-WebApp/src/NanumGothic.ttf'


def get_tags(text, max_count, min_length):
    # 명사만 추출합니다.
    t = Okt()
    nouns = t.nouns(text)
    processed = [n for n in nouns if len(n) >= min_length]

    # 모든 명사의 출현 빈도를 계산합니다.
    count = Counter(processed)
    result = {}

    # 출현 빈도가 높은 max_count 개의 명사만을 추출합니다.
    for n, c in count.most_common(max_count):
        result[n] = c

    # 추출된 단어가 하나도 없는 경우 '내용이 없습니다.'를 화면에 보여줍니다.
    if len(result) == 0:
        result["내용이 없습니다."] = 1
    return result


def make_cloud_image(tags, file_name):
    word_cloud = WordCloud(
        font_path=font_path,
        width=800,
        height=800,
        background_color="white"
    )
    word_cloud = word_cloud.generate_from_frequencies(tags)
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(word_cloud)
    plt.axis("off")
    fig.savefig("/Users/alex/Documents/GitHub/React-Wordcloud-WebApp/src/outputs/{0}.png".format(file_name))


def process_from_text(text, max_count, min_length, words, file_name):
    tags = get_tags(text, int(max_count), int(min_length))

    # 단어 가중치를 적용
    for n, c in words.items():
        if n in tags:
            tags[n] = tags[n] * float(words[n])
    make_cloud_image(tags, file_name)


@app.route("/process", methods=['GET', 'POST'])
def process():
    content = request.json
    words = {}
    if content['words'] is not None:
        for data in content['words'].values():
            words[data['word']] = data['weight']
    process_from_text(content['text'], content['maxCount'], content['minLength'], words, content['textID'])
    result = {'result':True}
    return jsonify(result)

@app.route("/outputs", methods=['GET', 'POST'])
def output():
    text_id = request.args.get('textID')
    return app.send_static_file(text_id + '.png')


@app.route('/validate', methods=['GET', 'POST'])
def validate():
    text_id = request.args.get('textID')
    path = "outputs/{0}.png".format(text_id)
    result = {}

    if os.path.isfile(path):
        result['result'] = True
    else:
        result['result'] = False
    return jsonify(result)

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)

