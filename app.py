import streamlit as st
import google.generativeai as genai
import time

# 🔑 Configure Gemini API
genai.configure(api_key="AIzaSyDlhVNfYq53gk80Au7lgUQiD6YTg-mUVwo")

model = genai.GenerativeModel("models/gemini-flash-latest")

# 🎨 Page Config
st.set_page_config(page_title="AI Exam Assistant", layout="centered")

# 🎯 Header
st.markdown("""
# 🎯 AI Student Exam Assistant  
### Plan smarter. Study better. Score higher.
""")

st.write("Fill your details and get a personalized study plan!")

# 🧾 INPUT SECTION (UPGRADED UI)
exam_days = st.slider("📅 Days left for exam", 1, 30, 5)
study_hours = st.slider("⏳ Hours you can study daily", 1, 12, 4)
subject = st.text_input("📘 Subject / Exam Name")
level = st.selectbox("📊 Your preparation level", ["Beginner", "Intermediate", "Advanced"])

# ⚠️ Smart Warning
if exam_days <= 3:
    st.error("⚠️ Very less time! Focus only on high-priority topics.")

# 🧠 LOGIC FUNCTION
def get_strategy(days):
    if days <= 3:
        return "Crash Preparation (focus only on important topics)"
    elif days <= 7:
        return "Focused Revision Strategy"
    else:
        return "Balanced Study Plan"

# 🧠 PROMPT GENERATION
def generate_prompt():
    strategy = get_strategy(exam_days)

    prompt = f"""
    You are an expert academic mentor.

    Student Details:
    - Subject: {subject}
    - Days left: {exam_days}
    - Daily study hours: {study_hours}
    - Level: {level}
    - Strategy: {strategy}

    Generate:
    1. A clear day-wise study plan
    2. Priority topics to focus
    3. Smart study tips based on level
    4. A short motivational message

    Format:
    - Use headings
    - Use bullet points
    - Keep it clean and structured
    """

    return prompt

# 🚀 GENERATE BUTTON
if st.button("🚀 Generate Study Plan"):

    if subject.strip() == "":
        st.warning("Please enter subject name!")
    else:
        with st.spinner("Generating your smart study plan..."):
            time.sleep(2)

            prompt = generate_prompt()
            response = model.generate_content(prompt)

            output = response.text

            # 📊 OUTPUT SECTION
            st.success("✅ Your Personalized Study Plan")
            st.markdown(output)

            # 📥 DOWNLOAD BUTTON
            st.download_button(
                label="📥 Download Study Plan",
                data=output,
                file_name="study_plan.txt"
            )

# ⚡ EXTRA SECTION
st.markdown("---")
st.markdown("## ⚡ Quick Study Tips")

st.write("""
- Use Pomodoro technique (25 min focus + 5 min break)
- Revise before sleeping for better memory
- Practice previous year papers
- Avoid distractions during study time
""")