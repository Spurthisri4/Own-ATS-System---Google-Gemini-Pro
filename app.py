import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf 

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('models/gemini-1.5-flash')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text 
   

input_prompt = """
 Hey Act like a skilled or very experience ATS(Application Tracking System)
 with a deep understanding of tech field, sofware engineering, data science, data analyst 
and big data engineer. Your task is to evaluate the resume based on the given job description
you must consider the job market is very compitative and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based
on Jd and 
the missing keywords with high accuracy
resume: {text}
description: {jd}

I want the response in one single string having the structure 
JD Match: 75%

Missing Keywords:
- keyword1
- keyword2
- keyword3

Profile Summary:
<your summary here>
"""

st.title('Smart ATS')
st.text("Improve Your Resume ATS")
jd=st.text_area('Paste the Job Description')
uploaded_file=st.file_uploader("Upload Your Resume",type='pdf',help='Please upload the pdf')

submit= st.button('Submit')

if submit:
    if uploaded_file is not None:
        text= input_pdf_text(uploaded_file)
        final_prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_response(final_prompt)
        st.subheader("ATS Evaluation Result")
        st.write(response)
   




