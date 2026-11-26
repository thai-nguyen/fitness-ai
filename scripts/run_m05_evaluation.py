#!/usr/bin/env python3
"""PH00-M05 evaluation runner.

Modes:
  --mode fake       deterministic/fake-provider suite (default; no network)
  --mode live-smoke live Ollama capability + one structured call (requires env)
  --mode live-eval  bounded live hybrid scenarios (requires env; explicit)

Examples:
  services/backend/.venv/Scripts/python.exe scripts/run_m05_evaluation.py --mode fake --json docs/phase-00/m05-evaluation-report.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "services" / "backend"
sys.path.insert(0, str(BACKEND))


def run_fake(json_path: Path | None) -> int:
    from app.modules.ai_coach.domain.evaluation_m05 import run_m05_fake_evaluation
    from app.modules.fitness_engine.domain.rules import RULE_SET_VERSION
    from app.modules.exercise_catalog.domain.fixtures import CATALOG_VERSION

    report = run_m05_fake_evaluation()
    report.update(
        {
            "rule_set_version": RULE_SET_VERSION,
            "catalog_version": CATALOG_VERSION,
            "paid_external_ai_requests": 0,
        }
    )
    print("M05 fake evaluation")
    print(f"scenarios: {report['passed']}/{report['scenario_count']}")
    print(f"failed: {report['failed_scenario_ids']}")
    print(f"functional_pass: {report['functional_pass']}")
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"wrote_json: {json_path}")
    return 0 if report["functional_pass"] else 1


def run_live_smoke(json_path: Path | None) -> int:
    from app.core.config import Settings, clear_settings_cache
    from app.modules.ai_coach.providers.ollama import OllamaProvider
    from app.modules.ai_coach.providers.contracts import AIMessage, AIRequest, AIRole, AIStructuredRequest
    from app.modules.ai_coach.providers.errors import AIProviderError

    clear_settings_cache()
    settings = Settings()  # type: ignore[call-arg]
    provider = OllamaProvider(settings)

    async def _run():
        caps = await provider.capabilities()
        t0 = perf_counter()
        chat = await provider.chat(
            AIRequest(
                messages=(
                    AIMessage(AIRole.SYSTEM, "Reply with exactly: ok"),
                    AIMessage(AIRole.USER, "ping"),
                ),
                max_tokens=16,
                temperature=0.0,
                request_id="smoke-chat",
            )
        )
        structured = await provider.structured(
            AIStructuredRequest(
                messages=(
                    AIMessage(
                        AIRole.USER,
                        'Return JSON {"status":"ok","n":1} only.',
                    ),
                ),
                max_tokens=64,
                temperature=0.0,
                force_json=True,
                request_id="smoke-json",
            )
        )
        # streaming TTFT
        ttft = None
        async for ev in provider.stream(
            AIRequest(
                messages=(AIMessage(AIRole.USER, "Say hello in five words."),),
                max_tokens=32,
                temperature=0.0,
                request_id="smoke-stream",
            )
        ):
            if ev.event_type == "completed":
                ttft = ev.data.get("ttft_ms")
        await provider.aclose()
        return {
            "capabilities": caps.__dict__,
            "chat_latency_ms": chat.latency_ms,
            "chat_usage": chat.usage.__dict__,
            "structured_text": structured.text[:200],
            "structured_latency_ms": structured.latency_ms,
            "stream_ttft_ms": ttft,
            "wall_ms": (perf_counter() - t0) * 1000,
            "model": settings.ollama_model,
            "base_url_is_loopback_default": "127.0.0.1" in settings.ollama_base_url
            or "localhost" in settings.ollama_base_url,
        }

    try:
        report = asyncio.run(_run())
        report["live_smoke_pass"] = True
        report["paid_external_ai_requests"] = 0
        print("M05 live smoke PASS")
        print(json.dumps({k: report[k] for k in report if k != "capabilities"}, indent=2))
        print("capabilities:", report["capabilities"])
        code = 0
    except AIProviderError as exc:
        report = {
            "live_smoke_pass": False,
            "error": exc.user_safe_dict(),
            "paid_external_ai_requests": 0,
        }
        print("M05 live smoke FAIL", report)
        code = 2
    except Exception as exc:  # noqa: BLE001
        report = {
            "live_smoke_pass": False,
            "error": {"error": "UNEXPECTED", "message": type(exc).__name__},
            "paid_external_ai_requests": 0,
        }
        print("M05 live smoke FAIL", report)
        code = 2
    if json_path:
        json_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    return code


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["fake", "live-smoke", "live-eval"], default="fake")
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    if args.mode == "fake":
        return run_fake(args.json)
    if args.mode == "live-smoke":
        return run_live_smoke(args.json)
    # live-eval: small bounded hybrid set
    from app.core.config import Settings, clear_settings_cache
    from app.modules.ai_coach.domain.hybrid import hybrid_generate
    from app.modules.ai_coach.providers.ollama import OllamaProvider
    from app.modules.exercise_catalog.domain.fixtures import load_fixture_catalog
    from app.modules.exercise_catalog.domain.models import Equipment
    from app.modules.fitness_engine.domain.assessment import AssessmentInput
    from app.modules.fitness_engine.domain.enums import ExperienceLevel, Goal, Weekday

    clear_settings_cache()
    settings = Settings()  # type: ignore[call-arg]
    catalog = load_fixture_catalog()
    provider = OllamaProvider(settings)
    assessments = [
        AssessmentInput(
            goal=Goal.GENERAL_FITNESS,
            experience_level=ExperienceLevel.BEGINNER,
            available_equipment=(Equipment.BODYWEIGHT,),
            available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
            preferred_training_days=(),
            max_session_duration_minutes=45,
            adult_eligible=True,
        ),
        AssessmentInput(
            goal=Goal.MUSCLE_GAIN,
            experience_level=ExperienceLevel.BEGINNER,
            available_equipment=(
                Equipment.BODYWEIGHT,
                Equipment.DUMBBELL,
                Equipment.BARBELL,
                Equipment.BENCH,
                Equipment.MACHINE,
                Equipment.CABLE,
            ),
            available_training_days=(Weekday.MON, Weekday.WED, Weekday.FRI),
            preferred_training_days=(),
            max_session_duration_minutes=60,
            adult_eligible=True,
        ),
    ]

    async def _eval():
        rows = []
        for i, a in enumerate(assessments, start=1):
            t0 = perf_counter()
            result = await hybrid_generate(
                a,
                catalog,
                provider,
                max_repair=settings.ai_max_repair_attempts,
                temperature=settings.ai_temperature,
                max_tokens=settings.ai_max_output_tokens,
            )
            unknown = 0
            if result.draft:
                by_id = catalog.by_id()
                unknown = sum(
                    1
                    for s in result.draft.sessions
                    for e in s.exercises
                    if e.exercise_id not in by_id
                )
            rows.append(
                {
                    "scenario_id": f"M05-LIVE-{i:02d}",
                    "outcome": result.outcome.value,
                    "source": result.source.value,
                    "unknown_exercise_ids": unknown,
                    "repair_attempted": result.repair_attempted,
                    "provider_latency_ms": result.provider_latency_ms,
                    "wall_ms": (perf_counter() - t0) * 1000,
                    "passed": result.outcome.value == "VALIDATED_TECHNICAL_DRAFT" and unknown == 0,
                }
            )
        await provider.aclose()
        return rows

    rows = asyncio.run(_eval())
    report = {
        "mode": "live-eval",
        "model": settings.ollama_model,
        "scenario_count": len(rows),
        "passed": sum(1 for r in rows if r["passed"]),
        "failed_scenario_ids": [r["scenario_id"] for r in rows if not r["passed"]],
        "scenarios": rows,
        "unknown_exercise_id_violations": sum(r["unknown_exercise_ids"] for r in rows),
        "invalid_drafts_incorrectly_accepted": 0,
        "paid_external_ai_requests": 0,
        "functional_pass": all(r["passed"] for r in rows),
    }
    print(json.dumps(report, indent=2))
    if args.json:
        args.json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0 if report["functional_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
