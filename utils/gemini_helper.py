import google.generativeai as genai
import os
import streamlit as st

def initialize_gemini():
    # Try from environment first, then Streamlit secrets
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except (FileNotFoundError, KeyError):
            pass
            
    if not api_key:
        return False
        
    genai.configure(api_key=api_key)
    return True

def get_model():
    # Reverting to the model name that was originally working for you
    return genai.GenerativeModel("models/gemini-flash-latest")

def generate_content(prompt):
    try:
        model = get_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"API Error: {str(e)}")

def generate_summary(text):
    prompt = f"Provide a comprehensive but concise summary of the following text:\n\n{text}"
    return generate_content(prompt)

def generate_key_points(text):
    prompt = f"Extract exactly 5 key bullet points highlighting the most important information from the following text. Format as a markdown list:\n\n{text}"
    return generate_content(prompt)

def generate_questions(text):
    prompt = f"Based on the following text, generate 3 important short-answer questions and 2 long-answer (essay) questions. Format clearly with headings.\n\n{text}"
    return generate_content(prompt)

def generate_quiz(text):
    prompt = f"Create a multiple-choice quiz with 5 questions based on the following text. For each question, provide 4 options (A, B, C, D) and clearly indicate the correct answer at the bottom.\n\n{text}"
    return generate_content(prompt)
