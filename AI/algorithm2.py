from collections import defaultdict
from pymongo import MongoClient

def convert_datetime_format(datetime_str):
    """
    Converts a datetime string format (e.g., "F 09:00 am - 10:50 am") into days list and tuple of float time values.
    """
    day_mapping = {'M': "Monday", 'T': "Tuesday", 'W': "Wednesday", 'R': "Thursday", 'F': "Friday"}
    
    parts = datetime_str.split(' ', 1)
    if len(parts) < 2:
        return [], (0, 0)  # Handle cases where time is missing
    
    days = [day_mapping[char] for char in parts[0] if char in day_mapping]
    time_str = parts[1]
    
    def time_to_float(t):
        hour, minute = map(int, t[:-3].split(':'))
        if 'pm' in t.lower() and hour != 12:
            hour += 12
        elif 'am' in t.lower() and hour == 12:
            hour = 0
        return hour + minute / 60
    
    time_parts = time_str.split(' - ')
    if len(time_parts) < 2:
        return days, (0, 0)  # Handle cases where time format is incorrect
    
    start, end = time_parts
    return days, (time_to_float(start), time_to_float(end))

def fetch_classes_from_db():
    """
    Fetches class data from the MongoDB database and formats it for scheduling.
    """
    client = MongoClient("mongodb+srv://suewulin12:Izlfl0VFsWfPotJQ@ratemyprof.oqxbh.mongodb.net/?retryWrites=true&w=majority&appName=RateMyProf")  # Adjust connection as needed
    db = client["test"]
    classes_collection = db["classes"]
    courses_collection = db["courses"]
    ratings_collection = db["ratings"]
    professors_collection = db["professors"]
    
    # Get class ratings
    ratings_dict = {}
    for rating in ratings_collection.find():
        class_name = rating.get("class_name", "")
        if class_name:
            ratings_dict.setdefault(class_name, []).append(rating.get("rating", 5))
    
    average_ratings = {key: sum(values) / len(values) for key, values in ratings_dict.items()}
    
    # Get professor ratings
    professor_ratings = {prof.get("name", ""): prof.get("overallRating", 3) for prof in professors_collection.find()}
    
    # Get course credit hours
    course_credits = {course.get("abbreviation", ""): float(course.get("creditHours", 3)) for course in courses_collection.find()}
    
    formatted_classes = []
    seen_courses = set()
    
    for cls in classes_collection.find():
        subject_code = cls.get("SubjectCode", "").replace(" ", "")
        name = cls.get("Name", "Unknown")
        if subject_code in seen_courses:
            continue  # Skip duplicate courses
        seen_courses.add(subject_code)
        
        weekday = cls.get("WeekDay", "")
        class_time = cls.get("ClassTime", "")
        datetime_str = f"{weekday} {class_time}".strip()
        professor = cls.get("Professor", "")
        
        rating = average_ratings.get(name, 5)
        prof_rating = professor_ratings.get(professor, 3)
        credits = course_credits.get(subject_code, 3)
        final_rating = (rating + prof_rating) / 2
        
        formatted_classes.append({
            "name": name,
            "rating": final_rating,
            "datetime": datetime_str,
            "credits": credits
        })
    
    return formatted_classes

def optimize_schedule(classes, max_credits=20):
    """
    Optimizes the schedule by selecting the highest-rated classes while resolving conflicts and considering credit limits.
    """
    classes.sort(key=lambda x: x['rating'], reverse=True)
    scheduled_classes = []
    occupied_times = []
    total_credits = 0
    
    for cls in classes:
        days, (start, end) = convert_datetime_format(cls['datetime'])
        if not days or (start == 0 and end == 0):  # Skip invalid data
            continue
        
        conflict = False
        for scheduled_cls in scheduled_classes:
            scheduled_days = scheduled_cls['days']
            scheduled_start, scheduled_end = scheduled_cls['time']
            if any(day in scheduled_days for day in days) and not (end <= scheduled_start or start >= scheduled_end):
                conflict = True
                break
        
        if not conflict and total_credits + cls['credits'] <= max_credits:
            scheduled_classes.append({"name": cls['name'], "days": days, "time": (start, end), "rating": cls['rating'], "credits": cls['credits']})
            occupied_times.append((days, start, end))
            total_credits += cls['credits']
    
    return scheduled_classes

# Fetch classes from MongoDB
db_classes = fetch_classes_from_db()

# Optimize schedule
optimized_schedule = optimize_schedule(db_classes)
for cls in optimized_schedule:
    print(f"Scheduled: {cls['name']} on {', '.join(cls['days'])} from {cls['time'][0]:.2f} to {cls['time'][1]:.2f} with rating {cls['rating']} ({cls['credits']} credits)")
