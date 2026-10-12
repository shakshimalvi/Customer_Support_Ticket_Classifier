
import html
import json
import streamlit as st
from app import classify_ticket
import traceback

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SupportIQ | Ticket Intelligence",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7ff 0%, #f8fafc 55%, #eef5ff 100%);
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}
[data-testid="stSidebar"] {
    background: #111827;
}
[data-testid="stSidebar"] * {
    color: #f9fafb;
}
.hero {
    padding: 28px 32px;
    border-radius: 22px;
    background: linear-gradient(120deg, #172554, #3730a3, #4338ca);
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 12px 30px rgba(49, 46, 129, 0.18);
}
.hero h1 {
    color: white;
    font-size: 34px;
    margin-bottom: 8px;
}
.hero p {
    color: #e0e7ff;
    font-size: 16px;
    margin-bottom: 0;
}
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #172554;
    margin: 12px 0 15px 0;
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
    min-height: 115px;
}
.metric-label {
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 12px;
}
.metric-value {
    color: #172554;
    font-size: 23px;
    font-weight: 750;
    overflow-wrap: anywhere;
}
.panel {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
    margin-bottom: 18px;
}
.response-panel {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 14px;
    padding: 20px;
    color: #14532d;
    line-height: 1.8;
    overflow-wrap: anywhere;
}
.small-muted {
    color: #64748b;
    font-size: 13px;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #4f46e5, #4338ca);
    border: none;
    border-radius: 10px;
    min-height: 46px;
    font-weight: 700;
}
.stButton > button {
    border-radius: 10px;
}
div[data-testid="stTextArea"] textarea {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("# 🎫 SupportIQ")
st.sidebar.caption("AI-powered ticket intelligence")
st.sidebar.divider()

st.sidebar.markdown("### How it works")
st.sidebar.markdown(
    "1. Enter a customer message\n\n"
    "2. Analyze the ticket with AI\n\n"
    "3. Review category and priority\n\n"
    "4. Use the suggested response"
)

examples = {
    "Duplicate billing charge": (
        "I was charged twice for my subscription. "
        "Please fix this immediately."
    ),
    "Password reset": "How do I reset my password?",
    "Vague issue": "Something is wrong",
    "Technical issue": (
        "The mobile app crashes whenever I try to open it."
    ),
    "Payment question": (
        "I made a payment, but it is still showing as pending."
    )
}

st.sidebar.markdown("### Try an example")
selected_example = st.sidebar.selectbox(
    "Choose a sample ticket",
    list(examples.keys())
)

if st.sidebar.button("Load example", use_container_width=True):
    st.session_state["ticket_input"] = examples[selected_example]

st.sidebar.divider()
st.sidebar.markdown("### Project information")
st.sidebar.caption("Model: NVIDIA API")
st.sidebar.caption("Backend: Python")
st.sidebar.caption("Interface: Streamlit")
st.sidebar.caption("Output: Structured JSON")

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>Customer Support Intelligence</h1>
    <p>
        Classify tickets, identify urgency, route issues to the right team,
        and generate professional response drafts.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- TICKET INPUT ----------------
st.markdown(
    '<div class="section-title">📝 Customer ticket</div>',
    unsafe_allow_html=True
)

with st.container(border=True):
    st.write("Enter the customer's message below.")

    if "ticket_input" not in st.session_state:
        st.session_state["ticket_input"] = ""

    ticket_text = st.text_area(
        "Ticket message",
        key="ticket_input",
        placeholder=(
            "Example: I was charged twice for my subscription..."
        ),
        height=150,
        label_visibility="collapsed"
    )

    analyze_col, hint_col = st.columns([1, 2])

    with analyze_col:
        analyze = st.button(
            "✨ Analyze Ticket",
            type="primary",
            use_container_width=True
        )

    with hint_col:
        st.caption("AI-generated results should be reviewed before sending.")

    if analyze:
        if not ticket_text.strip():
            st.warning("Please enter a ticket message first.")
        else:
            with st.spinner("Analyzing the customer ticket..."):
                try:
                    st.session_state["last_result"] = classify_ticket(
                        ticket_text.strip()
                        )
                    st.session_state["last_ticket"] = ticket_text.strip()
                    st.session_state.pop("analysis_error", None)
                except Exception as error:
                    import traceback
                    st.session_state.pop("last_result", None)
                    st.session_state["analysis_error"] = (
                        f"{type(error).__name__}: {st.error}\n\n"
                        f"{traceback.format_exc()}"
                        )
                print("Ticket analysis error:", traceback.format_exc())

# ---------------- ERROR DISPLAY ----------------
if st.session_state.get("analysis_error"):
    st.error(
        "Ticket analysis failed. Check your API connection and terminal "
        "for details."
    )
    with st.expander("Technical error details"):
        st.code(st.session_state["analysis_error"])

# ---------------- RESULTS ----------------
result = st.session_state.get("last_result")

if result:
    st.divider()
    st.markdown(
        '<div class="section-title">📊 Classification dashboard</div>',
        unsafe_allow_html=True
    )
    st.success("Analysis completed. Review the results below.")

    category = html.escape(result["category"])
    priority = html.escape(result["priority"])
    queue = html.escape(result["routing_queue"])

    priority_color = {
        "High": "#dc2626",
        "Medium": "#d97706",
        "Low": "#15803d"
    }.get(result["priority"], "#334155")

    card1, card2, card3 = st.columns(3)

    with card1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🏷️ Category</div>
            <div class="metric-value">{category}</div>
        </div>
        """, unsafe_allow_html=True)

    with card2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚡ Priority</div>
            <div class="metric-value" style="color:{priority_color}">
                {priority}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with card3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📬 Routing queue</div>
            <div class="metric-value">{queue}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown(
            '<div class="section-title">💬 Suggested response</div>',
            unsafe_allow_html=True
        )

        safe_response = html.escape(result["response_draft"])

        st.markdown(f"""
        <div class="response-panel">{safe_response}</div>
        """, unsafe_allow_html=True)

        st.caption(
            "Review and edit this AI-generated draft before sending it "
            "to the customer."
        )

        st.button(
            "📋 Copy response",
            on_click=lambda: st.write(
                "Select and copy the response text above."
            ),
            help="Use your browser to select and copy the suggested response."
        )

    with right:
        st.markdown(
            '<div class="section-title">🔎 Ticket summary</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True):
            st.markdown("**Customer message**")
            st.write(st.session_state.get("last_ticket", ""))

            st.divider()
            st.markdown("**Assigned team**")
            st.write(result["routing_queue"])

            st.markdown("**Current status**")
            st.write("Awaiting human review")

        with st.expander("View structured JSON"):
            st.json(result)

        st.download_button(
            label="⬇️ Download JSON result",
            data=json.dumps(result, indent=4, ensure_ascii=False),
            file_name="ticket_classification.json",
            mime="application/json",
            use_container_width=True
        )

else:
    st.markdown("""
    <div class="panel">
        <h3>✨ Your analysis will appear here</h3>
        <p style="color:#64748b">
            Enter a ticket and select <b>Analyze Ticket</b> to see its
            category, priority, routing queue, and suggested response.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    '<p class="small-muted" style="text-align:center">'
    'SupportIQ · Customer Support Ticket Classifier · '
    'Built with Python, Streamlit and NVIDIA AI'
    '</p>',
    unsafe_allow_html=True
)
