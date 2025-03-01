import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(review):
    """Returns sentiment label based on the review text."""
    sentiment_score = sia.polarity_scores(review)['compound']
    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def process_reviews(input_file, output_file):
    """Reads professor reviews, assigns sentiment labels, and saves results."""
    reviews = pd.read_csv(input_file)
    reviews["Sentiment"] = reviews["Review"].apply(analyze_sentiment)
    reviews.to_csv(output_file, index=False)
    print(f"Sentiment analysis completed. Results saved to {output_file}")

if __name__ == "__main__":
    process_reviews("professor_reviews.csv", "processed_reviews.csv")
