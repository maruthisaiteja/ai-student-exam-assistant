import streamlit as st
from dotenv import load_dotenv
import os
from utils.gemini_helper import initialize_gemini, generate_summary, generate_key_points, generate_questions, generate_quiz
from utils.document_processor import extract_text_from_file

# Load environment variables
load_dotenv()

# Setup Page Config
st.set_page_config(page_title="AI Study Assistant", page_icon="🎓", layout="wide")

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Style for buttons to look more premium */
    div.stButton > button:first-child {
        background-color: #4a90e2;
        color: white;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #357abd;
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    div.stDownloadButton > button:first-child {
        background-color: #2ecc71;
        color: white;
        border-radius: 8px;
        border: none;
    }
    div.stDownloadButton > button:first-child:hover {
        background-color: #27ae60;
    }
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        border-bottom: 3px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #4a90e2;
        color: #4a90e2 !important;
        font-weight: 600;
    }
    /* Title styling */
    h1 {
        background: -webkit-linear-gradient(45deg, #4a90e2, #9013fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "key_points" not in st.session_state:
    st.session_state.key_points = ""
if "questions" not in st.session_state:
    st.session_state.questions = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = ""

# Sidebar for Input
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input("Gemini API Key (Optional if in .env)", type="password", help="Get your API key from Google AI Studio")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        
    st.divider()
    
    st.header("📄 Input Source")
    input_method = st.radio("Choose Input Method:", ["Text Input", "File Upload"])
    
    if input_method == "Text Input":
        raw_text = st.text_area("Paste your notes here:", height=250, placeholder="Enter the text you want to study...")
        if st.button("Process Text", use_container_width=True):
            if raw_text.strip():
                st.session_state.extracted_text = raw_text
                st.success("Text loaded successfully!")
            else:
                st.warning("Please enter some text.")
                
    else:
        uploaded_file = st.file_uploader("Upload Document", type=['pdf', 'txt'], help="Upload PDF or TXT files")
        if st.button("Process File", use_container_width=True):
            if uploaded_file is not None:
                try:
                    with st.spinner("Extracting text from file..."):
                        text = extract_text_from_file(uploaded_file)
                        if text.strip():
                            st.session_state.extracted_text = text
                            st.success("File processed successfully!")
                        else:
                            st.warning("No text found in the file.")
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
            else:
                st.warning("Please upload a file first.")
                
    st.divider()
    st.caption("🚀 Built for Hackathons & Fast Learning")

# Main content
st.title("🎓 AI Student Exam Assistant")
st.markdown("### Transform your study materials into actionable insights.")

if not initialize_gemini():
    st.error("⚠️ Please configure your Google Gemini API key in the sidebar or via the `.env` file.")
    st.info("You can get a free API key from [Google AI Studio](https://aistudio.google.com/).")
    st.stop()

if st.session_state.extracted_text:
    with st.expander("🔍 Preview Extracted Text", expanded=False):
        preview = st.session_state.extracted_text[:1500] + ("..." if len(st.session_state.extracted_text) > 1500 else "")
        st.text(preview)

    st.markdown("### ⚡ AI Processing")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Generate Summary", use_container_width=True):
            with st.spinner("Analyzing and summarizing..."):
                try:
                    st.session_state.summary = generate_summary(st.session_state.extracted_text)
                except Exception as e:
                    st.error(str(e))
                    
    with col2:
        if st.button("💡 Extract Key Points", use_container_width=True):
            with st.spinner("Extracting critical information..."):
                try:
                    st.session_state.key_points = generate_key_points(st.session_state.extracted_text)
                except Exception as e:
                    st.error(str(e))
                    
    with col3:
        if st.button("❓ Generate Questions", use_container_width=True):
            with st.spinner("Formulating exam questions..."):
                try:
                    st.session_state.questions = generate_questions(st.session_state.extracted_text)
                except Exception as e:
                    st.error(str(e))
                    
    with col4:
        if st.button("🎯 Create Quiz", use_container_width=True):
            with st.spinner("Designing multiple-choice quiz..."):
                try:
                    st.session_state.quiz = generate_quiz(st.session_state.extracted_text)
                except Exception as e:
                    st.error(str(e))

    st.divider()

    # Tabs for Output
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "💡 Key Points", "❓ Questions", "🎯 Quiz"])
    
    with tab1:
        if st.session_state.summary:
            st.markdown(st.session_state.summary)
            st.download_button("📥 Download Summary (.txt)", st.session_state.summary, "summary.txt", key="dl_summary")
        else:
            st.info("Click 'Generate Summary' to see results here.")
            
    with tab2:
        if st.session_state.key_points:
            st.markdown(st.session_state.key_points)
            st.download_button("📥 Download Key Points (.txt)", st.session_state.key_points, "key_points.txt", key="dl_kp")
        else:
            st.info("Click 'Extract Key Points' to see results here.")
            
    with tab3:
        if st.session_state.questions:
            st.markdown(st.session_state.questions)
            st.download_button("📥 Download Questions (.txt)", st.session_state.questions, "questions.txt", key="dl_q")
        else:
            st.info("Click 'Generate Questions' to see results here.")
            
    with tab4:
        if st.session_state.quiz:
            st.markdown(st.session_state.quiz)
            st.download_button("📥 Download Quiz (.txt)", st.session_state.quiz, "quiz.txt", key="dl_quiz")
        else:
            st.info("Click 'Create Quiz' to see results here.")
else:
    st.info("👈 Please **paste text** or **upload a document** in the sidebar to begin your study session!")
    
    # Placeholder landing page UI
    st.markdown("---")
    st.markdown("### 🌟 Features")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("**📚 Document Support**\nUpload PDF or TXT files effortlessly.")
    with col_f2:
        st.markdown("**🧠 Gemini Powered**\nUtilizing Google's Gemini 1.5 Flash for lightning fast analysis.")
    with col_f3:
        st.markdown("**🎯 Exam Ready**\nGenerate summaries, questions, and quizzes instantly.")