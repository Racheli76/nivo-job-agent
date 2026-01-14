import sys
import types
import pytest
from services import openai as openai_service
from config import settings


def test_openai_available_false_by_default():
    # default settings.mock_mode is True in .env.example; ensure function respects mock mode
    orig_key = settings.openai_api_key
    orig_mock = settings.mock_mode
    settings.openai_api_key = ''
    settings.mock_mode = True
    try:
        assert openai_service.openai_available() is False
    finally:
        settings.openai_api_key = orig_key
        settings.mock_mode = orig_mock


def test_openai_available_true_when_key_and_not_mock():
    orig_key = settings.openai_api_key
    orig_mock = settings.mock_mode
    settings.openai_api_key = 'sk-test'
    settings.mock_mode = False
    try:
        assert openai_service.openai_available() is True
    finally:
        settings.openai_api_key = orig_key
        settings.mock_mode = orig_mock


def test_call_openai_chat_new_api(monkeypatch):
    # Simulate new OpenAI client with OpenAI class
    fake_openai = types.SimpleNamespace()

    class FakeClient:
        class chat:
            class completions:
                @staticmethod
                def create(model, messages, max_tokens):
                    resp = types.SimpleNamespace()
                    # emulate nested choices / message content
                    choice = types.SimpleNamespace()
                    msg = types.SimpleNamespace()
                    msg.content = 'assistant text from new API'
                    choice.message = msg
                    resp.choices = [choice]
                    return resp

    def FakeOpenAI(api_key=None):
        return FakeClient()

    fake_openai.OpenAI = FakeOpenAI
    monkeypatch.setitem(sys.modules, 'openai', fake_openai)

    out = openai_service.call_openai_chat([{'role': 'user', 'content': 'hello'}], max_tokens=10)
    assert 'assistant text from new API' in out


def test_call_openai_chat_old_api(monkeypatch):
    # Simulate old openai module with ChatCompletion.create
    fake_openai = types.SimpleNamespace()

    class ChatCompletion:
        @staticmethod
        def create(model, messages, max_tokens):
            resp = types.SimpleNamespace()
            choice = types.SimpleNamespace()
            choice_text = types.SimpleNamespace()
            choice_text.content = 'assistant text from old API'
            choice = types.SimpleNamespace()
            choice.message = choice_text
            resp.choices = [choice]
            return resp

    fake_openai.ChatCompletion = ChatCompletion
    fake_openai.api_key = None
    monkeypatch.setitem(sys.modules, 'openai', fake_openai)

    out = openai_service.call_openai_chat([{'role': 'user', 'content': 'hello'}], max_tokens=10)
    assert 'assistant text from old API' in out
