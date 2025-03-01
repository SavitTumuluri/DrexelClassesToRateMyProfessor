from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_with_bart(descriptions):
    text = " ".join(descriptions)
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

descriptions = [
    "This professor flirts with 20 year old girls at the age of 45",
    "Kurt is a really bad professor",
    "Looks like a discord mod that doesn't shower",
    "Terrible teacher. Doesn't even care about teaching and even says he doesn't get paid enough"
]

summary = summarize_with_bart(descriptions)
print("Summary:", summary)
