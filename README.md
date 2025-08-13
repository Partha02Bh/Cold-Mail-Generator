# 📧 Cold Email Generator (Job URL + Resume)

A simple AI-powered Streamlit app that generates **personalized cold emails** based on:
- A **Job Posting URL**
- Your **Resume (PDF, DOCX, or TXT)**

No CSVs, no manual data entry — just paste the job link, upload your resume, and get a professional email instantly.

---

## 🚀 Features
- Fetches and cleans job posting content from any given URL.
- Extracts structured data from your resume.
- Uses an LLM to craft a **personalized cold email**.
- Runs fully locally (no external API keys required if using an open-source LLM).
- Simple **Streamlit web interface**.

## Set-up
1. To get started we first need to get an API_KEY from here: https://console.groq.com/keys. Inside `app/.env` update the value of `GROQ_API_KEY` with the API_KEY you created. 


2. To get started, first install the dependencies using:
    ```commandline
     pip install -r requirements.txt
    ```
   
3. Run the streamlit app:
   ```commandline
   streamlit run app/main.py
   ```
