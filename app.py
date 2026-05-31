import streamlit as st
import google.generativeai as genai
import os
import time
import shutil
import tempfile
from pathlib import Path
import streamlit.components.v1 as components
from dotenv import load_dotenv

import yt_dlp

load_dotenv()

# ==============================================================================
# 1. KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="EchoDetect AI",
    page_icon="🎵",
    layout="wide"
)
# ==============================================================================
# LANGUAGE SETUP
# ==============================================================================
def get_current_language():
    try:
        lang = st.query_params.get("lang", "en")
    except Exception:
        params = st.experimental_get_query_params()
        lang = params.get("lang", ["en"])[0]

    if lang not in ["en", "id"]:
        lang = "en"

    return lang


LANG = get_current_language()


TEXT = {
    "en": {
        "nav_overview": "OVERVIEW",
        "nav_features": "FEATURES",
        "nav_use_cases": "USE CASES",
        "nav_start": "START SCAN",

        "eyebrow": "AUDIO INTELLIGENCE FOR CREATORS",
        "hero_title": "The precision of <em>sound</em>,<br>refined by intelligence.",
        "hero_subtitle": (
            "Detect songs from audio, video, or social media links. EchoDetect helps creators understand "
            "song titles, vibe, lyrical context, and content compatibility faster."
        ),

        "analysis_label": "ANALYSIS CORE",
        "drop_title": "Drop your media source.",
        "drop_desc": (
            "Upload an MP3/MP4 file or paste a link from YouTube, TikTok, Reels, "
            "and other sources supported by yt-dlp."
        ),

        "input_method": "CHOOSE INPUT METHOD",
        "upload_option": "Upload Audio/Video File",
        "link_option": "Paste Media Link",
        "upload_label": "UPLOAD FILE",
        "link_label": "PASTE MEDIA LINK",
        "link_placeholder": "Example: https://www.youtube.com/watch?v=...",
        "analyze_button": "START AUDIO ANALYSIS",

        "what_you_get": "WHAT YOU GET",
        "step_1_title": "Song Detection",
        "step_1_desc": "AI listens to the audio and finds the most likely song title or viral sound.",
        "step_2_title": "Vibe Analysis",
        "step_2_desc": "Mood, tempo, emotion, and lyrical context are explained clearly for creators.",
        "step_3_title": "Creator Guardrail",
        "step_3_desc": "Gives content recommendations and things creators should avoid.",

        "features_label": "FEATURES",
"features_title": "Built for fast audio discovery.",
"features_desc": (
    "EchoDetect helps creators detect songs from files or links, then provides insight "
    "so audio can be used more accurately."
),
"feature_1_title": "Song Detection",
"feature_1_desc": "Detects the most likely song title or sound from audio, video, or social media links.",
"feature_2_title": "URL & File Input",
"feature_2_desc": "Supports uploaded audio/video files and links from platforms that can be processed with yt-dlp.",
"feature_3_title": "Popup Workflow",
"feature_3_desc": "Shows a loading popup during processing and a result popup when analysis is complete.",

"use_cases_label": "USE CASES",
"use_cases_title": "Who is EchoDetect for?",
"use_cases_desc": "Designed for people who often deal with viral audio, background music, and short-form content.",
"case_1_title": "Content Creator",
"case_1_desc": "Helps identify the song behind a viral sound before using it for TikTok, Reels, or Shorts.",
"case_2_title": "Video Editor",
"case_2_desc": "Speeds up audio reference identification from client briefs or example videos.",
"case_3_title": "Social Media Team",
"case_3_desc": "Helps understand the audio vibe so sound selection fits the brand or campaign message.",
        "loading_url": "Analyzing URL",
        "loading_file": "Analyzing File",
        "loading_url_desc": "EchoDetect is extracting audio from the link, reading the sound signal, and sending it to the analysis engine.",
        "loading_file_desc": "EchoDetect is reading your uploaded file, parsing the audio, and preparing the investigation result.",

        "result_title": "Audio Search Result",
        "analyze_again": "ANALYZE AGAIN",
        "close_popup": "CLOSE POPUP",
        "detected_song_label": "DETECTED SONG",
        "copy_success": "Copied to clipboard",
        "copy_failed": "Copy failed",
        "footer": "© 2026 EchoDetect AI · Precision in sound."

        

    },

    "id": {
        "nav_overview": "RINGKASAN",
        "nav_features": "FITUR",
        "nav_use_cases": "KEGUNAAN",
        "nav_start": "MULAI SCAN",

        "eyebrow": "INTELIJEN AUDIO UNTUK KREATOR",
        "hero_title": "Ketepatan membaca <em>suara</em>,<br>dipertajam oleh kecerdasan AI.",
        "hero_subtitle": (
            "Deteksi lagu dari audio, video, atau link media sosial. EchoDetect membantu kreator memahami "
            "judul lagu, vibe, konteks lirik, dan kecocokan konten secara cepat."
        ),

        "analysis_label": "MESIN ANALISIS",
        "drop_title": "Masukkan sumber media kamu.",
        "drop_desc": (
            "Upload file MP3/MP4 atau tempel link dari YouTube, TikTok, Reels, "
            "dan sumber lain yang didukung yt-dlp."
        ),

        "input_method": "PILIH METODE INPUT",
        "upload_option": "Unggah Berkas Audio/Video",
        "link_option": "Tempel Link Media",
        "upload_label": "UNGGAH FILE",
        "link_label": "TEMPEL LINK MEDIA",
        "link_placeholder": "Contoh: https://www.youtube.com/watch?v=...",
        "analyze_button": "MULAI ANALISIS AUDIO",

        "what_you_get": "HASIL YANG DIDAPAT",
        "step_1_title": "Deteksi Lagu",
        "step_1_desc": "AI mendengarkan audio dan mencari judul lagu atau sound viral yang paling mungkin.",
        "step_2_title": "Analisis Vibe",
        "step_2_desc": "Mood, tempo, emosi, dan konteks lirik dijelaskan agar kreator lebih paham penggunaan audio.",
        "step_3_title": "Panduan Kreator",
        "step_3_desc": "Memberi rekomendasi jenis konten yang cocok dan hal yang sebaiknya dihindari.",

        "features_label": "FITUR",
"features_title": "Dibuat untuk pencarian audio yang cepat.",
"features_desc": (
    "EchoDetect membantu kreator mendeteksi lagu dari file atau link, lalu memberikan insight "
    "agar audio bisa dipakai dengan lebih tepat."
),
"feature_1_title": "Deteksi Lagu",
"feature_1_desc": "Mendeteksi judul lagu atau sound yang paling mungkin dari audio, video, maupun link media sosial.",
"feature_2_title": "Input URL & File",
"feature_2_desc": "Mendukung upload file audio/video dan link dari platform yang bisa diproses melalui yt-dlp.",
"feature_3_title": "Alur Popup",
"feature_3_desc": "Menampilkan popup loading saat proses berjalan dan popup hasil ketika analisis selesai.",

"use_cases_label": "KEGUNAAN",
"use_cases_title": "Untuk siapa EchoDetect dibuat?",
"use_cases_desc": "Dirancang untuk orang yang sering berurusan dengan audio viral, musik latar, dan konten pendek.",
"case_1_title": "Content Creator",
"case_1_desc": "Membantu mencari tahu lagu di balik sound viral sebelum dipakai untuk TikTok, Reels, atau Shorts.",
"case_2_title": "Video Editor",
"case_2_desc": "Mempercepat proses identifikasi audio referensi dari brief klien atau contoh video.",
"case_3_title": "Tim Media Sosial",
"case_3_desc": "Membantu memahami vibe audio agar pemilihan sound sesuai dengan pesan brand atau campaign.",
        "loading_url": "Menganalisis URL",
        "loading_file": "Menganalisis File",
        "loading_url_desc": "EchoDetect sedang mengambil audio dari tautan, membaca sinyal suara, lalu mengirimkannya ke mesin analisis.",
        "loading_file_desc": "EchoDetect sedang membaca file yang kamu upload, mengurai audio, lalu menyiapkan hasil investigasi.",

        "result_title": "Hasil Pencarian Audio",
        "analyze_again": "ANALISIS LAGI",
        "close_popup": "TUTUP POPUP",
        "detected_song_label": "LAGU TERDETEKSI",
        "copy_success": "Berhasil disalin",
        "copy_failed": "Gagal menyalin",
        "footer": "© 2026 EchoDetect AI · Presisi dalam suara."

        
    }
}

T = TEXT[LANG]

# ==============================================================================
# 2. API KEY
# ==============================================================================
# Untuk lokal, boleh isi langsung di sini.
# Jangan upload app.py yang berisi API key asli ke GitHub/public.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("API Key Gemini belum ditemukan. Pastikan file .env sudah berisi GEMINI_API_KEY.")
    st.stop()
else:
    genai.configure(api_key=GEMINI_API_KEY)


# ==============================================================================
# 3. SESSION STATE
# ==============================================================================
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""

if "last_error" not in st.session_state:
    st.session_state.last_error = ""

if "show_result_dialog" not in st.session_state:
    st.session_state.show_result_dialog = False

if "last_input_type" not in st.session_state:
    st.session_state.last_input_type = ""


def reset_result():
    st.session_state.analysis_result = ""
    st.session_state.last_error = ""
    st.session_state.show_result_dialog = False
    st.session_state.last_input_type = ""


# ==============================================================================
# 4. CSS OBSIDIAN UI + POPUP LOADING
# ==============================================================================
# Pakai st.html agar <style> tidak tampil sebagai code block di halaman.
st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&family=Manrope:wght@200..800&family=JetBrains+Mono:wght@100..800&display=swap');

.copy-row {
    margin: 18px 0 26px 0;
    padding: 18px 18px;
    border-radius: 18px;
    background: rgba(254, 182, 141, 0.08);
    border: 1px solid rgba(254, 182, 141, 0.22);
}

.copy-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.14em;
    color: var(--primary);
    margin-bottom: 10px;
    text-transform: uppercase;
}

.copy-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.copy-title {
    font-family: 'Manrope', sans-serif;
    font-size: 18px;
    font-weight: 800;
    color: #f7f7f8;
    line-height: 1.45;
    word-break: break-word;
}

.copy-button {
    flex: 0 0 auto;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.06);
    color: #f7f7f8;
    border-radius: 12px;
    width: 42px;
    height: 42px;
    cursor: pointer;
    font-size: 18px;
    transition: all 0.2s ease;
}

.copy-button:hover {
    border-color: rgba(254, 182, 141, 0.45);
    background: rgba(254, 182, 141, 0.14);
}

.copy-feedback {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--primary);
    margin-top: 10px;
    min-height: 16px;
}

.nav-menu a {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    color: var(--muted) !important;
    text-decoration: none !important;
    transition: color 0.2s ease;
}

.nav-menu a:hover {
    color: var(--primary) !important;
}

.lang-switch {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--muted) !important;
    text-decoration: none !important;
    padding: 8px 10px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
}

.lang-switch:hover {
    color: var(--primary) !important;
    border-color: rgba(254, 182, 141, 0.35);
}

.active-lang {
    color: #502406 !important;
    background: var(--primary) !important;
    border-color: var(--primary) !important;
}

html {
    scroll-behavior: smooth;
}

body {
    scroll-behavior: smooth;
}

.stApp {
    scroll-behavior: smooth;
}

[data-testid="stAppViewContainer"] {
    scroll-behavior: smooth;
}

.scroll-anchor {
    scroll-margin-top: 120px;
}

:root {
    --bg: #08090a;
    --surface: rgba(22, 24, 28, 0.72);
    --surface-strong: rgba(31, 32, 34, 0.94);
    --primary: #feb68d;
    --text: #e3e2e5;
    --muted: #8a8f98;
    --border: rgba(255, 255, 255, 0.08);
}

.stApp {
    background:
        radial-gradient(circle at 50% -20%, rgba(254, 182, 141, 0.18) 0%, rgba(8, 9, 10, 0) 44%),
        radial-gradient(circle at 10% 20%, rgba(60, 71, 90, 0.25) 0%, rgba(8, 9, 10, 0) 34%),
        linear-gradient(180deg, #111315 0%, #08090a 52%, #0d0e10 100%) !important;
    color: var(--text) !important;
    font-family: 'Manrope', sans-serif !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.stDeployButton {
    display: none !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1180px !important;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #08090a;
}

::-webkit-scrollbar-thumb {
    background: #343537;
    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: #52443c;
}

h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: var(--text);
}

.top-nav {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 22px;
    border: 1px solid var(--border);
    border-radius: 999px;
    background: rgba(18, 19, 21, 0.72);
    backdrop-filter: blur(18px);
    box-shadow: 0 20px 80px rgba(0, 0, 0, 0.24);
    margin-bottom: 4.8rem;
}

.brand {
    font-family: 'Newsreader', serif;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #f7f7f8;
}

.nav-menu {
    display: flex;
    gap: 28px;
    align-items: center;
}

.nav-menu a {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    color: var(--muted) !important;
    text-decoration: none !important;
    transition: color 0.2s ease;
}

.nav-menu a:hover {
    color: var(--primary) !important;
}

.nav-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #502406 !important;
    background: var(--primary);
    padding: 9px 18px;
    border-radius: 999px;
    text-decoration: none !important;
    cursor: pointer;
}

html {
    scroll-behavior: smooth;
}

.scroll-anchor {
    scroll-margin-top: 120px;
}

.nav-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #502406 !important;
    background: var(--primary);
    padding: 9px 18px;
    border-radius: 999px;
}

.hero {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-bottom: 3.2rem;
}

.hero-inner {
    width: 100%;
    max-width: 760px;
    text-align: center;
    margin: 0 auto;
}

.eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--primary);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero-title {
    font-family: 'Newsreader', serif;
    font-size: clamp(42px, 7vw, 76px);
    line-height: 1.05;
    letter-spacing: -0.04em;
    font-weight: 400;
    color: #f7f7f8;
    margin-bottom: 1.2rem;
    text-align: center !important;
}

.hero-title em {
    color: var(--primary);
    font-style: italic;
}

.hero-subtitle {
    width: 100%;
    max-width: 720px;
    margin: 0 auto;
    color: var(--muted);
    font-size: 17px;
    line-height: 1.75;
    text-align: center !important;
    display: block;
}

.section-label {
    font-family: 'JetBrains Mono', monospace;
    color: var(--primary);
    font-size: 12px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.soft-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 32px;
    padding: 34px;
    box-shadow:
        0 30px 120px rgba(0, 0, 0, 0.32),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(18px);
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
    margin-top: 3.5rem;
}

.feature-card {
    background: rgba(31, 32, 34, 0.52);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px;
    padding: 24px;
}

.feature-card h3 {
    font-family: 'Manrope', sans-serif;
    font-size: 17px;
    margin-bottom: 8px;
    color: #f7f7f8;
}

.feature-card p {
    font-size: 14px;
    line-height: 1.65;
    color: var(--muted);
    margin: 0;
}

.step-number {
    font-family: 'Newsreader', serif;
    font-size: 64px;
    color: rgba(254, 182, 141, 0.18);
    line-height: 1;
}

div[data-testid="stRadio"] label p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    color: var(--muted) !important;
    letter-spacing: 0.08em;
}

div[data-testid="stRadio"] p {
    color: var(--text) !important;
}

.stTextInput input {
    background: rgba(8, 9, 10, 0.72) !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    color: #f7f7f8 !important;
    border-radius: 16px !important;
    padding: 14px 16px !important;
}

.stTextInput input:focus {
    border-color: rgba(254, 182, 141, 0.55) !important;
    box-shadow: 0 0 0 1px rgba(254, 182, 141, 0.28) !important;
}

.stTextInput label p,
.stFileUploader label p {
    color: var(--muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.08em;
}

div[data-testid="stFileUploader"] section {
    background: rgba(8, 9, 10, 0.55) !important;
    border: 1px dashed rgba(254, 182, 141, 0.32) !important;
    border-radius: 22px !important;
    padding: 24px !important;
}

div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] p {
    color: var(--muted) !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #feb68d 0%, #fca370 100%) !important;
    color: #381402 !important;
    border: 0 !important;
    border-radius: 18px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em;
    padding: 0.95rem 1.4rem !important;
    box-shadow: 0 18px 45px rgba(254, 182, 141, 0.18);
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    filter: brightness(1.05);
    box-shadow: 0 22px 55px rgba(254, 182, 141, 0.24);
}

div.stButton > button p,
div.stButton > button span {
    color: #381402 !important;
}

.stAlert {
    background: rgba(31, 32, 34, 0.88) !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: var(--text) !important;
}

.stMarkdown a {
    color: var(--primary) !important;
}

hr {
    border: none;
    height: 1px;
    background: rgba(255, 255, 255, 0.08);
    margin: 32px 0;
}

/* Loading modal ala song finder */
.loading-backdrop {
    position: fixed;
    inset: 0;
    z-index: 999999;
    background:
        radial-gradient(circle at 50% 35%, rgba(254, 182, 141, 0.15), transparent 32%),
        rgba(8, 9, 10, 0.92);
    backdrop-filter: blur(18px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
}

.loading-modal {
    width: min(520px, 92vw);
    border-radius: 32px;
    background:
        linear-gradient(180deg, rgba(31, 32, 34, 0.96), rgba(18, 19, 21, 0.96));
    border: 1px solid rgba(254, 182, 141, 0.22);
    box-shadow:
        0 40px 120px rgba(0, 0, 0, 0.75),
        0 0 70px rgba(254, 182, 141, 0.08);
    padding: 42px 36px;
    text-align: center;
}

.loading-logo {
    position: relative;
    width: 96px;
    height: 96px;
    margin: 0 auto 24px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    background:
        radial-gradient(circle at 50% 50%, rgba(254, 182, 141, 0.18), rgba(254, 182, 141, 0.05) 55%, rgba(18, 19, 21, 0.9) 100%);
    border: 1px solid rgba(254, 182, 141, 0.18);
    box-shadow:
        0 0 45px rgba(254, 182, 141, 0.12),
        inset 0 0 24px rgba(254, 182, 141, 0.06);
    animation: logoPulse 2s ease-in-out infinite;
}

.loading-logo-ring {
    position: absolute;
    inset: 8px;
    border-radius: 999px;
    border: 1px solid rgba(254, 182, 141, 0.22);
    box-shadow: 0 0 25px rgba(254, 182, 141, 0.08);
}

.loading-eq {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: end;
    justify-content: center;
    gap: 5px;
    height: 34px;
}

.loading-eq span {
    display: block;
    width: 7px;
    border-radius: 999px;
    background: linear-gradient(180deg, #ffd7c0 0%, #feb68d 100%);
    box-shadow: 0 0 12px rgba(254, 182, 141, 0.25);
    animation: eqBounce 1s ease-in-out infinite;
}

.loading-eq span:nth-child(1) {
    height: 14px;
    animation-delay: 0s;
}
.loading-eq span:nth-child(2) {
    height: 26px;
    animation-delay: 0.12s;
}
.loading-eq span:nth-child(3) {
    height: 34px;
    animation-delay: 0.24s;
}
.loading-eq span:nth-child(4) {
    height: 22px;
    animation-delay: 0.36s;
}
.loading-eq span:nth-child(5) {
    height: 16px;
    animation-delay: 0.48s;
}

@keyframes logoPulse {
    0%, 100% {
        transform: scale(0.98);
        opacity: 0.92;
    }
    50% {
        transform: scale(1.04);
        opacity: 1;
    }
}

@keyframes eqBounce {
    0%, 100% {
        transform: scaleY(0.7);
        opacity: 0.7;
    }
    50% {
        transform: scaleY(1.15);
        opacity: 1;
    }
}

.loading-title {
    font-family: 'Newsreader', serif;
    font-size: 42px;
    font-weight: 400;
    color: #f7f7f8;
    margin-bottom: 10px;
    letter-spacing: -0.03em;
}

.loading-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--primary);
    margin-bottom: 16px;
}

.loading-desc {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.7;
    margin: 0 auto 24px auto;
    max-width: 390px;
}

.loading-bar {
    height: 8px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.04);
}

.loading-bar::after {
    content: "";
    display: block;
    height: 100%;
    width: 45%;
    background: linear-gradient(90deg, transparent, #feb68d, transparent);
    animation: slide 1.2s ease-in-out infinite;
}

@keyframes breathe {
    0%, 100% {
        transform: scale(0.96);
        opacity: 0.75;
    }
    50% {
        transform: scale(1.04);
        opacity: 1;
    }
}

@keyframes slide {
    0% { transform: translateX(-120%); }
    100% { transform: translateX(240%); }
}

/* Styling dialog Streamlit */
div[data-testid="stDialog"] {
    background: rgba(8, 9, 10, 0.72) !important;
    backdrop-filter: blur(14px) !important;
}

div[data-testid="stDialog"] > div {
    background:
        linear-gradient(180deg, rgba(31, 32, 34, 0.98), rgba(18, 19, 21, 0.98)) !important;
    border: 1px solid rgba(254, 182, 141, 0.22) !important;
    border-radius: 28px !important;
    color: var(--text) !important;
    box-shadow: 0 40px 120px rgba(0,0,0,0.82) !important;
}

@media (max-width: 768px) {
    .nav-menu {
        display: none;
    }

    .top-nav {
        margin-bottom: 3rem;
    }

    .feature-grid {
        grid-template-columns: 1fr;
    }

    .soft-card {
        padding: 24px;
        border-radius: 24px;
    }
}
</style>
""")


# ==============================================================================
# 5. HELPER FUNCTIONS
# ==============================================================================
def save_uploaded_file(uploaded_file, temp_dir: str) -> str:
    suffix = Path(uploaded_file.name).suffix.lower()

    if suffix not in [".mp3", ".mp4", ".m4a", ".wav", ".webm"]:
        suffix = ".mp3"

    output_path = os.path.join(temp_dir, f"uploaded_media{suffix}")

    with open(output_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return output_path


def download_audio_from_url(url: str, temp_dir: str) -> str:
    output_template = os.path.join(temp_dir, "link_audio.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "referer": "https://www.tiktok.com/",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        guessed_path = ydl.prepare_filename(info)

    if guessed_path and os.path.exists(guessed_path):
        return guessed_path

    downloaded_files = [
        os.path.join(temp_dir, file_name)
        for file_name in os.listdir(temp_dir)
        if os.path.isfile(os.path.join(temp_dir, file_name))
    ]

    if not downloaded_files:
        raise FileNotFoundError("Audio dari link gagal diunduh atau tidak ditemukan.")

    downloaded_files.sort(key=lambda file_path: os.path.getsize(file_path), reverse=True)
    return downloaded_files[0]


def wait_until_gemini_file_active(gemini_file, timeout_seconds: int = 90):
    start_time = time.time()

    while gemini_file.state.name != "ACTIVE":
        if gemini_file.state.name == "FAILED":
            raise RuntimeError("Gemini gagal memproses file audio/video ini.")

        if time.time() - start_time > timeout_seconds:
            raise TimeoutError("Timeout saat menunggu file diproses Gemini.")

        time.sleep(2)
        gemini_file = genai.get_file(gemini_file.name)

    return gemini_file


def analyze_audio_with_gemini(file_path: str) -> str:
    if GEMINI_API_KEY == "PASTE_API_KEY_GEMINI_KAMU_DISINI":
        raise ValueError("API Key Gemini belum diisi di kode.")

    uploaded_file = None

    try:
        uploaded_file = genai.upload_file(path=file_path)
        uploaded_file = wait_until_gemini_file_active(uploaded_file)

        model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
system_instruction=(
    "Anda adalah 'EchoDetect AI', pakar forensik audio digital dan asisten kreatif untuk content creator.\n"
    "Tugas Anda adalah menganalisis audio dari video media sosial, mendeteksi lagu yang paling mungkin, "
    "lalu membantu kreator memahami apakah audio tersebut cocok untuk konten mereka.\n\n"

    "ATURAN PENTING:\n"
    "1. Jangan menulis jawaban seperti esai panjang.\n"
    "2. Gunakan format Markdown yang rapi, ringkas, dan mudah discan.\n"
    "3. Pada bagian Hasil Deteksi, tulis judul lagu dan penyanyi secara jelas.\n"
    "4. Jika audio terdengar seperti remix, live version, sped up, slowed, mashup, atau edit viral, tulis di bagian Versi Terdeteksi.\n"
    "5. Jika tidak yakin, jujur tulis Confidence: Sedang atau Rendah.\n"
    "6. Jangan mengarang fakta spesifik yang tidak bisa dipastikan dari audio.\n"
    "7. Fokus pada manfaat untuk kreator konten.\n"
    "8. Pada bagian Arti & Makna Lagu, jangan hanya membahas potongan lirik yang terdengar di audio. "
    "Jelaskan makna asli lagu secara keseluruhan berdasarkan konteks lagu tersebut.\n"
    "9. Hindari terlalu banyak kutipan lirik. Jika perlu, cukup jelaskan dengan parafrase.\n"
    "10. Pada bagian Rekomendasi Lagu Serupa, berikan lagu yang memiliki vibe, mood, energi, atau tema emosional yang mirip. "
    "Jangan hanya memilih lagu dari penyanyi yang sama. Berikan variasi artis jika memungkinkan.\n\n"

    "Format output WAJIB seperti ini:\n\n"

    "### 🎵 Hasil Deteksi\n"
    "**Song ID:** [Judul Lagu - Penyanyi/Kreator]\n\n"
    "**Judul:** [Judul lagu]\n\n"
    "**Penyanyi/Kreator:** [Nama penyanyi atau kreator]\n\n"
    "**Versi Terdeteksi:** [Original / Live Edit / Remix / Sped Up / Slowed / Mashup / Tidak yakin]\n\n"
    "**Confidence:** [Tinggi / Sedang / Rendah]\n\n"

    "---\n\n"

    "### 📊 Analisis Vibe Konten\n"
    "**Mood Utama:** [3-5 kata yang menggambarkan mood]\n\n"
    "**Energi Audio:** [Low / Medium / High] - [penjelasan singkat]\n\n"
    "**Kesan Audio:** [jelaskan karakter musik, emosi, tempo, dan nuansa dalam 2-3 kalimat]\n\n"
    "**Arti & Makna Lagu:** [jelaskan makna asli lagu secara umum dalam bahasa sederhana. "
    "Fokus pada cerita utama lagu, konflik emosional, karakter/sudut pandang, dan pesan yang ingin disampaikan. "
    "Jangan terlalu banyak mengutip lirik. Tulis 2-4 kalimat yang mudah dipahami kreator konten.]\n\n"

    "---\n\n"

    "### 🎬 Rekomendasi Penggunaan Konten\n"
    "**Cocok untuk:**\n"
    "- [jenis konten 1]\n"
    "- [jenis konten 2]\n"
    "- [jenis konten 3]\n\n"

    "**Kurang cocok untuk:**\n"
    "- [jenis konten 1]\n"
    "- [jenis konten 2]\n\n"

    "**Ide Caption/Angle Konten:** [1-2 ide singkat yang relevan]\n\n"

    "---\n\n"

    "### 🎧 Rekomendasi Lagu dengan Vibe Serupa\n"
    "Berikan 5 rekomendasi lagu. Format setiap rekomendasi wajib seperti ini:\n\n"
    "1. **[Judul Lagu - Penyanyi]**\n"
    "   - **Vibe:** [3-5 kata vibe utama]\n"
    "   - **Kenapa mirip:** [jelaskan singkat kemiripan mood, energi, tema, atau nuansa]\n"
    "   - **Cocok untuk:** [jenis konten yang cocok]\n\n"

    "Pastikan rekomendasi lagu cukup populer atau mudah dicari oleh pengguna.\n\n"

    "---\n\n"

    "### ⚠️ Creator Guardrail\n"
    "**Risiko Konteks:** [jelaskan risiko salah konteks, lirik sensitif, atau vibe yang bisa disalahpahami]\n\n"
    "**Catatan Hak Cipta:** [ingatkan secara singkat agar mengikuti aturan platform]\n\n"
    "**Saran Aman:** [saran praktis agar kreator memakai audio dengan tepat]\n"
)               
 )

        response = model.generate_content(
    [
        uploaded_file,
        (
            "Analisis audio/video ini sesuai format yang sudah ditentukan. "
            "Deteksi lagu yang paling mungkin, jelaskan vibe dan makna asli lagunya, "
            "lalu berikan rekomendasi lagu lain yang punya vibe serupa. "
            "Rekomendasi lagu harus relevan berdasarkan mood, energi, tema emosional, dan karakter musik, "
            "bukan hanya karena artisnya sama."
        ),
    ]
)

        if not response.text:
            raise ValueError("Gemini tidak mengembalikan hasil analisis.")

        return response.text

    finally:
        if uploaded_file is not None:
            try:
                genai.delete_file(uploaded_file.name)
            except Exception:
                pass


def process_input(input_method: str, uploaded_file, url_link: str) -> str:
    temp_dir = tempfile.mkdtemp(prefix="echodetect_")

    try:
        if input_method == T["upload_option"]:
            if uploaded_file is None:
                raise ValueError("Kamu belum mengunggah file audio/video.")

            media_path = save_uploaded_file(uploaded_file, temp_dir)

        else:
            if not url_link or not url_link.strip():
                raise ValueError("Kamu belum memasukkan link media.")

            media_path = download_audio_from_url(url_link.strip(), temp_dir)

        return analyze_audio_with_gemini(media_path)

    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass


def render_loading_popup(input_type: str):
    if input_type == "url":
        title = T["loading_url"]
        desc = T["loading_url_desc"]
    else:
        title = T["loading_file"]
        desc = T["loading_file_desc"]

    st.html(
    f"""
    <div class="loading-backdrop">
        <div class="loading-modal">
            <div class="loading-logo">
                <div class="loading-logo-ring"></div>
                <div class="loading-eq">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>

            <div class="loading-subtitle">ECHO FORENSIC ENGINE</div>
            <div class="loading-title">{title}</div>
            <p class="loading-desc">{desc}</p>
            <div class="loading-bar"></div>
        </div>
    </div>
    """
)


# ==============================================================================
# 6. RESULT DIALOG
# ==============================================================================
def escape_html(text: str) -> str:
    if text is None:
        return ""

    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
        .replace("`", "&#96;")
    )


def extract_song_title(analysis_text: str) -> str:
    if not analysis_text:
        return ""

    lines = analysis_text.splitlines()

    title = ""
    artist = ""

    for line in lines:
        clean_line = line.strip().replace("**", "")

        if clean_line.startswith("Song ID:"):
            return clean_line.replace("Song ID:", "").strip()

        if clean_line.startswith("### 🎵 Hasil Deteksi:"):
            return clean_line.replace("### 🎵 Hasil Deteksi:", "").strip()

        if clean_line.startswith("### Hasil Deteksi:"):
            return clean_line.replace("### Hasil Deteksi:", "").strip()

        if "Hasil Deteksi:" in clean_line and "[" not in clean_line:
            return clean_line.split("Hasil Deteksi:", 1)[1].strip()

        if clean_line.startswith("Judul:"):
            title = clean_line.replace("Judul:", "").strip()

        if clean_line.startswith("Penyanyi/Kreator:"):
            artist = clean_line.replace("Penyanyi/Kreator:", "").strip()

    if title and artist:
        return f"{title} - {artist}"

    if title:
        return title

    return ""

@st.dialog("Forensic Analysis Complete", width="large")
def show_result_popup():
    st.html(
        f"""
        <div class="section-label">ECHO RESULT</div>
        <h2 style="font-family:'Newsreader',serif; font-size:34px; font-weight:400; margin-top:0;">
            {T["result_title"]}
        </h2>
        """
    )

    if st.session_state.last_error:
        st.error(st.session_state.last_error)
    else:
        song_title = extract_song_title(st.session_state.analysis_result)

        if song_title:
            safe_song_title = escape_html(song_title)

            components.html(
                f"""
                <style>
                    body {{
                        margin: 0;
                        background: transparent;
                        font-family: Arial, sans-serif;
                    }}

                    .copy-card {{
                        box-sizing: border-box;
                        width: 100%;
                        padding: 18px 20px;
                        border-radius: 18px;
                        background: rgba(254, 182, 141, 0.08);
                        border: 1px solid rgba(254, 182, 141, 0.25);
                    }}

                    .copy-label {{
                        font-family: monospace;
                        font-size: 11px;
                        letter-spacing: 0.14em;
                        color: #feb68d;
                        margin-bottom: 10px;
                        text-transform: uppercase;
                        font-weight: 700;
                    }}

                    .copy-row {{
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        gap: 16px;
                    }}

                    .copy-title {{
                        color: #f7f7f8;
                        font-size: 18px;
                        font-weight: 800;
                        line-height: 1.45;
                        word-break: break-word;
                    }}

                    .copy-button {{
                        flex: 0 0 auto;
                        width: 42px;
                        height: 42px;
                        border-radius: 12px;
                        border: 1px solid rgba(255,255,255,0.12);
                        background: rgba(255,255,255,0.06);
                        color: #f7f7f8;
                        cursor: pointer;
                        font-size: 18px;
                    }}

                    .copy-button:hover {{
                        border-color: rgba(254, 182, 141, 0.55);
                        background: rgba(254, 182, 141, 0.16);
                    }}

                    .copy-feedback {{
                        font-family: monospace;
                        font-size: 11px;
                        color: #feb68d;
                        margin-top: 10px;
                        min-height: 14px;
                    }}
                </style>

                <div class="copy-card">
                    <div class="copy-label">{T["detected_song_label"]}</div>

                    <div class="copy-row">
                        <div class="copy-title">{safe_song_title}</div>
                        <button class="copy-button" onclick="copySongTitle()" title="Copy">
                            ⧉
                        </button>
                    </div>

                    <div class="copy-feedback" id="copy-feedback"></div>
                </div>

                <script>
                function copySongTitle() {{
                    const text = `{safe_song_title}`;

                    navigator.clipboard.writeText(text).then(function() {{
                        const feedback = document.getElementById("copy-feedback");
                        feedback.innerText = `{T["copy_success"]}`;
                        setTimeout(function() {{
                            feedback.innerText = "";
                        }}, 1600);
                    }}).catch(function() {{
                        const feedback = document.getElementById("copy-feedback");
                        feedback.innerText = `{T["copy_failed"]}`;
                    }});
                }}
                </script>
                """,
                height=125
            )

        st.markdown(st.session_state.analysis_result)

    st.write("")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button(T["analyze_again"], use_container_width=True):
            reset_result()
            st.rerun()

    with col_b:
        if st.button(T["close_popup"], use_container_width=True):
            st.session_state.show_result_dialog = False
            st.rerun()

# ==============================================================================
# 7. NAVBAR & HERO
# ==============================================================================
st.html(
    f"""
    <div class="top-nav">
        <div class="brand">EchoDetect</div>

        <div class="nav-menu">
            <a href="#overview" class="smooth-nav">{T["nav_overview"]}</a>
            <a href="#features" class="smooth-nav">{T["nav_features"]}</a>
            <a href="#use-cases" class="smooth-nav">{T["nav_use_cases"]}</a>
        </div>

        <div style="display:flex; align-items:center; gap:10px;">
            <a href="?lang=en" class="lang-switch {'active-lang' if LANG == 'en' else ''}">EN</a>
            <a href="?lang=id" class="lang-switch {'active-lang' if LANG == 'id' else ''}">ID</a>
            <a href="#scan" class="nav-pill smooth-nav">{T["nav_start"]}</a>
        </div>
    </div>
    """
)

components.html(
    """
    <script>
    const parentDoc = window.parent.document;

    function attachSmoothScroll() {
        const links = parentDoc.querySelectorAll('a.smooth-nav[href^="#"]');

        links.forEach((link) => {
            if (link.dataset.smoothAttached === "true") return;

            link.dataset.smoothAttached = "true";

            link.addEventListener("click", function(event) {
                event.preventDefault();

                const targetId = this.getAttribute("href");
                const targetElement = parentDoc.querySelector(targetId);

                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }
            });
        });
    }

    setTimeout(attachSmoothScroll, 300);
    setTimeout(attachSmoothScroll, 1000);
    setTimeout(attachSmoothScroll, 2000);
    </script>
    """,
    height=0
)

st.html(
    f"""
    <section id="overview" class="hero scroll-anchor">
        <div class="hero-inner">
            <div class="eyebrow">{T["eyebrow"]}</div>
            <h1 class="hero-title">
                {T["hero_title"]}
            </h1>
            <p class="hero-subtitle">
                {T["hero_subtitle"]}
            </p>
        </div>
    </section>
    """
)


# ==============================================================================
# 8. INPUT AREA
# ==============================================================================
st.html('<div id="scan" class="scroll-anchor"></div>')

left_col, right_col = st.columns([1.05, 0.95], gap="large")

with left_col:
    st.html(
        f"""
        <div class="soft-card">
            <div class="section-label">{T["analysis_label"]}</div>
            <h2 style="font-family:'Newsreader',serif; font-weight:400; font-size:36px; margin:0 0 10px 0;">
                {T["drop_title"]}
            </h2>
            <p style="color:#8a8f98; line-height:1.7; margin-bottom:24px;">
                {T["drop_desc"]}
            </p>
        </div>
        """
    )

    input_method = st.radio(
        T["input_method"],
        [T["upload_option"], T["link_option"]],
        horizontal=True
    )

    uploaded_file = None
    url_link = ""

    if input_method == T["upload_option"]:
        uploaded_file = st.file_uploader(
            T["upload_label"],
            type=["mp3", "mp4", "m4a", "wav", "webm"],
            help="MP3, MP4, M4A, WAV, WEBM"
        )

        if uploaded_file is not None:
            file_name = uploaded_file.name.lower()

            if file_name.endswith((".mp3", ".m4a", ".wav")):
                st.audio(uploaded_file)
            elif file_name.endswith((".mp4", ".webm")):
                st.video(uploaded_file)

    else:
        url_link = st.text_input(
            T["link_label"],
            placeholder=T["link_placeholder"]
        )

    analyze_button = st.button(
        T["analyze_button"],
        use_container_width=True
    )

with right_col:
    st.html(
    f"""
    <div class="soft-card">
        <div class="section-label">{T["what_you_get"]}</div>

        <div style="display:flex; gap:18px; align-items:flex-start; margin-bottom:20px;">
            <div class="step-number">01</div>
            <div>
                <h3 style="margin:0 0 8px 0;">{T["step_1_title"]}</h3>
                <p style="color:#8a8f98; line-height:1.6; margin:0;">
                    {T["step_1_desc"]}
                </p>
            </div>
        </div>

        <div style="display:flex; gap:18px; align-items:flex-start; margin-bottom:20px;">
            <div class="step-number">02</div>
            <div>
                <h3 style="margin:0 0 8px 0;">{T["step_2_title"]}</h3>
                <p style="color:#8a8f98; line-height:1.6; margin:0;">
                    {T["step_2_desc"]}
                </p>
            </div>
        </div>

        <div style="display:flex; gap:18px; align-items:flex-start;">
            <div class="step-number">03</div>
            <div>
                <h3 style="margin:0 0 8px 0;">{T["step_3_title"]}</h3>
                <p style="color:#8a8f98; line-height:1.6; margin:0;">
                    {T["step_3_desc"]}
                </p>
            </div>
        </div>
    </div>
    """
)

# ==============================================================================
# 9. PROCESSING WITH LOADING POPUP
# ==============================================================================
loading_placeholder = st.empty()

if analyze_button:
    reset_result()

    if GEMINI_API_KEY == "PASTE_API_KEY_GEMINI_KAMU_DISINI":
        st.session_state.last_error = "API Key Gemini belum diisi."
        st.session_state.show_result_dialog = True
        st.rerun()

    input_type = "file" if input_method == T["upload_option"] else "url"
    st.session_state.last_input_type = input_type

    with loading_placeholder:
        render_loading_popup(input_type)

    try:
        result = process_input(input_method, uploaded_file, url_link)
        st.session_state.analysis_result = result
        st.session_state.last_error = ""

    except Exception as e:
        st.session_state.analysis_result = ""
        st.session_state.last_error = str(e)

    finally:
        loading_placeholder.empty()
        st.session_state.show_result_dialog = True
        st.rerun()

# ==============================================================================
# 10. SHOW RESULT POPUP
# ==============================================================================
if st.session_state.show_result_dialog:
    show_result_popup()


# ==============================================================================
# 11. FEATURES SECTION
# ==============================================================================
# ==============================================================================
# 11. FEATURES SECTION
# ==============================================================================
st.html(
    f"""
    <section id="features" class="scroll-anchor" style="margin-top:5rem;">
        <div style="text-align:center; max-width:720px; margin:0 auto 2.5rem auto;">
            <div class="section-label">{T["features_label"]}</div>
            <h2 style="font-family:'Newsreader',serif; font-size:46px; font-weight:400; margin:0 0 12px 0;">
                {T["features_title"]}
            </h2>
            <p style="color:#8a8f98; line-height:1.7; margin:0;">
                {T["features_desc"]}
            </p>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <h3>{T["feature_1_title"]}</h3>
                <p>{T["feature_1_desc"]}</p>
            </div>

            <div class="feature-card">
                <h3>{T["feature_2_title"]}</h3>
                <p>{T["feature_2_desc"]}</p>
            </div>

            <div class="feature-card">
                <h3>{T["feature_3_title"]}</h3>
                <p>{T["feature_3_desc"]}</p>
            </div>
        </div>
    </section>
    """
)

# ==============================================================================
# 12. USE CASES SECTION
# ==============================================================================
st.html(
    f"""
    <section id="use-cases" class="scroll-anchor" style="margin-top:5rem;">
        <div style="text-align:center; max-width:720px; margin:0 auto 2.5rem auto;">
            <div class="section-label">{T["use_cases_label"]}</div>
            <h2 style="font-family:'Newsreader',serif; font-size:46px; font-weight:400; margin:0 0 12px 0;">
                {T["use_cases_title"]}
            </h2>
            <p style="color:#8a8f98; line-height:1.7; margin:0;">
                {T["use_cases_desc"]}
            </p>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <h3>{T["case_1_title"]}</h3>
                <p>{T["case_1_desc"]}</p>
            </div>

            <div class="feature-card">
                <h3>{T["case_2_title"]}</h3>
                <p>{T["case_2_desc"]}</p>
            </div>

            <div class="feature-card">
                <h3>{T["case_3_title"]}</h3>
                <p>{T["case_3_desc"]}</p>
            </div>
        </div>

        <div style="margin-top:5rem; padding-top:2rem; border-top:1px solid rgba(255,255,255,0.06); text-align:center;">
            <p style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#4a4f57; letter-spacing:0.12em;">
                {T["footer"]}
            </p>
        </div>
    </section>
    """
)