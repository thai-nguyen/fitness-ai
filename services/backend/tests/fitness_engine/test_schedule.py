from app.modules.fitness_engine.domain.enums import Weekday
from app.modules.fitness_engine.domain.schedule import allocate_schedule
from app.modules.fitness_engine.domain.templates import TEMPLATES


def test_allocates_within_available():
    tmpl = next(t for t in TEMPLATES if t.template_id == "tmpl_beginner_full_body")
    result = allocate_schedule(
        (Weekday.MON, Weekday.WED, Weekday.FRI),
        (Weekday.MON, Weekday.FRI),
        tmpl,
    )
    assert result.days is not None
    assert set(result.days).issubset({Weekday.MON, Weekday.WED, Weekday.FRI})
    assert Weekday.MON in result.days
    assert Weekday.FRI in result.days


def test_insufficient_days():
    tmpl = next(t for t in TEMPLATES if t.template_id == "tmpl_gym_strength")
    result = allocate_schedule((Weekday.MON,), (), tmpl)
    assert result.days is None
    assert any(i.code == "INSUFFICIENT_DAYS" for i in result.issues)
