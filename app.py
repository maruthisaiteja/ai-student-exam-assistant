import streamlit as st
import google.generativeai as genai
import os
import time

# 🔐 API CONFIG
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API key not found. Please configure it in Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-flash-latest")

# 🎨 PAGE CONFIG
st.set_page_config(page_title="AI Exam Assistant", layout="centered")

# 🌟 PREMIUM HEADER
st.markdown("""
# 🎯 AI Student Exam Assistant  
### 🚀 Plan smarter. Study better. Score higher.

💡 Powered by **Google Gemini AI**
""")

st.info("⚡ AI-powered personalized study planning")

# 🎯 PROBLEM + SOLUTION
st.markdown("""
### 🎯 Problem
Students struggle with:
- Lack of planning  
- Poor time management  
- Confusion about important topics  

### ✅ Solution
This AI tool creates **personalized study strategies** based on your time, level, and subject.
""")

st.markdown("---")

# 🧾 INPUT SECTION
exam_days = st.slider("📅 Days left for exam", 1, 30, 5)
study_hours = st.slider("⏳ Study hours/day", 1, 12, 4)

subject = st.text_input("📘 Subject Name")

mode = st.radio("🎯 Study Mode", ["Normal", "Last-Minute"])
level = st.selectbox("📊 Preparation Level", ["Beginner", "Intermediate", "Advanced"])

# 📊 PROGRESS BAR
progress = (30 - exam_days) / 30
st.progress(progress)
st.caption("📊 Exam urgency level")

# ⚠️ WARNING
if exam_days <= 3:
    st.warning("⚡ Last-minute preparation detected!")

st.markdown("---")

# 🧠 LOGIC
def get_strategy(days, mode):
    if mode == "Last-Minute":
        return "Emergency Strategy"
    elif days <= 3:
        return "Crash Preparation"
    elif days <= 7:
        return "Focused Revision"
    else:
        return "Balanced Study"

# 🧠 PROMPT
def generate_prompt():
    strategy = get_strategy(exam_days, mode)

    return f"""
You are an AI academic mentor powered by Google Gemini.

Student:
Subject: {subject}
Days Left: {exam_days}
Study Hours: {study_hours}
Level: {level}
Strategy: {strategy}

Generate:
1. Day-wise plan
2. Important topics
3. Study tips
4. Motivation
"""

# 🧠 QUIZ PROMPT
def generate_quiz_prompt():
    return f"""
Generate 5 important exam questions for:

Subject: {subject}
Level: {level}

Keep them exam-focused and concise.
"""

# ⚡ CACHED RESPONSE
@st.cache_data
def get_ai_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# 🎯 MAIN BUTTON
if st.button("🚀 Generate Study Plan"):

    if not subject or len(subject) < 3:
        st.warning("Enter valid subject name")
    else:
        with st.spinner("⚡ Generating plan..."):
            try:
                start = time.time()

                prompt = generate_prompt()
                output = get_ai_response(prompt)

                end = time.time()

                st.success("✅ Study Plan Ready")
                st.markdown(output)

                st.markdown("### 🎯 Why This Works")
                st.write("Focused, time-optimized, and AI-personalized.")

                st.markdown("### 🤖 AI Logic")
                st.write("Generated using Google Gemini AI with context-aware reasoning.")

                st.caption(f"⚡ Generated in {round(end-start,2)} sec")

                st.download_button("📥 Download Plan", output)

            except:
                st.error("Something went wrong")

# 🧠 QUIZ FEATURE
st.markdown("---")
st.markdown("## 🧠 Practice Questions")

generate_quiz = st.button("📝 Generate Questions")

if generate_quiz:
    if not subject:
        st.warning("Enter subject first")
    else:
        with st.spinner("Generating questions..."):
            try:
                quiz_prompt = generate_quiz_prompt()
                quiz_output = get_ai_response(quiz_prompt)

                st.info("💡 Practice these questions")
                st.markdown(quiz_output)

            except:
                st.error("Error generating questions")

# ⚡ EXTRA TIPS
st.markdown("---")
st.markdown("## ⚡ Study Tips")

st.write("""
- Use Pomodoro technique  
- Revise before sleeping  
- Solve previous papers  
- Avoid distractions  
""")