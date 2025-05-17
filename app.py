import streamlit as st
from textblob import TextBlob
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Mental Health Chatbot")

if "chats" not in st.session_state:
    st.session_state.chats = []

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def add_message(message, is_user):
    st.session_state.chats.append({
        "message": message,
        "is_user": is_user,
        "timestamp": datetime.now(),
        "sentiment": analyze_sentiment(message) if is_user else None
    })

st.title("Mental Health Chatbot")

# Chat input
user_input = st.text_input("You:", key="input")

if user_input:
    add_message(user_input, True)
    # Simple empathetic response based on sentiment
    sentiment = analyze_sentiment(user_input)
    if sentiment > 0.1:
        response = "I'm glad to hear that! Would you like to share more?"
    elif sentiment < -0.1:
        response = "I'm sorry you're feeling this way. I'm here to listen."
    else:
        response = "Thank you for sharing. How else are you feeling?"
    add_message(response, False)
    st.experimental_rerun()

# Display chat messages
for chat in st.session_state.chats:
    if chat["is_user"]:
        st.chat_message("user").write(chat["message"])
    else:
        st.chat_message("assistant").write(chat["message"])

# Mood visualization
if st.session_state.chats:
    df = pd.DataFrame([
        {"timestamp": chat["timestamp"], "sentiment": chat["sentiment"]}
        for chat in st.session_state.chats if chat["is_user"]
    ])
    if not df.empty:
        df = df.set_index("timestamp").resample("D").mean()
        st.subheader("Mood Over Time")
        fig, ax = plt.subplots()
        ax.plot(df.index, df["sentiment"], marker='o')
        ax.set_ylim(-1, 1)
        ax.set_ylabel("Sentiment Polarity")
        ax.set_xlabel("Date")
        ax.grid(True)
        st.pyplot(fig)
