import streamlit as st
import re
from src.transcript import get_transcript
from src.model import train_model, predict_text, test_model

st.title("Ragebait Detector")
st.write("Hello! Paste a YouTube link or transcript to see how ragebait-like it is.")
st.write("Disclaimer: This is a simple tool for educational purposes and may not be 100% accurate. Use it as a guide and not a definitive judgment.")
st.write("This tool does not represent any political stance and is designed to analyze content based on language patterns, not ideology.")
#tried to make a broad category of as many ragebait phrases as possible 
#to cover a wide range of ragebait content and make the rule-based scoring more effective
RAGE_CATEGORIES = {
    "Anger": [
        "corrupt", "disgusting", "evil", "betrayed", "insane",
        "pathetic", "horrible", "pissed off", "grotesque",
        "depraved", "vulgar", "infuriating", "awful"
    ],
    "Fear": [
        "dangerous", "threat", "crisis", "destroying", "collapse",
        "under attack", "too late", "dark"
    ],
    "Conspiracy": [
        "they don't want you to know", "wake up", "the truth",
        "exposed", "cover up", "hiding the truth"
    ],
    "Us vs Them": [
        "elites", "sheep", "brainwashed", "people like you",
        "these people", "the left", "own the libs"
    ],
    "Exaggeration": [
        "shocking", "unbelievable", "this changes everything",
        "you won't believe", "losing their minds", "everybody is falling for",
        "most controversial", "step too far"
    ],
    "Insults or Dehumanizing Language": [
        "freak", "crazy", "triggered", "stupid", "no moral compass",
        "do anything for money"
    ]
}

@st.cache_resource
def load_model():
    return train_model()

@st.cache_data
def load_accuracy():
    return test_model()
#load the trained model and the accuracy score to display on the app and use for predictions
model = load_model()
accuracy = load_accuracy()

st.write(f"Naive Bayes test accuracy: {accuracy:.2f}")
#analyze the text to get rage bait score and the flagged categories and phrases to display on the app
def analyze_text(text):
    text_lower = text.lower()
    flagged_by_category = {}
    total_matches = 0

    for category, words in RAGE_CATEGORIES.items():
        matches = []

        for word in words:
            if word in text_lower:
                matches.append(word)

        if matches:
            flagged_by_category[category] = matches
            total_matches += len(matches)

    word_count = max(len(re.findall(r"\w+", text_lower)), 1)
    score = min(100, int(total_matches * 12))

    return score, flagged_by_category

youtube_url = st.text_input("Paste a YouTube link")
#upload the transcript from the YouTube URL and store it in session state to display in the text area for analysis
if st.button("Get Transcript"):
    try:
        transcript_text = get_transcript(youtube_url)
        st.session_state["transcript"] = transcript_text
        st.success("Transcript loaded.")
    except Exception as e:
        st.error(f"Encountered an error: {e}", icon="🚨")

text = st.text_area(
    "Paste transcript here",
    value=st.session_state.get("transcript", ""),
    height=250
)
#analyze the text when the button is clicked
if st.button("Analyze"):
    if text.strip() == "":
        st.warning("Please paste some text first.")
    else:
        score, flagged_by_category = analyze_text(text)
        prediction, confidence = predict_text(model, text)

        st.subheader(f"Rule-Based Ragebait Score: {score}/100")
#score ranges - we thought this is fine but this can be adjusted to maybe 50 or more
        if score >= 70:
            st.error("High ragebait likelihood")
        elif score >= 35:
            st.warning("Medium ragebait likelihood")
        else:
            st.success("Low ragebait likelihood")

        st.write("Flagged categories and phrases:")

        if flagged_by_category:
            for category, matches in flagged_by_category.items():
                st.write(f"**{category}:** {', '.join(matches)}")
        else:
            st.write("No major ragebait phrases found.")

        st.subheader("Naive Bayes Prediction")
        st.write(f"Prediction: **{prediction}**")

        ragebait_confidence = confidence.get("ragebait", 0)
        normal_confidence = confidence.get("normal", 0)

        st.write(f"Ragebait confidence: {ragebait_confidence:.2f}")
        st.write(f"Normal confidence: {normal_confidence:.2f}")