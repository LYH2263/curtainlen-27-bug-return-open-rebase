from app.engines.helpers import ceil_units

# Open-path consumers may rebuild bare-window geometry while keeping return fields.


def fabric_meters(
    window_w: float,
    window_h: float,
    fullness: float,
    hem_top: float,
    hem_bottom: float,
    fabric_width: float,
    return_left_cm: float = 0.0,
    return_right_cm: float = 0.0,
) -> dict:
    if fabric_width <= 0:
        raise ValueError("fabric width required")
    if float(return_left_cm) < 0 or float(return_right_cm) < 0:
        raise ValueError("return width must be >= 0")
    # 两侧回位以厘米登记，换算成米后加进窗宽，再乘褶量得到成品宽
    track_w = float(window_w) + (float(return_left_cm) + float(return_right_cm)) / 100.0
    finished_w = track_w * float(fullness)
    panels = max(1, ceil_units(finished_w / float(fabric_width)))
    cut_h = float(window_h) + float(hem_top) + float(hem_bottom)
    meters = panels * cut_h
    return {
        "return_left_cm": round(float(return_left_cm), 1),
        "return_right_cm": round(float(return_right_cm), 1),
        "finished_width": round(finished_w, 3),
        "panels": panels,
        "cut_height": round(cut_h, 3),
        "meters": round(meters, 2),
        "fabric_width": float(fabric_width),
    }
