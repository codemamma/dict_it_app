import streamlit as st
import pandas as pd
import random
from datetime import date
import os

# File path to save/load data
CSV_FILE = "vocab_data.csv"

# Load data from CSV if exists, else create new
if os.path.exists(CSV_FILE):
    vocab_df = pd.read_csv(CSV_FILE)
    vocab_df["Date Added"] = pd.to_datetime(vocab_df["Date Added"]).dt.date
else:
    vocab_df = pd.DataFrame(columns=[
        "Word", "Meaning", "Sentence", "Part of Speech",
        "Synonyms", "Notes", "Points", "Date Added"
    ])

st.set_page_config(page_title="Dict It", layout="wide")
st.title("📘 Dict It – My Personal Dictionary")

# Tabs
add_tab, vault_tab, quiz_tab, stats_tab = st.tabs(["➕ Add Word", "📚 Word Vault", "❓ Quiz Time", "📊 My Stats"])

# Add Word Tab
with add_tab:
    st.header("Add a New Word")
    with st.form("add_word_form"):
        word = st.text_input("Word")
        meaning = st.text_area("Meaning")
        pos = st.selectbox("Part of Speech", ["Noun", "Verb", "Adjective", "Adverb", "Other"])
        sentence = st.text_area("Use it in a sentence")
        synonyms = st.text_input("Synonyms / Antonyms (optional)")
        notes = st.text_input("Notes or Emoji (optional)")
        submitted = st.form_submit_button("Add to Vault")

        if submitted and word:
            new_entry = {
                "Word": word,
                "Meaning": meaning,
                "Sentence": sentence,
                "Part of Speech": pos,
                "Synonyms": synonyms,
                "Notes": notes,
                "Points": 10,
                "Date Added": date.today()
            }
            vocab_df = pd.concat([vocab_df, pd.DataFrame([new_entry])], ignore_index=True)
            vocab_df.to_csv(CSV_FILE, index=False)
            st.success(f"✅ '{word}' added to your vault! +10 points!")

# Word Vault Tab
with vault_tab:
    st.header("My Word Vault")
    st.dataframe(vocab_df, use_container_width=True)

# Quiz Tab
with quiz_tab:
    st.header("Quiz Time – Match the Meaning!")
    if len(vocab_df) < 4:
        st.warning("Need at least 4 words to play the quiz.")
    else:
        q_word = random.choice(vocab_df["Word"].tolist())
        correct_meaning = vocab_df[vocab_df["Word"] == q_word]["Meaning"].values[0]
        wrong_options = vocab_df[vocab_df["Word"] != q_word]["Meaning"].sample(3).tolist()
        options = wrong_options + [correct_meaning]
        random.shuffle(options)

        st.subheader(f"What does '{q_word}' mean?")
        answer = st.radio("Choose the correct meaning:", options)
        if st.button("Submit Answer"):
            if answer == correct_meaning:
                st.success("🎉 Correct! +5 points!")
            else:
                st.error(f"Oops! The correct answer was: {correct_meaning}")

# Stats Tab
with stats_tab:
    st.header("My Stats")
    total_words = len(vocab_df)
    total_points = vocab_df["Points"].sum()
    st.metric("📖 Total Words", total_words)
    st.metric("⭐ Total Points", total_points)

    if total_words >= 10:
        st.success("🏅 Badge Unlocked: Word Collector!")
    if total_points >= 100:
        st.success("🏆 Badge Unlocked: Vocab Champion!")

