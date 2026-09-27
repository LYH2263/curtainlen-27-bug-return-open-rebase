from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters
from app.repositories import fabrics, history, settings_repo, windows

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str,
                 return_left_cm: float = 0.0, return_right_cm: float = 0.0):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    # 回位为负直接失败，不落历史
    if float(return_left_cm) < 0 or float(return_right_cm) < 0:
        raise HTTPException(422, "return width must be >= 0")
    calc = fabric_meters(
        w["width"], w["height"], fullness,
        f["hem_top"], f["hem_bottom"], f["fabric_width"],
        return_left_cm, return_right_cm,
    )
    run_id = history.insert_run(window_id, fabric_id, calc, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **calc}
