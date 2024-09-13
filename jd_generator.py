"""Python JD Generator"""

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


# from googlegenai_llm import load_llm

# from groq_gemma_llm import load_llm

from llms.groq_llama_llm import load_llm

# from groq_mixtral_llm import load_llm

# from ollama_llama import load_llm

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
            "num_words": 300,
        }
    )


def get_job_description_sytem_propmt_msg():
    """Instruct the system to follow this"""
    return """
            TechInterrupt is a leading technology company
            specializing in software development. It is a system integrator,
            software development partner and managed services provider
            that helps companies improve their operational efficiency
            and decision-making capabilities.

            You are a hiring manager and looking to hire new employees.
            You need to prepare a job description(JD) for the job requirements.
            This JD should be SEO friendly and should highlight
            the unique features and benefits of the position.

            You need to prepare the JD in JSON format with the following fields
            * Job Title - No creativeness
            * Description
            * Responsibilities
            * Skills
            * Experience - more creative and list format
            * Closing Statment - most creative but just with one line
           """


def get_job_description_user_propmt_msg():
    """As Chat format is followed, the user message"""
    return """
              Write a job description for a {job_title}
              that is around {num_words} words or less in a neutral tone.
              This job needs the skills of {skills}.
              The experience of the candidate should be {experience}.
           """
