import pandas as pd

def load_data(course_file, review_file):
    """Loads course and professor sentiment data."""
    courses = pd.read_csv(course_file)
    reviews = pd.read_csv(review_file)
    return courses.merge(reviews, on="Professor", how="left")

def generate_schedule(courses, semester, max_credits, workload_preference=None, attendance_preference=None):
    """Generates a schedule prioritizing professor sentiment and rating."""
    
    available_courses = courses[courses["Semester"] == semester]

    if workload_preference:
        available_courses = available_courses[available_courses["Workload"] == workload_preference]

    if attendance_preference is not None:
        available_courses = available_courses[available_courses["Attendance"] == attendance_preference]

    sentiment_map = {"Positive": 2, "Neutral": 1, "Negative": 0}
    available_courses["Sentiment_Score"] = available_courses["Sentiment"].map(sentiment_map).fillna(1)

    available_courses = available_courses.sort_values(by=["Sentiment_Score", "Rating"], ascending=False)

    selected_courses = []
    total_credits = 0

    for _, course in available_courses.iterrows():
        if total_credits + course["Credits"] <= max_credits:
            selected_courses.append(course)
            total_credits += course["Credits"]

    schedule = pd.DataFrame(selected_courses)
    return schedule

if __name__ == "__main__":
    courses = load_data("courses.csv", "processed_reviews.csv")
    schedule = generate_schedule(courses, semester="Fall", max_credits=6, workload_preference="test", attendance_preference=False)
    schedule.to_csv("final_schedule.csv", index=False)
    print("Generated schedule saved to final_schedule.csv")
