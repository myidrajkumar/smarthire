"""Python JD Generator"""

from fastapi import FastAPI

from apis import categorized_apis, jd_generator_apis, resume_screen_apis

from jd_generator import get_jd_from_model_json
from jd_persister import save_jd_and_retrieve

app = FastAPI()

app.include_router(jd_generator_apis.router)
app.include_router(resume_screen_apis.router)
app.include_router(categorized_apis.router)


def get_job_description_inputs():
    """Get the inputs from HR"""
    job_title = input("Job Title:")
    skills = input("Skills:")
    experience = input("Experience:")
    return job_title, skills, experience


def generate_job_description():
    """Gnereate the job description"""
    (job_title, skills, experience) = get_job_description_inputs()
    llm_response = get_jd_from_model_json(job_title, skills, experience)
    print("LLM Response", llm_response)
    save_jd_and_retrieve(llm_response, job_title=job_title, bu_id=1)
    print("Job Description generated successfully!!!")


if __name__ == "__main__":
    #     # generate_job_description()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # connect(config)
