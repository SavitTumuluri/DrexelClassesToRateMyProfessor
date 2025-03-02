from flask import *
from transcriptParser import parse_transcipts

app = Flask(__name__)

#classes is an array of dictionary (str:str) one dict = one class
classes = [
        {"course_code": "SE201", 
         "ClassTime":"09:00 am - 10:50 am",
         "WeekDay":"TR",
         "Professor":"Preetha Chatterjee",
         "ClassType" : "Lecture"
         },
         {"course_code": "CS281",
          "ClassTime": "03:00 pm - 4:50 pm",
          "WeekDay" :"MW",
          "Professor": "Brian S Mitchell",
          "ClassType": "Lecture"},
          {
          "course_code": "CS281",
          "ClassTime": "09:00 am - 10:50 am",
          "WeekDay" : "F",
          "Professor": "Brian S Mitchell",
          "ClassType": "Lab" 
          },
        {
          "course_code": "CS375",
          "ClassTime": "04:30 pm - 5:50 pm",
          "WeekDay" : "TR",
          "Professor": "Hung N Do",
          "ClassType": "Lecture" 
        },
        {
          "course_code": "CS380",
          "ClassTime": "12:00 pm - 01:20 pm",
          "WeekDay" : "MW",
          "Professor": "Dario D Salvucci",
          "ClassType": "Lecture" 
        }
]

#classes = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get form data
        major = request.form.get('major', '')
        term = request.form.get('term', '')
        credits = request.form.get('credits', '')
        user_transcript = request.form.get('class-history', '')
        
        # Process the transcript data
        result = parse_transcipts(user_transcript)
        
        # Pass the hardcoded classes only for POST requests
        return render_template('index.html', result=result, classes=classes)
    
    # For GET requests, pass an empty list for classes
    return render_template('index.html', result=None, classes=[])




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    home()
