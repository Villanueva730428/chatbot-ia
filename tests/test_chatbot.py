import types

import pytest

import chatbot


def test_normalize_user_input_strips_and_lowercases() -> None:
    assert chatbot.normalize_user_input("  SaLiR  ") == "salir"


def test_validate_generation_parameters_accepts_valid() -> None:
    chatbot.validate_generation_parameters(temperature=0.0, max_tokens=1, top_p=1.0)
    chatbot.validate_generation_parameters(temperature=2.0, max_tokens=999, top_p=0.0)


@pytest.mark.parametrize(
    "temperature,max_tokens,top_p",
    [
        (-0.1, 10, 1.0),
        (2.1, 10, 1.0),
        (0.5, 0, 1.0),
        (0.5, -1, 1.0),
        (0.5, 10, -0.01),
        (0.5, 10, 1.01),
    ],
)
def test_validate_generation_parameters_rejects_invalid(
    temperature: float, max_tokens: int, top_p: float
) -> None:
    with pytest.raises(ValueError):
        chatbot.validate_generation_parameters(
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )


def test_load_configuration_missing_vars_raises_system_exit(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in chatbot.REQUIRED_ENV_VARS:
        monkeypatch.delenv(var, raising=False)

    with pytest.raises(SystemExit):
        chatbot.load_configuration(load_dotenv_file=False)


def test_load_configuration_normalizes_endpoint_trailing_slash(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT_NAME", "test-deployment")
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    configuration = chatbot.load_configuration(load_dotenv_file=False)
    assert configuration["azure_openai_endpoint"].endswith("/")


def _fake_chat_response(*, content: str, usage: dict | None = None):
    message = types.SimpleNamespace(content=content)
    choice = types.SimpleNamespace(message=message)
    response = types.SimpleNamespace(choices=[choice])
    if usage is not None:
        response.usage = types.SimpleNamespace(**usage)
    return response


def test_extract_token_usage_when_present() -> None:
    response = _fake_chat_response(
        content="hola",
        usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    )

    token_usage = chatbot._extract_token_usage(response)
    assert token_usage is not None
    assert token_usage.prompt_tokens == 10
    assert token_usage.completion_tokens == 5
    assert token_usage.total_tokens == 15


def test_token_tracker_accumulates() -> None:
    tracker = chatbot.TokenTracker()
    tracker.update(chatbot.TokenUsage(prompt_tokens=1, completion_tokens=2, total_tokens=3))
    tracker.update(chatbot.TokenUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30))

    assert tracker.prompt_tokens_total == 11
    assert tracker.completion_tokens_total == 22
    assert tracker.total_tokens_total == 33
