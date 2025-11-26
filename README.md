# Advanced English Learning Platform (CEFR A1–C2)

This repository contains a **full‑featured Streamlit application** for learning English from beginner (A1) to mastery (C2) level.  The platform is designed to meet modern pedagogical standards and takes inspiration from industry‑leading language apps.  It emphasizes **spaced repetition**, **multimedia exercises**, **AI‑powered feedback**, and **progress analytics** so that learners can improve vocabulary, grammar, reading, listening, writing and speaking skills in a structured yet engaging way.

## ✨ Key Features

### 📚 Multi‑level curriculum

The course content spans all six CEFR levels (A1–C2).  Each module—vocabulary, grammar, reading, listening, writing and speaking—is populated with level‑appropriate tasks.  Sample tasks are provided in `data/tasks.json`, and you can extend or replace them with your own content.

### 🧠 Spaced‑repetition flashcards

Vocabulary practice uses the classic **Leitner system**.  This flashcard methodology, developed by Sebastian Leitner, uses boxes with increasing review intervals to optimize memory retention: cards start in box 1 and are reviewed daily; correct answers move them to the next box, while mistakes send them back to box 1.  Reviews become less frequent as the material is mastered【431546430580006†L84-L118】.  The platform adapts this algorithm digitally and schedules cards based on your progress.

### 📝 Grammar and usage exercises

Each level includes multiple‑choice and open‑ended grammar tasks.  Explanations accompany every correct answer, making it easy to understand why a particular structure is appropriate.

### 📖 Reading comprehension

Short passages followed by comprehension questions help learners practise reading.  The difficulty of the texts and questions escalates from simple present‑tense narratives at A1 up to advanced expositions on topics like globalization and quantum computing for C1–C2 learners.

### 🎧 Listening practice

Listening modules provide transcripts (and can be extended with audio files).  Learners answer questions about key details and ideas.  Including transcripts ensures accessibility and allows the platform to function even in environments without audio support.

### ✍️ Writing tasks with AI feedback

For writing practice, the application prompts users to compose paragraphs, emails or essays.  If an **OpenAI API key** is provided via the `OPENAI_API_KEY` environment variable, the app will use the ChatGPT API to generate detailed feedback on grammar, vocabulary, coherence and style.  Without an API key, a fallback analysis gives basic statistics and improvement tips.

### 💬 Speaking & conversation practice

The speaking module offers a simple chat interface.  When an API key is available, the app uses ChatGPT as a friendly conversation partner; otherwise, it politely instructs the user to enable AI support.  This design is inspired by modern language platforms where **AI chatbots assist learners in practising speaking**【52753157646863†L176-L194】.

### 📈 Progress tracking & analytics

The dashboard visualises your performance across modules.  Inspired by platforms that offer detailed analytics and personalized schedules【52753157646863†L201-L216】, the app records accuracy on vocabulary and grammar tasks and counts completed reading, listening and writing exercises.  You can monitor your strengths, identify areas needing review and celebrate milestones.

### 🔄 Immediate feedback & adaptive learning

Lessons start by reviewing previously studied vocabulary using spaced repetition, then introduce new material with interactive questions.  Immediate corrective feedback is provided after each answer, an approach shown to aid retention and motivation【52753157646863†L135-L138】.  Combined with the Leitner system, this ensures that learners spend time on words and concepts they find challenging and revisit them at optimal intervals.

### 🧭 Inspired by modern language apps

This project takes inspiration from best‑in‑class language platforms:

- **Spaced repetition & flashcards:** Memrise uses spaced repetition and gamified flashcards for vocabulary【52753157646863†L48-L68】.  Our vocabulary module adopts a similar Leitner‑based algorithm to schedule reviews and maximise retention.
- **Comprehensive modules:** Leading courses emphasise vocabulary, grammar, listening, speaking and writing in thematic units【52753157646863†L112-L127】.  This app mirrors that structure, ensuring balanced skill development.
- **Immediate corrective feedback and daily review:** Research‑based platforms begin sessions with spaced‑repetition reviews and use interactive presentations with instant feedback【52753157646863†L135-L138】.  The platform implements the same cycle for vocabulary and grammar.
- **AI‑powered tutors:** State‑of‑the‑art apps employ AI chatbots and adaptive algorithms to personalise difficulty and offer conversation practice【52753157646863†L176-L194】.  With an OpenAI API key, this app offers similar conversational and writing feedback capabilities.
- **Interactive subtitles & click‑to‑translate:** Services like Lingopie allow learners to click on any word in dual subtitles to see translations and save vocabulary【503997962083549†L140-L145】.  While our initial implementation focuses on text, the modular code structure makes it straightforward to integrate video or subtitle‑based exercises in the future.

## 📂 Repository structure

```
english_learning_platform/
├── app.py             # Main Streamlit application
├── utils.py           # Helper functions (task loading, evaluation, AI integration)
├── data/
│   └── tasks.json     # Sample tasks for all modules and levels
├── requirements.txt   # Python dependencies
├── .gitignore         # Files and folders to be ignored by Git
└── README.md          # Project overview and usage instructions
```

## 🚀 Getting started

1. **Clone this repository** and navigate to the project directory.
   ```bash
   git clone <repo_url>
   cd english_learning_platform
   ```

2. **Create a virtual environment** (optional but recommended) and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set the OpenAI API key** (optional).  To enable AI‑powered writing feedback and chat, export your API key:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

4. **Run the app** using Streamlit:
   ```bash
   streamlit run app.py
   ```

5. **Navigate through the sidebar** to select your CEFR level and explore the different modules.  Your progress is stored in the session state and can be extended to persist between sessions (e.g., by writing progress data to a file).

## 🛠️ Extending the platform

- **Add more tasks:**  Edit `data/tasks.json` to include additional vocabulary, grammar, reading, listening and writing items.  Each entry requires a unique `id` and appropriate fields (`question`, `options`, `answer`, etc.).
- **Integrate audio/video:**  Populate the `listening` tasks with audio files and update the code to use `st.audio()` for playback.  You can also extend the reading module to support interactive subtitles similar to Lingopie【503997962083549†L140-L145】.
- **Persist progress:**  Modify the session state logic to save learners’ results to a file or database, enabling multi‑session learning and longitudinal progress tracking.
- **Gamify the experience:**  Add achievements, points or leaderboards to motivate learners.  The Leitner algorithm already lends itself to gamification through boxes and streaks【431546430580006†L114-L118】.
- **Community features:**  The research suggests that peer feedback and community flashcard sharing enhance motivation【52753157646863†L235-L253】.  You could integrate a backend to allow users to share word lists or collaborate on exercises.

## 📜 License

This project is released under the MIT License.  See `LICENSE` for details.

## 🙏 Acknowledgements

The design of this platform draws inspiration from leading language learning tools and research.  References include Memrise’s use of spaced repetition and AI chatbots【52753157646863†L48-L68】【52753157646863†L176-L194】, the classic Leitner flashcard system for memory retention【431546430580006†L84-L118】, comprehensive course structures covering vocabulary, grammar, listening, speaking and writing【52753157646863†L112-L127】 and innovative interactive subtitle features exemplified by Lingopie【503997962083549†L140-L145】.
