import streamlit as st
from pipeline import run_research_pipeline
from datetime import datetime

st.set_page_config(
    page_title="AI Research Studio",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Orange and cream theme
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #fff3e0 0%, #ffe0b2 55%, #ffcc80 100%
    );
    color: #39210f;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

h1, h2, h3, h4 {
    color: #9a3412 !important;
}

p, label, [data-testid="stMarkdownContainer"] {
    color: #39210f;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffcc80, #ffb74d);
}

/* Research topic input */
.stTextArea textarea {
    background-color: #fffaf5 !important;
    color: #39210f !important;
    border: 2px solid #fb923c !important;
    border-radius: 12px !important;
}

.stTextArea textarea:focus {
    border-color: #ea580c !important;
    box-shadow: 0 0 0 1px #ea580c !important;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button,
[data-testid="stDownloadButton"] button {
    background-color: #ea580c !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: background-color 0.2s ease;
}

.stButton button:hover,
.stFormSubmitButton button:hover,
[data-testid="stDownloadButton"] button:hover {
    background-color: #c2410c !important;
    color: white !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: #9a3412 !important;
}

.stTabs [aria-selected="true"] {
    color: #c2410c !important;
    border-bottom-color: #ea580c !important;
}

/* Expanders and alerts */
[data-testid="stExpander"] {
    background-color: #fff7ed;
    border: 1px solid #fdba74;
    border-radius: 12px;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Pipeline status */
[data-testid="stStatusWidget"] {
    background-color: #fff7ed;
    border-radius: 12px;
}

/* Code output */
[data-testid="stCode"] {
    background-color: #fff7ed;
    border: 1px solid #fdba74;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.title("🔬 Research Studio")
    st.caption("Multi-Agent Research Assistant")
    st.divider()

    st.markdown("### Pipeline")
    st.markdown("""
    1. 🔎 Search Agent
    2. 📚 Reader Agent
    3. ✍️ Writer Chain
    4. 🧪 Critic Chain
    """)

    st.divider()
    st.caption("Powered by LangChain and Streamlit")


# Main heading
st.title("🟠 AI Research Studio")
st.write(
    "Research any topic using your multi-agent pipeline."
)
st.divider()


# Research input
with st.form("research_form"):
    topic = st.text_area(
        "Enter your research topic",
        placeholder="Example: Future of AI",
        height=120,
    )

    submitted = st.form_submit_button(
        "🚀 Start Research",
        use_container_width=True,
    )


# Execute research pipeline
if submitted:
    clean_topic = topic.strip()

    if not clean_topic:
        st.warning("Please enter a research topic.")

    else:
        try:
            with st.spinner(
                "Agents are searching, reading, writing, and reviewing..."
            ):
                result = run_research_pipeline(clean_topic)

            if not isinstance(result, dict):
                st.error(
                    "Pipeline did not return a dictionary. "
                    "Ensure run_research_pipeline() returns state."
                )

            else:
                st.session_state["research_result"] = result
                st.session_state["research_topic"] = clean_topic
                st.session_state["research_time"] = (
                    datetime.now().strftime("%d %b %Y, %I:%M %p")
                )

                st.success("Research completed successfully!")

        except Exception as exc:
            st.error(f"Research failed: {exc}")
            st.info(
                "Check the terminal traceback, API quota, API keys, "
                "and network connection. If a model rate limit was "
                "reached, wait for it to reset before trying again."
            )


# Display research results
if "research_result" in st.session_state:
    result = st.session_state["research_result"]

    st.divider()
    st.header("📊 Research Dashboard")

    st.write(
        "**Topic:**",
        st.session_state.get("research_topic", "Research")
    )
    st.caption(
        "Completed at "
        + st.session_state.get("research_time", "Earlier")
    )

    def to_display_text(value):
        """Convert common LangChain outputs into readable text."""
        if value is None:
            return ""

        if isinstance(value, str):
            return value

        if hasattr(value, "content"):
            return str(value.content)

        if isinstance(value, dict):
            if "content" in value:
                return to_display_text(value["content"])
            return str(value)

        return str(value)

    search_results = to_display_text(
        result.get("search_results", "")
    )
    scraped_content = to_display_text(
        result.get("scraped_content", "")
    )
    report = to_display_text(
        result.get("report", "")
    )
    feedback = to_display_text(
        result.get("feedback", "")
    )

    search_tab, reader_tab, report_tab, critic_tab = st.tabs([
        "🔎 Search Results",
        "📚 Scraped Content",
        "📝 Final Report",
        "🧪 Critic Feedback",
    ])

    with search_tab:
        st.subheader("Search Agent Output")

        if search_results:
            st.markdown(search_results)
        else:
            st.info("No search results available.")

    with reader_tab:
        st.subheader("Reader Agent Output")

        if scraped_content:
            st.markdown(scraped_content)
        else:
            st.info("No scraped content available.")

    with report_tab:
        st.subheader("Generated Research Report")

        if report:
            st.markdown(report)

            st.download_button(
                label="⬇️ Download Report",
                data=report,
                file_name="research_report.md",
                mime="text/markdown",
            )
        else:
            st.info("No report available.")

    with critic_tab:
        st.subheader("Critic Review")

        if feedback:
            st.markdown(feedback)
        else:
            st.info("No critic feedback available.")