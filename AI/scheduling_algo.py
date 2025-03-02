def check_prerequisites(course_prereqs, completed_courses):
    """
    Validate course prerequisites.
    course_prereqs can be a nested list like:
      [ ["CS260"], [["CS281", "ECEC355"]] ]
    """
    for group in course_prereqs:
        # Check if group is a list of alternatives (OR condition)
        if isinstance(group[0], list):
            # For nested alternatives, ensure at least one is completed.
            if not any(req in completed_courses for req in group[0]):
                return False
        else:
            # For a simple list, all must be completed.
            if not all(req in completed_courses for req in group):
                return False
    return True

def calculate_score(professor_rating, professor_tags, user_tags):
    # Count the number of matching tags
    match_count = sum(1 for tag in professor_tags if tag in user_tags)
    return professor_rating + match_count

def filter_courses(courses, completed_courses):
    # Remove courses that are already completed
    return [course for course in courses if course['course_code'] not in completed_courses]

def schedule_courses(courses, professors, user_tags, completed_courses):
    # Filter courses based on completed courses and prerequisites
    available_courses = []
    for course in courses:
        if course['course_code'] in completed_courses:
            continue
        # Assume course['prerequisite'] is parsed into a nested list structure
        if 'prerequisite' in course:
            # e.g., course['prerequisite'] might be something like: [["CS260"], [["CS281", "ECEC355"]]]
            if not check_prerequisites(course['prerequisite'], completed_courses):
                continue
        available_courses.append(course)

    # Resolve scheduling conflicts: for simplicity, group by time slot
    schedule = {}
    for course in available_courses:
        time_slot = course['ClassTime']
        prof = next((p for p in professors if p['name'] == course['Professor']), None)
        if not prof:
            continue  # or handle missing professor info

        score = calculate_score(prof['overallRating'], prof.get('tags', []), user_tags)
        # If time_slot already has a course, choose the one with the higher score
        if time_slot in schedule:
            existing = schedule[time_slot]
            existing_score = calculate_score(existing['professor']['overallRating'],
                                             existing['professor'].get('tags', []),
                                             user_tags)
            if score > existing_score:
                schedule[time_slot] = {'course': course, 'professor': prof, 'score': score}
        else:
            schedule[time_slot] = {'course': course, 'professor': prof, 'score': score}

    # Optionally, perform a topological sort on the schedule based on prerequisite dependencies

    return schedule

# Example usage:
completed_courses = ["CS260", "CS150"]  # from class history
user_tags = ["fun", "clear", "organized"]  # user input for professor/course tags
courses = [...]  # list of course objects
professors = [...]  # list of professor objects

final_schedule = schedule_courses(courses, professors, user_tags, completed_courses)
