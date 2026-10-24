"""
========================================================================================
 CampusSaathi AI - Your Local AI College Companion
========================================================================================
 Built with: Streamlit, Ollama, Python, and Google Gemma 3:1B
 Premium Modern Frontend Edition:
   - Modern Typography: Google Fonts (Outfit & Plus Jakarta Sans)
   - Refined Text Hierarchy, Colors, and Clean Section Surfaces
   - Snap & Study (Photo Upload & Native Windows Offline OCR)
   - PDF Note Question Answering & AI Study Timetable Generator
   - 100% Local, Private, and Free (No API Keys Required)
========================================================================================
"""

import base64
import json
import os
import subprocess
import tempfile
from datetime import date, timedelta
from typing import Dict, Generator, List, Optional, Tuple
import pypdf
import requests
import streamlit as st

# ======================================================================================
# 1. STREAMLIT CONFIGURATION & ELEVATED CUSTOM STYLING
# ======================================================================================

st.set_page_config(
    page_title="CampusSaathi AI | Local College Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_custom_css():
    """Inject premium CSS to transform Streamlit into a modern EdTech application."""
    st.markdown(
        """
        <!-- Load Premium Google Fonts -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

        <style>
            /* Base Typography */
            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
                color: #334155;
            }
            h1, h2, h3, h4, .outfit-font {
                font-family: 'Outfit', sans-serif !important;
                letter-spacing: -0.3px;
                color: #0f172a !important;
            }

            /* Container padding */
            .main .block-container {
                padding-top: 1.6rem;
                padding-bottom: 2.5rem;
                max-width: 1240px;
            }

            /* Hero Header Card */
            .hero-header {
                background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
                color: #ffffff;
                padding: 1.6rem 2.2rem;
                border-radius: 18px;
                margin-bottom: 1.6rem;
                box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.18), 0 4px 10px -2px rgba(15, 23, 42, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.08);
                position: relative;
                overflow: hidden;
            }
            .hero-header::after {
                content: '';
                position: absolute;
                top: -30px;
                right: -30px;
                width: 160px;
                height: 160px;
                background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, transparent 70%);
                border-radius: 50%;
                pointer-events: none;
            }
            .hero-header h1 {
                color: #ffffff !important;
                font-size: 1.85rem !important;
                font-weight: 700;
                margin-bottom: 0.25rem;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .hero-header p {
                color: #cbd5e1 !important;
                font-size: 0.94rem;
                margin-bottom: 0;
                font-weight: 400;
                max-width: 800px;
            }

            /* Modern Status Badges */
            .status-badge-online {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background-color: #ecfdf5;
                color: #065f46;
                border: 1px solid #a7f3d0;
                padding: 5px 14px;
                border-radius: 9999px;
                font-size: 0.8rem;
                font-weight: 600;
            }
            .status-badge-offline {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background-color: #fef2f2;
                color: #991b1b;
                border: 1px solid #fecaca;
                padding: 5px 14px;
                border-radius: 9999px;
                font-size: 0.8rem;
                font-weight: 600;
            }

            /* Study Summary Callout Card */
            .study-summary-card {
                background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
                border: 1.5px solid #a7f3d0;
                border-left: 5px solid #10b981;
                border-radius: 14px;
                padding: 1.3rem 1.6rem;
                margin-bottom: 1.3rem;
                box-shadow: 0 4px 14px rgba(16, 185, 129, 0.08);
            }
            .study-summary-card h4 {
                color: #065f46 !important;
                font-size: 1.1rem;
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .study-summary-card div {
                color: #047857;
                font-size: 0.92rem;
                line-height: 1.65;
            }

            /* Notice Cards */
            .notice-card {
                background: #ffffff;
                border: 1.5px solid #e2e8f0;
                border-radius: 12px;
                padding: 1.15rem 1.4rem;
                margin-bottom: 1rem;
                transition: all 0.18s ease;
            }
            .notice-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px -3px rgba(15, 23, 42, 0.08);
                border-color: #cbd5e1;
            }
            .notice-date {
                font-size: 0.76rem;
                color: #64748b;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.6px;
            }
            .notice-title {
                font-family: 'Outfit', sans-serif;
                font-size: 1.08rem;
                font-weight: 700;
                color: #0f172a;
                margin: 0.25rem 0 0.35rem 0;
            }
            .notice-desc {
                font-size: 0.88rem;
                color: #334155;
                line-height: 1.55;
            }

            /* Category Tags */
            .badge-tag {
                display: inline-block;
                padding: 3px 10px;
                border-radius: 9999px;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.4px;
                text-transform: uppercase;
            }
            .tag-exam { background-color: #f3e8ff; color: #7e22ce; border: 1px solid #d8b4fe; }
            .tag-event { background-color: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
            .tag-library { background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
            .tag-fee { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }

            /* Disclaimer Banner */
            .demo-disclaimer {
                background-color: #fffbeb;
                border: 1.5px solid #fef3c7;
                border-left: 4px solid #f59e0b;
                color: #92400e;
                padding: 0.9rem 1.25rem;
                border-radius: 10px;
                font-size: 0.85rem;
                margin-bottom: 1.3rem;
                line-height: 1.5;
            }

            /* Stat cards */
            .stat-box {
                background: #ffffff;
                border: 1.5px solid #e2e8f0;
                border-radius: 12px;
                padding: 0.9rem 1.1rem;
                text-align: center;
                box-shadow: 0 2px 6px rgba(0,0,0,0.02);
            }
            .stat-box .stat-num {
                font-family: 'Outfit', sans-serif;
                font-size: 1.55rem;
                font-weight: 800;
                color: #4338ca;
            }
            .stat-box .stat-label {
                font-size: 0.75rem;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                font-weight: 600;
            }

            /* Streamlit button enhancements */
            div.stButton > button {
                border-radius: 10px !important;
                font-weight: 600 !important;
                font-size: 0.88rem !important;
                transition: all 0.18s ease !important;
            }
            div.stButton > button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15) !important;
            }

            /* Chat message bubbles */
            .stChatMessage {
                border-radius: 14px !important;
                padding: 1rem 1.2rem !important;
                margin-bottom: 0.8rem !important;
                border: 1px solid #e2e8f0 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_custom_css()

# ======================================================================================
# 2. SESSION STATE INITIALIZATION
# ======================================================================================

if "ollama_url" not in st.session_state:
    st.session_state.ollama_url = "http://localhost:11434"

if "model_name" not in st.session_state:
    st.session_state.model_name = "gemma3:1b"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.4

# 1. AI Study Assistant Chat History
if "study_messages" not in st.session_state:
    st.session_state.study_messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Namaste! I am CampusSaathi AI**, your local college study buddy powered by Gemma 3:1B.\n\n"
                "Ask me any syllabus question, request step-by-step mathematical proofs, "
                "or generate high-yield revision notes. What topic shall we master today?"
            ),
        }
    ]

# 2. Ask My Notes (PDF)
if "notes_messages" not in st.session_state:
    st.session_state.notes_messages = []

if "notes_extracted_text" not in st.session_state:
    st.session_state.notes_extracted_text = ""

if "notes_filename" not in st.session_state:
    st.session_state.notes_filename = ""

if "notes_page_count" not in st.session_state:
    st.session_state.notes_page_count = 0

# 3. Snap & Study (Photo Upload)
if "photo_extracted_text" not in st.session_state:
    st.session_state.photo_extracted_text = ""

if "photo_summary" not in st.session_state:
    st.session_state.photo_summary = ""

if "photo_messages" not in st.session_state:
    st.session_state.photo_messages = []

if "photo_filename" not in st.session_state:
    st.session_state.photo_filename = ""

if "photo_bytes" not in st.session_state:
    st.session_state.photo_bytes = None

# 4. AI Study Planner Output
if "saved_study_plan" not in st.session_state:
    st.session_state.saved_study_plan = ""

# ======================================================================================
# 3. OLLAMA API CLIENT FUNCTIONS (LOCAL REST API VIA REQUESTS)
# ======================================================================================


def test_ollama_connection(base_url: str) -> Tuple[bool, List[str], str]:
    """Checks if the local Ollama server is reachable and retrieves models."""
    clean_url = base_url.rstrip("/")
    urls_to_try = [f"{clean_url}/api/tags"]
    if "localhost" in clean_url:
        urls_to_try.append(f"{clean_url.replace('localhost', '127.0.0.1')}/api/tags")

    last_error = ""
    for endpoint in urls_to_try:
        try:
            response = requests.get(endpoint, timeout=2.5)
            if response.status_code == 200:
                data = response.json()
                models = [m.get("name", "") for m in data.get("models", [])]
                return True, models, ""
            else:
                last_error = f"Ollama returned HTTP Status {response.status_code}"
        except requests.exceptions.ConnectionError:
            last_error = "Could not connect to Ollama. Make sure Ollama is running."
        except requests.exceptions.Timeout:
            last_error = "Connection to Ollama timed out after 2.5 seconds."
        except Exception as e:
            last_error = f"Unexpected error: {str(e)}"

    return False, [], last_error


def call_ollama_stream(
    messages: List[Dict[str, str]],
    model: str = "gemma3:1b",
    system_prompt: Optional[str] = None,
    temperature: float = 0.4,
    base_url: str = "http://localhost:11434",
    images: Optional[List[str]] = None,
) -> Generator[str, None, None]:
    """Sends chat completion request to Ollama's /api/chat with streaming."""
    clean_url = base_url.rstrip("/")
    endpoint = f"{clean_url}/api/chat"

    formatted_messages = []
    if system_prompt:
        formatted_messages.append({"role": "system", "content": system_prompt})

    for idx, msg in enumerate(messages):
        msg_obj = {"role": msg["role"], "content": msg["content"]}
        if images and idx == len(messages) - 1 and msg["role"] == "user":
            msg_obj["images"] = images
        formatted_messages.append(msg_obj)

    payload = {
        "model": model,
        "messages": formatted_messages,
        "stream": True,
        "options": {
            "temperature": temperature,
        },
    }

    try:
        response = requests.post(
            endpoint, json=payload, stream=True, timeout=(5.0, 120.0)
        )

        if response.status_code == 404:
            yield (
                f"⚠️ **Model `{model}` not found in Ollama.**\n\n"
                f"Please open PowerShell and run:\n`ollama pull {model}`"
            )
            return

        if response.status_code != 200:
            yield f"⚠️ **Ollama Error ({response.status_code}):** {response.text}"
            return

        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    message_chunk = chunk.get("message", {}).get("content", "")
                    if message_chunk:
                        yield message_chunk
                except json.JSONDecodeError:
                    continue

    except requests.exceptions.ConnectionError:
        yield (
            "⚠️ **Cannot connect to Ollama Server.**\n\n"
            "Please check:\n"
            "1. Is Ollama running on your PC?\n"
            "2. Run `ollama serve` in PowerShell.\n"
            "3. Verify that `http://localhost:11434` is accessible."
        )
    except requests.exceptions.Timeout:
        yield "⚠️ **Request Timed Out.** Ollama took too long to respond."
    except Exception as e:
        yield f"⚠️ **Unexpected Error:** {str(e)}"


def call_ollama_sync(
    messages: List[Dict[str, str]],
    model: str = "gemma3:1b",
    system_prompt: Optional[str] = None,
    temperature: float = 0.4,
    base_url: str = "http://localhost:11434",
) -> str:
    """Non-streaming version for quick utility generation tasks."""
    chunks = list(
        call_ollama_stream(
            messages=messages,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature,
            base_url=base_url,
        )
    )
    return "".join(chunks)


# ======================================================================================
# 4. PDF & IMAGE TEXT EXTRACTION (PYPDF & WINDOWS NATIVE OCR)
# ======================================================================================


def extract_pdf_content(uploaded_file) -> Tuple[str, int, str]:
    """Extracts text from a PDF file using pypdf."""
    try:
        reader = pypdf.PdfReader(uploaded_file)
        num_pages = len(reader.pages)

        if num_pages == 0:
            return "", 0, "The uploaded PDF appears to be empty."

        extracted_text_list = []
        for index, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                extracted_text_list.append(
                    f"--- PAGE {index + 1} ---\n{page_text.strip()}"
                )

        full_text = "\n\n".join(extracted_text_list).strip()

        if not full_text:
            return (
                "",
                num_pages,
                "No selectable text found. Scanned image-only PDFs can be processed in the Snap & Study tab.",
            )

        return full_text, num_pages, "Success"

    except Exception as e:
        return "", 0, f"Error reading PDF file: {str(e)}"


def extract_text_from_photo(image_bytes: bytes) -> Tuple[str, str]:
    """
    Extracts text from a photo using Windows Native Offline OCR (Windows.Media.Ocr).
    100% offline, zero pip dependencies.
    """
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(image_bytes)
            temp_path = f.name

        ocr_script_path = os.path.abspath("ocr_helper.ps1")
        if not os.path.exists(ocr_script_path):
            return "", "OCR helper script not found."

        cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            ocr_script_path,
            "-ImagePath",
            os.path.abspath(temp_path),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        extracted_text = result.stdout.strip()

        if extracted_text:
            return extracted_text, "Success"
        else:
            return (
                "",
                "No text could be detected in this photo. Ensure the image is clear and well-lit.",
            )

    except subprocess.TimeoutExpired:
        return "", "OCR processing timed out. Please try a clearer image."
    except Exception as e:
        return "", f"OCR Error: {str(e)}"
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


# ======================================================================================
# 5. MOCK CAMPUS NOTICES DATA
# ======================================================================================

SAMPLE_NOTICES = [
    {
        "id": "NOT-2026-001",
        "category": "Examinations",
        "date": "October 22, 2026",
        "title": "Mid-Semester Examination Schedule Announced (Fall 2026)",
        "content": (
            "The Mid-Semester Examinations for all 2nd, 3rd, and 4th-year B.Tech / BCA / B.Sc students "
            "will commence from November 10, 2026. Detailed seating arrangements and subject-wise timetables "
            "are uploaded to the student portal. Students must carry physical college ID and admit cards."
        ),
        "tag": "EXAM TIMETABLE",
        "css_class": "tag-exam",
    },
    {
        "id": "NOT-2026-002",
        "category": "Events",
        "date": "October 20, 2026",
        "title": "Annual Inter-College Hackathon: CodeCraft 2026 Registrations Open",
        "content": (
            "Department of Computer Science invites teams of 2 to 4 students for the 36-hour CodeCraft Hackathon "
            "scheduled for November 28-29, 2026. Cash prizes worth ₹1,50,000 + internship opportunities. "
            "Last date to submit team abstract is November 5, 2026 at the Innovation Cell."
        ),
        "tag": "HACKATHON",
        "css_class": "tag-event",
    },
    {
        "id": "NOT-2026-003",
        "category": "Library",
        "date": "October 18, 2026",
        "title": "Central Library Book Return & Late Fee Waiver Week",
        "content": (
            "All overdue books from the previous semester must be returned between October 27 and November 2, 2026. "
            "The library advisory committee has approved a 100% late-fee waiver during this week. "
            "Digital library access card renewal will also be processed at Counter 3."
        ),
        "tag": "LIBRARY",
        "css_class": "tag-library",
    },
    {
        "id": "NOT-2026-004",
        "category": "Administrative",
        "date": "October 15, 2026",
        "title": "Examination Fee Submission & Form Verification Deadline",
        "content": (
            "The final date for submitting end-semester examination forms and online fee clearance without late fees "
            "is November 3, 2026. A late fee of ₹500 will apply until November 8. "
            "Submit the fee receipt copy to the Academic Section."
        ),
        "tag": "FEE DEADLINE",
        "css_class": "tag-fee",
    },
]

# ======================================================================================
# 6. SIDEBAR: NAVIGATION & REAL-TIME OLLAMA STATUS CHECK
# ======================================================================================

with st.sidebar:
    st.markdown("### 🎓 **CampusSaathi AI**")
    st.caption("Local AI College Companion | Offline & Private")

    st.markdown("---")

    is_online, installed_models, conn_err = test_ollama_connection(
        st.session_state.ollama_url
    )

    if is_online:
        st.markdown(
            """
            <div class="status-badge-online">
                <span>🟢</span> <b>Ollama Online</b> (Local Port 11434)
            </div>
            """,
            unsafe_allow_html=True,
        )

        target_model = st.session_state.model_name
        model_found = any(target_model in m for m in installed_models)

        if model_found:
            st.caption(f"Active Model: **`{target_model}`** ✅")
        else:
            st.warning(
                f"⚠️ Model `{target_model}` not detected.\n"
                f"Run in terminal: `ollama pull {target_model}`"
            )
    else:
        st.markdown(
            """
            <div class="status-badge-offline">
                <span>🔴</span> <b>Ollama Offline</b>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Start Ollama or run `ollama serve` in PowerShell.")

    st.markdown("---")

    selected_page = st.radio(
        "📌 **Navigate to Feature:**",
        options=[
            "📚 AI Study Assistant",
            "📸 Snap & Study (Photo Explainer)",
            "📄 Ask My Notes (PDF Q&A)",
            "📅 AI Study Planner",
            "📢 Campus Notices",
            "⚙️ Settings & System Status",
        ],
        index=0,
    )

    st.markdown("---")

    st.markdown("💡 **Student Quick Tips:**")
    st.markdown(
        "- **📸 Snap & Study:** Photos are processed offline via Windows OCR.\n"
        "- **100% Private:** Your files never leave your computer.\n"
        "- **Zero Cloud Fees:** No API keys or credit cards needed."
    )

    st.markdown("---")
    st.caption("v1.3.0 | Modern UI Edition")

# ======================================================================================
# 7. FEATURE 1: AI STUDY ASSISTANT (CHAT INTERFACE)
# ======================================================================================

if selected_page == "📚 AI Study Assistant":
    st.markdown(
        """
        <div class="hero-header">
            <h1>📚 AI Study Assistant</h1>
            <p>Your 24/7 personal college tutor. Ask doubts, request step-by-step derivations, and generate high-yield exam revision notes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_mode, col_clear = st.columns([4, 1.2])

    with col_mode:
        study_mode = st.selectbox(
            "🎯 **Select Tutoring Style:**",
            options=[
                "💡 Simple & Intuitive (Explain like I'm a 1st-year student)",
                "📝 Exam Revision Notes (High-Yield Bullet Points & Formulas)",
                "🪜 Step-by-Step Breakdown (Derivations, Algorithms & Proofs)",
                "💻 Code & Practical Examples (Clean code with explanations)",
                "🎯 Mock Viva & Quiz (Practice questions with model answers)",
            ],
            index=0,
        )

    with col_clear:
        st.write("")
        st.write("")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.study_messages = [
                {
                    "role": "assistant",
                    "content": "✨ Chat cleared! What topic shall we master next?",
                }
            ]
            st.rerun()

    st.caption("⚡ **Quick Topic Ideas:**")
    prompt_chips = [
        "Explain QuickSort vs MergeSort with time complexity and comparison table",
        "What is ACID in DBMS? Give real-world banking examples",
        "Explain Process vs Thread with memory layout comparison",
        "Derive Bernoulli's Equation step by step with assumptions",
    ]
    chip_cols = st.columns(len(prompt_chips))
    chosen_prompt = None

    for i, chip_text in enumerate(prompt_chips):
        with chip_cols[i]:
            if st.button(chip_text, key=f"chip_{i}", use_container_width=True):
                chosen_prompt = chip_text

    system_instruction = (
        "You are CampusSaathi AI, an encouraging and expert college tutor.\n"
        f"Selected Style: {study_mode}.\n"
        "FORMATTING GUIDELINES:\n"
        "- Use bold headings (###) for distinct concepts.\n"
        "- Highlight key technical terms in **bold**.\n"
        "- Use neat bullet points with clean spacing.\n"
        "- Format equations on separate lines.\n"
        "- Conclude with a helpful '🎯 Exam & Viva Tip' highlight box."
    )

    for message in st.session_state.study_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.chat_input("Ask any doubt or syllabus topic...")
    if chosen_prompt:
        user_query = chosen_prompt

    if user_query:
        st.session_state.study_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            if not is_online:
                error_msg = "⚠️ **Ollama is offline.** Please run `ollama serve` in PowerShell."
                st.markdown(error_msg)
                st.session_state.study_messages.append(
                    {"role": "assistant", "content": error_msg}
                )
            else:
                ollama_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.study_messages
                ]

                response_stream = call_ollama_stream(
                    messages=ollama_messages,
                    model=st.session_state.model_name,
                    system_prompt=system_instruction,
                    temperature=st.session_state.temperature,
                    base_url=st.session_state.ollama_url,
                )

                full_response = st.write_stream(response_stream)
                st.session_state.study_messages.append(
                    {"role": "assistant", "content": full_response}
                )

# ======================================================================================
# 8. FEATURE 2: SNAP & STUDY (PHOTO UPLOAD & OCR)
# ======================================================================================

elif selected_page == "📸 Snap & Study (Photo Explainer)":
    st.markdown(
        """
        <div class="hero-header">
            <h1>📸 Snap & Study (Photo Explainer)</h1>
            <p>Upload a photo of textbook pages, handwritten notes, numerical problems, or blackboard equations. 
            CampusSaathi AI reads the photo offline and generates structured summaries, step-by-step derivations, and formula sheets.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    photo_col, analysis_col = st.columns([1, 1.3], gap="large")

    with photo_col:
        st.markdown("### 📷 **1. Upload Study Photo**")

        uploaded_img = st.file_uploader(
            "Upload image (Textbook, Notes, Whiteboard, Exam Question)",
            type=["png", "jpg", "jpeg", "webp"],
            help="Images are processed offline using Windows Native OCR without leaving your PC.",
        )

        c_sample, c_clear_img = st.columns([1.5, 1])
        sample_img_path = os.path.join(
            "sample_notes", "Sample_Physics_Notes.png"
        )
        use_sample = False

        with c_sample:
            if os.path.exists(sample_img_path):
                if st.button("🧪 Try Sample Physics Photo", use_container_width=True):
                    use_sample = True
        with c_clear_img:
            if st.session_state.photo_extracted_text:
                if st.button("🗑️ Reset Photo", use_container_width=True):
                    st.session_state.photo_extracted_text = ""
                    st.session_state.photo_summary = ""
                    st.session_state.photo_messages = []
                    st.session_state.photo_filename = ""
                    st.session_state.photo_bytes = None
                    st.rerun()

        image_data = None
        img_name = ""

        if uploaded_img is not None:
            image_data = uploaded_img.getvalue()
            img_name = uploaded_img.name
        elif use_sample and os.path.exists(sample_img_path):
            with open(sample_img_path, "rb") as f:
                image_data = f.read()
            img_name = "Sample_Physics_Notes.png"

        if image_data and (st.session_state.photo_filename != img_name):
            st.session_state.photo_bytes = image_data
            st.session_state.photo_filename = img_name
            st.session_state.photo_messages = []
            st.session_state.photo_summary = ""

            with st.spinner("🔍 Reading text from photo using native offline OCR..."):
                ocr_text, ocr_status = extract_text_from_photo(image_data)
                if ocr_status == "Success":
                    st.session_state.photo_extracted_text = ocr_text
                    st.toast("✅ Photo text extracted successfully!", icon="📸")
                else:
                    st.error(ocr_status)

        if st.session_state.photo_bytes:
            st.image(
                st.session_state.photo_bytes,
                caption=f"📷 Uploaded: {st.session_state.photo_filename}",
                use_container_width=True,
            )

            st.markdown("#### 📝 Detected Text from Photo")
            st.session_state.photo_extracted_text = st.text_area(
                "You can edit or refine detected text below:",
                value=st.session_state.photo_extracted_text,
                height=140,
            )
        else:
            st.info(
                "👆 **Upload a study photo above** or click **'Try Sample Physics Photo'** to see equations analyzed!"
            )

    with analysis_col:
        st.markdown("### 🧠 **2. AI Photo Study Actions**")

        if not st.session_state.photo_extracted_text:
            st.markdown(
                """
                <div style="border: 2px dashed #cbd5e1; border-radius: 14px; padding: 3rem 1.5rem; text-align: center; color: #64748b; background: #ffffff;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📸</div>
                    <h4 style="font-family: 'Outfit';">No Photo Loaded Yet</h4>
                    <p style="font-size: 0.9rem;">Upload a photo of your study material on the left to get instant summaries, step-by-step problem solving, and formula breakdowns.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.caption("⚡ **Choose a study action for this photo:**")
            act1, act2, act3 = st.columns(3)
            act4, act5, act6 = st.columns(3)

            photo_action_prompt = None

            with act1:
                if st.button("📝 Full Summary", use_container_width=True):
                    photo_action_prompt = (
                        "Provide a structured, comprehensive study summary of the content in this photo. "
                        "Include: (1) Core Concept Overview, (2) Detailed Key Points, and (3) Practical Takeaways."
                    )
            with act2:
                if st.button("💡 Step-by-Step Solver", use_container_width=True):
                    photo_action_prompt = (
                        "Analyze any problems, derivations, or equations in this photo and explain them step-by-step. "
                        "State given variables, formulas applied, intermediate calculation steps, and final conclusion."
                    )
            with act3:
                if st.button("📌 Formula Sheet", use_container_width=True):
                    photo_action_prompt = (
                        "Extract all formulas, physical laws, mathematical theorems, SI units, and core definitions "
                        "from this photo into a high-yield exam cheat sheet."
                    )
            with act4:
                if st.button("🎯 Top Exam Qs", use_container_width=True):
                    photo_action_prompt = (
                        "Based on the content of this photo, predict the 5 most probable questions that can be asked "
                        "in college semester exams or viva-voce, along with concise model answers."
                    )
            with act5:
                if st.button("🪜 Explain Simply (ELI5)", use_container_width=True):
                    photo_action_prompt = (
                        "Explain the topic shown in this photo in extremely simple, intuitive language with real-world analogies, "
                        "as if teaching a 1st-year student."
                    )
            with act6:
                if st.button("💻 Practice Problem", use_container_width=True):
                    photo_action_prompt = (
                        "Create 2 practice numerical problems that directly test the student's "
                        "understanding of the concepts in this photo."
                    )

            if not st.session_state.photo_summary and is_online:
                with st.spinner("🤖 Gemma 3:1B is structuring your photo summary..."):
                    init_prompt = (
                        f"Summarize the study notes/text extracted from this uploaded college photo:\n\n"
                        f"{st.session_state.photo_extracted_text}\n\n"
                        "Highlight the main topic, core definitions, and 3 key takeaways for a college student."
                    )
                    st.session_state.photo_summary = call_ollama_sync(
                        messages=[{"role": "user", "content": init_prompt}],
                        model=st.session_state.model_name,
                        system_prompt="You are CampusSaathi AI Photo Tutor. Provide a clean, encouraging college summary with headings and bold keywords.",
                        temperature=0.4,
                        base_url=st.session_state.ollama_url,
                    )

            if st.session_state.photo_summary:
                st.markdown(
                    f"""
                    <div class="study-summary-card">
                        <h4>✨ Instant Photo Study Summary</h4>
                        <div>{st.session_state.photo_summary}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("---")
            st.markdown("#### 💬 **Ask Follow-up Doubts About This Photo**")

            for p_msg in st.session_state.photo_messages:
                with st.chat_message(p_msg["role"]):
                    st.markdown(p_msg["content"])

            photo_user_query = st.chat_input(
                "Ask any question about this photo (e.g., 'Explain equation 2 in detail')..."
            )
            if photo_action_prompt:
                photo_user_query = photo_action_prompt

            if photo_user_query:
                st.session_state.photo_messages.append(
                    {"role": "user", "content": photo_user_query}
                )
                with st.chat_message("user"):
                    st.markdown(photo_user_query)

                with st.chat_message("assistant"):
                    if not is_online:
                        st.error("⚠️ Ollama is offline. Please launch Ollama.")
                    else:
                        photo_system_instruction = (
                            "You are CampusSaathi AI Photo Study Mentor. The student has uploaded a photo of their study materials.\n"
                            "Here is the text extracted from the student's photo:\n"
                            f"=== PHOTO TEXT START ===\n{st.session_state.photo_extracted_text}\n=== PHOTO TEXT END ===\n\n"
                            "FORMATTING RULES:\n"
                            "- Use headings (###) for concepts.\n"
                            "- Break derivations into step-by-step numbered points.\n"
                            "- Highlight key formulas and variables in bold.\n"
                            "- Conclude with a helpful college exam tip."
                        )

                        photo_ollama_msgs = [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.photo_messages
                        ]

                        response_stream = call_ollama_stream(
                            messages=photo_ollama_msgs,
                            model=st.session_state.model_name,
                            system_prompt=photo_system_instruction,
                            temperature=0.4,
                            base_url=st.session_state.ollama_url,
                        )

                        p_resp = st.write_stream(response_stream)
                        st.session_state.photo_messages.append(
                            {"role": "assistant", "content": p_resp}
                        )

            if (
                st.session_state.photo_summary
                or st.session_state.photo_messages
            ):
                all_photo_notes = f"""# CampusSaathi AI - Study Photo Notes
**Image Source:** {st.session_state.photo_filename}  
**Date:** {date.today().strftime('%B %d, %Y')}

## 📝 Detected Content
```text
{st.session_state.photo_extracted_text}
```

## ✨ Executive Summary
{st.session_state.photo_summary}

## 💬 Q&A & Analysis
"""
                for m in st.session_state.photo_messages:
                    all_photo_notes += f"\n### {m['role'].capitalize()}:\n{m['content']}\n"

                st.download_button(
                    label="📥 Download Photo Study Sheet (Markdown)",
                    data=all_photo_notes,
                    file_name=f"Photo_Study_Notes_{date.today().strftime('%Y%m%d')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

# ======================================================================================
# 9. FEATURE 3: ASK MY NOTES (PDF Q&A)
# ======================================================================================

elif selected_page == "📄 Ask My Notes (PDF Q&A)":
    st.markdown(
        """
        <div class="hero-header">
            <h1>📄 Ask My Notes</h1>
            <p>Upload lecture notes, textbooks, or syllabus PDFs. Extract text locally with pypdf and query your materials with complete privacy.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pdf_col, chat_col = st.columns([1, 1.3], gap="large")

    with pdf_col:
        st.markdown("### 📤 **1. Upload College Notes (PDF)**")
        uploaded_pdf = st.file_uploader(
            "Choose a PDF file from your computer",
            type=["pdf"],
            help="Select text-based PDF notes. Scanned image-only PDFs can be processed in the Snap & Study tab.",
        )

        if uploaded_pdf is not None:
            if st.session_state.notes_filename != uploaded_pdf.name:
                with st.spinner("Extracting text from PDF using pypdf..."):
                    extracted_text, num_pages, status = extract_pdf_content(
                        uploaded_pdf
                    )

                    if status == "Success":
                        st.session_state.notes_extracted_text = extracted_text
                        st.session_state.notes_filename = uploaded_pdf.name
                        st.session_state.notes_page_count = num_pages
                        st.session_state.notes_messages = [
                            {
                                "role": "assistant",
                                "content": f"✅ Successfully loaded **`{uploaded_pdf.name}`** ({num_pages} pages). What would you like to prepare from these notes?",
                            }
                        ]
                    else:
                        st.error(status)

        if st.session_state.notes_extracted_text:
            text_len = len(st.session_state.notes_extracted_text)
            word_count = len(st.session_state.notes_extracted_text.split())

            st.markdown("#### 📊 Document Statistics")
            s1, s2, s3 = st.columns(3)
            with s1:
                st.markdown(
                    f"""<div class="stat-box"><div class="stat-num">{st.session_state.notes_page_count}</div><div class="stat-label">Pages</div></div>""",
                    unsafe_allow_html=True,
                )
            with s2:
                st.markdown(
                    f"""<div class="stat-box"><div class="stat-num">{word_count:,}</div><div class="stat-label">Words</div></div>""",
                    unsafe_allow_html=True,
                )
            with s3:
                st.markdown(
                    f"""<div class="stat-box"><div class="stat-num">{(text_len / 1024):.1f} KB</div><div class="stat-label">Text Size</div></div>""",
                    unsafe_allow_html=True,
                )

            st.markdown("#### ⚡ Quick Actions")
            qa_col1, qa_col2 = st.columns(2)

            quick_query = None
            with qa_col1:
                if st.button("📝 5-Minute Summary", use_container_width=True):
                    quick_query = "Provide a comprehensive 5-minute revision summary of these uploaded notes highlighting key definitions, core concepts, and major takeaways."
                if st.button("🎯 Top 5 Exam Questions", use_container_width=True):
                    quick_query = "Based strictly on these notes, generate the 5 most probable college exam questions with brief model answers."

            with qa_col2:
                if st.button("📌 Formulas & Definitions", use_container_width=True):
                    quick_query = "Extract all key definitions, laws, theorems, or formulas mentioned in these notes into a bulleted cheat sheet."
                if st.button("🗑️ Unload Document", use_container_width=True):
                    st.session_state.notes_extracted_text = ""
                    st.session_state.notes_filename = ""
                    st.session_state.notes_page_count = 0
                    st.session_state.notes_messages = []
                    st.rerun()

            with st.expander(
                "🔍 Preview Extracted Text (First 1,500 characters)", expanded=False
            ):
                st.text_area(
                    "Extracted Text",
                    value=st.session_state.notes_extracted_text[:1500] + "...",
                    height=180,
                    disabled=True,
                )
        else:
            st.info(
                "👆 **Upload a PDF above to get started.**\n\n"
                "Tip: You can use the generated `sample_notes/Sample_College_Notes.pdf` in your project folder!"
            )

    with chat_col:
        st.markdown("### 💬 **2. Chat with Your Notes**")

        if not st.session_state.notes_extracted_text:
            st.markdown(
                """
                <div style="border: 2px dashed #cbd5e1; border-radius: 14px; padding: 3rem 1.5rem; text-align: center; color: #64748b; background: #ffffff;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📖</div>
                    <h4 style="font-family: 'Outfit';">No Notes Loaded Yet</h4>
                    <p style="font-size: 0.9rem;">Please upload a PDF note file on the left panel to begin asking questions.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            chat_container = st.container()
            with chat_container:
                for note_msg in st.session_state.notes_messages:
                    with st.chat_message(note_msg["role"]):
                        st.markdown(note_msg["content"])

            note_user_input = st.chat_input("Ask a question about the uploaded notes...")
            if "quick_query" in locals() and quick_query:
                note_user_input = quick_query

            if note_user_input:
                st.session_state.notes_messages.append(
                    {"role": "user", "content": note_user_input}
                )
                with st.chat_message("user"):
                    st.markdown(note_user_input)

                with st.chat_message("assistant"):
                    if not is_online:
                        err_text = "⚠️ Ollama is offline. Please start Ollama."
                        st.markdown(err_text)
                        st.session_state.notes_messages.append(
                            {"role": "assistant", "content": err_text}
                        )
                    else:
                        safe_context = st.session_state.notes_extracted_text[:12000]
                        notes_system_prompt = (
                            "You are CampusSaathi AI, a rigorous academic assistant. "
                            "The student has uploaded personal college notes. "
                            "Answer questions accurately based ONLY on the provided notes context.\n"
                            "Format clearly with headings and bold bullet points.\n\n"
                            f"=== UPLOADED NOTES CONTEXT ({st.session_state.notes_filename}) ===\n"
                            f"{safe_context}\n"
                            f"=== END OF NOTES CONTEXT ===\n"
                        )

                        note_ollama_messages = [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.notes_messages
                        ]

                        response_stream = call_ollama_stream(
                            messages=note_ollama_messages,
                            model=st.session_state.model_name,
                            system_prompt=notes_system_prompt,
                            temperature=0.3,
                            base_url=st.session_state.ollama_url,
                        )

                        note_response = st.write_stream(response_stream)
                        st.session_state.notes_messages.append(
                            {"role": "assistant", "content": note_response}
                        )

# ======================================================================================
# 10. FEATURE 4: AI STUDY PLANNER (CUSTOM TIMETABLE GENERATOR)
# ======================================================================================

elif selected_page == "📅 AI Study Planner":
    st.markdown(
        """
        <div class="hero-header">
            <h1>📅 AI Study Planner</h1>
            <p>Generate a realistic, stress-free day-by-day timetable tailored to your subjects, daily hours, and target exam date.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    form_col, result_col = st.columns([1, 1.4], gap="large")

    with form_col:
        st.markdown("### 📝 **Enter Study Parameters**")

        with st.form("study_planner_form"):
            subjects_input = st.text_area(
                "📚 Subjects to cover (comma-separated):",
                value="Data Structures & Algorithms, Operating Systems, Database Management Systems, Computer Networks",
                height=90,
            )

            c1, c2 = st.columns(2)
            with c1:
                daily_hours = st.slider(
                    "⏰ Daily study hours:",
                    min_value=1.0,
                    max_value=12.0,
                    value=4.0,
                    step=0.5,
                )
            with c2:
                prep_level = st.selectbox(
                    "📊 Current level:",
                    options=[
                        "Beginner (Starting from scratch)",
                        "Intermediate (Familiar with basics)",
                        "Revision (Full syllabus already done once)",
                    ],
                    index=1,
                )

            exam_target_date = st.date_input(
                "🎯 Target Exam / Submission Date:",
                value=date.today() + timedelta(days=14),
                min_value=date.today() + timedelta(days=1),
                max_value=date.today() + timedelta(days=180),
            )

            study_goals = st.text_input(
                "🎯 Specific Goals / Priorities:",
                value="Focus on previous year questions (PYQs) and solve numericals",
            )

            submit_plan = st.form_submit_button(
                "🚀 Generate My Study Plan", use_container_width=True
            )

        days_remaining = (exam_target_date - date.today()).days
        st.info(
            f"⏳ **Time Remaining:** `{days_remaining}` days until `{exam_target_date.strftime('%B %d, %Y')}`"
        )

    with result_col:
        st.markdown("### 📋 **Your Generated Timetable**")

        if submit_plan:
            if not is_online:
                st.error("⚠️ Ollama is offline. Please launch Ollama.")
            else:
                with st.spinner(
                    f"Gemma 3:1B is structuring your {days_remaining}-day timetable..."
                ):
                    planner_prompt = f"""
Create a highly practical, realistic, day-by-day college study timetable based on these constraints:

- Subjects to cover: {subjects_input}
- Total days available: {days_remaining} days (From {date.today().strftime('%Y-%m-%d')} to {exam_target_date.strftime('%Y-%m-%d')})
- Available hours per day: {daily_hours} hours
- Student Preparation Level: {prep_level}
- Student Goals: {study_goals}

Structure clearly with:
1. 🎯 **Executive Strategy**: 2-3 sentences.
2. ⏰ **Recommended Daily Routine**: Divide {daily_hours} hours into Pomodoro blocks.
3. 🗓️ **Day-by-Day Roadmap**: Grouped into Phase 1 (Foundation), Phase 2 (PYQs & Problem Solving), Phase 3 (Mock Tests & Final Revision).
4. 💡 **Last 48-Hour Exam Checklist**: Key tips before the exam.
"""

                    planner_system = (
                        "You are an expert college academic mentor and schedule planner. "
                        "You craft realistic, achievable, stress-free timetables that help students maximize marks."
                    )

                    plan_stream = call_ollama_stream(
                        messages=[{"role": "user", "content": planner_prompt}],
                        model=st.session_state.model_name,
                        system_prompt=planner_system,
                        temperature=0.4,
                        base_url=st.session_state.ollama_url,
                    )

                    st.session_state.saved_study_plan = st.write_stream(plan_stream)

        elif st.session_state.saved_study_plan:
            st.markdown(st.session_state.saved_study_plan)
        else:
            st.markdown(
                """
                <div style="border: 2px dashed #cbd5e1; border-radius: 14px; padding: 3rem 1.5rem; text-align: center; color: #64748b; background: #ffffff;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📅</div>
                    <h4 style="font-family: 'Outfit';">No Plan Generated Yet</h4>
                    <p style="font-size: 0.9rem;">Fill in your subjects and hours on the left, then click <b>'Generate My Study Plan'</b>.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.session_state.saved_study_plan:
            st.download_button(
                label="📥 Download Study Plan (Markdown)",
                data=st.session_state.saved_study_plan,
                file_name=f"CampusSaathi_Study_Plan_{date.today().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

# ======================================================================================
# 11. FEATURE 5: CAMPUS NOTICES
# ======================================================================================

elif selected_page == "📢 Campus Notices":
    st.markdown(
        """
        <div class="hero-header">
            <h1>📢 Campus Notices & Bulletin Board</h1>
            <p>Stay updated with college circulars, exam dates, fee reminders, and campus events.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="demo-disclaimer">
            <b>⚠️ DEMO BULLETIN BOARD:</b> The circulars and announcements displayed below are 
            <b>sample mock examples</b> created solely for educational demonstration in this college project. 
            They do <u>not</u> represent real official announcements from any educational institution.
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_board, tab_ask_notice = st.tabs(
        ["📋 College Notice Board", "🤖 Ask Notice Assistant"]
    )

    with tab_board:
        filter_col, search_col = st.columns([1, 2])
        with filter_col:
            categories = [
                "All Categories",
                "Examinations",
                "Events",
                "Library",
                "Administrative",
            ]
            selected_cat = st.selectbox("Filter by Category:", options=categories)
        with search_col:
            search_term = st.text_input(
                "🔍 Search Notices:", placeholder="Type keywords like 'exam', 'fee'..."
            )

        filtered_notices = SAMPLE_NOTICES
        if selected_cat != "All Categories":
            filtered_notices = [
                n for n in filtered_notices if n["category"] == selected_cat
            ]
        if search_term.strip():
            term = search_term.strip().lower()
            filtered_notices = [
                n
                for n in filtered_notices
                if term in n["title"].lower()
                or term in n["content"].lower()
                or term in n["category"].lower()
            ]

        st.caption(f"Showing **{len(filtered_notices)}** notice(s)")

        for notice in filtered_notices:
            st.markdown(
                f"""
                <div class="notice-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="notice-date">📅 {notice['date']} | Reference: {notice['id']}</span>
                        <span class="badge-tag {notice.get('css_class', 'tag-exam')}">{notice['tag']}</span>
                    </div>
                    <div class="notice-title">{notice['title']}</div>
                    <div class="notice-desc">{notice['content']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_ask_notice:
        st.markdown("#### 🤖 Ask Questions About the Campus Notices")
        st.caption(
            "Use Gemma 3:1B to quickly find deadlines, exam schedules, or eligibility criteria from the bulletin board."
        )

        notice_query = st.text_input(
            "Ask anything about the campus notices:",
            placeholder="E.g., When is the last date to submit the exam fee without penalty?",
        )

        if st.button("🔎 Query Notice Board", use_container_width=True):
            if not notice_query.strip():
                st.warning("Please type a question.")
            elif not is_online:
                st.error("⚠️ Ollama is offline. Please launch Ollama.")
            else:
                all_notices_text = "\n\n".join(
                    [
                        f"Notice ID: {n['id']}\nCategory: {n['category']}\nDate: {n['date']}\nTitle: {n['title']}\nContent: {n['content']}"
                        for n in SAMPLE_NOTICES
                    ]
                )

                system_notice_prompt = (
                    "You are the Campus Notice Desk AI. A student is asking a question regarding college announcements. "
                    "Answer their question accurately and concisely using ONLY the following mock notice board database.\n\n"
                    f"=== CAMPUS NOTICES DATABASE ===\n{all_notices_text}\n=== END OF NOTICES ===\n"
                    "Always mention the relevant Notice Date, Title, and Reference ID in your answer."
                )

                with st.spinner("Checking notices..."):
                    response = call_ollama_sync(
                        messages=[{"role": "user", "content": notice_query}],
                        model=st.session_state.model_name,
                        system_prompt=system_notice_prompt,
                        temperature=0.2,
                        base_url=st.session_state.ollama_url,
                    )
                    st.markdown(response)

# ======================================================================================
# 12. FEATURE 6: SETTINGS & SYSTEM DIAGNOSTICS
# ======================================================================================

elif selected_page == "⚙️ Settings & System Status":
    st.markdown(
        """
        <div class="hero-header">
            <h1>⚙️ Settings & System Diagnostics</h1>
            <p>Verify your local Ollama connection, manage local models, and configure response parameters.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_settings, col_guide = st.columns([1, 1], gap="large")

    with col_settings:
        st.markdown("### 🔌 **Ollama API Configuration**")

        st.text_input(
            "Ollama Base URL:",
            value=st.session_state.ollama_url,
            key="config_url_input",
            help="Default is http://localhost:11434.",
        )

        if st.button("🔄 Test Connection Now", use_container_width=True):
            st.session_state.ollama_url = st.session_state.config_url_input
            test_ok, models_found, err_msg = test_ollama_connection(
                st.session_state.ollama_url
            )
            if test_ok:
                st.success(
                    f"✅ Successfully connected to Ollama! Found {len(models_found)} model(s)."
                )
            else:
                st.error(f"❌ Connection Failed: {err_msg}")

        st.markdown("---")
        st.markdown("### 🧠 **Model Selection**")

        if is_online and installed_models:
            model_options = list(installed_models)
            if "gemma3:1b" not in model_options:
                model_options.insert(0, "gemma3:1b (Not installed yet)")

            selected_model = st.selectbox(
                "Active Model:",
                options=model_options,
                index=0,
                help="Gemma 3:1B is recommended for low memory usage and high speed on laptops.",
            )
            clean_selected_model = selected_model.split(" ")[0]
            st.session_state.model_name = clean_selected_model
        else:
            st.session_state.model_name = st.text_input(
                "Model Tag:",
                value=st.session_state.model_name,
                help="Default: gemma3:1b",
            )

        st.session_state.temperature = st.slider(
            "🌡️ Creativity (Temperature):",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.05,
            help="Lower values (0.2) give more deterministic/factual answers; higher values (0.8) are more creative.",
        )

    with col_guide:
        st.markdown("### 🛠️ **Troubleshooting Checklist for Windows**")

        with st.expander("1. How Photo OCR Works Completely Offline", expanded=True):
            st.markdown(
                """
                - **Zero Extra Installs:** Uses Windows' native `Windows.Media.Ocr` API.
                - **High Privacy:** Your photos never leave your device.
                - **Textbook & Handwriting Support:** Recognizes printed textbook text, equations, and neat handwriting.
                """
            )

        with st.expander("2. Ollama is showing 'Offline' in CampusSaathi"):
            st.markdown(
                """
                - Run in PowerShell: `ollama serve`
                - Test in browser: Navigate to `http://localhost:11434`
                """
            )

        with st.expander("3. Error: 'Model gemma3:1b not found'"):
            st.markdown(
                """
                Open PowerShell and run:
                ```powershell
                ollama pull gemma3:1b
                ```
                """
            )

# ======================================================================================
# END OF FILE: app.py
# ======================================================================================
