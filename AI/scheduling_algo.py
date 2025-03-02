import datetime

def check_prerequisites(course_prereqs, completed_courses):
    """
    Validate course prerequisites.
    course_prereqs is expected to be a nested list structure such as:
      [ ["CS260"], [["CS281", "ECEC355"]] ]
    where the first list requires CS260 and the second list means at least one of CS281 or ECEC355 must be completed.
    """
    for group in course_prereqs:
        # If the first element is a list, then treat it as alternatives (OR condition)
        if isinstance(group[0], list):
            if not any(req in completed_courses for req in group[0]):
                return False
        else:
            if not all(req in completed_courses for req in group):
                return False
    return True

def calculate_score(professor_rating, professor_tags, user_tags):
    """
    Compute score as the sum of the professor's overall rating and the count of matching tags.
    """
    match_count = sum(1 for tag in professor_tags if tag in user_tags)
    return professor_rating + match_count

def parse_time(time_str):
    """Parse a time string like '09:00 am' into a datetime.time object."""
    return datetime.datetime.strptime(time_str, "%I:%M %p").time()

def time_to_minutes(t):
    """Convert a time object into minutes since midnight."""
    return t.hour * 60 + t.minute

def parse_time_slot(slot_str):
    """
    Parse a time slot string (e.g., "09:00 am - 10:50 am") and return a tuple of start and end times in minutes.
    """
    parts = slot_str.split("-")
    start_str = parts[0].strip()
    end_str = parts[1].strip()
    start_time = parse_time(start_str)
    end_time = parse_time(end_str)
    return (time_to_minutes(start_time), time_to_minutes(end_time))

def sections_conflict(sec1, sec2):
    """
    Check if two sections conflict.
    They must be on the same weekday and their time ranges must overlap.
    """
    if sec1.get('WeekDay') != sec2.get('WeekDay'):
        return False
    start1, end1 = parse_time_slot(sec1['ClassTime'])
    start2, end2 = parse_time_slot(sec2['ClassTime'])
    return max(start1, start2) < min(end1, end2)

def group_course_packages(courses):
    """
    Group course sections by their course code.
    We assume each course dict contains either 'course_code' or 'SubjectCode'.
    Sections that share the same code (and thus represent lectures, labs, recitations) will be combined.
    """
    packages = {}
    for course in courses:
        code = course.get('course_code') or course.get('SubjectCode')
        if not code:
            continue
        if code not in packages:
            packages[code] = []
        packages[code].append(course)
    return packages

def package_score(package, professors, user_tags):
    """
    Calculate the overall score for a package.
    Prefer the lecture section (if available) to determine the professor's rating.
    """
    main_section = None
    for sec in package:
        # Assume the main lecture is marked as 'Lecture' (case-insensitive)
        if sec.get('ClassType', '').lower() == 'lecture':
            main_section = sec
            break
    if not main_section:
        main_section = package[0]
    prof_name = main_section.get('Professor')
    # Find the matching professor
    prof = next((p for p in professors if p.get('name') == prof_name), None)
    if not prof:
        # If professor info is missing, return a default score of 0
        return 0
    return calculate_score(prof.get('overallRating', 0), prof.get('tags', []), user_tags)

def package_conflicts(pkg, scheduled_packages):
    """
    Check if any section in pkg conflicts with any section in any already scheduled package.
    """
    for sec in pkg:
        for scheduled_pkg in scheduled_packages:
            for scheduled_sec in scheduled_pkg:
                if sections_conflict(sec, scheduled_sec):
                    return True
    return False

def schedule_courses(courses, professors, user_tags, completed_courses):
    """
    Build a final schedule by:
      1. Filtering out courses already completed or that fail prerequisites.
      2. Grouping sections into course packages (which automatically considers attached labs/recitations).
      3. Sorting packages by score (higher score is prioritized).
      4. Adding packages one by one if none of their sections conflict with already scheduled packages.
    """
    # Filter courses based on completed courses and prerequisites
    filtered = []
    for course in courses:
        code = course.get('course_code') or course.get('SubjectCode')
        if code in completed_courses:
            continue
        if 'prerequisite' in course and course['prerequisite']:
            # Expecting prerequisite to be in the nested list format, e.g., [["CS260"], [["CS281", "ECEC355"]]]
            if not check_prerequisites(course['prerequisite'], completed_courses):
                continue
        filtered.append(course)
    
    # Group courses into packages by course code
    packages_dict = group_course_packages(filtered)
    packages = list(packages_dict.values())
    
    # Sort packages by their calculated score (using the main lecture's professor if available)
    packages.sort(key=lambda pkg: package_score(pkg, professors, user_tags), reverse=True)
    
    final_schedule = []
    for pkg in packages:
        if not package_conflicts(pkg, final_schedule):
            final_schedule.append(pkg)
    return final_schedule

# Example usage:
if __name__ == "__main__":
    # Sample completed courses and user tag preferences
    completed_courses = ["CS260", "CS150"]
    user_tags = ["fun", "clear", "organized"]
    
    # Sample course sections (each dict represents a section)
    courses = [
        # CS150 has a lab and a lecture. Since CS150 is already completed (per completed_courses), it will be filtered out.
        {"course_code": "CS150", "ClassTime": "09:00 am - 10:50 am", "WeekDay": "F", "Professor": "Daniel W Moix", "ClassType": "Lab"},
        {"course_code": "CS150", "ClassTime": "11:00 am - 12:50 pm", "WeekDay": "T", "Professor": "Daniel W Moix", "ClassType": "Lecture"},
        
        # CS164 has a prerequisite that is a nested list structure
        {"course_code": "CS164", "ClassTime": "01:00 pm - 02:50 pm", "WeekDay": "W", "Professor": "Brian L Stuart", "ClassType": "Lab", 
         "prerequisite": [["CS260"], [["CS281", "ECEC355"]]]},
        {"course_code": "CS164", "ClassTime": "09:00 am - 10:50 am", "WeekDay": "M", "Professor": "Brian L Stuart", "ClassType": "Lecture",
         "prerequisite": [["CS260"], [["CS281", "ECEC355"]]]},
        
        # CS171 has a lab and a lecture; assume no prerequisites here.
        {"course_code": "CS171", "ClassTime": "09:00 am - 10:50 am", "WeekDay": "W", "Professor": "Daniel W Moix", "ClassType": "Lab"},
        {"course_code": "CS171", "ClassTime": "09:00 am - 10:50 am", "WeekDay": "T", "Professor": "Daniel W Moix", "ClassType": "Lecture"}
    ]
    
    # Sample professor data with overall rating and tags
    professors = [
        {"name": "Daniel W Moix", "overallRating": 4.0, "tags": ["organized", "fun"]},
        {"name": "Brian L Stuart", "overallRating": 3.5, "tags": ["clear", "challenging"]}
    ]
    
    final_schedule = schedule_courses(courses, professors, user_tags, completed_courses)
    
    # Print the final schedule.
    print("Final Schedule:")
    for pkg in final_schedule:
        course_code = pkg[0].get('course_code') or pkg[0].get('SubjectCode')
        score = package_score(pkg, professors, user_tags)
        print(f"\nCourse: {course_code} (Score: {score})")
        for sec in pkg:
            print(f"  Type: {sec.get('ClassType')}, Day: {sec.get('WeekDay')}, Time: {sec.get('ClassTime')}, Professor: {sec.get('Professor')}")
