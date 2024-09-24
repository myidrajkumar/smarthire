"""Python JD Generator"""

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


# from llms.googlegenai_llm import load_llm

# from llms.groq_gemma_llm import load_llm

from llms.groq_llama_llm import load_llm

# from llms.groq_mixtral_llm import load_llm

# from llms.ollama_llama import load_llm

load_dotenv()


def get_jd_from_model_json(job_title, skills, experience):
    """Connect and Get the response"""
    llm = load_llm()

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

    parser = JsonOutputParser()

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
            * Skills & Experience - An in-depth section outlining the required skills and experience with as much detail as possible. This should be in list format only
            
            Guidelines
            * The job description is as accurate and precise as possible.
            * The experience and skills sections are detailed and tailored to the job title.
            * The language is professional and suitable for a formal job posting.
            * Provide the response in JSON format only
            * Use professional and inclusive language suitable for a formal job posting.
            * Except description, all other fields should be list only


            The Json field names should be the following only
            * JobTitle
            * Description
            * Responsibilities
            * SkillsAndExperience
            
            The final output should be a well-structured, one-page document ready for publication in job listings.
           """


def get_job_description_user_propmt_msg():
    """As Chat format is followed, the user message"""
    return """
              Write a job description for a {job_title}
              that is around {num_words} words or less ONLY in a neutral tone.
              This job needs the skills of {skills}.
              The experience of the candidate should be {experience}.
           """
