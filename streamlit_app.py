# streamlit_app.py
import streamlit as st
import requests

st.title("Resume Screener Dashboard")

job_description = st.text_area("Enter Job Description:")

if st.button("Match Resumes"):
    if job_description:
        # Send job description to the FastAPI match endpoint.
        response = requests.post("http://localhost:8000/match/", data={"job_description": job_description})
        if response.status_code == 200:
            results = response.json()["results"]
            st.write("Ranked Resumes:")
            for resume_id, score in results:
                st.write(f"Resume ID: {resume_id} - Score: {score:.2f}")
        else:
            st.error("Error matching resumes. Please check the API logs.")
    else:
        st.warning("Please enter a job description.")
