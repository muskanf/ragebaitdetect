import streamlit as st
import re
from src.transcript import get_transcript
from src.model import train_model, predict_text, test_model

st.title("Ragebait Detector")
st.write("Paste a YouTube link or transcript to estimate how ragebait-like it is.")

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
        "freak", "crazy", "triggered", "hose", "no moral compass",
        "do anything for money"
    ]
}

@st.cache_resource
def load_model():
    return train_model()

@st.cache_data
def load_accuracy():
    return test_model()

model = load_model()
accuracy = load_accuracy()

st.write(f"Naive Bayes test accuracy: {accuracy:.2f}")

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

if st.button("Get Transcript"):
    try:
        transcript_text = get_transcript(youtube_url)
        st.session_state["transcript"] = transcript_text
        st.success("Transcript loaded.")
    except Exception as e:
        st.error(f"Could not load transcript: {e}")

text = st.text_area(
    "Paste transcript here",
    value=st.session_state.get("transcript", ""),
    height=250
)

if st.button("Analyze"):
    if text.strip() == "":
        st.warning("Please paste some text first.")
    else:
        score, flagged_by_category = analyze_text(text)
        prediction, confidence = predict_text(model, text)

        st.subheader(f"Rule-Based Ragebait Score: {score}/100")

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