from transformers import pipeline

# Initialize the summarization pipeline.
summarizer = pipeline("summarization")

def summarize_course_package(package, professors):
    """
    Given a course package (a list of course sections for a single course) and professor data,
    this function aggregates all review comments for the relevant course based on its course code
    and uses the summarization pipeline to produce a concise summary.
    
    It no longer cares about class type—only the course code (from 'course_code' or 'SubjectCode').
    """
    # Extract the course code from the first section in the package.
    course_code = package[0].get("course_code") or package[0].get("SubjectCode", "Unknown Course")
    
    # Filter professor data for entries that match this course code.
    relevant_profs = [p for p in professors if p.get("class_name") == course_code]
    
    if relevant_profs:
        # Aggregate all comments from the relevant professors.
        aggregated_comments = " ".join(
            p.get("comment", "") for p in relevant_profs if p.get("comment")
        )
        # Optionally, aggregate ratings (here we just list them).
        aggregated_ratings = ", ".join(
            str(p.get("rating", "N/A")) for p in relevant_profs
        )
        text_to_summarize = (
            f"For course {course_code}, ratings are: {aggregated_ratings}. "
            f"Reviews: {aggregated_comments}"
        )
    else:
        text_to_summarize = f"No professor information available for course {course_code}."
    
    # Generate a summary using the summarization pipeline.
    summary = summarizer(text_to_summarize, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
    return summary

def summarize_schedule(final_schedule, professors):
    """
    Generate summaries for each course package in the final_schedule.
    Returns a dictionary mapping course codes (or SubjectCodes) to their generated summaries.
    """
    summaries = {}
    for pkg in final_schedule:
        # Extract the course code; if missing, use "Unknown Course"
        code = pkg[0].get("course_code") or pkg[0].get("SubjectCode", "Unknown Course")
        summary = summarize_course_package(pkg, professors)
        summaries[code] = summary
    return summaries

if __name__ == "__main__":
    # Example usage for testing the summarizer independently.
    final_schedule = [
        [
            {"course_code": "CS164", "Professor": "Brian L Stuart"},
            {"course_code": "CS164", "Professor": "Brian L Stuart"}
        ],
        [
            {"course_code": "CS171", "Professor": "Daniel W Moix"},
            {"course_code": "CS171", "Professor": "Daniel W Moix"}
        ]
    ]
    
    professors = [
        {
            "name": "Brian L Stuart",
            "rating": 3.5,
            "class_name": "CS164",
            "comment": ("A decent professor, though his lectures can be a bit confusing at times. "
                        "He is very knowledgeable but sometimes uses overly technical language.")
        },
        {
            "name": "Daniel W Moix",
            "rating": 1,
            "class_name": "CS171",
            "comment": ("Honestly one of the biggest regrets I have taking this professor. "
                        "His lectures are literally pointless and a waste of time.")
        }
    ]
    
    summaries = summarize_schedule(final_schedule, professors)
    for course, summary in summaries.items():
        print(f"Course: {course}\nSummary: {summary}\n")
