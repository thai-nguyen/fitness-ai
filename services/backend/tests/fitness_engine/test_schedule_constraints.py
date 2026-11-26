"""F-M04-003 schedule hard vs soft constraint evidence."""

from __future__ import annotations

from app.modules.fitness_engine.domain.enums import Weekday
from app.modules.fitness_engine.domain.schedule import allocate_schedule
from app.modules.fitness_engine.domain.templates import TEMPLATES


def _tmpl(template_id: str):
    return next(t for t in TEMPLATES if t.template_id == template_id)


def test_hard_insufficient_days_for_template():
    result = allocate_schedule((Weekday.MON,), (), _tmpl("tmpl_gym_strength"))
    assert result.days is None
    assert any(i.code == "INSUFFICIENT_DAYS" for i in result.issues)


def test_hard_no_available_days():
    result = allocate_schedule((), (Weekday.MON,), _tmpl("tmpl_beginner_full_body"))
    assert result.days is None
    assert any(i.code == "NO_AVAILABLE_DAYS" for i in result.issues)


def test_preferred_days_honored_when_feasible():
    result = allocate_schedule(
        (Weekday.MON, Weekday.WED, Weekday.FRI),
        (Weekday.FRI, Weekday.MON),
        _tmpl("tmpl_beginner_full_body"),
    )
    assert result.days is not None
    assert Weekday.MON in result.days
    assert Weekday.FRI in result.days


def test_soft_spacing_prefers_gaps_but_allows_consecutive_when_only_option():
    """BR-SCHED-005 is soft: consecutive days are allowed when availability forces it."""
    result = allocate_schedule(
        (Weekday.MON, Weekday.TUE, Weekday.WED),
        (),
        _tmpl("tmpl_beginner_full_body"),
    )
    assert result.days is not None
    assert len(result.days) >= 2
    # No hard error for consecutive days — soft preference only
    assert result.issues == ()


def test_template_min_days_not_silently_relaxed():
    tmpl = _tmpl("tmpl_gym_strength")
    assert tmpl.min_days == 3
    result = allocate_schedule((Weekday.MON, Weekday.WED), (), tmpl)
    assert result.days is None
