import pytest
from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters
from app.services import estimate_service

def test_seed_bedroom():
    assert fabric_meters(2.2, 1.5, 2.0, 0.10, 0.15, 1.4)["panels"] == 4

def test_negative_return_fails_without_history(monkeypatch):
    """任一侧回位为负时接口失败，且历史不增行。"""
    monkeypatch.setattr(estimate_service.windows, "get_window",
                        lambda wid: {"id": wid, "width": 3.0, "height": 2.6,
                                     "fullness": 2.0, "data_quality": "clean"})
    monkeypatch.setattr(estimate_service.fabrics, "get_fabric",
                        lambda fid: {"id": fid, "fabric_width": 1.4,
                                     "hem_top": 0.1, "hem_bottom": 0.15})
    monkeypatch.setattr(estimate_service.settings_repo, "get_all", lambda: {})
    calls = {"n": 0}
    def fake_insert(*a, **k):
        calls["n"] += 1
        return 1
    monkeypatch.setattr(estimate_service.history, "insert_run", fake_insert)
    with pytest.raises(HTTPException) as ei:
        estimate_service.run_estimate(1, 1, True, "", -1.0, 0.0)
    assert ei.value.status_code == 422
    assert calls["n"] == 0
