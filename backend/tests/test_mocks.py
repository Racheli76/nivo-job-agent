from mocks import mock_analyze_cv, mock_match_job, mock_simulate_interview


def test_mock_analyze_cv_he():
    out = mock_analyze_cv('שלום', 'he')
    # Score should be between 0-100
    assert isinstance(out['score'], int) and 0 <= out['score'] <= 100
    # Check for improved score
    assert isinstance(out['score_after_improvement'], int) and 0 <= out['score_after_improvement'] <= 100
    # Check for new CV fields
    assert 'improved_cv' in out and isinstance(out['improved_cv'], str)
    assert 'summary' in out and isinstance(out['summary'], str)
    assert 'suggestions' in out and isinstance(out['suggestions'], list)


def test_mock_analyze_cv_en():
    out = mock_analyze_cv('hello', 'en')
    # Score should be between 0-100
    assert isinstance(out['score'], int) and 0 <= out['score'] <= 100
    # Check for improved score
    assert isinstance(out['score_after_improvement'], int) and 0 <= out['score_after_improvement'] <= 100
    # Check for new CV fields
    assert 'improved_cv' in out and isinstance(out['improved_cv'], str)
    assert 'summary' in out and isinstance(out['summary'], str)
    assert 'suggestions' in out and isinstance(out['suggestions'], list)


def test_mock_match_job():
    out = mock_match_job('cv text', 'job desc', 'he')
    assert out['match_score'] == 70
    assert 'cover_letter' in out


def test_mock_analyze_cv_with_job_desc():
    out = mock_analyze_cv('cv text', 'en', 'job desc')
    # Check base fields
    assert 'score' in out and 'score_after_improvement' in out
    assert 'improved_cv' in out and 'summary' in out
    # Check conditional fields when job_desc provided
    assert 'tailored_cv' in out and isinstance(out['tailored_cv'], str)
    assert 'missing_skills' in out and isinstance(out['missing_skills'], list)


def test_mock_simulate_interview():
    out = mock_simulate_interview('Engineer', 'en')
    assert isinstance(out['questions'], list)
    assert 'Answer briefly' in out['advice'] or isinstance(out['advice'], str)
