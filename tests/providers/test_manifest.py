"""Manifest provider converts Pydantic content blocks correctly."""

from api.models.anthropic import ContentBlockText, Message, MessagesRequest
from providers.base import ProviderConfig
from providers.manifest import ManifestProvider


def _minimal_config():
    return ProviderConfig(
        api_key="mnfst_unit_test_key",
        base_url="http://localhost:2099/v1",
        rate_limit=40,
        rate_window=60,
        max_concurrency=5,
        http_read_timeout=120,
        http_write_timeout=10,
        http_connect_timeout=10,
        enable_thinking=True,
        proxy="",
        log_raw_sse_events=False,
        log_api_error_tracebacks=False,
    )


def test_build_request_body_with_content_block_text_instances():
    """Regression: assistant/user content lists use ContentBlockText models, not dicts."""
    provider = ManifestProvider(_minimal_config())
    req = MessagesRequest(
        model="manifest/auto",
        messages=[
            Message(
                role="user",
                content=[ContentBlockText(type="text", text="Hello")],
            ),
            Message(
                role="assistant",
                content=[ContentBlockText(type="text", text="Hi there")],
            ),
        ],
        max_tokens=256,
        stream=True,
    )
    body = provider._build_request_body(req, thinking_enabled=False)
    assert body["model"] == "manifest/auto"
    assert body["max_tokens"] == 256
    assert isinstance(body["messages"], list)
    assert len(body["messages"]) >= 2
    assert body["messages"][-2]["role"] == "user"
    assert isinstance(body["messages"][-2]["content"], str)
    assert "Hello" in body["messages"][-2]["content"]
