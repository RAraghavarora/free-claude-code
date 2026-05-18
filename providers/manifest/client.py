"""Manifest provider implementation."""

from typing import Any

from loguru import logger

from core.anthropic import ReasoningReplayMode, build_base_request_body
from core.anthropic.conversion import OpenAIConversionError
from providers.base import ProviderConfig
from providers.defaults import MANIFEST_DEFAULT_BASE
from providers.exceptions import InvalidRequestError
from providers.openai_compat import OpenAIChatTransport


class ManifestProvider(OpenAIChatTransport):
    """Manifest provider using OpenAI-compatible chat completions endpoint."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="MANIFEST",
            base_url=config.base_url or MANIFEST_DEFAULT_BASE,
            api_key=config.api_key,
        )

    def _build_request_body(
        self, request: Any, thinking_enabled: bool | None = None
    ) -> dict:
        """Build an OpenAI-compatible request body from the Anthropic Messages request."""
        thinking_enabled = self._is_thinking_enabled(request, thinking_enabled)
        try:
            return build_base_request_body(
                request,
                reasoning_replay=ReasoningReplayMode.REASONING_CONTENT
                if thinking_enabled
                else ReasoningReplayMode.DISABLED,
            )
        except OpenAIConversionError as exc:
            logger.warning(
                "MANIFEST_REQUEST_BUILD_FAILED model={} thinking_enabled={} exc_type={}",
                getattr(request, "model", None),
                thinking_enabled,
                type(exc).__name__,
            )
            raise InvalidRequestError(str(exc)) from exc
