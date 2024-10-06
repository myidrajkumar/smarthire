"""APIs which are used across but could not be categorized"""

from fastapi import APIRouter

from db.connect import get_business_units, get_jds_for_bu_db

router = APIRouter()


@router.get("/businessunits")
async def get_businessunits():
    """Retrieving business units"""

    results = get_business_units()
    return {"message": "Success", "data": results}


@router.get("/businessunits/{bu_id}/jds")
async def get_jds_for_bu(bu_id):
    """Getting JD titles for a specific BU"""

    results = get_jds_for_bu_db(bu_id)
    return {"message": "Success", "data": results}
