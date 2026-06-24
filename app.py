import streamlit as st
import anthropic

st.set_page_config(page_title="Performance Review Coach", page_icon="📊", layout="wide")

st.title("📊 Performance Review Coach")
st.caption("Turn rough manager notes into structured, fair, evidence-based performance reviews")

# ── API Key ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        st.success("API key loaded from secrets ✓")
    except Exception:
        api_key = st.text_input("Anthropic API Key", type="password",
                                help="Get yours at console.anthropic.com")

    st.markdown("---")
    st.markdown(
        "**How it works**\n\n"
        "1. Fill in the employee details\n"
        "2. Paste your rough notes — bullet points, fragments, anything\n"
        "3. Click **Generate Review**\n"
        "4. Get a structured review with competency ratings, coaching plan, and SMART goals\n\n"
        "Built for Singapore-context performance reviews."
    )

if not api_key:
    st.warning("👈 Enter your Anthropic API key in the sidebar to get started.")
    st.stop()

# ── Form ─────────────────────────────────────────────────────────────────────
with st.form("review_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        employee_name = st.text_input("Employee Name *", placeholder="Sarah Tan")
    with c2:
        role = st.text_input("Role / Job Title *", placeholder="Marketing Executive")
    with c3:
        review_period = st.text_input("Review Period *", placeholder="January – June 2026")

    manager_notes = st.text_area(
        "Your raw notes about this employee *",
        height=220,
        placeholder=(
            "Write naturally — bullet points, fragments, whatever you have.\n\n"
            "Example:\n"
            "- Delivered Q3 campaign on time despite brief changing three times\n"
            "- Great with clients, quiet in team meetings, might be confidence\n"
            "- Helped onboard two junior staff — not in her job scope\n"
            "- Missed a few internal report deadlines but client work always done\n"
            "- Wants to move to senior role next year, needs to speak up more"
        ),
    )

    submitted = st.form_submit_button(
        "✨ Generate Performance Review", type="primary", use_container_width=True
    )

# ── Generate ─────────────────────────────────────────────────────────────────
if submitted:
    missing = [f for f, v in [
        ("Employee Name", employee_name),
        ("Role", role),
        ("Review Period", review_period),
        ("Manager Notes", manager_notes),
    ] if not v.strip()]

    if missing:
        st.error(f"Please fill in: {', '.join(missing)}")
        st.stop()

    with st.spinner("Generating structured performance review …"):
        claude = anthropic.Anthropic(api_key=api_key)

        prompt = f"""You are an expert HR coach helping managers write fair, structured, and evidence-based performance reviews in Singapore.

Manager's raw notes about the employee:
{manager_notes}

Employee name: {employee_name}
Role: {role}
Review period: {review_period}

Generate a structured performance review in this exact format:

## PERFORMANCE REVIEW
**Employee:** {employee_name}
**Role:** {role}
**Period:** {review_period}

## OVERALL RATING: [Choose one: Exceptional / Exceeds Expectations / Meets Expectations / Needs Improvement / Unsatisfactory]

## KEY ACHIEVEMENTS
(3-4 specific achievements with evidence drawn from the manager's notes)

## AREAS FOR DEVELOPMENT
(2-3 specific development areas with practical coaching suggestions)

## COMPETENCY RATINGS
- Delivery & Results: [1-5] — [one line justification]
- Communication: [1-5] — [one line justification]
- Teamwork & Collaboration: [1-5] — [one line justification]
- Initiative & Innovation: [1-5] — [one line justification]
- Leadership (if applicable): [1-5] — [one line justification]

## COACHING FRAMEWORK
(3 specific, actionable coaching recommendations with suggested timelines)

## SUGGESTED GOALS FOR NEXT PERIOD
(3 SMART goals based on development areas)

## MANAGER SUMMARY
(2-3 sentences summarising overall performance and potential)"""

        response = claude.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )

    review_text = response.content[0].text

    st.markdown("---")
    st.markdown(review_text)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Download as Markdown",
            data=review_text,
            file_name=f"performance_review_{employee_name.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col2:
        st.download_button(
            "📥 Download as Text",
            data=review_text,
            file_name=f"performance_review_{employee_name.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
