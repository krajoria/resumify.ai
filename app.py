#Importing the necessary libraries
from dotenv import load_dotenv

load_dotenv()# Load environment variables
import base64
import streamlit as st
import os
import io
import time
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Configure Google Generative AI with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define a function for the typewriter effect
def typewriter_effect(text):
    html_code = f"""
    <style>
        @keyframes type {{
            from {{ width: 0; }}
            to {{ width: 100%; }}
        }}

        .typewriter-text {{
            white-space: nowrap;
            overflow: hidden;
            animation: type 5s steps(100) infinite;
            display: inline-block;
            font-size: 7vw;
            margin-bottom: 3px;
        }}
    </style>
    <div class="typewriter-text">{text}</div>
    """

    st.markdown(html_code, unsafe_allow_html=True)


def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')# Creating a GenerativeModel with the specified model type
    response=model.generate_content([input,pdf_content[0],prompt])# Generating content using the model with the provided input, PDF content, and prompt
    return response.text # Returning the generated text response

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        # Create a list with a dictionary representing the PDF parts
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode image data to base64
            }
        ]
         # Returning the list containing PDF parts
        return pdf_parts
    else:
        # An error is raised if no file is uploaded
        raise FileNotFoundError("No file uploaded")

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
typewriter_effect("RESUMIFYYYYYY.AI")
st.markdown("From Resume to Reality: Land your dream job with Resumify.AI")
input_text=st.text_area("What is the job description? ",key="input")
uploaded_file=st.file_uploader("Upload your resume in PDF format",type=["pdf"])


if uploaded_file is not None:
    st.write("Successfully uploaded")


submit1 = st.button("Tell me about my Resume")

submit2 = st.button("How can I improve my skills?")

submit3 = st.button("Analyze the fit")

submit4 = st.button("Interview Tips!!")


input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a seasoned Career Development Coach, and your goal is to provide personalized advice to help the candidate enhance their skills and career prospects. 
Please guide the candidate on how they can improve their skills effectively. 
Highlight specific areas where they can focus, recommend learning resources, and suggest practical steps for skill development.
"""


input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description and then give me detailed explanation about the fit and keywords missing and last final thoughts.
"""

input_prompt4 = """
You are an AI-powered Career Advisor assisting a job candidate in preparing for an upcoming interview. 
Based on the provided resume, generate personalized interview tips and suggestions to help the candidate succeed in their job interview. 
Consider highlighting their strengths, suggesting areas for improvement, and providing general interview strategies.
"""


if submit1:
    st.empty()  # Clear previous output
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Here you go!!")
        st.write(response)
    else:
        st.write("Please upload the resume")


elif submit3:
    st.empty()
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("Analyzing...")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("You're doing great but you are worthy of even greater things.....")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("Slay IT !!")
        st.write(response)
    else:
        st.write("Please upload the resume")






   




