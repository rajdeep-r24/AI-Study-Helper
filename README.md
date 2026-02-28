# ⚡ ExamForge AI — Final Prep Platform

A stunning, AI-powered exam preparation platform built with Streamlit + Google Gemini.

---

## 🚀 Setup (2 minutes)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get your Gemini API Key
- Go to https://aistudio.google.com/app/apikey
- Create a free API key
- Copy it

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Enter API key in the code

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 📁 Upload Notes | PDF, DOCX, TXT → AI reads YOUR syllabus |
| 📄 Exam Generator | Full exam papers with answer keys + Bloom's tags |
| 🗂️ Question Bank | Expected questions + sample papers, 2 separate sections |
| 🃏 Flashcards | Flip-card revision for key concepts |
| ⏱️ Timed Practice | Simulate exam pressure with countdown timer |
| 📚 PYQ Analyser | Past year question pattern analysis for YOUR university |
| 🔥 Imp Topics | AI identifies highest-probability exam topics |
| 📈 Analytics | Difficulty, Bloom's, and type distribution insights |

---

## 💡 How to Use

1. **Enter your Gemini API key** in the code
2. **Fill in your university, subject, and topic** in the sidebar
3. **Upload your notes** (PDF/DOCX/TXT) in the Upload tab
4. Click:
   - "Extract Imp Topics" → go to 🔥 Imp Topics tab
   - "Generate Flashcards" → go to 🃏 Flashcards tab
   - "Auto-fill Question Bank" → go to 🗂️ Question Bank tab
5. **Generate exam papers** in the 📄 Exam Generator tab
6. **Practice with timer** in ⏱️ Timed Practice
7. **Analyse PYQ patterns** by entering your university in 📚 PYQ Analyser

---

## 🎨 Design

- **Theme**: Dark futuristic with electric indigo + cyan accents
- **Fonts**: Syne (headings) + Outfit (body) + DM Mono (code/labels)
- **Animations**: Floating stats, shimmer gradient titles, slide-up cards, pulse badges
- **Fully responsive** sidebar navigation

---

## ⚙️ Tech Stack

- **Frontend**: Streamlit with custom CSS animations
- **AI**: Google Gemini 1.5 Flash
- **File parsing**: PyPDF2, python-docx
- **Export**: JSON + TXT download

---

## 🔑 API Key

Get yours free at: https://aistudio.google.com/app/apikey

The free tier supports ~60 requests/minute which is more than enough for exam prep.
