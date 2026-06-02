# ruff: noqa: E402

import crewai_env

crewai_env.configure_crewai_environment()

from crewai import Crew, Process

from agents import scout_agent, guardian_agent, hunter_agent
from guard import kill_switch_check, proxy_block
from mock_data import GRACE_APPLICATION
from tasks import build_tasks

print("\n" + "=" * 60)
print("FAIR LENDING GUARDIAN — AGENT PRIDE PROTOTYPE")
print("Ujima SACCO | Module 4: Agent Savannah | June 2026")
print("=" * 60)

print("\nApplicant loaded:")
print(f"  Name: {GRACE_APPLICATION['name']}")
print(f"  Loan requested: KES {GRACE_APPLICATION['loan_amount_kes']:,}")
print(f"  Purpose: {GRACE_APPLICATION['loan_purpose']}")
print(f"  Occupation: {GRACE_APPLICATION['occupation']}")
print(f"  Sub-county: {GRACE_APPLICATION['sub_county']}")
print("\nGUARD pre-flight checks running...")

try:
    proxy_block({"income": 1, "mpesa_history": 1})
    print("  GUARD proxy block: PASSED — no banned features in inputs")
except ValueError as e:
    print(f"  GUARD proxy block: FAILED — {e}")

try:
    kill_switch_check("I need school fees help")
    print("  GUARD kill switch: PASSED — no escalation triggers in member message")
except ValueError as e:
    print(f"  GUARD kill switch: TRIGGERED — {e}")

print("\nLaunching agent pride...\n")
print("-" * 60)

tasks = build_tasks(GRACE_APPLICATION)

crew = Crew(
    agents=[scout_agent, guardian_agent, hunter_agent],
    tasks=tasks,
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()

print("\n" + "=" * 60)
print("HUNT PROTOCOL COMPLETE — FINAL BRIEFING PACKET")
print("=" * 60)
print(result)
print("\n" + "=" * 60)
print("PRIDE LOOP REMINDER")
print("=" * 60)
print("This briefing packet is advisory only.")
print("A named human loan officer must make the final decision.")
print("Loan amount KES 28,000 exceeds KES 15,000 threshold.")
print("PRIDE Loop Pause Point activated — human review mandatory.")
print("Officer SLA: 15 minutes from this timestamp.")
print("Member appeal right: dial *#123# — free, zero credit score impact.")
print("=" * 60)
