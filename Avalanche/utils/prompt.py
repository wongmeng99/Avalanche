

# GenAI function for Sentiment analysis
def build_sentiment_prompt(summary, score):
    return f"""
You are a sentiment analysis expert. Given the following customer review and its precomputed sentiment score, classify the sentiment as Positive, Neutral, or Negative.

Review Summary: "{summary}"
Sentiment Score: {score}

Respond with only one word: Positive, Neutral, or Negative.
"""