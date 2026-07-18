from pathlib import Path

from mros.method import check_operational_language, compile_method, load_method_config, render_kernel


def test_method_compiles_kernel_and_profiles(project: Path):
    package_root = Path(__file__).resolve().parents[1]
    (project / "config").mkdir(exist_ok=True)
    (project / "config" / "methodology.yaml").write_text(
        (package_root / "config" / "methodology.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    out = compile_method(project)
    assert out.exists()
    assert (project / ".mros/compiled/run-profiles/evidence.md").exists()
    assert "formal claim" in out.read_text(encoding="utf-8")


def test_render_kernel_contains_each_invariant():
    root = Path(__file__).resolve().parents[1]
    config = load_method_config(root)
    text = render_kernel(config)
    assert text.count("\n") >= len(config["invariants"])
    for invariant in config["invariants"]:
        assert invariant["operational_rule"] in text


def test_repository_operational_prompts_do_not_use_prohibited_terms():
    root = Path(__file__).resolve().parents[1]
    assert check_operational_language(root) == []
