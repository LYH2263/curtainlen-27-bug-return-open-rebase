import json
import sqlite3

import pytest

from app.engines.curtain_math import fabric_meters
from app.repositories import history


@pytest.fixture
def db(tmp_path, monkeypatch):
    conn = sqlite3.connect(tmp_path / "test.db")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
    CREATE TABLE windows(id INTEGER PRIMARY KEY,name TEXT,width REAL,height REAL,fullness REAL,data_quality TEXT,note TEXT);
    CREATE TABLE fabrics(id INTEGER PRIMARY KEY,name TEXT,fabric_width REAL,hem_top REAL,hem_bottom REAL,data_quality TEXT,note TEXT);
    CREATE TABLE calc_runs(id INTEGER PRIMARY KEY AUTOINCREMENT,window_id INT,fabric_id INT,result_json TEXT,note TEXT,created_at TEXT);
    """)
    conn.execute("INSERT INTO windows VALUES (1,'客厅',3.0,2.6,2.0,'clean','')")
    conn.execute("INSERT INTO fabrics VALUES (1,'遮光1.4m',1.4,0.10,0.15,'clean','')")
    conn.commit()

    def connect():
        c = sqlite3.connect(tmp_path / "test.db")
        c.row_factory = sqlite3.Row
        return c

    monkeypatch.setattr(history, "connect", connect)
    return conn


def test_detail_returns_persisted_snapshot(db):
    """保存进历史后，详情页成品宽/幅数/米数/回位厘米只能来自落库快照。"""
    snap = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 15.0, 25.0)
    run_id = history.insert_run(1, 1, snap, "带左右回位")

    got = history.get_run(run_id)["result"]
    assert got == snap
    assert got["return_left_cm"] == 15.0
    assert got["return_right_cm"] == 25.0
    # 成品宽必须已计入回位：(3.0 + 0.40) * 2.0
    assert got["finished_width"] == 6.8
    assert got["panels"] == snap["panels"]
    assert got["meters"] == snap["meters"]


def test_list_and_detail_share_snapshot(db):
    """列表行与详情页对同一编号必须返回同一套数字。"""
    snap = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 10.0, 10.0)
    run_id = history.insert_run(1, 1, snap)

    listed = next(r for r in history.list_runs() if r["id"] == run_id)["result"]
    detail = history.get_run(run_id)["result"]
    assert listed == detail == snap


def test_old_run_pinned_after_window_fabric_changes(db):
    """旧编号钉住当初成品宽与米数：之后窗宽、门幅、回位全改也不重算。"""
    old = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 15.0, 25.0)
    run_id = history.insert_run(1, 1, old)

    # 改窗宽、门幅与褶量，模拟“再改回位测新单”之后的当下参数。
    db.execute("UPDATE windows SET width=4.2, fullness=2.5 WHERE id=1")
    db.execute("UPDATE fabrics SET fabric_width=2.8 WHERE id=1")
    db.commit()

    pinned = history.get_run(run_id)["result"]
    assert pinned == old

    # 新单吃新参数与新回位，另起一行。
    new = fabric_meters(4.2, 2.6, 2.5, 0.10, 0.15, 2.8, 5.0, 0.0)
    new_id = history.insert_run(1, 1, new)
    assert new_id != run_id
    assert history.get_run(run_id)["result"] == old
    assert history.get_run(new_id)["result"] == new


def test_snapshot_json_untouched(db):
    """result_json 原样出库，不注入任何开放视图片段字段。"""
    snap = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 15.0, 25.0)
    run_id = history.insert_run(1, 1, snap)
    raw = db.execute("SELECT result_json FROM calc_runs WHERE id=?", (run_id,)).fetchone()[0]
    assert history.get_run(run_id)["result"] == json.loads(raw)
