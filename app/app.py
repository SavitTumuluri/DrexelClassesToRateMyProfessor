from flask import *
from transcriptParser import parse_transcipts

app = Flask(__name__)

#classes is an array of dictionary (str:str) one dict = one class
""" classes = [{"course_code": "CS150", 
           "ClassTime": "09:00 am - 10:50 am", 
           "WeekDay": "F",
           "Professor": "Daniel W Moix", 
           "ClassType": "Lab"}, 
    {
        "course_code": "MATH101",
        "ClassTime": "11:00 am - 12:30 pm",
        "WeekDay": "M/W/F",
        "Professor": "Dr. John Doe",
        "ClassType": "Lecture"
    }] """

classes = []

@app.route('/', methods=['GET', 'POST'])

def home():
    result = None
    
    if request.method == 'POST':
        user_transcript = request.form['class-history']
        result = parse_transcipts(user_transcript)
    
    return render_template('index.html', result = result, classes=classes)




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    home()
