import streamlit as st
import pdfplumber
import re

st.set_page_config(
    page_title="Contract Intelligence System",
    layout="wide"
)

st.title("📄 Contract Intelligence System")

st.write(
    "Upload a financing contract PDF and generate "
    "contract intelligence automatically."
)

uploaded_file = st.file_uploader(
    "Upload Contract",
    type=["pdf"]
)

if uploaded_file:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    st.success("Contract processed successfully.")

    # -----------------------------
    # Extraction
    # -----------------------------

    contract_type = re.search(
        r"^[A-Z\s]+AGREEMENT",
        text,
        re.MULTILINE
    )

    borrower = re.search(
        r"BORROWER:\s*(.*?)(?:,|\n)",
        text
    )

    lender = re.search(
        r"LENDER:\s*(.*?)(?:,|\n)",
        text
    )

    amount = re.search(
        r"FINANCED AMOUNT:\s*(\$[\d,\.]+)",
        text
    )

    clauses = re.findall(
        r"CLAUSE\s+\w+\s+–\s+([A-Z]+)",
        text
    )

    # -----------------------------
    # Summary
    # -----------------------------

    st.subheader("📋 Contract Summary")

    st.write(
        {
            "Contract Type":
            contract_type.group(0)
            if contract_type else "Not Found",

            "Borrower":
            borrower.group(1)
            if borrower else "Not Found",

            "Lender":
            lender.group(1)
            if lender else "Not Found",

            "Amount":
            amount.group(1)
            if amount else "Not Found"
        }
    )

    # -----------------------------
    # Clauses
    # -----------------------------

    st.subheader("⚖️ Detected Clauses")

    st.write(list(set(clauses)))

    # -----------------------------
    # Risk Score
    # -----------------------------

    risk_score = 0

    for risk_clause in [
        "DEFAULT",
        "TERMINATION",
        "GUARANTEES"
    ]:

        if risk_clause in clauses:

            risk_score += 1

    st.subheader("🚨 Risk Assessment")

    st.metric(
        "Risk Score",
        risk_score
    )

    if risk_score == 3:

        st.error("High Risk")

    elif risk_score == 2:

        st.warning("Medium Risk")

    else:

        st.success("Low Risk")
