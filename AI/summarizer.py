from transformers import pipeline

# Initialize the summarization pipeline.
summarizer = pipeline("summarization")

def summarize_course_package(package, professors):
    """
    Given a course package (a list of course sections for a single course) and professor data,
    this function aggregates all review comments for the relevant professor and uses the summarization
    pipeline to produce a concise summary.
    """
    # Prefer a lecture section; if none, use the first available section.
    main_section = None
    for sec in package:
        if sec.get("ClassType", "").lower() == "lecture":
            main_section = sec
            break
    if not main_section:
        main_section = package[0]
    
    prof_name = main_section.get("Professor", "Unknown Professor")
    # Retrieve professor info from the provided professors list.
    prof = next((p for p in professors if p.get("name") == prof_name), None)
    
    if prof:
        rating = prof.get('rating', 'N/A')
        # If the professor has multiple comments, aggregate them.
        # Expecting 'comments' to be a list; if not, fallback to the single 'comment' field.
        comments = prof.get('comments')
        if comments and isinstance(comments, list):
            aggregated_comments = " ".join(comments)
        else:
            aggregated_comments = prof.get('comment', 'No comment available.')
        
        text_to_summarize = (
            f"Professor {prof_name} teaches this course. "
            f"Rating: {rating}. "
            f"Reviews: {aggregated_comments}"
        )
    else:
        text_to_summarize = "No professor information available for this course package."
    
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
        # Use course_code or fallback to SubjectCode; default to "Unknown Course" if missing.
        code = pkg[0].get("course_code") or pkg[0].get("SubjectCode", "Unknown Course")
        summary = summarize_course_package(pkg, professors)
        summaries[code] = summary
    return summaries

if __name__ == "__main__":
    # Example usage for testing the summarizer independently.
    final_schedule = [
        [
            {"course_code": "CS164", "ClassType": "Lecture", "Professor": "Brian L Stuart"},
            {"course_code": "CS164", "ClassType": "Lab", "Professor": "Brian L Stuart"}
        ],
        [
            {"course_code": "CS171", "ClassType": "Lecture", "Professor": "Daniel W Moix"},
            {"course_code": "CS171", "ClassType": "Lab", "Professor": "Daniel W Moix"}
        ]
    ]
    
    professors = [
        {
            "name": "Brian L Stuart",
            "rating": 3.5,
            "comments": [
                "A decent professor, though his lectures can be a bit confusing at times.",
                "He is very knowledgeable but sometimes uses overly technical language."
            ]
        },
        {
            "name": "Daniel W Moix",
            "rating": 1,
            "comments": [
                "Honestly one of the biggest regrets I have taking this professor.",
                "His lectures are literally pointless and a waste of time."
            ]
        }
    ]
    
    summaries = summarize_schedule(final_schedule, professors)
    for course, summary in summaries.items():
        print(f"Course: {course}\nSummary: {summary}\n")
