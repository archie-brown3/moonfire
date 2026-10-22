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
