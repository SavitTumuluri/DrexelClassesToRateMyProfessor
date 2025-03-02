from flask import *
from transcriptParser import parse_transcipts

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    
    if request.method == 'POST':
        user_transcript = request.form['class-history']
        result = parse_transcipts(user_transcript)

    return render_template('index.html', result = result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)