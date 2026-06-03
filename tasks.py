from crewai import Task

from agents import guardian_agent, hunter_agent, scout_agent


def build_tasks(application: dict) -> list:

    scout_task = Task(
        description=(
            f"A member has sent the following SMS: 'No money for school fees this term.' "
            f"Member profile: {application['name']}, age {application['age']}, "
            f"occupation {application['occupation']}, sub-county {application['sub_county']}. "
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
            "A structured financial stress assessment with: (1) stress signal confirmed "
            "or not, (2) child ages, (3) next harvest date, (4) estimated current "
            "savings, (5) any GUARD kill switch flags. "
            "Write in plain English. No banned dignity filter terms."
        ),
        agent=scout_agent,
    )

    guardian_task = Task(
        description=(
            f"Receive the Scout Agent handoff and screen this loan application. "
            f"Applicant: {application['name']}. "
            f"Loan amount requested: KES {application['loan_amount_kes']}. "
            f"Purpose: {application['loan_purpose']}. "
            f"52-week M-Pesa weekly inflows (KES): {application['mpesa_weekly_inflows']}. "
            f"Harvest months: {application['harvest_months']}. "
            f"School fee months: {application['school_fee_months']}. "
            f"Step 1: Calculate average weekly inflow. "
            f"Step 2: Identify the 3 lowest and 3 highest income weeks. "
            f"Step 3: Calculate the high-to-low ratio. If above 3.0, classify as seasonal. "
            f"Step 4: Check whether income dips align with school fee months or harvest gaps. "
            f"Step 5: Score creditworthiness 0 to 100 using only cashflow metrics. "
            f"Do NOT use occupation, sub-county, or gender in your scoring. "
            f"Step 6: If score is 70 to 89, prepare enriched handoff for Hunter Agent. "
            f"If score is 90 or above and amount is KES 15,000 or below, approve directly. "
            f"If score is below 70 with 3+ risk flags, decline with empathetic SMS."
        ),
        expected_output=(
            "A structured credit assessment with: (1) average weekly inflow, "
            "(2) income stability classification, (3) creditworthiness score 0-100, "
            "(4) decision: approve, decline, or escalate to Hunter, "
            "(5) income variance detail, (6) repayment capacity ratio, "
            "(7) cultural context flags such as school fee timing or harvest gap. "
            "If escalating, include all 6 data points for the Hunter Agent briefing."
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
            "The briefing must include: applicant name, age, and occupation, "
            "income peak months, dependant ages, loan purpose and amount, "
            "all risk flags (or confirmation that none exist), "
            "and one cross-sell opportunity relevant to the applicant's context. "
            "Alert the matched officer within 15 minutes. "
            "You may NOT approve or deny this application. "
            "Your output is a briefing packet only."
        ),
        expected_output=(
            "A structured briefing packet formatted for a human loan officer containing: "
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
