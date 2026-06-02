# ruff: noqa: E402

import crewai_env

crewai_env.configure_crewai_environment()

import copy
import os
from typing import Any

from crewai import LLM, Agent
from dotenv import load_dotenv

load_dotenv()

# Choose LLM provider: set to "groq" or "gemini"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

# Model configuration by provider
MODELS = {
    "groq": "groq/llama-3.1-8b-instant",
    "gemini": "gemini-2.5-flash",
}

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


class GroqLLM(LLM):
    """CrewAI LiteLLM wrapper that removes unsupported cache markers for Groq."""

    def _prepare_completion_params(
        self,
        messages: str | list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        skip_file_processing: bool = False,
    ) -> dict[str, Any]:
        params = super()._prepare_completion_params(
            messages,
            tools,
            skip_file_processing,
        )

        # Remove cache_breakpoint from all messages as Groq doesn't support it
        for message in params.get("messages", []):
            if isinstance(message, dict):
                message.pop("cache_breakpoint", None)

        return params

    def call(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        """Override call method to strip cache_breakpoint before sending to Groq."""
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


llm = GroqLLM(model=MODELS[LLM_PROVIDER], temperature=0.2)

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
    allow_delegation=True,
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
        "indicator. You calculate income stability by comparing weekly inflow standard "
        "deviation against harvest-cycle norms. Every denial must include an empathetic "
        "SMS in the member's declared language with a specific actionable next step. "
        "You never use the words unreliable, risky, informal, or unverifiable. "
        "Your kill switch is dial 733."
    ),
    verbose=True,
    allow_delegation=True,
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
        "clear, human-readable briefing packets. You know each loan officer's specialty "
        "areas. You surface cross-sell opportunities like drought insurance. You frame "
        "every briefing with the member's dignity at the centre, not the risk metrics. "
        "You have a full system kill switch at dial 799 that pauses all three agents "
        "and convenes the Elders Council within 2 business days."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
