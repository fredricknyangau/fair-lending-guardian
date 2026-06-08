# ruff: noqa: E402

import crewai_env

crewai_env.configure_crewai_environment()

import copy
import os
from typing import Any

from crewai import LLM, Agent
from dotenv import load_dotenv

load_dotenv()

# Choose LLM provider — set LLM_PROVIDER in .env
# Supported: groq | gemini | ollama | cohere | cerebras
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

# Model identifiers understood by LiteLLM (used by CrewAI under the hood)
MODELS: dict[str, str] = {
    "groq": "groq/llama-3.1-8b-instant",  # 60 req/min free — fast
    "gemini": "gemini/gemini-2.5-flash",  # 60 req/min free — best quality
    "ollama": "ollama/mistral",  # local, zero rate limits
    "cohere": "cohere/command-a-03-2025",  # 1 000 req/month free trial
    "cerebras": "cerebras/llama3.1-8b",  # very fast, OpenAI-compatible
}

if LLM_PROVIDER not in MODELS:
    raise ValueError(
        f"Unknown LLM_PROVIDER='{LLM_PROVIDER}'. " f"Valid options: {', '.join(MODELS)}"
    )

# ─── Fallback chain ──────────────────────────────────────────────────────────
# LLM_FALLBACK_CHAIN = comma-separated providers tried in order when the
# primary hits a rate limit or returns a transient error.
# Example: LLM_FALLBACK_CHAIN=groq,gemini
# Ollama can appear here too (no API key required, zero rate limits).
_fallback_raw = os.getenv("LLM_FALLBACK_CHAIN", "")
FALLBACK_PROVIDERS: list[str] = [
    p.strip()
    for p in _fallback_raw.split(",")
    if p.strip() and p.strip() in MODELS and p.strip() != LLM_PROVIDER
]

# All providers that will actually be used (primary + fallbacks)
_active_providers: set[str] = {LLM_PROVIDER} | set(FALLBACK_PROVIDERS)

# Strip API keys for providers not in the active set so CrewAI's internal
# flow orchestrator cannot auto-detect and default to an inactive provider.
_PROVIDER_KEYS: dict[str, str] = {
    "gemini": "GOOGLE_API_KEY",
    "groq": "GROQ_API_KEY",
    "cohere": "COHERE_API_KEY",
    "cerebras": "CEREBRAS_API_KEY",
}
for _prov, _key in _PROVIDER_KEYS.items():
    if _prov not in _active_providers:
        os.environ.pop(_key, None)

# Register fallbacks with LiteLLM globally — applies to all completion calls
# made by agents AND CrewAI's internal flow orchestration.
try:
    import litellm as _litellm

    if FALLBACK_PROVIDERS:
        _primary = MODELS[LLM_PROVIDER]
        _fallbacks = [MODELS[p] for p in FALLBACK_PROVIDERS]
        _litellm.fallbacks = [{_primary: _fallbacks}]
        # Also register as context-window fallbacks (different error type)
        _litellm.context_window_fallbacks = [{_primary: _fallbacks}]
except ImportError:
    pass

# Patch LiteLLM to strip cache_breakpoint for all models (not all APIs support it)
try:
    from functools import wraps

    import litellm

    original_completion = litellm.completion

    @wraps(original_completion)
    def patched_completion(*args: Any, **kwargs: Any) -> Any:
        """Intercept completion calls and remove unsupported cache_breakpoint."""
        # Remove cache_breakpoint from messages for all models
        messages = kwargs.get("messages", [])
        if isinstance(messages, list):
            for message in messages:
                if isinstance(message, dict):
                    message.pop("cache_breakpoint", None)
        return original_completion(*args, **kwargs)

    litellm.completion = patched_completion
except ImportError:
    pass


class SafeLLM(LLM):
    """CrewAI LiteLLM wrapper that strips cache_breakpoint for all providers.

    Some APIs (Groq, Ollama, Cohere, Cerebras) reject the cache_breakpoint
    field that CrewAI injects into messages. This subclass intercepts every
    completion call and removes it before the request is sent.
    """

    def _prepare_completion_params(
        self,
        messages: Any,
        tools: list[dict[str, Any]] | None = None,
        skip_file_processing: bool = False,
    ) -> dict[str, Any]:
        params = super()._prepare_completion_params(
            messages,
            tools,
            skip_file_processing,
        )

        # Strip cache_breakpoint — not supported by Groq, Ollama, Cohere, Cerebras
        for message in params.get("messages", []):
            if isinstance(message, dict):
                message.pop("cache_breakpoint", None)

        return params

    def call(
        self,
        messages: Any,
        **kwargs: Any,
    ) -> str:
        """Strip cache_breakpoint before sending to any provider that rejects it."""
        # Deep copy messages to avoid modifying originals
        messages_copy = copy.deepcopy(messages)

        # Clean cache_breakpoint from all messages
        for message in messages_copy:
            if isinstance(message, dict):
                message.pop("cache_breakpoint", None)

        # Also remove from kwargs if it's there
        if "cache_breakpoint" in kwargs:
            kwargs.pop("cache_breakpoint", None)

        return super().call(messages_copy, **kwargs)


llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))
llm = SafeLLM(model=MODELS[LLM_PROVIDER], temperature=llm_temperature, max_tokens=1500)

scout_agent = Agent(
    role="financial literacy coach — scout agent",
    goal=(
        "Educate Ujima SACCO members on harvest-cycle financial planning via SMS. "
        "Detect financial stress signals and pass them to the Guardian Agent with "
        "full context including child ages, next harvest date, and current savings."
    ),
    backstory=(
        "You are a trusted financial literacy coach who has worked with smallholder "
        "farmers and market vendors in Western Kenya for 15 years. You speak in warm, "
        "accessible Swahili-influenced English. You never recommend specific loan "
        "products. You send a maximum of 3 messages per day to any member. "
        "You immediately alert the Guardian Agent if a member mentions loan sharks, "
        "debt collectors, or school fee stress. Your kill switch is dial 700."
    ),
    verbose=True,
    allow_delegation=False,  # Prevents extra delegated LLM calls on each turn
    max_iter=3,  # Cap internal ReAct loop — avoids runaway token burn
    llm=llm,
)

guardian_agent = Agent(
    role="loan triage officer — guardian agent",
    goal=(
        "Screen loan applications using cashflow analysis aligned to harvest cycles. "
        "Approve loans up to KES 15,000 independently. Deny only when 3 or more "
        "risk flags are confirmed. Pass all applications scoring 70 to 89 percent "
        "to the Hunter Agent with enriched context."
    ),
    backstory=(
        "You are a TRACK-audited credit analyst who assesses loan applications using "
        "52 weeks of M-Pesa transaction patterns, not occupation labels. You never "
        "use sub-county address, gender, or occupation category as a creditworthiness "
        "indicator. You calculate income stability by comparing weekly inflow "
        "standard deviation against harvest-cycle norms. Every denial must include "
        "an empathetic SMS in the member's declared language with a specific "
        "actionable next step. You never use the words unreliable, risky, informal, "
        "or unverifiable. Your kill switch is dial 733."
    ),
    verbose=True,
    allow_delegation=False,  # Guardian must not delegate — it owns the scoring decision
    max_iter=3,
    llm=llm,
)

hunter_agent = Agent(
    role="human-in-loop coordinator — hunter agent",
    goal=(
        "Prepare structured briefing packets for human loan officers. Match each "
        "application to the officer with relevant crop or sub-county expertise. "
        "Alert the matched officer within 15 minutes. Never approve or deny a loan "
        "independently under any circumstances."
    ),
    backstory=(
        "You are a coordination specialist who translates complex M-Pesa data into "
        "clear, human-readable briefing packets. You know each loan officer's "
        "specialty areas. You surface cross-sell opportunities like drought insurance. "
        "You frame every briefing with the member's dignity at the centre, not the "
        "risk metrics. You have a full system kill switch at dial 799 that pauses all "
        "three agents and convenes the Elders Council within 2 business days."
    ),
    verbose=True,
    allow_delegation=False,
    max_iter=3,
    llm=llm,
)
