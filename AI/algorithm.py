from collections import defaultdict

def convert_datetime_format(datetime_str):
    """
    Converts a datetime string format (e.g., "F 09:00 am - 10:50 am") into days list and tuple of float time values.
    """
    day_mapping = {'M': "Monday", 'T': "Tuesday", 'W': "Wednesday", 'R': "Thursday", 'F': "Friday"}
    
    parts = datetime_str.split(' ')
    days = [day_mapping[char] for char in parts[0] if char in day_mapping]
    time_str = ' '.join(parts[1:])
    
    def time_to_float(t):
        hour, minute = map(int, t[:-3].split(':'))
        if 'pm' in t.lower() and hour != 12:
            hour += 12
        elif 'am' in t.lower() and hour == 12:
            hour = 0
        return hour + minute / 60
    
    start, end = time_str.split(' - ')
    return days, (time_to_float(start), time_to_float(end))

def optimize_schedule(classes, max_credits=20):
    """
    Optimizes the schedule by selecting the highest-rated classes while resolving conflicts and considering credit limits.
    
    :param classes: List of dictionaries with class details {"name": str, "rating": int, "datetime": str, "credits": int}
    :param max_credits: Maximum allowed credits for the schedule
    :return: List of scheduled classes without conflicts
    """
    # Sort classes by rating in descending order
    classes.sort(key=lambda x: x['rating'], reverse=True)
    
    scheduled_classes = []
    occupied_times = []
    total_credits = 0
    
    for cls in classes:
        days, (start, end) = convert_datetime_format(cls['datetime'])
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

# Example usage:
classes = [
    {"name": "CS270", "rating": 9, "datetime": "MW 11:00 am - 1:00 pm", "credits": 4},
    {"name": "CS260", "rating": 9, "datetime": "MW 10:00 am - 12:00 pm", "credits": 4},
    {"name": "MATH241", "rating": 8, "datetime": "MW 11:00 am - 1:00 pm", "credits": 4},
    {"name": "PHYS211", "rating": 7, "datetime": "TR 9:00 am - 10:00 am", "credits": 3},
    {"name": "STAT400", "rating": 6, "datetime": "TR 2:00 pm - 4:00 pm", "credits": 3},
    {"name": "ECE110", "rating": 7, "datetime": "MW 10:00 am - 11:00 am", "credits": 3},
]

optimized_schedule = optimize_schedule(classes)
for cls in optimized_schedule:
    print(f"Scheduled: {cls['name']} on {', '.join(cls['days'])} from {cls['time'][0]:.2f} to {cls['time'][1]:.2f} with rating {cls['rating']} ({cls['credits']} credits)")
