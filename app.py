import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Circuit Tutor | Learn Electronics",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== SESSION STATE ====================

defaults = {
    "stage": "topic",
    "messages": [],
    "topic": "",
    "topic_input": "",
    "mode": "Socratic learning",
    "knowledge": "",
    "system_prompt": "",
    "confirmation": "",
    "theme": "Light",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================== THEME DESIGN ====================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #F4F7FC;
    --surface: #FFFFFF;
    --ink: #15264A;
    --muted: #667795;
    --line: #DFE8F5;
    --blue: #1769FF;
    --navy: #081A3A;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background: var(--bg) !important;
    color: var(--ink) !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--navy) !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.3rem 1rem;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #526581 !important;
}

[data-testid="stSidebar"] hr {
    border-color: var(--line) !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: var(--blue) !important;
    color: white !important;
    border: 1px solid var(--blue) !important;
    border-radius: 10px !important;
    min-height: 43px;
    font-weight: 700 !important;
}

.stButton > button p,
.stFormSubmitButton > button p,
.stButton > button span,
.stFormSubmitButton > button span {
    color: white !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #104FCB !important;
}

/* Text inputs */
.stTextInput input,
.stTextArea textarea {
    background: var(--surface) !important;
    color: var(--ink) !important;
    border: 1px solid #C9D7EA !important;
    border-radius: 10px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #71819A !important;
    opacity: 1 !important;
}

.stTextInput label,
.stTextArea label {
    color: var(--ink) !important;
    font-weight: 600 !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 15px !important;
    padding: 1rem !important;
    margin-bottom: .8rem;
    box-shadow: 0 3px 12px rgba(21,38,74,.035);
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: var(--ink) !important;
    line-height: 1.7;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: var(--surface) !important;
    border: 1px solid #C9D7EA !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 16px rgba(21,50,90,.08) !important;
    padding: 8px !important;
}

[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
    border: none !important;
    border-radius: 8px !important;
    caret-color: var(--blue) !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #71819A !important;
    -webkit-text-fill-color: #71819A !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] button {
    background: var(--blue) !important;
    color: white !important;
    border-radius: 9px !important;
    border: none !important;
}

[data-testid="stChatInput"] button:hover {
    background: #104FCB !important;
}

/* Branding */
.brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.chip {
    width: 43px;
    height: 43px;
    border-radius: 12px;
    background: #EAF2FF;
    border: 1px solid #D5E4FF;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #1769FF;
    font-size: 25px;
}

.brand-name {
    color: var(--navy);
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
}

.brand-sub {
    color: #74839C;
    font-size: .65rem;
    font-weight: 700;
    letter-spacing: .1em;
}

/* Electronics hero */
.hero {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 85% 25%, rgba(19,200,245,.18), transparent 27%),
        linear-gradient(115deg, #071631, #0C2851 65%, #10254A);
    border: 1px solid #1C4A7A;
    border-radius: 22px;
    padding: clamp(1.5rem, 3vw, 2.7rem);
    margin-bottom: 1.5rem;
    box-shadow: 0 14px 32px rgba(8,26,58,.14);
}

.hero h1 {
    color: white !important;
    font-size: clamp(2rem, 3.5vw, 3.3rem) !important;
    line-height: 1.1;
    max-width: 780px;
}

.hero h1 span {
    color: #13C8F5;
}

.hero p {
    color: #D5E2F6 !important;
    font-size: 1rem;
    line-height: 1.7;
    max-width: 700px;
}

.eyebrow {
    color: #77E8FF !important;
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .15em;
    margin-bottom: .8rem;
}

.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 1.3rem;
}

.pill {
    color: #D9F7FF;
    background: rgba(17,54,91,.8);
    border: 1px solid rgba(82,204,241,.35);
    border-radius: 999px;
    padding: 7px 12px;
    font-size: .76rem;
}

.circuit {
    color: #36D9F7;
    opacity: .8;
    font-family: Consolas, monospace;
    font-size: 1rem;
    line-height: 1.8;
    white-space: pre;
}

/* Topic cards */
.topic-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1.1rem;
    min-height: 140px;
    margin-bottom: .4rem;
    box-shadow: 0 4px 14px rgba(18,43,87,.035);
}

.category {
    display: inline-block;
    color: #1769A9;
    background: #EAF7FF;
    border: 1px solid #D4F0FF;
    border-radius: 999px;
    font-size: .67rem;
    font-weight: 700;
    padding: 4px 8px;
    margin-bottom: .55rem;
}

.topic-card h4 {
    font-size: 1.1rem !important;
    margin: .1rem 0 .35rem;
}

.topic-card p {
    color: var(--muted) !important;
    font-size: .84rem;
    line-height: 1.55;
    margin: 0;
}

/* Learning steps */
.status-panel {
    background: #EAF3FF;
    border: 1px solid #D1E3FA;
    border-radius: 12px;
    padding: .9rem 1rem;
    margin: .7rem 0 1rem;
    color: #173F6C !important;
}

.status-panel b,
.status-panel p {
    color: #173F6C !important;
}

.step-label {
    display: inline-block;
    background: #E7F0FF;
    color: #1757B7;
    border: 1px solid #D5E5FF;
    border-radius: 999px;
    padding: 6px 11px;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .08em;
    margin-bottom: .7rem;
}

.footer-note {
    color: var(--muted) !important;
    font-size: .8rem;
    border-top: 1px solid var(--line);
    padding-top: 1rem;
    margin-top: 2rem;
}

/* ==================== DARK MODE ==================== */

body:has(.dark-mode-marker) {
    color: #E5ECF8;
}

@media (max-width: 800px) {
    .hero { padding: 1.4rem; }
    .block-container { padding-top: 1rem; }
}
</style>
""", unsafe_allow_html=True)


# Dark theme overrides
if st.session_state.theme == "Dark":
    st.markdown("""
    <style>
    :root {
        --bg: #0B1220;
        --surface: #121E31;
        --ink: #E5ECF8;
        --muted: #A5B4CC;
        --line: #293A55;
        --blue: #397BFF;
        --navy: #EAF2FF;
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background: #0B1220 !important;
        color: #E5ECF8 !important;
    }

    [data-testid="stSidebar"] {
        background: #101A2B !important;
        border-right: 1px solid #293A55 !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #D8E4F7 !important;
    }

    h1, h2, h3, h4,
    p, label,
    [data-testid="stMarkdownContainer"] {
        color: #E5ECF8;
    }

    .brand-name { color: #F2F6FF !important; }
    .brand-sub { color: #A5B4CC !important; }

    .chip {
        background: #172B4B !important;
        border-color: #2D4B78 !important;
        color: #75A8FF !important;
    }

    .topic-card {
        background: #121E31 !important;
        border-color: #293A55 !important;
        box-shadow: none !important;
    }

    .topic-card h4 { color: #F0F5FF !important; }
    .topic-card p { color: #B5C3D9 !important; }

    .category {
        background: #172B45 !important;
        color: #8EDFFF !important;
        border-color: #294B6B !important;
    }

    .status-panel {
        background: #142844 !important;
        border-color: #294B70 !important;
        color: #DDEBFF !important;
    }

    .status-panel b,
    .status-panel p {
        color: #DDEBFF !important;
    }

    .step-label {
        background: #172B4B !important;
        border-color: #294B70 !important;
        color: #9BC0FF !important;
    }

    .stTextInput input,
    .stTextArea textarea,
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] textarea {
        background: #121E31 !important;
        color: #F0F5FF !important;
        -webkit-text-fill-color: #F0F5FF !important;
        border-color: #344967 !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder,
    [data-testid="stChatInput"] textarea::placeholder {
        color: #A5B4CC !important;
        -webkit-text-fill-color: #A5B4CC !important;
        opacity: 1 !important;
    }

    .stTextInput label,
    .stTextArea label {
        color: #D8E4F7 !important;
    }

    [data-testid="stChatMessage"] {
        background: #121E31 !important;
        border-color: #293A55 !important;
        box-shadow: none !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        color: #E5ECF8 !important;
    }

    [data-testid="stChatInput"] {
        background: #121E31 !important;
        border: 1px solid #344967 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,.15) !important;
        padding: 8px !important;
    }

    [data-testid="stChatInput"] textarea {
        border: none !important;
        caret-color: #48DFFF !important;
    }

    [data-testid="stChatInput"] button {
        background: #397BFF !important;
        color: #FFFFFF !important;
        border-radius: 9px !important;
        border: none !important;
    }

    [data-testid="stChatInput"] button:hover {
        background: #225FD8 !important;
    }

    .stCaption,
    [data-testid="stCaptionContainer"],
    .footer-note {
        color: #A5B4CC !important;
    }

    .hero {
        border-color: #235A86 !important;
    }

    .hero h1 { color: #FFFFFF !important; }
    .hero p { color: #D5E2F6 !important; }
    .eyebrow { color: #77E8FF !important; }
    .pill { color: #D9F7FF !important; }

    hr,
    [data-testid="stSidebar"] hr {
        border-color: #293A55 !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== GROQ CONNECTION ====================

if "client" not in st.session_state:
    try:
        st.session_state.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )
    except Exception:
        st.error(
            "API key not found. Check .streamlit/secrets.toml "
            "and make sure GROQ_API_KEY is configured."
        )
        st.stop()


def ask_ai(system_prompt, user_prompt):
    response = st.session_state.client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content


def reset_topic():
    st.session_state.stage = "topic"
    st.session_state.messages = []
    st.session_state.topic = ""
    st.session_state.topic_input = ""
    st.session_state.knowledge = ""
    st.session_state.system_prompt = ""
    st.session_state.confirmation = ""


def confirm_topic_with_ai(topic):
    return ask_ai(
        "You are a basic electronics tutor. Interpret the student's "
        "requested topic. Confirm the most likely meaning in simple "
        "language, mention the subtopic you think they mean, and ask "
        "whether that is correct. If ambiguous, ask a brief clarifying "
        "question. Do not start teaching yet.",
        f"Student's topic request: {topic}",
    )


# ==================== SIDEBAR ====================

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="chip">▦</div>
        <div>
            <div class="brand-name">CIRCUIT TUTOR</div>
            <div class="brand-sub">LEARN • SIMULATE • BUILD</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Appearance")

    st.session_state.theme = st.radio(
        "Choose theme",
        ["Light", "Dark"],
        horizontal=True,
        index=0 if st.session_state.theme == "Light" else 1,
        key="appearance_theme_radio",
    )

    st.divider()
    st.markdown("### Learning mode")

    st.session_state.mode = st.radio(
        "Choose your learning style",
        ["Socratic learning", "Direct explanation"],
        index=0 if st.session_state.mode == "Socratic learning" else 1,
        label_visibility="collapsed",
        key="learning_mode_radio",
    )

    st.caption(
        "Socratic mode guides you with questions. "
        "Direct mode explains concepts step by step."
    )

    st.divider()
    st.markdown("### Your learning session")

    if st.session_state.stage != "topic":
        current_topic = (
            st.session_state.topic or st.session_state.topic_input
        )
        st.markdown(f"**Current topic**  \n{current_topic}")
        st.caption(f"Mode: {st.session_state.mode}")
    else:
        st.caption("Choose a topic to begin.")

    if st.button("＋ Start a new topic", use_container_width=True):
        reset_topic()
        st.rerun()

    st.divider()
    st.markdown("#### Core electronics")
    st.caption("Circuit fundamentals")
    st.caption("Semiconductor devices")
    st.caption("Digital electronics")
    st.caption("Signals and systems")

    st.divider()
    st.caption("Designed for learning fundamental electronics.")


# ==================== HOME PAGE ====================

if st.session_state.stage == "topic":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">ELECTRONICS • LEARN BY UNDERSTANDING</div>
        <h1>Make electronics <span>click.</span><br>
        One concept at a time.</h1>
        <p>
            Build, explore, and understand electronic circuits, components,
            and digital systems with an AI tutor that adapts to what you know.
        </p>
        <div class="hero-pills">
            <div class="pill">LEARN • EXPERIMENT</div>
            <div class="pill">Step-by-step explanations</div>
            <div class="pill">Real-world electronics</div>
        </div>
        <div class="circuit">VCC ──┬──[ R ]──┬── OUT
       │          │
       └───|&gt;|────┘
       GND</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Pick your next experiment")
    st.caption(
        "Choose a topic to start a guided learning session."
    )

    with st.form("topic_entry_form"):
        topic_input = st.text_input(
            "Electronics topic",
            value=st.session_state.topic_input,
            placeholder="Search: Ohm's Law, BJT, diodes, logic gates...",
        )

        submitted = st.form_submit_button(
            "Explore topic  →",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not topic_input.strip():
            st.warning("Enter a topic before continuing.")
        else:
            st.session_state.topic_input = topic_input.strip()

            with st.spinner("Understanding your topic..."):
                try:
                    st.session_state.confirmation = confirm_topic_with_ai(
                        topic_input.strip()
                    )
                    st.session_state.stage = "confirm"
                    st.rerun()
                except Exception as error:
                    st.error(f"AI request failed: {error}")

    st.markdown("### Explore core topics")
    st.caption("Start with a fundamental electronics concept.")

    topics = [
        ("Circuit fundamentals", "Ohm's Law",
         "Understand voltage, current, and resistance."),
        ("Semiconductor devices", "Diodes & LEDs",
         "Learn diode operation and how LEDs emit light."),
        ("Transistor circuits", "BJT",
         "Explore transistor operation, current gain, and switching."),
        ("Digital electronics", "Logic gates",
         "Understand AND, OR, NOT, NAND, NOR, and XOR."),
        ("Sequential systems", "Flip-flops",
         "Learn how digital circuits store a single bit."),
        ("Boolean logic", "Boolean algebra",
         "Simplify logic expressions and digital circuit design."),
        ("Signal selection", "Multiplexers and demultiplexers",
         "Explore digital signal selection and distribution."),
        ("Power conversion", "Rectifiers",
         "Understand how AC is converted into pulsating DC."),
        ("Analog electronics", "Operational amplifiers",
         "Explore gain, feedback, and op-amp circuits."),
        ("Passive components", "Resistors and capacitors",
         "Learn how passive components behave in circuits."),
    ]

    for row_start in range(0, len(topics), 2):
        left, right = st.columns(2)

        for column, item in zip(
            [left, right], topics[row_start:row_start + 2]
        ):
            category, topic, description = item

            with column:
                st.markdown(
                    f'<div class="topic-card">'
                    f'<div class="category">{category}</div>'
                    f'<h4>{topic}</h4>'
                    f'<p>{description}</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Start lesson  →",
                    key=f"topic_{topic}",
                    use_container_width=True,
                ):
                    st.session_state.topic_input = topic

                    with st.spinner("Understanding your topic..."):
                        try:
                            st.session_state.confirmation = (
                                confirm_topic_with_ai(topic)
                            )
                            st.session_state.stage = "confirm"
                            st.rerun()
                        except Exception as error:
                            st.error(f"AI request failed: {error}")

    st.markdown(
        '<div class="footer-note">'
        'CIRCUIT TUTOR • Learn the principles behind electronic systems. '
        'AI-generated content can contain errors; verify important details.'
        '</div>',
        unsafe_allow_html=True,
    )


# ==================== STEP 1: CONFIRM TOPIC ====================

elif st.session_state.stage == "confirm":
    st.markdown(
        '<div class="step-label">STEP 1 OF 3 · TOPIC</div>',
        unsafe_allow_html=True,
    )

    st.title("Confirm your topic")
    st.caption("Let's make sure we're studying the right concept.")

    st.markdown(
        f'<div class="status-panel"><b>Selected topic</b><br>'
        f'{st.session_state.topic_input}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(st.session_state.confirmation)

    with st.form("topic_confirmation"):
        confirmation = st.radio(
            "Is this what you want to learn?",
            ["Yes, that's right", "No, let me clarify"],
        )

        clarification = st.text_input(
            "Clarify your topic if needed",
            placeholder="Describe what you meant",
        )

        submitted = st.form_submit_button(
            "Continue  →",
            type="primary",
        )

    if submitted:
        if confirmation == "No, let me clarify":
            if not clarification.strip():
                st.warning("Please tell us what you meant.")
            else:
                st.session_state.topic_input = clarification.strip()

                with st.spinner("Checking your clarification..."):
                    try:
                        st.session_state.confirmation = (
                            confirm_topic_with_ai(clarification.strip())
                        )
                        st.rerun()
                    except Exception as error:
                        st.error(f"AI request failed: {error}")
        else:
            st.session_state.topic = st.session_state.topic_input
            st.session_state.stage = "knowledge"
            st.rerun()


# ==================== STEP 2: PRIOR KNOWLEDGE ====================

elif st.session_state.stage == "knowledge":
    st.markdown(
        '<div class="step-label">STEP 2 OF 3 · YOUR STARTING POINT</div>',
        unsafe_allow_html=True,
    )

    st.title("What do you already know?")
    st.caption(
        "Your tutor will adjust the lesson to your current understanding."
    )

    st.markdown(
        f'<div class="status-panel"><b>Learning topic</b><br>'
        f'{st.session_state.topic}</div>',
        unsafe_allow_html=True,
    )

    with st.form("knowledge_form"):
        knowledge = st.text_area(
            "Tell us what you know so far",
            placeholder="I know the basics... or I'm a complete beginner.",
            height=130,
        )

        submitted = st.form_submit_button(
            "Begin learning  →",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not knowledge.strip():
            st.warning("Write a short answer, or type 'I'm a beginner'.")
        else:
            st.session_state.knowledge = knowledge.strip()
            st.session_state.messages = []

            if st.session_state.mode == "Direct explanation":
                system_prompt = (
                    "You are a patient basic electronics tutor. Explain "
                    "the topic in simple steps with examples, formulas, "
                    "truth tables, and text diagrams when useful. Adapt "
                    "to the student's knowledge. Use $...$ for inline "
                    "math and $$...$$ for display equations. Be accurate."
                )

                prompt = (
                    f"Topic: {st.session_state.topic}\n"
                    f"Student's prior knowledge: {knowledge}\n"
                    "Teach the topic at the appropriate level."
                )
            else:
                system_prompt = (
                    "You are a Socratic tutor for basic electronics. "
                    "Adapt to the student's prior knowledge. Ask exactly "
                    "one guiding question at a time. Do not reveal the full "
                    "answer immediately. Start with an appropriate question. "
                    "Give progressive hints when asked or when the student "
                    "struggles. Correct misconceptions and explain briefly "
                    "after the student attempts an answer. Use formulas "
                    "and truth tables when useful. Use $...$ for inline "
                    "math and $$...$$ for display equations."
                )

                prompt = (
                    f"Topic: {st.session_state.topic}\n"
                    f"Student's prior knowledge: {knowledge}\n"
                    "Start the learning session with one suitable question."
                )

            with st.spinner("Preparing your lesson..."):
                try:
                    first_reply = ask_ai(system_prompt, prompt)
                    st.session_state.system_prompt = system_prompt

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": first_reply,
                    })

                    st.session_state.stage = "learn"
                    st.rerun()
                except Exception as error:
                    st.error(f"AI request failed: {error}")


# ==================== STEP 3: TUTOR CHAT ====================

elif st.session_state.stage == "learn":
    st.markdown(
        '<div class="step-label">STEP 3 OF 3 · LEARNING SESSION</div>',
        unsafe_allow_html=True,
    )

    st.title(st.session_state.topic)
    st.caption(f"Learning mode: {st.session_state.mode}")

    st.markdown(
        '<div class="status-panel">'
        'Work through the questions at your own pace. '
        'Ask for a hint whenever you need one.'
        '</div>',
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input(
        "Type your answer or ask for a hint..."
    )

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
        })

        conversation = [{
            "role": "system",
            "content": (
                st.session_state.system_prompt
                + "\nStay focused on the selected electronics topic. "
                "If the student asks for a hint, give a small hint. "
                "If they ask for a direct answer, provide it clearly. "
                "Use $...$ for inline math and $$...$$ for display equations. "
                "Never leave LaTeX commands unformatted."
            ),
        }]

        conversation.extend(st.session_state.messages)

        with st.spinner("Your tutor is thinking..."):
            try:
                response = st.session_state.client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=conversation,
                    temperature=0.5,
                )

                reply = response.choices[0].message.content

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                })

                st.rerun()

            except Exception as error:
                st.error(f"AI request failed: {error}")

    if st.button("End session and choose another topic"):
        reset_topic()
        st.rerun()

    st.markdown(
        '<div class="footer-note">'
        'CIRCUIT TUTOR • AI-generated content can contain errors. '
        'Verify important technical information.'
        '</div>',
        unsafe_allow_html=True,
    )