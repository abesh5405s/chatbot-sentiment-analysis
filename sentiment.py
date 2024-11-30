from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import nltk

# Ensure necessary data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

app = Flask(__name__)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity, subjectivity = analysis.sentiment.polarity, analysis.sentiment.subjectivity
    sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
    return sentiment, polarity, subjectivity

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['GET','POST'])
def analyze():
    if request.method == 'POST':
        data = request.json
        user_input = data.get("text", "")
        if not user_input.strip():
            return jsonify({"error": "Empty text provided."}), 400
        
        sentiment, polarity, subjectivity = analyze_sentiment(user_input)
        response = {
            "sentiment": sentiment,
            "polarity": round(polarity, 2),
            "subjectivity": round(subjectivity, 2)
        }
        return jsonify(response)
    return jsonify({"error": "Invalid request method."}), 405

if __name__ == '__main__':
    app.run(debug=True)