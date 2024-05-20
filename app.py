from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
import PyPDF2 as pdf


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt, jd, pdf_content_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, jd, pdf_content_text])
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())

    return text


# Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
jd = st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing(as bullet points) and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content_text = input_pdf_text(uploaded_file)
        jd = "Job Description: \n" + jd
        pdf_content_text = "Resume: \n" + pdf_content_text
        response = get_gemini_response(input_prompt1, jd, pdf_content_text)
        st.subheader("The Repsonse is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content_text = input_pdf_text(uploaded_file)
        jd = "Job Description: \n" + jd
        pdf_content_text = "Resume: \n" + pdf_content_text
        response = get_gemini_response(input_prompt2, jd, pdf_content_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")