import pytest
from app.engines.curtain_math import fabric_meters

def test_living_room():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    assert r["panels"] == 5
    assert r["cut_height"] == 2.85
    assert r["meters"] == 14.25

def test_single_panel_narrow():
    r = fabric_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8)
    assert r["panels"] == 1
    assert r["meters"] == 2.0

def test_zero_returns_keep_old_result():
    """两侧回位皆 0 时，结果须与改造前同窗同布完全一致。"""
    old = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    new = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 0.0, 0.0)
    for k in ("finished_width", "panels", "cut_height", "meters"):
        assert new[k] == old[k]
    assert new["return_left_cm"] == 0
    assert new["return_right_cm"] == 0

def test_returns_widen_finished_width():
    """左右回位厘米换算成米加进窗宽，再乘褶量得到成品宽。"""
    base = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 15.0, 25.0)
    assert r["finished_width"] == round((3.0 + 0.40) * 2.0, 3)
    assert r["panels"] >= base["panels"]
    assert r["meters"] >= base["meters"]
    # cut_height 与回位无关
    assert r["cut_height"] == base["cut_height"]

def test_negative_return_raises():
    with pytest.raises(ValueError):
        fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, -1.0, 0.0)
    with pytest.raises(ValueError):
        fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 0.0, -5.0)
