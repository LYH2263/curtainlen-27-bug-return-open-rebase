"""Shape payloads for history storage and open views (return wings)."""

from __future__ import annotations

from copy import deepcopy

from app.engines.helpers import ceil_units


def _recompute_bare(
    width: float,
    height: float,
    fullness: float,
    fabric_width: float,
    hem_top: float,
    hem_bottom: float,
) -> dict:
    """Recompute finished_width / panels / meters from bare window width (no returns)."""
    finished_w = float(width) * float(fullness)
    panels = max(1, ceil_units(finished_w / float(fabric_width)))
    cut_h = float(height) + float(hem_top) + float(hem_bottom)
    meters = panels * cut_h
    return {
        "finished_width": round(finished_w, 3),
        "panels": panels,
        "cut_height": round(cut_h, 3),
        "meters": round(meters, 2),
    }


def has_returns(result: dict) -> bool:
    left = float(result.get("return_left_cm") or 0)
    right = float(result.get("return_right_cm") or 0)
    return left > 0 or right > 0


def open_return_view(result: dict, dims: dict | None = None) -> dict:
    """Keep return_left_cm / return_right_cm, but rebase finished / panels / meters without returns."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if not has_returns(out):
        return out
    width = height = fullness = fabric_width = hem_top = hem_bottom = None
    if dims:
        width = dims.get("width")
        height = dims.get("height")
        fullness = dims.get("fullness")
        fabric_width = dims.get("fabric_width")
        hem_top = dims.get("hem_top")
        hem_bottom = dims.get("hem_bottom")
    if fabric_width is None:
        fabric_width = out.get("fabric_width")
    if cut := out.get("cut_height"):
        if height is None and hem_top is not None and hem_bottom is not None:
            height = float(cut) - float(hem_top) - float(hem_bottom)
    if fullness is None:
        fullness = 2.0
    if None in (width, height, fabric_width, hem_top, hem_bottom):
        return out
    rebuilt = _recompute_bare(
        float(width), float(height), float(fullness),
        float(fabric_width), float(hem_top), float(hem_bottom),
    )
    # Preserve return metadata while replacing the bare-window figures.
    out["finished_width"] = rebuilt["finished_width"]
    out["panels"] = rebuilt["panels"]
    out["cut_height"] = rebuilt["cut_height"]
    out["meters"] = rebuilt["meters"]
    out["open_returns_ignored"] = True
    out["list_return_left_cm"] = out.get("return_left_cm")
    out["list_return_right_cm"] = out.get("return_right_cm")
    return out


def list_summary_view(result: dict, dims: dict | None = None) -> dict:
    """List path applies the same open rebase; return fields stay visible."""
    return open_return_view(result, dims)


def summarize_returns(result: dict) -> dict:
    """Flat view of return flags / bare meters for open consumers."""
    if not isinstance(result, dict):
        return {}
    return {
        "return_left_cm": result.get("return_left_cm"),
        "return_right_cm": result.get("return_right_cm"),
        "finished_width": result.get("finished_width"),
        "panels": result.get("panels"),
        "meters": result.get("meters"),
        "open_returns_ignored": bool(result.get("open_returns_ignored")),
    }
