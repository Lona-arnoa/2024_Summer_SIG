from flask import Flask, render_template, request, send_file
from Hannanum_WordCloud_Flask import make_wordcloud
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html', result=request.args.get('result'))



@app.route('/sum', methods=['GET'])
def display_wordcloud():
    a = request.args.get('search-input')
    make_wordcloud(a)
    return render_template('result.html')


if __name__ == '__main__':
    app.debug = True
    app.run()