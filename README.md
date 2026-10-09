# 🐍 Python Notes & Automated Educational Documentation

An open-source Python learning repository powered by an **Automated Daily Video-to-Notes Engine**. This system extracts video transcripts from tutorials, breaks them down into modular topics, generates clean markdown notes with code snippets & memory breakdowns, and commits each topic individually.

---

## ⚡ How the Automated System Works

```
                       ┌────────────────────────┐
                       │  Video Queue / Manual  │
                       │    (YouTube / File)    │
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │   Transcript Extract   │
                       │ (API / Gemini Audio)   │
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │   AI Topic Breakdown   │
                       │     (Gemini 2.5)       │
                       └───────────┬────────────┘
                                   │
                                   ▼
        ┌──────────────────────────┴──────────────────────────┐
        ▼                                                     ▼
┌───────────────┐                                     ┌───────────────┐
│ Topic 1 Note  │ ──► [Commit #1 & Push]              │  Topic 2 Note │ ──► [Commit #2 & Push]
└───────────────┘                                     └───────────────┘
```

1. **Daily Video Fetching:** The system picks the next URL from `video_queue.txt` (or receives a link via GitHub Actions).
2. **Audio/Subtitle Extraction:** Fetches YouTube subtitles instantly, with automatic fallback to Gemini File API audio transcription.
3. **Modular Topic Partitioning:** Gemini divides the lecture into 2–5 distinct educational sub-topics with code samples, edge cases, and memory models.
4. **Individual Topic Commits:** Commits each topic note file with its own commit message, maximizing repository activity visibility.
5. **Index Auto-Sync:** Automatically registers every new topic note into this README index.

---

## 🚀 Setup & Configuration

### 1. Add GitHub Repository Secret
Go to **Settings** ➔ **Secrets and variables** ➔ **Actions** ➔ **New repository secret**:
- **Name:** `GEMINI_API_KEY`
- **Value:** Your Google Gemini API Key

### 2. Add Videos to Queue
Simply append your YouTube links to `video_queue.txt`:
```text
https://youtu.be/ZEKiIwWv9nM?si=uEq-ADaTkXLOYnpM
https://www.youtube.com/watch?v=...
```

### 3. Run Manually or On Schedule
- **Automated Schedule:** Runs automatically every day at `06:00 UTC`.
- **Manual Trigger:** Go to **Actions** ➔ **Daily Educational Notes Generator** ➔ **Run workflow** (enter optional video URL).

---

## 📚 Table of Contents & Learning Log

### 📖 Core Foundation Modules
| Chapter | Topic | Link |
|---|---|---|
| 001 | Environment Setup & Execution | [001.md](001.md) |
| 002 | Python Core Concepts | [002.md](002.md) |
| 003 | Python Shell & REPL | [003 Python shell.md](003%20Python%20shell.md) |
| 004 | Mutable vs Immutable Data Types | [004 Immutable and Mutable.md](004%20Immutable%20and%20Mutable.md) |
| 005 | Data Types Overview | [005 Data Types.md](005%20Data%20Types.md) |
| 006 | Internal Working: Reference Counts, Slicing | [006 Internal working of python - Copy, reference counts, slice.md](006%20Internal%20working%20of%20python%20-%20Copy,%20reference%20counts,%20slice.md) |
| 007 | Numbers & Arithmetic Internals | [007 Numbers in python.md](007%20Numbers%20in%20python.md) |
| 008 | Strings Deep Dive | [008 Strings in Python.md](008%20Strings%20in%20Python.md) |
| 009 | Lists & Memory Model | [009 Lists in Python.md](009%20Lists%20in%20Python.md) |
| 010 | Dictionaries & Hash Maps | [010 Dictionaries.md](010%20Dictionaries.md) |
| 011 | Tuples in Python | [011 Tuples in python.md](011%20Tuples%20in%20python.md) |
| 012 | Conditionals (Problem Solving) | [012 Conditionals (Problem Solving).md](012%20Conditionals%20(Problem%20Solving).md) |
| 013 | Loops (Problem Solving) | [013 Loops (Problem Solving).md](013%20Loops%20(Problem%20Solving).md) |
| 014 | Behind The Scenes of Loops | [014 BTS of Loops in Python.md](014%20BTS%20of%20Loops%20in%20Python.md) |
| 015 | Problem Solving Exercises | [015 Problem Solving.md](015%20Problem%20Solving.md) |
| 016 | Scopes, Namespaces & Closures | [016 Scopes and Closures.md](016%20Scopes%20and%20Closures.md) |
| 017 | Object-Oriented Programming (OOP) | [017 OOP.md](017%20OOP.md) |
| 018 | Decorators in Python | [018 Decorators in python.md](018%20Decorators%20in%20python.md) |
| 019 | File Handling & JSON Serialization | [019.md](019.md) |

---

## 📚 Index of Topics

| Date | Topic | Notes Link | Source |
|---|---|---|---|
