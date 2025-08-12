


import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self, temperature: float = 0.0):
        self.llm = ChatGroq(
            temperature=temperature,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="openai/gpt-oss-20b"
        )

    def _parse_json(self, content: str):
        parser = JsonOutputParser()
        try:
            return parser.parse(content)
        except Exception:
            raise OutputParserException("Unable to parse model output as JSON.")

    def extract_jobs(self, cleaned_text: str):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from a careers/job page. Extract job postings from this text.
            Return a JSON array of objects with keys strictly:
              - role: string
              - experience: string (years or seniority if available; else "Not specified")
              - skills: array of strings (core skills, technologies, tools)
              - description: string (concise summary of responsibilities and requirements)

            If multiple roles exist, include multiple objects. If only one, still return an array.

            ### JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        data = self._parse_json(res.content)
        return data if isinstance(data, list) else [data]

    def parse_resume(self, resume_text: str):
        prompt_resume = PromptTemplate.from_template(
            """
            ### RESUME TEXT:
            {resume_text}

            ### INSTRUCTION:
            Analyze the resume and extract a compact JSON with:
              - name: string or "Candidate"
              - title: string (current/desired role)
              - years_experience: string (e.g., "5+ years") or "Not specified"
              - skills: array of strings (top relevant skills)
              - highlights: array of 3-6 bullet-like achievements/experiences
              - summary: 2-4 sentence professional summary emphasizing strengths, domains, and impact.

            Return strictly valid JSON only.
            """
        )
        chain_resume = prompt_resume | self.llm
        res = chain_resume.invoke({"resume_text": resume_text})
        data = self._parse_json(res.content)

        data.setdefault("skills", [])
        data.setdefault("highlights", [])
        data.setdefault("summary", "")
        data.setdefault("name", "Candidate")
        data.setdefault("title", "")
        data.setdefault("years_experience", "Not specified")
        return data

    def write_mail(self, job, resume, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION (STRUCTURED JSON):
            {job_json}

            ### CANDIDATE RESUME SUMMARY (STRUCTURED JSON):
            {resume_json}

            ### PORTFOLIO LINKS:
            {link_list}

            ### INSTRUCTION:
            - Write a professional cold email FROM the candidate (first-person perspective) to the HR or referral person at the company hiring for the job.
            - Start with a polite greeting and mention how the candidate found the role.
            - Highlight the candidate’s strongest points from the resume that match the job description.
            - Clearly explain why they are the perfect fit for the role.
            - Keep tone confident but humble, concise, and respectful.
            - Mention relevant portfolio/project links inline if available.
            - End with a clear call to action (e.g., scheduling an interview or discussing further).
            - Length: 140–220 words.
            - Output only the email text. No preamble.

            ### EMAIL:
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke(
            {
                "job_json": str(job),
                "resume_json": str(resume),
                "link_list": links if links else "[Portfolio Link 1], [Portfolio Link 2]"
            }
        )
        return res.content