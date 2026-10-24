"""
========================================================================================
 CampusSaathi AI - Standalone Zero-Dependency Local Web Server
========================================================================================
 Premium Modern Frontend Edition:
   - Modern Typography: Google Fonts (Outfit & Plus Jakarta Sans)
   - Refined Text Hierarchy, Micro-Interactions, and Polished Color Palette
   - Card Surfaces with Subtle Borders & Layered Shadows
   - Categorized Notice Badges, Interactive Chips, and Polished Chat Bubbles
   - 100% Offline & Zero External Python Dependencies
========================================================================================
"""

import base64
import http.server
import json
import os
import socketserver
import subprocess
import sys
import tempfile
import urllib.request
import webbrowser
from urllib.parse import parse_qs, urlparse

PORT = 8501
OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "gemma3:1b"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CampusSaathi AI | Local AI College Companion</title>
    
    <!-- Premium Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

    <style>
        :root {
            /* Primary Brand Colors */
            --primary: #4338ca;
            --primary-hover: #3730a3;
            --primary-gradient: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            --header-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
            
            /* Neutral Backgrounds */
            --bg-canvas: #f8fafc;
            --surface: #ffffff;
            --surface-hover: #f1f5f9;
            --surface-subtle: #f8fafc;
            
            /* Text & Contrast */
            --text-heading: #0f172a;
            --text-body: #334155;
            --text-muted: #64748b;
            --text-light: #94a3b8;
            
            /* Borders & Shadows */
            --border-subtle: #e2e8f0;
            --border-hover: #cbd5e1;
            --border-focus: #818cf8;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 16px -2px rgba(15, 23, 42, 0.08), 0 2px 6px -1px rgba(15, 23, 42, 0.04);
            --shadow-lg: 0 10px 25px -3px rgba(15, 23, 42, 0.1), 0 4px 10px -2px rgba(15, 23, 42, 0.05);
            --shadow-primary: 0 4px 14px 0 rgba(79, 70, 229, 0.25);
            
            /* Status & Accents */
            --success: #10b981;
            --success-bg: #ecfdf5;
            --success-border: #a7f3d0;
            --warning: #f59e0b;
            --warning-bg: #fffbeb;
            --danger: #ef4444;
            --danger-bg: #fef2f2;
            
            --radius-lg: 16px;
            --radius-md: 10px;
            --radius-sm: 6px;
            --radius-pill: 9999px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        body {
            background-color: var(--bg-canvas);
            color: var(--text-body);
            display: flex;
            height: 100vh;
            overflow: hidden;
            font-size: 0.925rem;
            line-height: 1.5;
        }

        /* ================= SIDEBAR ================= */
        aside {
            width: 300px;
            background: var(--surface);
            border-right: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            padding: 1.5rem 1.15rem;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.02);
            z-index: 10;
        }

        .brand-container {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 0.35rem;
        }
        .brand-icon {
            width: 38px;
            height: 38px;
            background: var(--primary-gradient);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            box-shadow: var(--shadow-primary);
        }
        .brand-text {
            font-family: 'Outfit', sans-serif;
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .brand-sub {
            font-size: 0.78rem;
            color: var(--text-muted);
            font-weight: 500;
            margin-bottom: 1.25rem;
            padding-left: 50px;
        }

        /* Status Badge */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            border-radius: var(--radius-pill);
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            width: fit-content;
        }
        .status-badge.online {
            background: var(--success-bg);
            color: #065f46;
            border: 1px solid var(--success-border);
        }
        .status-badge.offline {
            background: var(--danger-bg);
            color: #991b1b;
            border: 1px solid #fecaca;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: currentColor;
            display: inline-block;
            box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.15); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }

        /* Navigation List */
        nav {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .nav-label {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-light);
            margin: 0.5rem 0 0.4rem 0.5rem;
        }
        .nav-btn {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0.75rem 1rem;
            border-radius: var(--radius-md);
            border: 1px solid transparent;
            background: transparent;
            color: var(--text-body);
            font-size: 0.88rem;
            font-weight: 600;
            cursor: pointer;
            text-align: left;
            transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .nav-btn:hover {
            background: var(--surface-hover);
            color: var(--text-heading);
            transform: translateX(2px);
        }
        .nav-btn.active {
            background: #eef2ff;
            color: var(--primary);
            border-color: #c7d2fe;
            box-shadow: 0 2px 6px rgba(79, 70, 229, 0.08);
        }

        .sidebar-footer {
            margin-top: auto;
            background: var(--surface-subtle);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 0.85rem 1rem;
            font-size: 0.78rem;
            color: var(--text-muted);
        }
        .sidebar-footer b { color: var(--text-heading); }

        /* ================= MAIN CONTENT ================= */
        main {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background-color: var(--bg-canvas);
        }

        /* Hero Header */
        header {
            background: var(--header-gradient);
            color: #ffffff;
            padding: 1.4rem 2.2rem;
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.15);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .header-title-box h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: -0.4px;
            color: #ffffff;
            margin-bottom: 0.2rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .header-title-box p {
            font-size: 0.88rem;
            color: #cbd5e1;
            font-weight: 400;
        }
        .header-badge {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #f8fafc;
            padding: 6px 14px;
            border-radius: var(--radius-pill);
            font-size: 0.78rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Content Area */
        .content-area {
            flex: 1;
            overflow-y: auto;
            padding: 1.8rem 2.2rem;
            scroll-behavior: smooth;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; animation: fadeIn 0.25s ease-out; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Card Surfaces */
        .card {
            background: var(--surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin-bottom: 1.4rem;
            box-shadow: var(--shadow-sm);
            transition: box-shadow 0.2s, border-color 0.2s;
        }
        .card:hover {
            box-shadow: var(--shadow-md);
            border-color: var(--border-hover);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
        }
        .card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-heading);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .card-description {
            font-size: 0.88rem;
            color: var(--text-muted);
            margin-bottom: 1rem;
            line-height: 1.55;
        }

        /* Action Buttons Grid */
        .action-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 0.8rem;
        }
        .btn-action-tile {
            background: #ffffff;
            border: 1.5px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 0.85rem 1rem;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-heading);
            cursor: pointer;
            text-align: left;
            transition: all 0.18s ease;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .btn-action-tile .tile-icon { font-size: 1.25rem; }
        .btn-action-tile .tile-desc { font-size: 0.72rem; color: var(--text-muted); font-weight: 400; }
        .btn-action-tile:hover {
            border-color: var(--border-focus);
            background: #f5f7ff;
            color: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.12);
        }

        /* Prompt Chips */
        .chips-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 1.2rem;
        }
        .chip {
            background: var(--surface);
            color: var(--primary);
            border: 1px solid #c7d2fe;
            padding: 6px 14px;
            border-radius: var(--radius-pill);
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            box-shadow: var(--shadow-sm);
        }
        .chip:hover {
            background: var(--primary);
            color: #ffffff;
            border-color: var(--primary);
            transform: translateY(-1px);
            box-shadow: var(--shadow-primary);
        }

        /* Chat Workspace */
        .chat-box {
            display: flex;
            flex-direction: column;
            gap: 14px;
            margin-bottom: 1.2rem;
            min-height: 280px;
            max-height: 480px;
            overflow-y: auto;
            padding: 1rem;
            background: var(--surface-subtle);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
        }
        .chat-box::-webkit-scrollbar { width: 6px; }
        .chat-box::-webkit-scrollbar-track { background: transparent; }
        .chat-box::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }

        .msg-bubble {
            max-width: 82%;
            padding: 1rem 1.25rem;
            border-radius: 14px;
            font-size: 0.92rem;
            line-height: 1.6;
            word-wrap: break-word;
        }
        .msg-bubble.user {
            align-self: flex-end;
            background: var(--primary-gradient);
            color: #ffffff;
            border-bottom-right-radius: 4px;
            box-shadow: var(--shadow-primary);
        }
        .msg-bubble.ai {
            align-self: flex-start;
            background: var(--surface);
            color: var(--text-heading);
            border: 1px solid var(--border-subtle);
            border-bottom-left-radius: 4px;
            box-shadow: var(--shadow-sm);
        }
        .msg-bubble.ai h3, .msg-bubble.ai h4 {
            font-family: 'Outfit', sans-serif;
            color: var(--text-heading);
            margin: 0.6rem 0 0.3rem 0;
            font-weight: 700;
        }
        .msg-bubble.ai ul, .msg-bubble.ai ol {
            margin-left: 1.4rem;
            margin-top: 0.3rem;
            margin-bottom: 0.5rem;
        }
        .msg-bubble.ai code {
            font-family: 'JetBrains Mono', monospace;
            background: #1e293b;
            color: #f8fafc;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.82rem;
        }
        .msg-bubble.ai pre {
            background: #0f172a;
            color: #f8fafc;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 0.6rem 0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.84rem;
        }

        /* Chat Input Bar */
        .chat-input-bar {
            display: flex;
            gap: 10px;
            background: var(--surface);
            padding: 6px;
            border: 1.5px solid var(--border-subtle);
            border-radius: 12px;
            box-shadow: var(--shadow-sm);
            transition: all 0.2s;
        }
        .chat-input-bar:focus-within {
            border-color: var(--border-focus);
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.12);
        }
        .chat-input-bar input {
            flex: 1;
            border: none;
            outline: none;
            padding: 0.75rem 1rem;
            font-size: 0.92rem;
            color: var(--text-heading);
            background: transparent;
        }
        .chat-input-bar input::placeholder { color: var(--text-light); }

        /* General Inputs */
        input[type="text"], input[type="number"], textarea, select {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 1.5px solid var(--border-subtle);
            border-radius: var(--radius-md);
            font-size: 0.9rem;
            color: var(--text-heading);
            background: var(--surface);
            outline: none;
            transition: border-color 0.15s, box-shadow 0.15s;
        }
        input:focus, textarea:focus, select:focus {
            border-color: var(--border-focus);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12);
        }

        /* Buttons */
        .btn-primary {
            background: var(--primary-gradient);
            color: #ffffff;
            border: none;
            padding: 0.75rem 1.6rem;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.18s ease;
            box-shadow: var(--shadow-primary);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(79, 70, 229, 0.35);
        }
        .btn-secondary {
            background: var(--surface);
            color: var(--text-body);
            border: 1.5px solid var(--border-subtle);
            padding: 0.6rem 1rem;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 0.82rem;
            cursor: pointer;
            transition: all 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .btn-secondary:hover {
            background: var(--surface-hover);
            border-color: var(--border-hover);
            color: var(--text-heading);
        }

        /* Study Summary Card Callout */
        .summary-callout {
            background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
            border: 1.5px solid #a7f3d0;
            border-left: 5px solid #10b981;
            border-radius: var(--radius-md);
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.2rem;
            box-shadow: var(--shadow-sm);
        }
        .summary-callout-header {
            font-family: 'Outfit', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            color: #065f46;
            margin-bottom: 0.4rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .summary-callout-body {
            font-size: 0.9rem;
            color: #047857;
            line-height: 1.6;
            white-space: pre-wrap;
        }

        /* Notice Board Cards */
        .notice-card {
            background: var(--surface);
            border: 1.5px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 1.2rem 1.4rem;
            margin-bottom: 1rem;
            transition: all 0.18s ease;
            position: relative;
        }
        .notice-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            border-color: #cbd5e1;
        }
        .notice-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.4rem;
        }
        .notice-date {
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .notice-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-heading);
            margin-bottom: 0.35rem;
        }
        .notice-desc {
            font-size: 0.88rem;
            color: var(--text-body);
            line-height: 1.5;
        }

        /* Category Badges */
        .badge-cat {
            padding: 3px 10px;
            border-radius: var(--radius-pill);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.4px;
            text-transform: uppercase;
        }
        .badge-exam { background: #f3e8ff; color: #7e22ce; border: 1px solid #d8b4fe; }
        .badge-event { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
        .badge-library { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
        .badge-fee { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }

        /* Demo Disclaimer Banner */
        .demo-banner {
            background: #fffbeb;
            border: 1.5px solid #fef3c7;
            border-left: 4px solid var(--warning);
            border-radius: var(--radius-md);
            padding: 0.9rem 1.2rem;
            font-size: 0.84rem;
            color: #92400e;
            margin-bottom: 1.2rem;
            line-height: 1.5;
        }

        /* File Dropzone Style */
        .upload-dropzone {
            border: 2px dashed #c7d2fe;
            background: #f8faff;
            border-radius: var(--radius-md);
            padding: 1.6rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: 0.8rem;
        }
        .upload-dropzone:hover {
            border-color: var(--primary);
            background: #f0f4ff;
        }
    </style>
</head>
<body>

    <!-- ================= SIDEBAR ================= -->
    <aside>
        <div class="brand-container">
            <div class="brand-icon">🎓</div>
            <div class="brand-text">CampusSaathi</div>
        </div>
        <div class="brand-sub">Local AI College Companion</div>
        
        <div id="status-pill" class="status-badge online">
            <span class="status-dot"></span>
            <span>Checking Ollama...</span>
        </div>

        <nav>
            <div class="nav-label">Academic Tools</div>
            <button class="nav-btn active" onclick="switchTab('tab-study')">
                <span>📚</span> AI Study Assistant
            </button>
            <button class="nav-btn" onclick="switchTab('tab-photo')">
                <span>📸</span> Snap & Study (Photo)
            </button>
            <button class="nav-btn" onclick="switchTab('tab-notes')">
                <span>📄</span> Ask My Notes
            </button>
            <button class="nav-btn" onclick="switchTab('tab-planner')">
                <span>📅</span> AI Study Planner
            </button>
            
            <div class="nav-label" style="margin-top: 1rem;">Campus Info</div>
            <button class="nav-btn" onclick="switchTab('tab-notices')">
                <span>📢</span> Campus Notices
            </button>
            <button class="nav-btn" onclick="switchTab('tab-settings')">
                <span>⚙️</span> System & Diagnostics
            </button>
        </nav>

        <div class="sidebar-footer">
            <div style="font-weight: 700; color: var(--text-heading); margin-bottom: 2px;">Offline & Free</div>
            <div>Powered by <b>Gemma 3:1B</b> via Ollama. 100% private on your machine.</div>
        </div>
    </aside>

    <!-- ================= MAIN WORKSPACE ================= -->
    <main>
        <header>
            <div class="header-title-box">
                <h1 id="header-title">📚 AI Study Assistant</h1>
                <p id="header-desc">Your 24/7 personal college tutor for concepts, derivations, and exam revision notes.</p>
            </div>
            <div class="header-badge">
                <span>🧠</span> Model: <b>gemma3:1b</b>
            </div>
        </header>

        <div class="content-area">
            
            <!-- 1. AI STUDY ASSISTANT -->
            <section id="tab-study" class="tab-content active">
                <div class="card" style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <label style="font-size: 0.88rem; font-weight: 700; color: var(--text-heading);">🎯 Tutoring Style:</label>
                            <select id="study-mode" style="width: auto; padding: 6px 12px; font-weight: 600;">
                                <option value="Simple & Intuitive">💡 Simple & Intuitive (1st Year Level)</option>
                                <option value="Exam Revision Notes">📝 Exam Revision Notes (High-Yield Bullet Points)</option>
                                <option value="Step-by-Step Breakdown">🪜 Step-by-Step Derivation & Algorithms</option>
                                <option value="Mock Viva Questions">🎯 Mock Viva & Quiz Questions</option>
                            </select>
                        </div>
                        <button class="btn-secondary" onclick="clearStudyChat()">🗑️ Clear Chat</button>
                    </div>
                </div>

                <div class="chips-container">
                    <span class="chip" onclick="fillPrompt('Explain QuickSort vs MergeSort with time complexity and tabular comparison')">⚡ QuickSort vs MergeSort</span>
                    <span class="chip" onclick="fillPrompt('Explain ACID properties in DBMS with real banking examples')">⚡ ACID in DBMS</span>
                    <span class="chip" onclick="fillPrompt('Difference between Process and Thread with memory architecture')">⚡ Process vs Thread</span>
                    <span class="chip" onclick="fillPrompt('Explain Database Normalization from 1NF to BCNF in short notes')">⚡ Normalization 1NF-BCNF</span>
                </div>

                <div id="study-chat" class="chat-box">
                    <div class="msg-bubble ai">
                        👋 <b>Namaste! I am CampusSaathi AI</b>, your local college study buddy.<br><br>
                        Ask me any concept from your syllabus, request step-by-step mathematical proofs, or get high-yield revision notes. How can I help you excel today?
                    </div>
                </div>

                <div class="chat-input-bar">
                    <input type="text" id="study-input" placeholder="Type your college subject question or doubt..." onkeydown="if(event.key==='Enter') sendStudyMessage()">
                    <button class="btn-primary" onclick="sendStudyMessage()">Send Question</button>
                </div>
            </section>

            <!-- 2. SNAP & STUDY (PHOTO UPLOAD & OCR) -->
            <section id="tab-photo" class="tab-content">
                <div style="display: grid; grid-template-columns: 1fr 1.35fr; gap: 1.6rem;">
                    
                    <!-- Left: Upload & Detected Content -->
                    <div>
                        <div class="card">
                            <div class="card-header">
                                <div class="card-title">📸 Upload Study Photo</div>
                            </div>
                            <p class="card-description">Upload textbook pages, handwritten notes, numerical problems, or blackboard equations. Windows native OCR extracts text completely offline.</p>
                            
                            <input type="file" id="photo-input" accept="image/*" style="display: none;" onchange="handlePhotoUpload(this)">
                            
                            <div class="upload-dropzone" onclick="document.getElementById('photo-input').click()">
                                <div style="font-size: 2rem; margin-bottom: 0.3rem;">📷</div>
                                <div style="font-weight: 700; color: var(--text-heading); font-size: 0.95rem;">Click to Upload Photo</div>
                                <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">Supports PNG, JPG, JPEG, WEBP</div>
                            </div>

                            <div style="display: flex; gap: 8px;">
                                <button class="btn-secondary" style="flex: 1;" onclick="loadSamplePhysicsPhoto()">🧪 Try Sample Physics Photo</button>
                                <button class="btn-secondary" onclick="clearPhoto()">🗑️ Clear</button>
                            </div>

                            <div id="photo-preview-container" style="margin-top: 14px; display: none;">
                                <img id="photo-preview" src="" style="width: 100%; max-height: 200px; object-fit: contain; border-radius: var(--radius-md); border: 1.5px solid var(--border-subtle); background: #ffffff;">
                            </div>

                            <div style="margin-top: 14px;">
                                <label style="font-size: 0.82rem; font-weight: 700; color: var(--text-heading);">📝 Detected Text from Photo (Editable):</label>
                                <textarea id="photo-extracted-text" style="height: 120px; margin-top: 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;" placeholder="Text extracted from the photo will appear here..."></textarea>
                            </div>
                        </div>
                    </div>

                    <!-- Right: Study Actions & Results -->
                    <div>
                        <div class="card">
                            <div class="card-header">
                                <div class="card-title">🧠 Academic Study Actions</div>
                            </div>
                            <div class="action-grid">
                                <button class="btn-action-tile" onclick="runPhotoAction('summarize')">
                                    <span class="tile-icon">📝</span>
                                    <span>Full Summary</span>
                                    <span class="tile-desc">High-yield revision points</span>
                                </button>
                                <button class="btn-action-tile" onclick="runPhotoAction('solve')">
                                    <span class="tile-icon">💡</span>
                                    <span>Step-by-Step Solver</span>
                                    <span class="tile-desc">Derivations & numericals</span>
                                </button>
                                <button class="btn-action-tile" onclick="runPhotoAction('formulas')">
                                    <span class="tile-icon">📌</span>
                                    <span>Formula Sheet</span>
                                    <span class="tile-desc">Laws, SI units & constants</span>
                                </button>
                                <button class="btn-action-tile" onclick="runPhotoAction('questions')">
                                    <span class="tile-icon">🎯</span>
                                    <span>Top Exam Qs</span>
                                    <span class="tile-desc">Probable viva questions</span>
                                </button>
                                <button class="btn-action-tile" onclick="runPhotoAction('eli5')">
                                    <span class="tile-icon">🪜</span>
                                    <span>Explain Simply</span>
                                    <span class="tile-desc">Intuitive real-life analogy</span>
                                </button>
                                <button class="btn-action-tile" onclick="runPhotoAction('practice')">
                                    <span class="tile-icon">💻</span>
                                    <span>Practice Problem</span>
                                    <span class="tile-desc">Test your understanding</span>
                                </button>
                            </div>
                        </div>

                        <div id="photo-summary-container" style="display: none;">
                            <div class="summary-callout">
                                <div class="summary-callout-header">✨ Instant Study Summary</div>
                                <div class="summary-callout-body" id="photo-summary-content"></div>
                            </div>
                        </div>

                        <div id="photo-chat" class="chat-box" style="max-height: 240px;">
                            <div class="msg-bubble ai">📷 Upload a photo on the left or click <b>'Try Sample Physics Photo'</b> to analyze equations and notes instantly.</div>
                        </div>

                        <div class="chat-input-bar">
                            <input type="text" id="photo-chat-input" placeholder="Ask any question about this photo (e.g. 'Explain formula 2')..." onkeydown="if(event.key==='Enter') sendPhotoChat()">
                            <button class="btn-primary" onclick="sendPhotoChat()">Ask Photo</button>
                        </div>
                    </div>

                </div>
            </section>

            <!-- 3. ASK MY NOTES -->
            <section id="tab-notes" class="tab-content">
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">📄 Uploaded Notes Context</div>
                    </div>
                    <p class="card-description">Sample college lecture notes covering Data Structures (BST, Big-O) and DBMS (ACID, Normalization) are active below. You can also paste your syllabus.</p>
                    
                    <textarea id="notes-text" style="height: 110px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;">UNIT 1: DATA STRUCTURES & ALGORITHM COMPLEXITY
- Big-O Notation: Upper bound runtime in the worst case.
- Binary Search Tree (BST): Left child < Root < Right child. Balanced search: O(log n).
- Degenerate BST: Degrades to linked list with worst-case O(n) search time.

UNIT 2: DATABASE MANAGEMENT SYSTEMS (ACID & NORMALIZATION)
- Atomicity: All operations succeed or completely rollback.
- Consistency: Ensures database conforms to all constraints and business rules.
- Isolation: Concurrent transactions execute without dirty read conflicts.
- Durability: Committed updates persist even after power loss or hardware failure.
- 1NF: Atomic values only. 2NF: No partial dependency. 3NF: No transitive dependency.</textarea>
                    
                    <div style="display: flex; gap: 8px; margin-top: 10px;">
                        <button class="btn-secondary" onclick="queryNotesQuick('Give a 5-minute revision summary of these notes with core definitions')">📝 5-Min Summary</button>
                        <button class="btn-secondary" onclick="queryNotesQuick('Extract the top 3 probable semester exam questions from these notes')">🎯 Top 3 Exam Questions</button>
                        <button class="btn-secondary" onclick="queryNotesQuick('Create a formula and definition cheat sheet from these notes')">📌 Definition Sheet</button>
                    </div>
                </div>

                <div id="notes-chat" class="chat-box">
                    <div class="msg-bubble ai">📖 Notes loaded! Ask any specific question grounded in these lecture notes.</div>
                </div>

                <div class="chat-input-bar">
                    <input type="text" id="notes-input" placeholder="Ask a question about the uploaded lecture notes..." onkeydown="if(event.key==='Enter') sendNotesMessage()">
                    <button class="btn-primary" onclick="sendNotesMessage()">Query Notes</button>
                </div>
            </section>

            <!-- 4. AI STUDY PLANNER -->
            <section id="tab-planner" class="tab-content">
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">📅 Custom Study Timetable Generator</div>
                    </div>
                    <p class="card-description">Set your subjects and study parameters. Gemma 3:1B will structure an achievable, stress-free day-by-day roadmap.</p>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 10px;">
                        <div>
                            <label style="font-size: 0.84rem; font-weight: 700; color: var(--text-heading);">📚 Subjects to Cover:</label>
                            <input type="text" id="plan-subjects" value="Data Structures, DBMS, Operating Systems, Computer Networks">
                        </div>
                        <div>
                            <label style="font-size: 0.84rem; font-weight: 700; color: var(--text-heading);">⏰ Daily Study Commitment (Hours):</label>
                            <input type="number" id="plan-hours" value="4" min="1" max="12">
                        </div>
                        <div>
                            <label style="font-size: 0.84rem; font-weight: 700; color: var(--text-heading);">⏳ Days Available Until Exam:</label>
                            <input type="number" id="plan-days" value="14" min="1" max="120">
                        </div>
                        <div>
                            <label style="font-size: 0.84rem; font-weight: 700; color: var(--text-heading);">📊 Preparation Level:</label>
                            <select id="plan-level">
                                <option>Intermediate (Familiar with fundamental concepts)</option>
                                <option>Beginner (Starting from scratch)</option>
                                <option>Revision (Full syllabus covered once)</option>
                            </select>
                        </div>
                    </div>
                    <button class="btn-primary" style="margin-top: 16px; width: 100%;" onclick="generateStudyPlan()">🚀 Generate Day-by-Day Study Plan</button>
                </div>

                <div id="plan-result" class="card" style="display: none;">
                    <div class="card-header">
                        <div class="card-title">📋 Your Generated Timetable</div>
                    </div>
                    <div id="plan-text" style="white-space: pre-wrap; font-size: 0.92rem; line-height: 1.65; margin-top: 8px;"></div>
                </div>
            </section>

            <!-- 5. CAMPUS NOTICES -->
            <section id="tab-notices" class="tab-content">
                <div class="demo-banner">
                    <b>⚠️ DEMO BULLETIN BOARD:</b> The announcements below are sample mock circulars for project demonstration. They do not represent official announcements from any educational institution.
                </div>

                <div class="notice-card">
                    <div class="notice-meta">
                        <span class="notice-date">📅 October 22, 2026 | Ref: NOT-2026-001</span>
                        <span class="badge-cat badge-exam">Examination</span>
                    </div>
                    <div class="notice-title">Mid-Semester Examination Schedule Announced (Fall 2026)</div>
                    <div class="notice-desc">Mid-Semester exams commence November 10, 2026 for all 2nd, 3rd, and 4th-year students. Detailed subject-wise timetables are uploaded to the student portal. Physical ID is mandatory.</div>
                </div>

                <div class="notice-card">
                    <div class="notice-meta">
                        <span class="notice-date">📅 October 20, 2026 | Ref: NOT-2026-002</span>
                        <span class="badge-cat badge-event">Event / Hackathon</span>
                    </div>
                    <div class="notice-title">Inter-College Hackathon: CodeCraft 2026 Registrations Open</div>
                    <div class="notice-desc">36-hour hackathon scheduled for November 28-29, 2026. Cash prizes worth ₹1,50,000 + internship opportunities. Submit team abstract before November 5, 2026.</div>
                </div>

                <div class="notice-card">
                    <div class="notice-meta">
                        <span class="notice-date">📅 October 18, 2026 | Ref: NOT-2026-003</span>
                        <span class="badge-cat badge-library">Library</span>
                    </div>
                    <div class="notice-title">Central Library Late Fee Waiver Drive</div>
                    <div class="notice-desc">Return all overdue books between October 27 and November 2, 2026 to enjoy a 100% late fee waiver approved by the academic committee.</div>
                </div>

                <div class="notice-card">
                    <div class="notice-meta">
                        <span class="notice-date">📅 October 15, 2026 | Ref: NOT-2026-004</span>
                        <span class="badge-cat badge-fee">Fees & Admin</span>
                    </div>
                    <div class="notice-title">Examination Fee Submission & Clearance Deadline</div>
                    <div class="notice-desc">The deadline for submitting end-semester exam forms without late fee is November 3, 2026. A late fine of ₹500 will apply until November 8.</div>
                </div>

                <div class="card" style="margin-top: 1.4rem;">
                    <div class="card-header">
                        <div class="card-title">🤖 Ask Campus Notice Assistant</div>
                    </div>
                    <div class="chat-input-bar">
                        <input type="text" id="notice-input" placeholder="E.g., What is the deadline to pay exam fees without fine?">
                        <button class="btn-primary" onclick="queryNoticeAssistant()">Ask Desk</button>
                    </div>
                    <div id="notice-answer" style="margin-top: 12px; font-size: 0.92rem; color: var(--primary); font-weight: 600; line-height: 1.55;"></div>
                </div>
            </section>

            <!-- 6. SETTINGS -->
            <section id="tab-settings" class="tab-content">
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">⚙️ System Diagnostics & Ollama Connection</div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px; font-size: 0.9rem;">
                        <p>Status: <span id="diag-status" style="font-weight: 700; color: var(--success);">Checking...</span></p>
                        <p>Active LLM Model: <b>gemma3:1b</b></p>
                        <p>Vision & Photo OCR: <b>Windows.Media.Ocr (Native Offline Engine)</b></p>
                        <p>Local API Endpoint: <code>http://localhost:11434/api/chat</code></p>
                    </div>
                    <button class="btn-primary" style="margin-top: 14px;" onclick="checkHealth()">🔄 Refresh Ollama Connection</button>
                </div>
            </section>

        </div>
    </main>

    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');

            const titles = {
                'tab-study': ['📚 AI Study Assistant', 'Your 24/7 personal college tutor for concepts, derivations, and exam revision notes.'],
                'tab-photo': ['📸 Snap & Study (Photo Explainer)', 'Upload textbook & note photos. Auto-summarize, solve problems & extract formulas.'],
                'tab-notes': ['📄 Ask My Notes', 'Grounded academic question answering based on your uploaded lecture notes.'],
                'tab-planner': ['📅 AI Study Planner', 'Personalized day-by-day timetable tailored to your hours and exam deadline.'],
                'tab-notices': ['📢 Campus Notices', 'Demo bulletin board with interactive AI question answering.'],
                'tab-settings': ['⚙️ System & Diagnostics', 'Verify local Ollama connectivity, models, and OCR status.']
            };
            document.getElementById('header-title').innerText = titles[tabId][0];
            document.getElementById('header-desc').innerText = titles[tabId][1];
        }

        function fillPrompt(text) {
            document.getElementById('study-input').value = text;
            sendStudyMessage();
        }

        async function checkHealth() {
            try {
                const res = await fetch('/api/health');
                const data = await res.json();
                const pill = document.getElementById('status-pill');
                const diag = document.getElementById('diag-status');
                if (data.online) {
                    pill.className = 'status-badge online';
                    pill.innerHTML = '<span class="status-dot"></span><span>Ollama Connected (' + data.model + ')</span>';
                    diag.innerHTML = '🟢 Connected & Ready (gemma3:1b)';
                    diag.style.color = '#059669';
                } else {
                    pill.className = 'status-badge offline';
                    pill.innerHTML = '<span class="status-dot" style="background:red;"></span><span>Ollama Disconnected</span>';
                    diag.innerHTML = '🔴 Disconnected - Run `ollama serve` in PowerShell';
                    diag.style.color = '#dc2626';
                }
            } catch (e) {
                document.getElementById('status-pill').className = 'status-badge offline';
                document.getElementById('status-pill').innerHTML = '<span class="status-dot" style="background:red;"></span><span>Ollama Offline</span>';
            }
        }

        async function sendStudyMessage() {
            const input = document.getElementById('study-input');
            const q = input.value.trim();
            if (!q) return;
            input.value = '';

            const chat = document.getElementById('study-chat');
            chat.innerHTML += `<div class="msg-bubble user">${escapeHtml(q)}</div>`;
            chat.scrollTop = chat.scrollHeight;

            const mode = document.getElementById('study-mode').value;
            const aiMsg = document.createElement('div');
            aiMsg.className = 'msg-bubble ai';
            aiMsg.innerHTML = '<i>✨ Gemma 3:1B is drafting a structured answer...</i>';
            chat.appendChild(aiMsg);
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ prompt: q, mode: mode, type: 'study' })
                });
                const data = await res.json();
                aiMsg.innerHTML = formatMarkdown(data.reply || data.error);
            } catch (err) {
                aiMsg.innerHTML = '⚠️ Error contacting local AI: ' + err.message;
            }
            chat.scrollTop = chat.scrollHeight;
        }

        function clearStudyChat() {
            document.getElementById('study-chat').innerHTML = '<div class="msg-bubble ai">✨ Chat cleared! What topic shall we master next?</div>';
        }

        // ==================== PHOTO (SNAP & STUDY) ====================
        async function handlePhotoUpload(input) {
            if (!input.files || !input.files[0]) return;
            const file = input.files[0];
            const reader = new FileReader();

            reader.onload = async function(e) {
                const base64Data = e.target.result;
                document.getElementById('photo-preview').src = base64Data;
                document.getElementById('photo-preview-container').style.display = 'block';

                document.getElementById('photo-extracted-text').value = 'Extracting text using native Windows OCR...';
                try {
                    const res = await fetch('/api/ocr', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ image_base64: base64Data.split(',')[1] })
                    });
                    const data = await res.json();
                    if (data.text) {
                        document.getElementById('photo-extracted-text').value = data.text;
                        runPhotoAction('summarize');
                    } else {
                        document.getElementById('photo-extracted-text').value = '⚠️ ' + (data.error || 'No text detected in image.');
                    }
                } catch (err) {
                    document.getElementById('photo-extracted-text').value = '⚠️ OCR error: ' + err.message;
                }
            };
            reader.readAsDataURL(file);
        }

        async function loadSamplePhysicsPhoto() {
            try {
                const res = await fetch('/api/sample_photo');
                const data = await res.json();
                if (data.base64) {
                    const fullSrc = 'data:image/png;base64,' + data.base64;
                    document.getElementById('photo-preview').src = fullSrc;
                    document.getElementById('photo-preview-container').style.display = 'block';
                    document.getElementById('photo-extracted-text').value = data.text;
                    runPhotoAction('summarize');
                }
            } catch (err) {
                alert('Could not load sample photo: ' + err.message);
            }
        }

        function clearPhoto() {
            document.getElementById('photo-input').value = '';
            document.getElementById('photo-preview').src = '';
            document.getElementById('photo-preview-container').style.display = 'none';
            document.getElementById('photo-extracted-text').value = '';
            document.getElementById('photo-summary-container').style.display = 'none';
            document.getElementById('photo-chat').innerHTML = '<div class="msg-bubble ai">📷 Photo reset. Upload an image to analyze notes!</div>';
        }

        async function runPhotoAction(actionType) {
            const photoText = document.getElementById('photo-extracted-text').value.trim();
            if (!photoText) {
                alert('Please upload a photo first or wait for OCR text to appear.');
                return;
            }

            const prompts = {
                'summarize': 'Summarize the core concepts, laws, and points in this study photo concisely into high-yield bullet points with an exam takeaway.',
                'solve': 'Explain and solve step-by-step any numericals, formulas, or derivations shown in this photo with intermediate calculation steps.',
                'formulas': 'Extract all formulas, physical laws, constants, and definitions from this photo into a clear exam revision formula sheet.',
                'questions': 'Predict the top 4 college exam or viva-voce questions that can be asked based on this photo, along with model answers.',
                'eli5': 'Explain the concept shown in this photo in extremely simple language with a practical real-world analogy as if to a 1st year student.',
                'practice': 'Generate 2 practice numerical problems testing the student on the concepts seen in this photo.'
            };

            const userPrompt = prompts[actionType] || 'Summarize this photo.';

            const chat = document.getElementById('photo-chat');
            chat.innerHTML += `<div class="msg-bubble user">⚡ Action: ${escapeHtml(userPrompt)}</div>`;
            chat.scrollTop = chat.scrollHeight;

            const aiMsg = document.createElement('div');
            aiMsg.className = 'msg-bubble ai';
            aiMsg.innerHTML = '<i>✨ Gemma 3:1B is analyzing your photo...</i>';
            chat.appendChild(aiMsg);
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        type: 'photo',
                        prompt: userPrompt,
                        photo_text: photoText
                    })
                });
                const data = await res.json();
                const reply = data.reply || data.error;
                aiMsg.innerHTML = formatMarkdown(reply);

                if (actionType === 'summarize') {
                    document.getElementById('photo-summary-content').innerHTML = formatMarkdown(reply);
                    document.getElementById('photo-summary-container').style.display = 'block';
                }
            } catch (err) {
                aiMsg.innerHTML = '⚠️ Error: ' + err.message;
            }
            chat.scrollTop = chat.scrollHeight;
        }

        async function sendPhotoChat() {
            const input = document.getElementById('photo-chat-input');
            const q = input.value.trim();
            if (!q) return;
            input.value = '';

            const photoText = document.getElementById('photo-extracted-text').value.trim();
            const chat = document.getElementById('photo-chat');
            chat.innerHTML += `<div class="msg-bubble user">${escapeHtml(q)}</div>`;
            chat.scrollTop = chat.scrollHeight;

            const aiMsg = document.createElement('div');
            aiMsg.className = 'msg-bubble ai';
            aiMsg.innerHTML = '<i>✨ Checking photo context...</i>';
            chat.appendChild(aiMsg);

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        type: 'photo',
                        prompt: q,
                        photo_text: photoText
                    })
                });
                const data = await res.json();
                aiMsg.innerHTML = formatMarkdown(data.reply || data.error);
            } catch (err) {
                aiMsg.innerHTML = '⚠️ Error: ' + err.message;
            }
            chat.scrollTop = chat.scrollHeight;
        }

        // ==================== ASK MY NOTES ====================
        async function sendNotesMessage() {
            const input = document.getElementById('notes-input');
            const q = input.value.trim();
            if (!q) return;
            input.value = '';
            queryNotesCore(q);
        }

        function queryNotesQuick(text) {
            queryNotesCore(text);
        }

        async function queryNotesCore(q) {
            const chat = document.getElementById('notes-chat');
            chat.innerHTML += `<div class="msg-bubble user">${escapeHtml(q)}</div>`;
            chat.scrollTop = chat.scrollHeight;

            const notes = document.getElementById('notes-text').value;
            const aiMsg = document.createElement('div');
            aiMsg.className = 'msg-bubble ai';
            aiMsg.innerHTML = '<i>✨ Searching notes...</i>';
            chat.appendChild(aiMsg);

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ prompt: q, notes_context: notes, type: 'notes' })
                });
                const data = await res.json();
                aiMsg.innerHTML = formatMarkdown(data.reply || data.error);
            } catch (err) {
                aiMsg.innerHTML = '⚠️ Error: ' + err.message;
            }
            chat.scrollTop = chat.scrollHeight;
        }

        // ==================== STUDY PLANNER ====================
        async function generateStudyPlan() {
            const subjects = document.getElementById('plan-subjects').value;
            const hours = document.getElementById('plan-hours').value;
            const days = document.getElementById('plan-days').value;
            const level = document.getElementById('plan-level').value;

            const resDiv = document.getElementById('plan-result');
            const textDiv = document.getElementById('plan-text');
            resDiv.style.display = 'block';
            textDiv.innerHTML = '<i>✨ Structuring your realistic day-by-day timetable with Gemma 3:1B...</i>';

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        type: 'planner',
                        subjects: subjects,
                        hours: hours,
                        days: days,
                        level: level
                    })
                });
                const data = await res.json();
                textDiv.innerHTML = formatMarkdown(data.reply || data.error);
            } catch (err) {
                textDiv.innerHTML = '⚠️ Error generating plan: ' + err.message;
            }
        }

        // ==================== NOTICES ====================
        async function queryNoticeAssistant() {
            const q = document.getElementById('notice-input').value.trim();
            if (!q) return;
            const out = document.getElementById('notice-answer');
            out.innerHTML = '<i>✨ Checking official bulletin circulars...</i>';

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ prompt: q, type: 'notices' })
                });
                const data = await res.json();
                out.innerHTML = formatMarkdown('📌 **Notice Desk:** ' + (data.reply || data.error));
            } catch (err) {
                out.innerHTML = '⚠️ Error: ' + err.message;
            }
        }

        // ==================== MARKDOWN FORMATTER ====================
        function formatMarkdown(text) {
            if (!text) return '';
            let formatted = escapeHtml(text);
            
            // Bold **text**
            formatted = formatted.replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>');
            // Italic *text*
            formatted = formatted.replace(/\\*(.*?)\\*/g, '<i>$1</i>');
            // Inline code `code`
            formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
            // Headers
            formatted = formatted.replace(/^### (.*$)/gim, '<h4>$1</h4>');
            formatted = formatted.replace(/^## (.*$)/gim, '<h3>$1</h3>');
            // Bullet points
            formatted = formatted.replace(/^\\* (.*$)/gim, '• $1<br>');
            formatted = formatted.replace(/^- (.*$)/gim, '• $1<br>');
            // Line breaks
            formatted = formatted.replace(/\\n/g, '<br>');
            return formatted;
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }

        checkHealth();
    </script>
</body>
</html>
"""


class CampusSaathiHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/" or url.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

        elif url.path == "/api/health":
            online = False
            models = []
            try:
                req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
                with urllib.request.urlopen(req, timeout=2.0) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        models = [m.get("name", "") for m in data.get("models", [])]
                        online = True
            except Exception:
                online = False

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "online": online,
                        "model": DEFAULT_MODEL,
                        "models_installed": models,
                    }
                ).encode("utf-8")
            )

        elif url.path == "/api/sample_photo":
            sample_path = os.path.join(
                "sample_notes", "Sample_Physics_Notes.png"
            )
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    bytes_data = f.read()
                b64_str = base64.b64encode(bytes_data).decode("utf-8")

                ocr_script = os.path.abspath("ocr_helper.ps1")
                cmd = [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    ocr_script,
                    "-ImagePath",
                    os.path.abspath(sample_path),
                ]
                res = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=10
                )
                text = res.stdout.strip()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"base64": b64_str, "text": text}).encode(
                        "utf-8"
                    )
                )
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        url = urlparse(self.path)

        if url.path == "/api/ocr":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len).decode("utf-8")
            data = json.loads(post_body)

            image_base64 = data.get("image_base64", "")
            if not image_base64:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(
                    json.dumps({"error": "No image data received"}).encode(
                        "utf-8"
                    )
                )
                return

            try:
                img_bytes = base64.b64decode(image_base64)
                with tempfile.NamedTemporaryFile(
                    suffix=".png", delete=False
                ) as tmp:
                    tmp.write(img_bytes)
                    tmp_name = tmp.name

                ocr_script = os.path.abspath("ocr_helper.ps1")
                cmd = [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    ocr_script,
                    "-ImagePath",
                    os.path.abspath(tmp_name),
                ]
                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=20
                )
                extracted_text = result.stdout.strip()

                if os.path.exists(tmp_name):
                    os.remove(tmp_name)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"text": extracted_text}).encode("utf-8")
                )

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps(
                        {"error": f"OCR processing failed: {str(e)}"}
                    ).encode("utf-8")
                )

        elif url.path == "/api/chat":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len).decode("utf-8")
            data = json.loads(post_body)

            req_type = data.get("type", "study")
            prompt = data.get("prompt", "")

            # Elevated Academic Prompt Engineering with clear formatting & style
            if req_type == "study":
                mode = data.get("mode", "Simple & Intuitive")
                system_prompt = (
                    "You are CampusSaathi AI, an encouraging and expert college study tutor.\n"
                    f"Selected Style: {mode}.\n"
                    "FORMATTING RULES:\n"
                    "- Use bold headings (###) for distinct concepts.\n"
                    "- Use clear bullet points with bold keywords.\n"
                    "- Break complex formulas into intuitive steps.\n"
                    "- Conclude with a helpful '🎯 Exam & Viva Tip' box."
                )
                user_msg = prompt

            elif req_type == "photo":
                photo_text = data.get("photo_text", "")
                system_prompt = (
                    "You are CampusSaathi AI Photo Study Mentor. The student has uploaded a photo of study material.\n"
                    f"=== EXTRACTED PHOTO CONTENT ===\n{photo_text}\n=== END ===\n"
                    "Analyze the content thoroughly:\n"
                    "- Provide structured headings (###).\n"
                    "- State the core principle, laws, formulas, and derivations clearly.\n"
                    "- Highlight exam questions and practical applications."
                )
                user_msg = prompt

            elif req_type == "notes":
                context = data.get("notes_context", "")
                system_prompt = (
                    "You are CampusSaathi AI. Answer the student's question strictly based on these lecture notes:\n"
                    f"=== NOTES ===\n{context}\n=== END ===\n"
                    "Be rigorous, concise, and highlight key definitions and points."
                )
                user_msg = prompt

            elif req_type == "planner":
                subjects = data.get("subjects", "")
                hours = data.get("hours", "4")
                days = data.get("days", "14")
                level = data.get("level", "Intermediate")
                system_prompt = (
                    "You are an expert college academic mentor. Create a realistic, day-by-day timetable.\n"
                    "Structure into: (1) Strategy, (2) Daily Routine, (3) Day-by-Day Roadmap by Phases, (4) Final 48-Hour Exam Checklist."
                )
                user_msg = f"Create a {days}-day study timetable for {subjects}. Daily hours: {hours}. Preparation level: {level}."

            elif req_type == "notices":
                system_prompt = (
                    "You are the Campus Notice Desk. Answer the question using this notice information:\n"
                    "- Mid-Semester Exams start Nov 10, 2026.\n"
                    "- Exam form submission deadline without late fee is Nov 3, 2026. Fine of Rs 500 applies until Nov 8.\n"
                    "- Library book return waiver week is Oct 27 to Nov 2, 2026.\n"
                    "Mention specific dates and guidelines clearly."
                )
                user_msg = prompt
            else:
                system_prompt = "You are CampusSaathi AI."
                user_msg = prompt

            # Query Ollama
            ollama_payload = {
                "model": DEFAULT_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg},
                ],
                "stream": False,
                "options": {"temperature": 0.4},
            }

            try:
                req = urllib.request.Request(
                    f"{OLLAMA_URL}/api/chat",
                    data=json.dumps(ollama_payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=90.0) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    ai_reply = resp_data.get("message", {}).get("content", "")

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"reply": ai_reply}).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps(
                        {
                            "error": f"Ollama connection error: {str(e)}. Make sure `ollama serve` is running."
                        }
                    ).encode("utf-8")
                )


class ReusableThreadedServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    print("=" * 65)
    print(" 🎓 CampusSaathi AI - Premium Multithreaded Server")
    print("=" * 65)
    print(f" Starting server on: http://localhost:{PORT}")
    print(f" Alternative direct URL: http://127.0.0.1:{PORT}")
    print(f" Connecting to Ollama: {OLLAMA_URL} (Model: {DEFAULT_MODEL})")
    print(" Press Ctrl+C to stop.")
    print("=" * 65)

    try:
        webbrowser.open(f"http://127.0.0.1:{PORT}")
    except Exception:
        pass

    with ReusableThreadedServer(("", PORT), CampusSaathiHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
