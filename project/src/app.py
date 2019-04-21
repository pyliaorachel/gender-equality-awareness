from flask import Flask, render_template, request
app = Flask(__name__)

from .wordemb import WordEmb

emb_model = WordEmb()
emb_model.init()
print('Emb model ready!')

def color_text(text):
    res = ''
    for line in text.split('\n'):
        for raw_word in line.split():
            # Strip punctuations
            start = 0
            end = len(raw_word) - 1
            for i in range(len(raw_word)):
                c = raw_word[i]
                if c >= 'A' and c <= 'z': # english letter
                    start = i
                    break
            for i in range(len(raw_word) - 1, -1, -1):
                c = raw_word[i]
                if c >= 'A' and c <= 'z': # english letter
                    end = i + 1
                    break
            word = raw_word[start:end]

            # Scoring
            gender_score, sent_score = emb_model.gender_score(word), emb_model.sent_score(word)
            gender_score, sent_score = gender_score * 5, sent_score * 5 # scale-up

            if gender_score < 0: # male-like
                bg_color = 'rgba(0, 0, 255, {})'.format(abs(gender_score))
            else:
                bg_color = 'rgba(255, 0, 0, {})'.format(abs(gender_score))

            if sent_score < 0: # neg
                border_color = 'rgba(255, 0, 0, {})'.format(abs(sent_score))
            else:
                border_color = 'rgba(0, 255, 0, {})'.format(abs(sent_score))

            res += raw_word[:start]
            res += '<span style="background-color: {}; border: 2px solid {}">{}</span>'.format(bg_color, border_color, word)
            res += raw_word[end:] + ' '

        res += '<br>'
    return res

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_data()
    if not data:
        return ''
    data = data.decode()

    res = color_text(data)
    return res

@app.route('/gender/<word>')
def gender_score(word):
    return str(emb_model.gender_score(word))

@app.route('/sent/<word>')
def sent_score(word):
    return str(emb_model.sent_score(word))

if __name__ == '__main__':
    app.run()
