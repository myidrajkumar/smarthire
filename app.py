"""Python JD Generator"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from apis import (
    categorized_apis,
    data_visualizations,
    jd_generator_apis,
    preliminary_questions_api,
    resume_screen_apis,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(jd_generator_apis.router)
app.include_router(resume_screen_apis.router)
app.include_router(categorized_apis.router)
app.include_router(data_visualizations.router)
app.include_router(preliminary_questions_api.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
