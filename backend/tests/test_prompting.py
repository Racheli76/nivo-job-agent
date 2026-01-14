import pytest
from services import prompting


def test_build_analyze_cv_prompt_contains_json_keys():
    p = prompting.build_analyze_cv_prompt('some cv text', 'en')
    # Check for required fields in the prompt
    assert 'score' in p and 'summary' in p and 'improved_cv' in p
    assert 'score_after_improvement' in p and 'cover_letter' in p
    # Check for language indicator
    assert 'English' in p or 'en' in p


def test_build_analyze_cv_prompt_hebrew():
    p = prompting.build_analyze_cv_prompt('some cv text', 'he')
    # Check for required fields in Hebrew prompt
    assert 'score' in p and 'summary' in p and 'improved_cv' in p
    assert 'score_after_improvement' in p


def test_build_match_job_prompt_contains_sections():
    p = prompting.build_match_job_prompt('cv text', 'job desc', 'en')
    assert 'match_score' in p and ('JOB DESCRIPTION' in p or 'job desc' in p)
    # Test Hebrew version works too
    p_he = prompting.build_match_job_prompt('cv text', 'job desc', 'he')
    assert 'match_score' in p_he and 'job desc' in p_he


def test_run_analyze_cv_calls_openai(monkeypatch):
    called = {}

    def fake_call(messages, max_tokens=400):
        called['messages'] = messages
        return 'mock-response'

    monkeypatch.setattr(prompting, 'call_openai_chat', fake_call)
    out = prompting.run_analyze_cv('cv text', 'en')
    assert out == 'mock-response'
    assert 'cv text' in called['messages'][0]['content']
