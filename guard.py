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
        try:
            import streamlit as st
            st.error(f"GUARD UNUSUAL PATTERN: approval rate dropped {drop:.1f}pp vs baseline. SASRA notification triggered.")
        except ImportError:
            pass
        
        try:
            from database import log_sasra_alert
            log_sasra_alert(f"Drop {drop:.1f}pp vs baseline. Kill Switch triggered.")
        except ImportError:
            pass


def kill_switch_check(message: str) -> None:
    """Trigger kill switch on specific phrases."""
    triggers = ["loan shark", "debt collector", "lawyer", "court"]
    for trigger in triggers:
        if trigger.lower() in message.lower():
            raise ValueError(
                f"GUARD KILL SWITCH: phrase '{trigger}' detected. "
                f"Escalating to human supervisor immediately."
            )
