from drivers import openevolve_driver as drv


def test_load_env_parses_key(tmp_path):
    p = tmp_path / ".env"
    p.write_text("GEMINI_API_KEY=abc\n# comment\n\n")
    assert drv.load_env(str(p)) == {"GEMINI_API_KEY": "abc"}


def test_score_train_returns_combined_score():
    r = drv.score_train("policy.py")
    assert r.metrics["combined_score"] > 0
    assert r.artifacts["error"] == ""


def test_score_train_error_scores_zero(tmp_path):
    bad = tmp_path / "bad.py"
    bad.write_text("import os\ndef decide(*a): return 0.0\n")
    r = drv.score_train(str(bad))
    assert r.metrics["combined_score"] == 0
    assert r.artifacts["error"]


def test_build_config_sets_key_and_guards():
    cfg = drv.build_config("drivers/openevolve.yaml", "k")
    assert cfg.llm.api_key == "k"
    assert cfg.enforce_evolve_blocks and cfg.diff_based_evolution
    assert cfg.evaluator.timeout == 10
    assert "EVOLVE-BLOCK" in cfg.prompt.system_message


def test_main_without_key_exits_one(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert drv.main(["--iterations", "1"]) == 1


def test_score_train_is_self_contained():
    # OpenEvolve writes the evaluator's source into a temp module; it must run with no module globals.
    import inspect
    ns = {}
    exec(inspect.getsource(drv.score_train), ns)
    r = ns["score_train"]("policy.py")
    assert r.metrics["combined_score"] > 0


def test_write_history_from_trace(tmp_path):
    import json
    recs = [
        {"iteration": 1, "child_changes_description": "wider margin", "child_metrics": {"combined_score": 31.0}},
        {"iteration": 2, "child_changes_description": "longer horizon", "child_metrics": {"combined_score": 33.0}},
        {"iteration": 3, "child_changes_description": "bad idea", "child_metrics": {"combined_score": 0.0}},
    ]
    (tmp_path / "evolution_trace.jsonl").write_text("\n".join(json.dumps(r) for r in recs) + "\n")
    drv.write_history(str(tmp_path), seed_score=32.42)
    text = (tmp_path / "history.md").read_text()
    assert "| 0 | seed | 32.42 | baseline |" in text
    assert "| 1 | wider margin | 31.00 | no |" in text
    assert "| 2 | longer horizon | 33.00 | yes |" in text
    assert "| 3 | bad idea | 0.00 | no |" in text


def test_main_returns_two_when_nothing_beats_seed(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    seed = open("policy.py").read()

    class Stub:
        best_code = seed
        best_score = 32.42

    monkeypatch.setattr(drv, "run_evolution", lambda **kw: Stub())
    assert drv.main(["--iterations", "1"]) == 2
