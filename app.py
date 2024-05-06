import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


def ai_gen(requirement: str, prompt: str):
    response = model.generate_content([requirement, prompt])
    return response.text


# Function to extract text from PDF file
def get_text(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


# Main function
def main():
    st.title("Mock Interview System📑")  # Add the heading "feedback Generator"
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    if uploaded_file is not None:
        st.write("Resume Uploaded Successfully!")
        resume_text = get_text(uploaded_file)
        st.session_state.resume_text = resume_text
    sNum = st.number_input("Number of suggestions you need", min_value=1, max_value=20)
    qNum = st.number_input("Number of mock questions you need", min_value=1, max_value=20)
    if st.button("Generate Feedback"):
        with st.spinner("Your feedback is being generated!! Hang Tight!"):
            # Generate feedback if both resume and job description are provided
            if st.session_state.resume_text is not None:
                requirement = 'Generate %s suggestions and %s possible questions based on my resume' % (sNum, qNum)
                feedback = ai_gen(requirement, st.session_state.resume_text)
                st.write("Generated Feedback:")
                st.write(feedback)

if __name__ == "__main__":
    main()