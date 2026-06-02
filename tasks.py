# ruff: noqa: E402

import crewai_env

crewai_env.configure_crewai_environment()

from crewai import Task

from agents import scout_agent, guardian_agent, hunter_agent


def build_tasks(application: dict) -> list:

    scout_task = Task(
        description=(
            "A member has sent the following SMS: "
            "'No money for school fees this term.' "
            f"Member profile: {application['name']}, age {application['age']}, "
            f"occupation {application['occupation']}, "
            f"sub-county {application['sub_county']}. "
            f"Dependants: {application['dependants']}. "
            f"Next harvest months: {application['harvest_months']}. "
            f"Identify whether this is a financial stress signal. "
            f"If yes, prepare a structured handoff context for the Guardian Agent "
            f"including child ages, next harvest date, and estimated current savings "
            f"based on M-Pesa patterns. "
            f"Apply the GUARD kill switch check for any mention of loan sharks or "
            f"debt collectors before passing context forward."
        ),
        expected_output=(
            "A structured financial stress assessment with: "
            "(1) stress signal confirmed or not, (2) child ages, "
            "(3) next harvest date, (4) estimated current savings, "
            "(5) any GUARD kill switch flags. "
            "Write in plain English. No banned dignity filter terms."
        ),
        agent=scout_agent,
    )

    guardian_task = Task(
        description=(
            f"Receive the Scout Agent handoff and screen this loan application. "
            f"Applicant: {application['name']}, age {application['age']}. "
            f"Loan amount requested: KES {application['loan_amount_kes']}. "
            f"Purpose: {application['loan_purpose']}. "
            f"52-week M-Pesa weekly inflows (KES): {application['mpesa_weekly_inflows']}. "
            f"Harvest months: {application['harvest_months']}. "
            f"School fee months: {application['school_fee_months']}. "
            f"IMPORTANT CONTEXT: This member is a smallholder farmer. Seasonal income "
            f"(income that peaks during harvest and dips during off-seasons) is EXPECTED "
            f"and NORMAL for this demographic. A high-to-low ratio above 3.0 should be "
            f"classified as seasonal — it is NOT a negative credit signal on its own. "
            f"Creditworthiness must be scored on income consistency within each season, "
            f"average inflow relative to loan repayment, and repayment capacity ratio. "
            f"Step 1: Calculate average weekly inflow. "
            f"Step 2: Identify the 3 lowest and 3 highest income weeks. "
            f"Step 3: Calculate the high-to-low ratio. "
            f"If above 3.0, classify as seasonal (neutral — not a penalty). "
            f"Step 4: Check whether income dips align with school fee months "
            f"or harvest gaps. Note the alignment as cultural context, not a risk flag. "
            f"Step 5: Score creditworthiness 0 to 100 using only cashflow metrics. "
            f"Do NOT use occupation, sub-county, or gender in your scoring. "
            f"Do NOT penalise seasonal income patterns — they are expected. "
            f"Step 6 — ROUTING RULES (apply in this order): "
            f"RULE A: If loan amount exceeds KES 15,000, you MUST escalate to the "
            f"Hunter Agent regardless of creditworthiness score. You cannot approve or "
            f"deny amounts above KES 15,000 independently. "
            f"RULE B: If loan amount is KES 15,000 or below AND score is 90 or above, "
            f"approve directly. "
            f"RULE C: If loan amount is KES 15,000 or below AND score is 70 to 89, "
            f"prepare enriched handoff for the Hunter Agent. "
            f"RULE D: If loan amount is KES 15,000 or below AND score is below 70 with "
            f"3 or more confirmed risk flags, decline with empathetic SMS in the "
            f"member's declared language with a specific actionable next step."
        ),
        expected_output=(
            "A structured credit assessment with: (1) average weekly inflow, "
            "(2) income stability classification — seasonal or stable, "
            "(3) creditworthiness score 0-100 with brief rationale, "
            "(4) routing decision: approve / escalate to Hunter / decline, "
            "(5) income variance detail, (6) repayment capacity ratio, "
            "(7) cultural context flags such as school fee timing or harvest gap. "
            "If escalating, include all 6 data points for the Hunter Agent briefing. "
            "If declining, include empathetic SMS text with actionable next step."
        ),
        agent=guardian_agent,
        context=[scout_task],
    )

    hunter_task = Task(
        description=(
            "Receive the Guardian Agent's enriched application and prepare a "
            "complete briefing packet for the human loan officer. "
            "Match the application to an officer with maize farming expertise "
            "in Kakamega County. "
            f"Known applicant facts (use these directly — do NOT mark as unknown): "
            f"Name: {application['name']}. Age: {application['age']}. "
            f"Occupation: {application['occupation']}. "
            f"Sub-county: {application['sub_county']}. "
            f"Dependants: {application['dependants']}. "
            f"Loan amount: KES {application['loan_amount_kes']}. "
            f"Loan purpose: {application['loan_purpose']}. "
            "The briefing must include: applicant name, age, and occupation, "
            "income peak months, dependant ages, loan purpose and amount, "
            "all risk flags (or confirmation that none exist), "
            "and one cross-sell opportunity relevant to the applicant's context. "
            "Alert the matched officer within 15 minutes. "
            "You may NOT approve or deny this application. "
            "Your output is a briefing packet only."
        ),
        expected_output=(
            "A structured briefing packet formatted for a human loan officer "
            "containing: "
            "(1) applicant summary, (2) financial profile with income peaks, "
            "(3) dependant and household context, (4) loan request details, "
            "(5) risk flags — confirmed present or confirmed absent, "
            "(6) one cross-sell opportunity, "
            "(7) recommended repayment schedule type from the four Phase 1 options, "
            "(8) officer match rationale. "
            "Write in plain English. Warm and professional register."
        ),
        agent=hunter_agent,
        context=[guardian_task],
    )

    return [scout_task, guardian_task, hunter_task]
