# 📘 WhistleSafe — Anonymous AI-Powered Crime Reporting System

WhistleSafe is a dual-dashboard Streamlit application that enables **citizens to anonymously report crimes** and allows **authorities to verify reports** using:

- ✅ AI-powered text analysis (Gemini)  
- ✅ Deepfake detection for uploaded videos  
- ✅ Auto-translation using Lingo.dev  
- ✅ Multi-language UI (English, Hindi, Telugu, Tamil, Spanish, French)  
- ✅ Auto-generated downloadable report (.docx)

This project solves the huge problem of **fake video reports**, **miscommunication**, and **language barriers** in public crime reporting.

---

# 🚀 Features Overview

## 🧑‍💻 1. Anonymous User Reporting Dashboard (`user_input.py`)

Users can:

- Create an anonymous account  
- Upload a crime-related video  
- Submit a text description of the incident  
- The system **auto-translates the text to English** for uniform processing  
- Track the progress/status of their past reports  
- Logout and login securely  

All reports are stored in **SQLite database** and visible to authorities.

---

## 🛂 2. Authority Verification Dashboard (`submission_verification.py`)

Authorities can:

### 🔍 View all reports
Each report contains:
- User ID  
- Uploaded video  
- Text description (auto-translated into selected UI language)  
- Current status (Pending / Accepted / Rejected)

### 🎥 AI Deepfake Detection (video analysis)

Uses a custom deepfake pipeline:
- Facial movement consistency  
- Frequency domain analysis  
- Audio-visual sync  

Produces:
- Final deepfake score  
- Component-wise breakdown  
- Interpretation + anomaly list  

*Video analysis output remains in English.*

### 🧠 AI Text Crime Analysis (Gemini)

Gemini extracts:
- Time of crime  
- Place of crime  
- Short summary  

Output is:
- Stored in English  
- Translated to chosen UI language using Lingo.dev  

### 📄 Auto-Generated DOCX Report

Upon Accept / Reject:
- A `.docx` file is generated  
- Contains translated text analysis  
- Contains translated status  
- Video analysis stays in English  
- Download button available  

---

# 🌐 Full Multi-Language Support (via Lingo.dev)

WhistleSafe uses Lingo.dev’s **Ultra-Fast AI Translation Engine**.

### ✔ What is Translated?
- All UI text  
- Text reports (user input → English)  
- Gemini output (English → UI language)  
- Dashboard labels, buttons, sections  
- DOCX final report (except video analysis)  

### ❗ What is NOT Translated?
- Deepfake detection output (kept in English for accuracy)

### 🔑 Example usage
```python
from lingo_translation import translate

translated_text = translate("Hello world", "hi")
