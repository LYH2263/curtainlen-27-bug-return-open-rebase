from fastapi import APIRouter, Query
from app.schemas.estimate import EstimateRequest
from app.services import estimate_service
router = APIRouter()
@router.get("/estimate")
def get_est(
    window_id: int = Query(...),
    fabric_id: int = Query(...),
    save: bool = False,
    return_left_cm: float = Query(0.0, ge=0),
    return_right_cm: float = Query(0.0, ge=0),
):
    return estimate_service.run_estimate(
        window_id, fabric_id, save, "", return_left_cm, return_right_cm
    )
@router.post("/estimate")
def post_est(body: EstimateRequest):
    return estimate_service.run_estimate(
        body.window_id, body.fabric_id, body.save, body.note,
        body.return_left_cm, body.return_right_cm,
    )
