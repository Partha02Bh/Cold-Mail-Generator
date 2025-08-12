


# import streamlit as st
# from langchain_community.document_loaders import WebBaseLoader

# from chains import Chain
# from portfolio import Portfolio
# from utils import clean_text, extract_resume_text


# def create_streamlit_app(llm, portfolio):
#     st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
#     st.title("📧 Cold Mail Generator ")

#     # Step 1: Job URL input
#     job_url = st.text_input("Enter a Job Posting URL")

#     # Step 2: Resume upload
#     resume_file = st.file_uploader(
#         "Upload Your Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"]
#     )

#     # Step 3: When both job URL and resume are provided
#     if job_url and resume_file:
#         # Load and clean job posting text
#         with st.spinner("Loading and processing job posting..."):
#             loader = WebBaseLoader(job_url)
#             job_text_raw = loader.load()[0].page_content
#             job_text = clean_text(job_text_raw)
#             job_data = llm.extract_jobs(job_text)  # ✅ Extracted structured job data

#         # Parse resume data
#         with st.spinner("Extracting resume details..."):
#             resume_text_raw = extract_resume_text(resume_file)
#             resume_text = clean_text(resume_text_raw)
#             resume_data = llm.parse_resume(resume_text)  # ✅ Extracted structured resume data

#         # Get portfolio links
#         with st.spinner("Fetching portfolio links..."):
#             portfolio_links = portfolio.query_links("developer")  # You can make this dynamic

#         # Generate cold email
#         with st.spinner("Generating personalized cold email..."):
#             generated_mail = llm.write_mail(job_data, resume_data, portfolio_links)

#         # Display result
#         st.subheader("✉ Generated Cold Email")
#         st.write(generated_mail)

#     else:
#         st.info("Please provide both a Job Posting URL and upload your resume.")


# if __name__ == "__main__":
#     # Initialize your LLM chain
#     llm = Chain()

#     # Initialize your portfolio handler
#     portfolio = Portfolio()

#     # Run the Streamlit app
#     create_streamlit_app(llm, portfolio)


import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from utils import clean_text, extract_resume_text

def create_streamlit_app(llm):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    st.title("📧 Cold Mail Generator")

    # Step 1: Job URL input
    job_url = st.text_input("Enter a Job Posting URL")

    # Step 2: Resume upload
    resume_file = st.file_uploader(
        "Upload Your Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"]
    )

    # Step 3: When both job URL and resume are provided
    if job_url and resume_file:
        # Load and clean job posting text
        with st.spinner("Loading and processing job posting..."):
            loader = WebBaseLoader(job_url)
            job_text_raw = loader.load()[0].page_content
            job_text = clean_text(job_text_raw)
            job_data = llm.extract_jobs(job_text)

        # Parse resume data
        with st.spinner("Extracting resume details..."):
            resume_text_raw = extract_resume_text(resume_file)
            resume_text = clean_text(resume_text_raw)
            resume_data = llm.parse_resume(resume_text)

        # No portfolio — pass an empty list or placeholder
        portfolio_links = []

        # Generate cold email
        with st.spinner("Generating personalized cold email..."):
            generated_mail = llm.write_mail(job_data, resume_data, portfolio_links)

        # Display result
        st.subheader("✉ Generated Cold Email")
        st.write(generated_mail)

    else:
        st.info("Please provide both a Job Posting URL and upload your resume.")


if __name__ == "__main__":
    # Initialize your LLM chain
    llm = Chain()

    # Run the Streamlit app
    create_streamlit_app(llm)
