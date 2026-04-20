import streamlit as st
import google.generativeai as genai
import time
import os


# 🔑 Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")

# 🎨 Page Config
st.set_page_config(page_title="AI Exam Assistant", layout="centered")

# 🎯 Header
st.markdown("""
# 🎯 AI Student Exam Assistant  
### Plan smarter. Study better. Score higher.

👋 This tool helps students generate a **personalized study plan** based on their preparation level and time available.

👉 Fill the details below and click *Generate Study Plan*
""")

st.write("Fill your details and get a personalized study plan!")
st.info("⚡ Powered by Google Gemini AI for intelligent study planning")

# 🧾 INPUT SECTION (UPGRADED UI)
exam_days = st.slider(
    "📅 Days left for exam",
    1, 30, 5,
    help="Select how many days you have before your exam"
)

study_hours = st.slider(
    "⏳ Hours you can study daily",
    1, 12, 4,
    help="Select how many hours you can realistically study per day"
)

subject = st.text_input(
    "📘 Subject / Exam Name",
    help="Enter your subject (e.g., Data Structures, Indian Constitution)"
)

mode = st.radio(
    "🎯 Select Study Mode",
    ["Normal", "Last-Minute"],
    help="Choose Last-Minute if exam is very near"
)

level = st.selectbox(
    "📊 Your preparation level",
    ["Beginner", "Intermediate", "Advanced"],
    help="Select your current level of preparation"
)

# 📊 Progress Indicator
progress = (30 - exam_days) / 30
st.progress(progress)

st.caption("📊 Your preparation urgency level")

# ⚠️ Smart Warning
if exam_days <= 3:
    st.error("⚠️ Very less time! Focus only on high-priority topics.")


# 🧠 LOGIC FUNCTION
def get_strategy(days, mode):
    if mode == "Last-Minute":
        return "Emergency Strategy (focus only on high-priority topics and revision)"
    elif days <= 3:
        return "Crash Preparation"
    elif days <= 7:
        return "Focused Revision"
    else:
        return "Balanced Study Plan"

# 🧠 PROMPT GENERATION
def generate_prompt():
    strategy = get_strategy(exam_days, mode)

    prompt = f"""
    You are an intelligent academic assistant powered by Google Gemini AI.

    Your task is to analyze the student's situation and generate a highly personalized study plan.

    Student Details:
    - Subject: {subject}
    - Days left: {exam_days}
    - Daily study hours: {study_hours}
    - Preparation level: {level}
    - Strategy: {strategy}
    - Mode: {mode}

    Instructions:
    - Use reasoning to prioritize important topics
    - Adapt based on time constraints
    - If Last-Minute mode → focus only on high-impact topics
    - Provide concise and structured output

    Output Format:
    1. 📅 Day-wise Study Plan
    2. 🎯 Priority Topics
    3. 🧠 Smart Study Tips
    4. 💡 Motivation Message
    """

    return prompt


# 🚀🔥 ADD THIS BLOCK (VERY IMPORTANT FOR EFFICIENCY)
@st.cache_data(show_spinner=False)
def get_ai_response(prompt):
    response = model.generate_content(prompt)
    return response.text


# 🚀 GENERATE BUTTON
if st.button("🚀 Generate Study Plan"):

    if subject.strip() == "":
        st.warning("Please enter subject name!")
    else:
        with st.spinner("⚡ Generating optimized study plan..."):

            try:
                prompt = generate_prompt()

                # ⏱️ TIME TRACKING (EFFICIENCY BOOST)
                start_time = time.time()

                # 🔥 USE CACHED FUNCTION (NOT DIRECT CALL)
                output = get_ai_response(prompt)

                end_time = time.time()

                # 📊 OUTPUT
                st.success("✅ Your Personalized Study Plan")
                st.markdown(output)
                
                st.markdown("### 🤖 How AI Generated This Plan")
                st.write("""
                This plan is generated using Google Gemini AI by analyzing:
                - Time constraints
                - Study capacity
                - Preparation level

                The AI dynamically prioritizes topics to maximize exam performance.
                """)

                # ⚡ SHOW PERFORMANCE
                st.caption(f"⚡ Generated in {round(end_time - start_time, 2)} seconds")

                # 📥 DOWNLOAD
                st.download_button(
                    label="📥 Download Study Plan",
                    data=output,
                    file_name="study_plan.txt"
                )

            except Exception as e:
                st.error("⚠️ Unable to generate study plan. Please try again later.")

# ⚡ EXTRA SECTION
st.markdown("---")
st.markdown("## ⚡ Quick Study Tips")

st.write("""
- Use Pomodoro technique (25 min focus + 5 min break)
- Revise before sleeping for better memory
- Practice previous year papers
- Avoid distractions during study time
""")