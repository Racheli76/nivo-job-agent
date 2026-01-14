from mocks import mock_analyze_cv, mock_match_job, mock_simulate_interview


def test_mock_analyze_cv_he():
    out = mock_analyze_cv('שלום', 'he')
    assert out['score'] == 80
    assert 'שפרי' in out['bullets'][0] or isinstance(out['summary'], str)


def test_mock_analyze_cv_en():
    out = mock_analyze_cv('hello', 'en')
    assert out['score'] == 80
    assert 'Improve' in out['suggestions'][0] or isinstance(out['summary'], str)


def test_mock_match_job():
    out = mock_match_job('cv text', 'job desc', 'he')
    assert out['match_score'] == 70
    assert 'cover_letter' in out


def test_mock_simulate_interview():
    out = mock_simulate_interview('Engineer', 'en')
    assert isinstance(out['questions'], list)
    assert 'Answer briefly' in out['advice'] or isinstance(out['advice'], str)
