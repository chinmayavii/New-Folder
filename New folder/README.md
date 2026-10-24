# 🎓 CampusSaathi AI — Local AI College Companion

> **A 100% Local, Private, and Free AI-Powered Academic Assistant for College Students**  
> Built with **Python**, **Streamlit**, **Ollama**, and Google's lightweight **Gemma 3:1B** model.  
> *No API keys, no internet connection required for inference, and zero cloud subscription fees.*

---

## 🌟 Table of Contents
1. [Overview](#-overview)
2. [Why CampusSaathi AI?](#-why-campussaathi-ai)
3. [Key Features](#-key-features)
4. [Tech Stack](#-tech-stack)
5. [Project Folder Structure](#-project-folder-structure)
6. [Windows Installation & Setup Guide](#-windows-installation--setup-guide)
7. [Running the Application](#-running-the-application)
8. [Troubleshooting Common Issues](#-troubleshooting-common-issues)
9. [College Viva & Presentation Q&A](#-college-viva--presentation-qa)
10. [License](#-license)

---

## 📖 Overview

**CampusSaathi AI** is designed specifically for undergraduate and diploma college students. It provides a complete personal academic workspace that runs entirely on the student's personal computer or laptop.

Unlike commercial AI tools that require paid API subscriptions, cloud credits, or continuous high-speed internet, **CampusSaathi AI** leverages **Ollama**, the ultra-efficient **Gemma 3:1B** language model, and **Windows Native Offline OCR** to provide instant study help, photo note comprehension, PDF extraction, personalized study scheduling, and college circular queries—all completely offline and private.

---

## 💡 Why CampusSaathi AI?

| Feature | Cloud AI Tools (ChatGPT / Gemini Cloud) | CampusSaathi AI (Local) |
| :--- | :--- | :--- |
| **Data Privacy** | Notes & photos uploaded to remote servers | **100% Private** on local disk |
| **API Cost / Keys** | Requires credit card or paid API keys | **₹0 Free Forever** (No API Key needed) |
| **Offline Capability**| Fails when internet or WiFi is down | **Works Completely Offline** |
| **Photo / Notes OCR** | Cloud vision APIs with billing | **Native Windows Offline OCR** (0 cost) |
| **Hardware Fit** | Heavy enterprise backends | **Runs on student laptops** (4GB–8GB RAM) |
| **Student-Focused** | Generic general-purpose chat | **Custom prompts for college exams & notes** |

---

## ✨ Key Features

### 1. 📚 AI Study Assistant
* **Adaptive Explanation Modes:**
  * 💡 *Simple & Intuitive:* Breaks down tough concepts for 1st-year students using intuitive analogies.
  * 📝 *Exam Revision Notes:* Formulates concise bullet points, definitions, laws, and key formulas.
  * 🪜 *Step-by-Step Breakdown:* Generates derivations, algorithm traces, and numerical solutions.
  * 💻 *Code & Examples:* Generates clean, well-commented code snippets in C, C++, Python, Java, etc.
  * 🎯 *Mock Viva & Quiz:* Quizzes students with typical viva-voce questions and model answers.
* **Streamed Responses:** Uses real-time token streaming (`requests` + `st.write_stream`) for zero wait times.

### 2. 📸 Snap & Study (Photo Explainer & Native OCR) — *NEW!*
* **Upload Study Photos:** Students can upload photos of:
  * Textbook pages and printed notes
  * Neat handwritten notes
  * Blackboard / whiteboard lecture photos
  * Numerical problems, equations, and question paper snapshots
* **Zero-Cloud Offline OCR:** Uses Windows' native `Windows.Media.Ocr` engine to extract text directly from the photo in under 1 second without internet or third-party cloud OCR APIs.
* **Instant Auto-Summary:** Automatically produces an executive study summary upon upload.
* **Study Model Actions:**
  * 📝 *Full Study Summary:* High-yield overview and key concepts.
  * 💡 *Step-by-Step Solver:* Explains numericals and derivation steps.
  * 📌 *Formulas & Constants:* Extracts laws, variables, and SI units into a cheat sheet.
  * 🎯 *Top Exam Questions:* Predicts 4–5 college semester exam and viva questions.
  * 🪜 *Explain Simply (ELI5):* Explains the photo in plain words with a real-world analogy.
  * 💻 *Practice Problems:* Generates practice questions based on the photo.
* **Interactive Photo Chat:** Multi-turn Q&A specifically grounded in the photo content.
* **Export Study Sheet:** Download the full photo analysis as a Markdown file.

### 3. 📄 Ask My Notes (PDF Q&A)
* **Local PDF Extraction:** Uses `pypdf` to read text-based lecture notes and textbooks directly into memory.
* **Document Diagnostics:** Shows page count, word count, and extracted text preview.
* **Instant Academic Actions:** 5-Minute Summary, Top 5 Exam Questions, Formula Sheet.
* **Context-Grounded Chat:** Prompts Gemma 3:1B to answer questions strictly using the uploaded notes.

### 4. 📅 AI Study Planner
* **Input Parameters:** Accepts subjects list, available study hours (1–12 hrs/day), exam deadline date, current prep level, and personal goals.
* **Day-by-Day Roadmap:** Creates a realistic Pomodoro-based study schedule with built-in revision cycles and mock test days.
* **Downloadable Schedule:** One-click download button (`.md` format) to save the study plan for offline tracking.

### 5. 📢 Campus Notices & Bulletin Board
* **Mock Notice Board:** Displays realistic categorized announcements (Exams, Hackathons, Library, Placements, Fees).
* **Transparent Disclaimer:** Clearly labeled with demo banners as sample announcements for academic illustration.
* **AI Notice Assistant:** Students can query the notice board in natural language (e.g., *"When is the exam form deadline without late fee?"*).

### 6. ⚙️ Diagnostics & Settings
* **Real-time Ollama Ping:** Displays a live green/red connection status badge.
* **Model Detection:** Detects installed Ollama models and alerts if `gemma3:1b` needs to be pulled.
* **Adjustable Temperature:** Slider to fine-tune AI response creativity vs factual accuracy.

---

## 🛠️ Tech Stack

* **Frontend & Web Framework:** [Streamlit](https://streamlit.io/) + Standalone Pure-Python Web UI
* **LLM Engine:** [Ollama](https://ollama.com/) (Local model serving runtime)
* **Language Model:** Google [Gemma 3:1B](https://ollama.com/library/gemma3:1b) (Quantized ~800 MB footprint)
* **OCR Engine:** Windows Native `Windows.Media.Ocr` (Offline, zero dependencies)
* **PDF Parser:** [pypdf](https://pypi.org/project/pypdf/) (Pure Python PDF library)
* **Networking:** [requests](https://pypi.org/project/requests/) (REST API communication with Ollama)

---

## 📂 Project Folder Structure

```text
CampusSaathi-AI/
│
├── app.py                 # Main Streamlit fullstack application (UI, logic, OCR & Ollama client)
├── web_server.py          # Standalone pure Python web server (zero pip dependencies)
├── ocr_helper.ps1         # Windows native offline OCR bridge (Windows.Media.Ocr)
├── setup.bat              # One-click automated setup for Windows
├── run.bat                # One-click Streamlit launcher
├── run_standalone.bat     # One-click standalone launcher
├── requirements.txt       # Python package dependencies (streamlit, requests, pypdf)
├── README.md              # Detailed project documentation and setup manual
├── .gitignore             # Standard git ignore file for Python & Streamlit projects
├── LICENSE                # Open-source MIT license
└── sample_notes/
    ├── Sample_College_Notes.pdf      # Sample text PDF (Data Structures & DBMS)
    └── Sample_Physics_Notes.png      # Sample study photo (Physics formulas for testing)
```

---

## 💻 Windows Installation & Setup Guide

### Step 1: Install Python (Version 3.10+)
1. Download Python from [python.org](https://www.python.org/downloads/).
2. **Important:** Check the box **"Add python.exe to PATH"**.

### Step 2: Install Ollama & Pull Gemma 3:1B
1. Download Ollama from [ollama.com/download](https://ollama.com/download) and run `OllamaSetup.exe`.
2. Open **PowerShell** and pull Gemma 3:1B:
   ```powershell
   ollama pull gemma3:1b
   ```

### Step 3: Run CampusSaathi AI
You have **two easy ways** to run CampusSaathi AI:

#### Option A: One-Click (Recommended)
Simply **double-click** [`setup.bat`](file:///c:/Users/Avnish/Downloads/New%20folder/setup.bat) or [`run_standalone.bat`](file:///c:/Users/Avnish/Downloads/New%20folder/run_standalone.bat).

#### Option B: Terminal Command
```powershell
# In PowerShell inside the project directory:
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🔧 Troubleshooting Common Issues

### 1. `Ollama Offline` indicator in red
* **Fix:** Open PowerShell and run: `ollama serve`. Make sure `http://localhost:11434` displays `Ollama is running`.

### 2. Error: `Model 'gemma3:1b' not found`
* **Fix:** Run `ollama pull gemma3:1b` in PowerShell.

### 3. Photo text not recognized or blurry
* **Fix:** Ensure the photo is clear, well-lit, and upright. You can also manually edit any detected characters in the **"Detected Text"** box.

---

## 🎓 College Viva & Presentation Q&A

1. **Q: How does the Photo Upload feature work without a paid cloud API like Google Cloud Vision?**  
   *A:* CampusSaathi AI leverages Windows' built-in `Windows.Media.Ocr` engine via PowerShell interop. It executes locally on CPU in sub-second time with zero cloud costs and zero privacy leaks. The extracted text is then fed into the local Gemma 3:1B model for academic analysis.

2. **Q: Why is Gemma 3:1B ideal for student laptops?**  
   *A:* Gemma 3:1B uses ~800 MB of disk space and under 1.5 GB of RAM during generation. It runs comfortably on budget dual-core and quad-core laptops without requiring an expensive NVIDIA GPU.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
