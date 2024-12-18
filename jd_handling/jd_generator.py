"""Python JD Generator"""

from typing import List
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel


# from llms.googlegenai_llm import load_llm

# from llms.groq_gemma_llm import load_llm

from llms.groq_llama_llm import load_llm

# from llms.groq_mixtral_llm import load_llm

# from llms.ollama_llama import load_llm

load_dotenv()


class JobDescription(BaseModel):
    """Job Description Model"""

    job_title: str
    description: str
    responsibilities: List[str]
    skills_experience: List[str]


def get_jd_from_model_json(job_title, skills, experience):
    """Connect and Get the response"""
    llm = load_llm()
    print(job_title)
    prompt_template = ChatPromptTemplate(
        [
            (
                "system",
                get_job_description_sytem_propmt_msg(),
            ),
            (
                "user",
                get_job_description_user_propmt_msg(),
            ),
        ]
    )

    parser = PydanticOutputParser(pydantic_object=JobDescription)

    chain = prompt_template | llm | parser
    return chain.invoke(
        {
            "job_title": job_title,
            "skills": skills,
            "experience": experience,
            "num_words": 220,
        }
    )


def get_job_description_sytem_propmt_msg():
    """Instruct the system to follow this"""
    return """
            You are an AI assistant specialized in creating comprehensive and
            accurate job descriptions. Your task is to generate a 1 page
            job description that includes

            * Job Title - No creativeness
            * Description - A clear and engaging overview of the job role
            * Responsibilities - A detailed list of duties and responsibilities associated with the role. Please provide in list format
            * Skills & Experience - An in-depth of the required skills and experience with as much detail as possible. This should be in list format only

            Guidelines
            * The job description is as accurate and precise as possible.
            * The experience and skills sections are detailed and tailored to the job title.
            * The experience and skills sections should contain all the relevant technical stack related to the skills section.
            * The language is professional and suitable for a formal job posting.
            * Provide the response in JSON format only
            * Use professional and inclusive language suitable for a formal job posting.
            * Except description, all other fields should be list only

            Return a response in JSON format with the following structure
            {{
                "job_title": "string",
                "description": "string",
                "responsibilities":["list of responsibilities"],
                "skills_experience": ["list"]
            }}

           """


def get_job_description_user_propmt_msg():
    """As Chat format is followed, the user message"""
    return """
              Write a job description for a {job_title}
              that is around {num_words} words or less ONLY in a neutral tone.
              This job needs the skills of {skills}.
              The experience of the candidate should be {experience}.
           """
