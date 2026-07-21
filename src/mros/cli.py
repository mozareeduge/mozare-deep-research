from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from .audit import audit_project
from .coverage import compute_question_coverage
from .events import append_event, verify_event_chain
from .io import dump_data, load_data, load_model_list, read_jsonl
from .method import check_operational_language, compile_method
from .models import EvidenceCard, EventRecord, HandoffReceipt, QueryRecord, ResearchQuestion, ClaimRecord, RunState
from .project import copy_claude_harness, init_project
from .quotes import verify_quote_file
from .runs import OutputProfile, ResearchMode, RunStage, append_run_record, init_run, summarize_run, update_run_state, validate_run
from .verify import verify_project


def _root(value: str) -> Path:
    return Path(value).expanduser().resolve()


def cmd_init(args: argparse.Namespace) -> int:
    root = _root(args.path)
    init_project(root, args.project_id, args.title, force=args.force)
    if args.with_claude:
        copy_claude_harness(root)
    print(f"Initialized MROS project at {root}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    report = audit_project(_root(args.path), release_mode=False)
    print(report.model_dump_json(indent=2))
    return 0 if report.ok else 1


def cmd_audit(args: argparse.Namespace) -> int:
    report = audit_project(_root(args.path), release_mode=args.release)
    if args.json:
        print(report.model_dump_json(indent=2))
    else:
        print(f"MROS audit: {'PASS' if report.ok else 'FAIL'}")
        for issue in report.issues:
            loc = f" [{issue.path}]" if issue.path else ""
            obj = f" ({issue.object_id})" if issue.object_id else ""
            print(f"- {issue.severity.upper()} {issue.code}{loc}{obj}: {issue.message}")
        print(f"Blockers: {len(report.blockers)} | Warnings: {len(report.warnings)}")
    return 0 if report.ok else 1


def cmd_quote(args: argparse.Namespace) -> int:
    match = verify_quote_file(_root(args.source), args.text, allow_normalized=not args.exact_only)
    print(json.dumps(match.__dict__, ensure_ascii=False, indent=2))
    return 0 if match.matched else 1


def cmd_event_append(args: argparse.Namespace) -> int:
    path = _root(args.path) / "events" / "events.jsonl"
    event = EventRecord(
        event_id=args.event_id,
        actor=args.actor,
        action=args.action,
        input_ids=args.input or [],
        output_ids=args.output or [],
        tool=args.tool,
        decision_note=args.note or "",
    )
    result = append_event(path, event)
    state_path = _root(args.path) / "research" / "state.yaml"
    if state_path.exists():
        state = RunState.model_validate(load_data(state_path))
        updated = RunState.model_validate({
            **state.model_dump(mode="python"),
            "last_event_hash": result.event_hash,
            "updated_at": result.timestamp,
        })
        dump_data(state_path, updated)
    print(result.model_dump_json(indent=2))
    return 0


def cmd_event_verify(args: argparse.Namespace) -> int:
    issues = verify_event_chain(_root(args.path) / "events" / "events.jsonl")
    if issues:
        print("\n".join(issues))
        return 1
    print("Event chain valid")
    return 0


def cmd_coverage(args: argparse.Namespace) -> int:
    root = _root(args.path)
    questions = load_model_list(root / "research/questions.yaml", "questions", ResearchQuestion)
    claims = load_model_list(root / "claims/claims.yaml", "claims", ClaimRecord)
    cards = load_model_list(root / "evidence/cards/cards.yaml", "cards", EvidenceCard)
    queries = [QueryRecord.model_validate(row) for row in read_jsonl(root / "queries/ledger.jsonl")]
    result = [x.to_dict() for x in compute_question_coverage(questions, claims, cards, queries)]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(x["requirement_met"] for x in result if x["critical"]) else 1


def cmd_compile(args: argparse.Namespace) -> int:
    root = _root(args.path)
    path = compile_method(root)
    issues = check_operational_language(root)
    print(f"Compiled method kernel to {path}")
    if issues:
        print("Operational language check failed:")
        print("\n".join(f"- {x}" for x in issues))
        return 1
    print("Operational language check passed")
    return 0


def cmd_handoff(args: argparse.Namespace) -> int:
    root = _root(args.path)
    receipt = HandoffReceipt(
        objective_completed=args.objective,
        state_files_changed=args.changed or [],
        unresolved=args.unresolved or [],
        next_actions=args.next or [],
        verification=args.verification or [],
    )
    dump_data(root / "research/handoff.yaml", receipt)
    print(receipt.model_dump_json(indent=2))
    return 0




def cmd_run_init(args: argparse.Namespace) -> int:
    state = init_run(
        _root(args.path),
        mode=ResearchMode(args.mode),
        title=args.title,
        source_lanes=args.source_lane or [],
        excluded_lanes=args.exclude_lane or [],
        output_profile=OutputProfile(args.output_profile),
        route_reason=args.route_reason or "",
        requirements=args.requirement or [],
        force=args.force,
    )
    print(state.model_dump_json(indent=2))
    return 0


def cmd_run_append(args: argparse.Namespace) -> int:
    if args.json_file:
        raw = _root(args.json_file).read_text(encoding="utf-8")
    elif args.json:
        raw = args.json
    else:
        raw = sys.stdin.read()
    if not raw.strip():
        raise ValueError("provide --json-file, --json, or JSON on stdin")
    record = json.loads(raw)
    result = append_run_record(_root(args.path), args.kind, record)
    print(result.model_dump_json(indent=2))
    return 0


def cmd_run_state(args: argparse.Namespace) -> int:
    changes: dict[str, object] = {}
    if args.status is not None:
        changes["status"] = args.status
    if args.stage is not None:
        changes["current_stage"] = args.stage
    if args.next is not None:
        changes["next_actions"] = args.next
    if args.open_question is not None:
        changes["open_questions"] = args.open_question
    if args.user_visible_status is not None:
        changes["user_visible_status"] = args.user_visible_status
    state = update_run_state(_root(args.path), **changes)
    print(state.model_dump_json(indent=2))
    return 0


def cmd_run_validate(args: argparse.Namespace) -> int:
    result = validate_run(_root(args.path))
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result["ok"] else 1


def cmd_run_summary(args: argparse.Namespace) -> int:
    result = summarize_run(_root(args.path))
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result["ok"] else 1

def cmd_verify(args: argparse.Namespace) -> int:
    result = verify_project(_root(args.path), phase_stop=args.phase_stop)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


def cmd_doctor(args: argparse.Namespace) -> int:
    root = _root(args.path)
    checks = {
        "project_marker": (root / ".mros/project.yaml").exists(),
        "claude_kernel": (root / "CLAUDE.md").exists(),
        "claude_settings": (root / ".claude/settings.json").exists(),
        "methodology_config": (root / "config/methodology.yaml").exists(),
        "event_log": (root / "events/events.jsonl").exists(),
    }
    try:
        import paperqa  # noqa: F401
        checks["paperqa_optional"] = True
    except ImportError:
        checks["paperqa_optional"] = False
    print(json.dumps(checks, indent=2))
    return 0 if all(v for k, v in checks.items() if k != "paperqa_optional") else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mros", description="Mozare Research Operating System")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init"); p.add_argument("path"); p.add_argument("--project-id", required=True); p.add_argument("--title", required=True); p.add_argument("--force", action="store_true"); p.add_argument("--with-claude", action="store_true"); p.set_defaults(func=cmd_init)
    p = sub.add_parser("validate"); p.add_argument("path", nargs="?", default="."); p.set_defaults(func=cmd_validate)
    p = sub.add_parser("audit"); p.add_argument("path", nargs="?", default="."); p.add_argument("--release", action="store_true"); p.add_argument("--json", action="store_true"); p.set_defaults(func=cmd_audit)
    p = sub.add_parser("quote-verify"); p.add_argument("source"); p.add_argument("--text", required=True); p.add_argument("--exact-only", action="store_true"); p.set_defaults(func=cmd_quote)
    p = sub.add_parser("event-append"); p.add_argument("path", nargs="?", default="."); p.add_argument("--event-id", required=True); p.add_argument("--actor", required=True); p.add_argument("--action", required=True); p.add_argument("--input", action="append"); p.add_argument("--output", action="append"); p.add_argument("--tool"); p.add_argument("--note"); p.set_defaults(func=cmd_event_append)
    p = sub.add_parser("event-verify"); p.add_argument("path", nargs="?", default="."); p.set_defaults(func=cmd_event_verify)
    p = sub.add_parser("coverage"); p.add_argument("path", nargs="?", default="."); p.set_defaults(func=cmd_coverage)
    p = sub.add_parser("compile-method"); p.add_argument("path", nargs="?", default="."); p.set_defaults(func=cmd_compile)
    p = sub.add_parser("handoff"); p.add_argument("path", nargs="?", default="."); p.add_argument("--objective", required=True); p.add_argument("--changed", action="append"); p.add_argument("--unresolved", action="append"); p.add_argument("--next", action="append"); p.add_argument("--verification", action="append"); p.set_defaults(func=cmd_handoff)
    p = sub.add_parser("verify"); p.add_argument("path", nargs="?", default="."); p.add_argument("--phase-stop", action="store_true"); p.set_defaults(func=cmd_verify)
    p = sub.add_parser("doctor"); p.add_argument("path", nargs="?", default="."); p.set_defaults(func=cmd_doctor)
    p = sub.add_parser("run-init"); p.add_argument("path"); p.add_argument("--mode", choices=[x.value for x in ResearchMode], required=True); p.add_argument("--title"); p.add_argument("--source-lane", action="append"); p.add_argument("--exclude-lane", action="append"); p.add_argument("--output-profile", choices=[x.value for x in OutputProfile], default=OutputProfile.RESEARCH_NOTE.value); p.add_argument("--route-reason"); p.add_argument("--requirement", action="append"); p.add_argument("--force", action="store_true"); p.set_defaults(func=cmd_run_init)
    p = sub.add_parser("run-append"); p.add_argument("path"); p.add_argument("--kind", choices=["query", "source", "term", "evidence", "claim"], required=True); group = p.add_mutually_exclusive_group(); group.add_argument("--json-file"); group.add_argument("--json"); p.set_defaults(func=cmd_run_append)
    p = sub.add_parser("run-state"); p.add_argument("path"); p.add_argument("--status", choices=["active", "needs_input", "blocked", "complete"]); p.add_argument("--stage", choices=[x.value for x in RunStage]); p.add_argument("--next", action="append"); p.add_argument("--open-question", action="append"); p.add_argument("--user-visible-status"); p.set_defaults(func=cmd_run_state)
    p = sub.add_parser("run-validate"); p.add_argument("path"); p.set_defaults(func=cmd_run_validate)
    p = sub.add_parser("run-summary"); p.add_argument("path"); p.set_defaults(func=cmd_run_summary)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        code = args.func(args)
    except (ValidationError, FileNotFoundError, FileExistsError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        code = 2
    raise SystemExit(code)
