"""Python JD Generator"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from apis import (
    access_credentials_api,
    categorized_apis,
    dashboard_api,
    data_visualizations,
    jd_generator_apis,
    preliminary_questions_api,
    resume_screen_apis,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(jd_generator_apis.router)
app.include_router(resume_screen_apis.router)
app.include_router(categorized_apis.router)
app.include_router(data_visualizations.router)
app.include_router(preliminary_questions_api.router)
app.include_router(access_credentials_api.router)
app.include_router(dashboard_api.router)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard Serving API"""
    return templates.TemplateResponse(request=request, name="dashboard.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
