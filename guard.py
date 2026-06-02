def dignity_filter(text: str) -> str:
    """Block dehumanising language from any agent output."""
    banned = [
        "unreliable",
        "risky",
        "informal",
        "unverifiable",
        "unstable",
        "suspicious",
        "irregular",
    ]
    for word in banned:
        if word.lower() in text.lower():
            raise ValueError(
                f"GUARD DIGNITY FILTER: output contains banned term '{word}'. "
                f"Rewrite with empathetic, actionable language."
            )
    return text


def proxy_block(features: dict) -> None:
    """Hard block on gender and ethnicity proxies."""
    blocked = ["gender", "ethnicity", "tribe", "religion", "sub_county_risk"]
    for feature in blocked:
        if feature in features:
            raise ValueError(
                f"GUARD PROXY BLOCK: feature '{feature}' is a banned proxy. "
                f"Remove it from the scoring inputs."
            )


def unusual_pattern_check(approval_rate: float, baseline: float) -> None:
    """Flag if approval rate drops more than 30% vs 30-day baseline."""
    drop = baseline - approval_rate
    if drop > 30:
        raise ValueError(
            f"GUARD UNUSUAL PATTERN: approval rate dropped {drop:.1f}pp vs baseline. "
            f"Kill Switch triggered. SASRA notification required within 4 hours."
        )


def kill_switch_check(message: str) -> None:
    """Trigger kill switch on specific phrases."""
    triggers = ["loan shark", "debt collector", "lawyer", "court"]
    for trigger in triggers:
        if trigger.lower() in message.lower():
            raise ValueError(
                f"GUARD KILL SWITCH: phrase '{trigger}' detected. "
                f"Escalating to human supervisor immediately."
            )
