from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load a pre-trained sentiment analysis pipeline.
# (This will download the model on first run.)
sentiment_analyzer = pipeline("sentiment-analysis")

def interpret_dream(dream_text):
    """
    Analyze the dream text with sentiment analysis and provide a simple interpretation.
    """
    # Run sentiment analysis on the dream description.
    result = sentiment_analyzer(dream_text)[0]
    label = result['label']
    score = result['score']
    
    interpretation = ""
    # Interpret based on sentiment.
    if label == "POSITIVE":
        interpretation += "Your dream carries a positive, uplifting message. "
    elif label == "NEGATIVE":
        interpretation += "Your dream may be reflecting inner struggles or challenges. "
    else:
        interpretation += "Your dream has a balanced tone. "

    # Additional dream symbolism heuristics.
    text_lower = dream_text.lower()
    if "flying" in text_lower:
        interpretation += "Flying dreams often symbolize freedom and ambition. "
    elif "falling" in text_lower:
        interpretation += "Falling dreams might indicate feelings of insecurity or a loss of control. "
    elif "water" in text_lower:
        interpretation += "Dreams involving water can represent emotions or the subconscious mind. "
    else:
        interpretation += "Consider how the elements of your dream relate to your current life circumstances. "

    interpretation += f"(Sentiment: {label} with confidence {score:.2f})"
    return interpretation

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dream_text = request.form.get("dream_text")
        if not dream_text:
            error_msg = "Please enter your dream description."
            return render_template("index.html", error=error_msg)
        interpretation = interpret_dream(dream_text)
        return render_template("result.html", dream_text=dream_text, interpretation=interpretation)
    return render_template("index.html")

if __name__ == "__main__":
    # Run in debug mode for development
    app.run(debug=True)
