"""To plot charts"""

from io import BytesIO

import matplotlib.pyplot as plt
import seaborn as sns
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from db.connect import (
    get_candidates_pipeline,
    get_time_to_hire,
)

router = APIRouter()


@router.get("/pipelinechart")
def get_candidates_pipeline_chart():
    """Pipeline Plots"""

    pipeline_data = get_candidates_pipeline()

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x="stage", y="candidates", data=pipeline_data)
    plt.title("Candidate Pipeline by Stage")

    # Save to BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")


@router.get("/timetohire")
def get_time_to_hire_chart():
    """Time to Hire Charts"""

    time_to_hire_data = get_time_to_hire()

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        x=time_to_hire_data["job_id"].astype(str),  # Treat Job IDs as categorical
        y=time_to_hire_data["avg_time_to_hire"],
    )
    plt.title("Time to Hire Trends by Job ID")
    plt.xlabel("Job IDs")
    plt.ylabel("Average Time to Hire (Days)")

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")
