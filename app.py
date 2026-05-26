import streamlit as st
import re

RAGE_WORDS = [
    "exposed", "corrupt", "disgusting", "shocking", "destroying",
    "betrayed", "evil", "insane", "dangerous", "threat",
    "they don't want you to know", "wake up", "the truth",
    "sheep", "brainwashed", "outrage", "crisis"
]

def analyze_text(text):
    text_lower = text.lower()
    flagged = []

    for word in RAGE_WORDS:
        if word in text_lower:
            flagged.append(word)

    word_count = max(len(re.findall(r"\w+", text_lower)), 1)
    score = min(100, int((len(flagged) / word_count) * 1000))

    return score, flagged

st.title("Ragebait Detector")
st.write("Paste a transcript or online content text to estimate how ragebait-like it is.")

text = st.text_area("Paste transcript here", height=250)

if st.button("Analyze"):
    if text.strip() == "":
        st.warning("Please paste some text first.")
    else:
        score, flagged = analyze_text(text)

        st.subheader(f"Ragebait Score: {score}/100")

        if score >= 70:
            st.error("High ragebait likelihood")
        elif score >= 35:
            st.warning("Medium ragebait likelihood")
        else:
            st.success("Low ragebait likelihood")

        st.write("Flagged words or phrases:")
        st.write(flagged if flagged else "No major ragebait phrases found.")