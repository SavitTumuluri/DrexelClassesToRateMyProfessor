from transformers import pipeline

# Initialize the summarization pipeline.
summarizer = pipeline("summarization")

def summarize_course_package(package, professors):
    """
    Given a course package (a list of course sections for a single course) and professor data,
    this function aggregates review details from a representative section (preferably a lecture)
    and uses the summarization pipeline to produce a concise summary.
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
        # Build a text block with professor review details.
        text_to_summarize = (
            f"Professor {prof_name} teaches this course. "
            f"Rating: {prof.get('rating', 'N/A')}. "
            f"Review: {prof.get('comment', 'No comment available.')}"
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
    # Sample final_schedule: a list of course packages where each package is a list of sections.
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
    
    # Sample professor data.
    professors = [
        {
            "name": "Brian L Stuart",
            "rating": 3.5,
            "comment": "A decent professor, though his lectures can be a bit confusing at times."
        },
        {
            "name": "Daniel W Moix",
            "rating": 1,
            "comment": "Honestly one of the biggest regrets I have taking this professor. His lectures are literally pointless and a waste of time."
        }
    ]
    
    # Generate and print summaries.
    summaries = summarize_schedule(final_schedule, professors)
    for course, summary in summaries.items():
        print(f"Course: {course}\nSummary: {summary}\n")
