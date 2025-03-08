from autogen import AssistantAgent, UserProxyAgent

# Load LLM configuration (e.g., OpenAI API key)
config_list = [
    {
        "model": "llama3.2",  # or other models like "mistral" or "gemma"
        "base_url": "http://localhost:11434/v1",
        "api_type": "ollama"
    }
]

# Define the Scheduler Agent
assistant = AssistantAgent(
    name="assistant",
    llm_config={
        "config_list": config_list,
        "temperature": 0,  # Ensure deterministic behavior
    },
    system_message="You are a course scheduler. Your task is to generate a course schedule based on the provided data and algorithm. Use the algorithm idea to filter courses, check prerequisites, calculate scores, and avoid conflicts. Return the final schedule in a structured format."
)

# Define the User Proxy Agent (to interact with the scheduler)
user_proxy = UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",  # Automate the interaction
    code_execution_config={"work_dir": "scheduling", "use_docker": False},
)

# Define the algorithm and data as a string
algorithm_and_data = """
# Algorithm (Python code)
import datetime

def check_prerequisites(course_prereqs, completed_courses):
    #Validate course prerequisites.
    #course_prereqs is expected to be a nested list structure such as:
    #  [ ["CS260"], [["CS281", "ECEC355"]] ]
    #where the first list requires CS260 and the second list means at least one of CS281 or ECEC355 must be completed.
    for group in course_prereqs:
        # If the first element is a list, then treat it as alternatives (OR condition)
        if isinstance(group[0], list):
            if not any(req in completed_courses for req in group[0]):
                return False
        else:
            if not all(req in completed_courses for req in group):
                return False
    return True

def calculate_score(professor_rating, comment, user_tags):
    #Compute score as the sum of the professor's rating and the number of user-supplied keywords
    #found in the professor's comment (case-insensitive).
    match_count = sum(1 for tag in user_tags if tag.lower() in comment.lower())
    return professor_rating + match_count

def parse_time(time_str):
    #Parse a time string like '09:00 am' into a datetime.time object.
    return datetime.datetime.strptime(time_str, "%I:%M %p").time()

def time_to_minutes(t):
    #Convert a time object into minutes since midnight.#
    return t.hour * 60 + t.minute

def parse_time_slot(slot_str):
    #Parse a time slot string (e.g., "09:00 am - 10:50 am") and return a tuple of start and end times in minutes.
    
    parts = slot_str.split("-")
    start_str = parts[0].strip()
    end_str = parts[1].strip()
    start_time = parse_time(start_str)
    end_time = parse_time(end_str)
    return (time_to_minutes(start_time), time_to_minutes(end_time))

def sections_conflict(sec1, sec2):
    #Check if two sections conflict.
    #They must be on the same weekday and their time ranges must overlap.
    
    if sec1.get('WeekDay') != sec2.get('WeekDay'):
        return False
    start1, end1 = parse_time_slot(sec1['ClassTime'])
    start2, end2 = parse_time_slot(sec2['ClassTime'])
    return max(start1, start2) < min(end1, end2)

def group_course_packages(courses):
    #Group course sections by their course code.
    #Sections that share the same code (and thus represent lectures, labs, recitations) will be combined.
    
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
    #Calculate the overall score for a package.
    #We prefer to use the lecture section (if available) to determine the professor's rating and comment.

    main_section = None
    for sec in package:
        if sec.get('ClassType', '').lower() == 'lecture':
            main_section = sec
            break
    if not main_section:
        main_section = package[0]
    prof_name = main_section.get('Professor')
    prof = next((p for p in professors if p.get('name') == prof_name), None)
    if not prof:
        return 0
    return calculate_score(prof.get('rating', 0), prof.get('comment', ""), user_tags)

def package_conflicts(pkg, scheduled_packages):
    #Check if any section in pkg conflicts with any section in any already scheduled package.
    for sec in pkg:
        for scheduled_pkg in scheduled_packages:
            for scheduled_sec in scheduled_pkg:
                if sections_conflict(sec, scheduled_sec):
                    return True
    return False

def schedule_courses(courses, professors, user_tags, completed_courses):
    #Build a final schedule by:
      #1. Filtering out courses that are already completed or that fail prerequisites.
      #2. Grouping sections into course packages (automatically considering attached labs/recitations).
      #3. Sorting packages by score (higher score is prioritized).
      #4. Adding packages one by one if none of their sections conflict with already scheduled packages.
    # 1. Filter courses based on completed courses and prerequisites
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
    
    # 2. Group courses into packages by course code
    packages_dict = group_course_packages(filtered)
    packages = list(packages_dict.values())
    
    # 3. Sort packages by their calculated score (using the main lecture's professor review)
    packages.sort(key=lambda pkg: package_score(pkg, professors, user_tags), reverse=True)
    
    # 4. Add packages to the final schedule if they do not conflict with already scheduled sections
    final_schedule = []
    for pkg in packages:
        if not package_conflicts(pkg, final_schedule):
            final_schedule.append(pkg)
    return final_schedule

# Example usage:
if __name__ == "__main__":
    # Sample completed courses and user tag preferences (keywords to match in professor comments)
    completed_courses = ["CS260", "CS150"]
    user_tags = ["pointless", "waste", "confused"]
    
    # Sample course sections (each dict represents a section)
    courses = [
        # CS150 has a lab and a lecture. Since CS150 is already completed, these will be filtered out.
        {"course_code": "CS150", "ClassTime": "09:00 am - 10:50 am", "WeekDay": "F", "Professor": "Daniel W Moix", "ClassType": "Lab"},
        {"course_code": "CS150", "ClassTime": "11:00 am - 12:50 pm", "WeekDay": "T", "Professor": "Daniel W Moix", "ClassType": "Lecture"},
        
        # CS164 has a prerequisite that is a nested list structure.
        {"course_code": "CS164", "ClassTime": "01:00 pm - 02:50 pm", "WeekDay": "W", "Professor": "Brian L Stuart", "ClassType": "Lab", 
         "prerequisite": [["CS260"], [["CS281", "ECEC355"]]]},
        {"course_code": "CS164", "ClassTime": "09:00 am - 10:50 am", "WeekDay": "M", "Professor": "Brian L Stuart", "ClassType": "Lecture",
         "prerequisite": [["CS260"], [["CS281", "ECEC355"]]]},
        
        # CS171 has a lab and a lecture; assume no prerequisites here.
        {"course_code": "CS171", "ClassTime": "09:00 am - 10:50 am", "WeekDay": "W", "Professor": "Daniel W Moix", "ClassType": "Lab"},
        {"course_code": "CS171", "ClassTime": "09:00 am - 10:50 am", "WeekDay": "T", "Professor": "Daniel W Moix", "ClassType": "Lecture"}
    ]
    
    # Sample professor data updated to use the API format (only rating, difficulty, comment, and class_name available)
    professors = [
        {
            "name": "Daniel W Moix", 
            "rating": 1, 
            "difficulty": 5, 
            "comment": "Honestly one of the biggest regrets I have taking this professor. His lectures are literally pointless and a waste of time. The HWs are extremely long and barely correlates to the lectures and he literally takes points off for fun. He is aggressive towards students that ask for help. He doesn't submit grades on time so students are always confused.", 
            "class_name": "CS260"
        },
        {
            "name": "Brian L Stuart", 
            "rating": 3.5, 
            "difficulty": 3.7, 
            "comment": "A decent professor, though his lectures can be a bit confusing at times.", 
            "class_name": "CS164"
        }
    ]
    
    final_schedule = schedule_courses(courses, professors, user_tags, completed_courses)
    
    print("Final Schedule:")
    for pkg in final_schedule:
        code = pkg[0].get('course_code') or pkg[0].get('SubjectCode')
        score = package_score(pkg, professors, user_tags)
        print(f"\nCourse: {code} (Score: {score})")
        for sec in pkg:
            print(f"  Type: {sec.get('ClassType')}, Day: {sec.get('WeekDay')}, Time: {sec.get('ClassTime')}, Professor: {sec.get('Professor')}")

user_tags = ["easygrader", "helpful"]
completed_courses = ["CS 164", "CS 171", "CS 172", "SE 210", "CS 265", "CS 260"]
"""

# Define the task for the scheduler agent
task = """
Using the provided algorithm and data, generate a course schedule. Follow these steps:
1. Filter courses based on completed courses and prerequisites.
2. Group sections into course packages.
3. Sort packages by score.
4. Add packages to the schedule if they do not conflict with already scheduled sections.
5. Return the final schedule in a structured format.
"""

# Combine the algorithm, data, and task into a single prompt
prompt = f"{algorithm_and_data}\n\n{task}"

user_proxy.initiate_chat(
    assistant,
    message=prompt,
)

print("\n=== FINAL SCHEDULE RESULTS ===")
print(user_proxy.last_message()["content"])