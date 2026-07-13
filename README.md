# RAG based AI Lecture Assistant - Complete Setup Guide

A powerful **Retrieval-Augmented Generation (RAG)** system that transforms recorded lecture videos into an intelligent, searchable knowledge base. Extract speech, transcribe audio, create embeddings, and query your lectures using natural language.

---

## 🎯 What This Project Does

This is a complete end-to-end pipeline that:

1. **Video to Audio**: Extracts and converts video files to MP3 format using FFmpeg
2. **Audio to Text**: Transcribes MP3 files with timestamped segments using OpenAI Whisper
3. **Text to Embeddings**: Creates vector embeddings for semantic search using BGE-M3 model
4. **Query & Retrieve**: Search across lectures with AI-generated responses using Ollama LLM

---

## ✅ Prerequisites & Installation

### System Requirements (Windows)

You need these installed on your machine:

#### 1. **Python 3.11+**
   ```
   Download: https://www.python.org/downloads/
   ⚠️ During installation, CHECK "Add Python to PATH"
   ```

#### 2. **FFmpeg**
   ```powershell
   # Quick install via winget (recommended)
   winget install ffmpeg
   
   # Verify installation
   ffmpeg -version
   ```
   Or download from: https://ffmpeg.org/download.html

#### 3. **Ollama** (Embedding Model & LLM)
   ```
   Download: https://ollama.ai
   Install and run the application
   ```

   **Pull required models:**
   ```powershell
   ollama pull bge-m3      # Embedding model
   ollama pull llama2      # LLM for responses
   ```
   
   ⚠️ Keep Ollama running in background (http://localhost:11434)

#### 4. **Python Packages**
   ```powershell
   pip install whisper requests tqdm pandas scikit-learn numpy joblib
   ```

---

## 🚀 Setup

### Option A: Quick Setup (Recommended)

```powershell
# Navigate to project folder
cd RAG

# Create virtual environment
python -m venv aienv

# Activate it
& .\aienv\Scripts\Activate.ps1

# Install dependencies
pip install whisper requests tqdm pandas scikit-learn numpy joblib
```

### Option B: Using Existing Environment

```powershell
cd RAG
pip install whisper requests tqdm pandas scikit-learn numpy joblib
```

---

## 📖 Step-by-Step Beginner's Guide (5 Steps)

### **STEP 1: Collect Your Videos** 🎥

**What to do:**
1. Gather all lecture/tutorial videos (MP4, AVI, MOV, WebM, etc.)
2. **Move files to the `videos/` folder** in this project
3. **Rename videos using this format:** `#N | Title.mp4`
   - `#N` = Tutorial number (e.g., `#01`, `#02`, `#03`)
   - After ` | ` = Your descriptive title

**Example filenames:**
```
#01 | Python Basics.mp4
#02 | Data Structures.mp4
#03 | Advanced Functions.mp4
#04 | OOP and Classes.mp4
```

✅ **Result:** Videos organized in `videos/` folder

---

### **STEP 2: Convert Videos to MP3** 🎵

**Run this command:**
```powershell
python video_to_mp3.py
```

**What happens:**
- Reads all files from `videos/` folder
- Extracts audio using FFmpeg
- Saves MP3 files to `audios/` with names like `01_Python Basics.mp3`

**Time estimate:** 1-5 minutes per video

✅ **Result:** MP3 files appear in `audios/` folder

---

### **STEP 3: Convert MP3 to JSON Transcripts** 📝

**Run this command:**
```powershell
python mp3_to_json.py
```

**What happens:**
- Uses OpenAI Whisper (large-v2 model) to transcribe
- **DEFAULT LANGUAGE:** Hindi (`language="hi"`)
- Creates timestamped segments
- Saves JSON files to `jsons/` folder

**⚠️ Important:** First run downloads Whisper model (~3GB) - takes 2-5 minutes

**Time estimate:** 5-10 minutes per video (after model download)

**To change language:**
1. Open `mp3_to_json.py` in text editor
2. Find the line: `language="hi"`
3. Change to your language code:
   - `"en"` for English
   - `"es"` for Spanish  
   - `"fr"` for French
   - `"de"` for German
   - [See all language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

✅ **Result:** JSON files appear in `jsons/` folder

---

### **STEP 4: Convert JSON to Vector Embeddings** 🧠

**Run this command:**
```powershell
python preprocess_json.py
```

**What happens:**
- Loads all JSON transcripts from `jsons/` folder
- Generates vector embeddings for each chunk using BGE-M3 model
- Connects to Ollama API to create embeddings
- Saves complete knowledge base to `embeddings.joblib`

⚠️ **CRITICAL:** Ollama must be running!
- Open Ollama application before running this step
- It will listen on `http://localhost:11434`

**Time estimate:** 2-5 minutes (depending on transcript length)

✅ **Result:** `embeddings.joblib` file created (your knowledge base!)

---

### **STEP 5: Query Your Lectures with AI** 🤖

**Run this command:**
```powershell
python process_incomming.py
```

**What happens:**
- Loads `embeddings.joblib` into memory
- Prompts for your question
- Finds similar transcript chunks using embeddings
- Uses Ollama's LLM to generate intelligent responses
- Shows matching sections with timestamps

**Example usage:**
```
>>> Enter your question: What are Python data structures?
>>> [System finds similar lecture sections and generates answer]

>>> Enter your question: Explain OOP concepts
>>> [Retrieves relevant sections from lectures and summarizes]
```

✅ **Result:** Interactive query system for all your lectures!

---

## 📁 Project Structure

```
RAG/
├── videos/              ← 📹 ADD YOUR VIDEO FILES HERE
├── audios/              ← 🎵 Generated MP3 files (from STEP 2)
├── jsons/               ← 📄 Generated JSON transcripts (from STEP 3)
├── embeddings.joblib    ← 🧠 Knowledge base file (from STEP 4)
│
├── video_to_mp3.py      ← STEP 2 script
├── mp3_to_json.py       ← STEP 3 script
├── preprocess_json.py   ← STEP 4 script
├── process_incomming.py ← STEP 5 script
│
├── prompt.txt           ← System prompts
├── response.txt         ← Generated responses
└── README.md            ← This file
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ffmpeg not found` | Install FFmpeg (`winget install ffmpeg`), restart terminal |
| `whisper model download fails` | Check internet, first run takes 5+ minutes, ~3GB required |
| `Connection refused to localhost:11434` | Start Ollama application before STEP 4 |
| `Ollama model not found` | Run `ollama pull bge-m3` in terminal |
| `ModuleNotFoundError: whisper` | Run `pip install whisper` |
| `Timeout error in STEP 4` | Ollama is processing - wait longer, or restart Ollama |
| `CUDA out of memory` | Close other applications, run Ollama with less threads |
| `Videos not being converted` | Check video filenames match `#N | Title` format |
| `JSON files not created` | Ensure MP3 files are properly named with `_` separator |

---

## ⚠️ Important Notes

### Order Matters! 
Follow this sequence exactly:
1. Videos → 2. MP3 → 3. JSON → 4. Embeddings → 5. Query

### Don't Skip Steps
- Each step depends on the previous one
- Skipping steps will cause errors

### First-Time Setup Takes Time
- Whisper model download: 2-5 minutes
- Full pipeline (10 videos): 30-60 minutes total
- Subsequent runs are faster

### Backing Up
- **Back up `embeddings.joblib`** - it's your knowledge base!
- To add new videos: add to `videos/` and re-run STEP 2-4

### Language Settings
- Default: **Hindi** (`language="hi"`)
- To use English: Change `language="en"` in `mp3_to_json.py`
- Edit file before running STEP 3

---

## 📊 What Each Script Does

### `video_to_mp3.py` (STEP 2)
- Uses FFmpeg to extract audio from videos
- Converts to MP3 format
- Preserves tutorial number in filename

### `mp3_to_json.py` (STEP 3)
- Uses OpenAI Whisper for transcription
- Creates timestamped segments
- Outputs searchable JSON format

### `preprocess_json.py` (STEP 4)
- Creates embeddings via Ollama's BGE-M3 model
- Serializes to joblib format
- Enables semantic search

### `process_incomming.py` (STEP 5)
- Loads embeddings knowledge base
- Accepts natural language queries
- Computes similarity scores
- Returns top matching sections + LLM response

---

## 💡 Use Cases

✅ **For Students:**
- Find lecture sections WITHOUT rewatching
- Search by topic instead of timeline
- Get concise answers from lecture content

✅ **For Teachers:**
- Create searchable lecture archives
- Auto-generate study materials
- Help students review topics

✅ **For Researchers:**
- Build semantic search over video content
- Extract key concepts automatically
- Generate summaries

---

## 🔮 Future Improvements

- [ ] Web-based interface for queries
- [ ] Support multiple languages simultaneously
- [ ] Batch video processing
- [ ] Transcript editing before embedding
- [ ] Document summarization
- [ ] Export results to PDF/Word
- [ ] LMS integration (Canvas, Blackboard, Moodle)
- [ ] Real-time transcription

---

## 📝 License

This project is open for educational use. Modify and distribute as needed.

---

## ❓ FAQ

**Q: Can I use this for non-Hindi languages?**  
A: Yes! Edit `mp3_to_json.py` and change `language="hi"` to your language code before running STEP 3.

**Q: How large can my video collection be?**  
A: Limited only by disk space. Embeddings are efficient (~1MB per hour of video).

**Q: Can I run this on Mac/Linux?**  
A: Yes! All tools work on Mac and Linux. Use `source aienv/bin/activate` instead of `.ps1` script.

**Q: What if I add new videos later?**  
A: Add to `videos/` folder, re-run STEP 2-4 (STEP 5 will use updated embeddings).

**Q: Is internet required?**  
A: Only for first Whisper model download (~2-5 min). Everything runs locally after that.
