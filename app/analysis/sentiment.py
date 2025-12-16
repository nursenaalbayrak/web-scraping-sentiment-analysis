import re

positive_words = [
    "good", "great", "excellent", "happy", "love", "amazing",
    "wonderful", "best", "beauty", "genius", "miracle"
]

negative_words = [
    "bad", "worst", "sad", "hate", "terrible", "boring",
    "stupid", "ugly", "awful"
]

def analyze_sentiment(text):
    text = text.lower()

    pos_count = sum(word in text for word in positive_words)
    neg_count = sum(word in text for word in negative_words)

    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral"
    
def split_into_sentences(text):
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    return sentences

def sentiment_to_score(sentiment):
    if sentiment == "Positive":
        return 1
    elif sentiment == "Negative":
        return -1
    else:
        return 0 

if __name__ == "__main__":
    sample_text = "Life is beautiful and wonderful"
    print(analyze_sentiment(sample_text))