import crewai_env
crewai_env.configure_crewai_environment()

import streamlit as st

st.set_page_config(
    page_title="Fair Lending Guardian", 
    page_icon="🦁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Data Stewardship: OASIS Protocol")

st.subheader("Five-step data sovereignty flow")
st.info("1. Member opts in via IVR in their declared language. Declining carries zero penalty and does not affect the loan outcome.")
st.info("2. M-Pesa data ingested. PII fields hashed with SHA-256 before any model sees the data.")
st.info("3. Scoring model receives anonymised transaction patterns only. No raw transaction ever passes to the model.")
st.info("4. All data stored on AWS Africa Cape Town region only. No transmission outside the African continent.")
st.info("5. Auto-delete scheduler runs nightly. Applications older than 180 days from final decision are deleted.")

st.code("""os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["CREWAI_DISABLE_TRACKING"] = "true\"""", language="python")
st.caption("CrewAI telemetry and tracking are disabled. No member data leaves the local environment.")

st.subheader("Swahili consent script (IVR audio, 45 seconds)")
st.code("""Habari yako. Ujima SACCO inatumia mfumo wa kompyuta kusaidia kupitia
maombi ya mkopo. Mfumo huu utaangalia muundo wa malipo yako ya M-Pesa.
Uamuzi wa mwisho utafanywa na afisa wa mkopo wa Ujima, si kompyuta
peke yake. Data yako ya M-Pesa itatumika tu na Ujima SACCO kufanya
uamuzi wa mkopo wako. Haitashirikiwa na mtu mwingine. Kwa kukubali,
bonyeza moja. Kwa kukataa, bonyeza mbili. Kukataa hakutaathiri ombi
lako.""", language="text")

st.subheader("Luhya Bukusu consent script (IVR audio, 45 seconds)")
st.code("""Okhwela. Ujima SACCO ifumbiria mfumo wa simu kufumya ombi lya mkopo.
Mfumo ono ukhaangalikha malipo yako ya M-Pesa. Omukufu wa Ujima ndiye
ofumya uamuzi, si simu yeke. Taarifa yako ifumiwe Kenya tu. Okhukhula
si lazima. Okukubali, finya imo. Okughairi, finya ibiri.""", language="text")

st.subheader("Technical security")
security_data = [
    {"Specification": "API encryption", "Implementation": "TLS 1.3"},
    {"Specification": "USSD and SMS channel", "Implementation": "Signal Protocol double ratchet"},
    {"Specification": "PII hashing", "Implementation": "SHA-256 before model ingestion"},
    {"Specification": "Data residency", "Implementation": "AWS Africa Cape Town"},
    {"Specification": "Authentication", "Implementation": "PIN plus biometric"},
    {"Specification": "Minimum anonymisation group size", "Implementation": "50 members"},
]
st.dataframe(security_data, use_container_width=True)
