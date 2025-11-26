"""
Streamlit application for the advanced English learning platform.

This app provides interactive modules for vocabulary, grammar, reading,
listening, writing and speaking practice across CEFR levels A1–C2.  It
implements a Leitner spaced‑repetition system for vocabulary flashcards,
delivers immediate feedback on answers, offers optional AI‑powered
writing and chat capabilities, and visualises learning progress.

To start the application, run ``streamlit run app.py`` from the project
root.  For AI features, set the ``OPENAI_API_KEY`` environment variable.
"""

import os
import datetime
import json
from typing import Dict, List, Any

import streamlit as st
import pandas as pd
import numpy as np

from utils import (
    load_tasks,
    evaluate_answer,
    update_leitner,
    tasks_due,
    evaluate_writing,
    simple_chat,
)


LEVELS: List[str] = ["A1", "A2", "B1", "B2", "C1", "C2"]
MODULES: List[str] = ["Vocabulary", "Grammar", "Reading", "Listening", "Writing", "Speaking", "Progress"]


def init_session_state() -> None:
    """Initialize session state variables if they don't exist."""
    if "progress" not in st.session_state:
        # Leitner progress for vocabulary cards: {task_id: {box, next_review}}
        st.session_state.progress: Dict[str, Dict[str, Any]] = {}
    if "task_results" not in st.session_state:
        # Store correctness of tasks: {module: {level: {task_id: bool}}}
        st.session_state.task_results: Dict[str, Dict[str, Dict[str, bool]]] = {}
    if "indices" not in st.session_state:
        # Current index for modules without Leitner scheduling
        st.session_state.indices: Dict[str, Dict[str, int]] = {}
    if "chat_history" not in st.session_state:
        # List of (sender, message) pairs for the speaking module
        st.session_state.chat_history: List[Dict[str, str]] = []


def get_api_key() -> str:
    """Retrieve the OpenAI API key from the environment if set."""
    return os.environ.get("OPENAI_API_KEY", "")


def record_task_result(module: str, level: str, task_id: str, correct: bool) -> None:
    """Record the result (correct/incorrect) of a task."""
    results = st.session_state.task_results
    if module not in results:
        results[module] = {}
    if level not in results[module]:
        results[module][level] = {}
    results[module][level][task_id] = correct


def vocabulary_module(level: str) -> None:
    """Render the vocabulary practice module using spaced repetition."""
    tasks = load_tasks(module="vocabulary", level=level)
    # Determine which tasks are due based on Leitner progress
    due_tasks = tasks_due(tasks, st.session_state.progress)
    st.write(f"### Vocabulary Practice – Level {level}")
    if not due_tasks:
        st.success("No flashcards are due today! Come back tomorrow or reset your progress to practice again.")
        if st.button("Reset vocabulary progress"):
            # Remove progress for vocabulary tasks of this level
            for t in tasks:
                tid = str(t["id"])
                st.session_state.progress.pop(tid, None)
            st.experimental_rerun()
        return
    # Use the first due task
    task = due_tasks[0]
    tid = str(task["id"])
    st.write(f"**Question:** {task['question']}")
    user_answer = ""
    if task.get("options"):
        user_answer = st.radio("Select your answer:", task["options"], key=f"vocab_radio_{tid}")
    else:
        user_answer = st.text_input("Your answer", key=f"vocab_input_{tid}")
    if st.button("Submit", key=f"vocab_submit_{tid}"):
        correct, similarity = evaluate_answer(task, user_answer)
        update_leitner(st.session_state.progress, tid, correct)
        record_task_result("Vocabulary", level, tid, correct)
        if correct:
            st.success("Correct! 🎉")
        else:
            st.error("Incorrect. Try again next time!")
        if task.get("explanation"):
            st.info(task["explanation"])
        # Offer to move to next card
        if st.button("Next card", key=f"vocab_next_{tid}"):
            st.experimental_rerun()


def generic_quiz_module(level: str, module_name: str) -> None:
    """Render a generic quiz module for grammar, reading or listening."""
    st.write(f"### {module_name} – Level {level}")
    # Set up index tracker
    if module_name not in st.session_state.indices:
        st.session_state.indices[module_name] = {}
    if level not in st.session_state.indices[module_name]:
        st.session_state.indices[module_name][level] = 0
    index = st.session_state.indices[module_name][level]
    tasks = load_tasks(module=module_name.lower(), level=level)
    if index >= len(tasks):
        st.success("You have completed all tasks for this module at this level! 🎉")
        if st.button("Restart module"):
            st.session_state.indices[module_name][level] = 0
            # Optionally clear recorded results
            st.session_state.task_results.get(module_name, {}).get(level, {}).clear()
            st.experimental_rerun()
        return
    task = tasks[index]
    tid = str(task["id"])
    # Different handling based on module
    if module_name == "Grammar":
        st.write(f"**Question:** {task['question']}")
        if task.get("options"):
            user_answer = st.radio("Select your answer:", task["options"], key=f"gram_radio_{tid}")
        else:
            user_answer = st.text_input("Your answer", key=f"gram_input_{tid}")
        if st.button("Submit", key=f"gram_submit_{tid}"):
            correct, _ = evaluate_answer(task, user_answer)
            record_task_result(module_name, level, tid, correct)
            if correct:
                st.success("Correct! 🎉")
            else:
                st.error("Incorrect.")
            if task.get("explanation"):
                st.info(task["explanation"])
            st.session_state.indices[module_name][level] += 1
            st.experimental_rerun()
    elif module_name == "Reading":
        st.write(f"**Passage:**\n\n{task['text']}")
        answers: List[str] = []
        for i, q in enumerate(task["questions"]):
            ans = st.text_input(q["question"], key=f"read_q{i}_{tid}")
            answers.append(ans)
        if st.button("Submit Answers", key=f"read_submit_{tid}"):
            all_correct = True
            for ans, q in zip(answers, task["questions"]):
                correct, _ = evaluate_answer({"answer": q["answer"]}, ans)
                all_correct = all_correct and correct
                if correct:
                    st.write(f"✅ Question: {q['question']} – Correct")
                else:
                    st.write(f"❌ Question: {q['question']} – Correct answer(s): {', '.join(q['answer'])}")
            record_task_result(module_name, level, tid, all_correct)
            st.session_state.indices[module_name][level] += 1
            st.experimental_rerun()
    elif module_name == "Listening":
        # Display transcript and ask questions
        st.write("**Transcript:**")
        st.info(task["transcript"])
        answers: List[str] = []
        for i, q in enumerate(task["questions"]):
            ans = st.text_input(q["question"], key=f"listen_q{i}_{tid}")
            answers.append(ans)
        if st.button("Submit Answers", key=f"listen_submit_{tid}"):
            all_correct = True
            for ans, q in zip(answers, task["questions"]):
                correct, _ = evaluate_answer({"answer": q["answer"]}, ans)
                all_correct = all_correct and correct
                if correct:
                    st.write(f"✅ Question: {q['question']} – Correct")
                else:
                    st.write(f"❌ Question: {q['question']} – Correct answer(s): {', '.join(q['answer'])}")
            record_task_result(module_name, level, tid, all_correct)
            st.session_state.indices[module_name][level] += 1
            st.experimental_rerun()


def writing_module(level: str) -> None:
    """Render the writing practice module with optional AI feedback."""
    tasks = load_tasks(module="writing", level=level)
    if not tasks:
        st.info("No writing prompts available for this level.")
        return
    # Use index tracker
    module_name = "Writing"
    if module_name not in st.session_state.indices:
        st.session_state.indices[module_name] = {}
    if level not in st.session_state.indices[module_name]:
        st.session_state.indices[module_name][level] = 0
    index = st.session_state.indices[module_name][level]
    if index >= len(tasks):
        st.success("You have completed all writing prompts for this level! 🎉")
        if st.button("Restart writing prompts"):
            st.session_state.indices[module_name][level] = 0
            st.experimental_rerun()
        return
    task = tasks[index]
    tid = str(task["id"])
    st.write(f"### Writing Practice – Level {level}")
    st.write(f"**Prompt:** {task['prompt']}")
    user_text = st.text_area("Your response", height=200, key=f"write_area_{tid}")
    if st.button("Get Feedback", key=f"write_submit_{tid}"):
        api_key = get_api_key()
        feedback = evaluate_writing(user_text, api_key=api_key, level=level)
        if "error" in feedback:
            st.error(feedback["error"])
        elif "feedback" in feedback:
            st.success("AI Feedback:")
            st.write(feedback["feedback"])
        else:
            st.success("Basic Analysis:")
            st.write(f"Word count: {feedback['word_count']}")
            st.write(f"Sentence count: {feedback['sentence_count']}")
            st.info(feedback["tips"])
        # For writing tasks we mark completion regardless of correctness
        record_task_result(module_name, level, tid, True)
        st.session_state.indices[module_name][level] += 1
        st.experimental_rerun()


def speaking_module() -> None:
    """Render the speaking (chat) practice module."""
    st.write("### Speaking Practice – Chat with AI")
    api_key = get_api_key()
    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["sender"] == "user":
            st.write(f"**You:** {chat['message']}")
        else:
            st.write(f"**AI:** {chat['message']}")
    # Use Streamlit's chat input (available in newer versions) or fallback to text input
    if hasattr(st, "chat_input"):
        user_msg = st.chat_input("Type your message and press Enter")
        if user_msg is not None:
            st.session_state.chat_history.append({"sender": "user", "message": user_msg})
            reply = simple_chat(user_msg, api_key=api_key)
            st.session_state.chat_history.append({"sender": "ai", "message": reply})
            st.experimental_rerun()
    else:
        user_msg = st.text_input("Enter your message", key="chat_input")
        if st.button("Send"):
            if user_msg:
                st.session_state.chat_history.append({"sender": "user", "message": user_msg})
                reply = simple_chat(user_msg, api_key=api_key)
                st.session_state.chat_history.append({"sender": "ai", "message": reply})
                st.experimental_rerun()


def progress_module() -> None:
    """Display a dashboard summarising user progress across modules and levels."""
    st.write("### Progress Dashboard")
    results = st.session_state.task_results
    if not results:
        st.info("No progress recorded yet. Complete some tasks to see your statistics!")
        return
    # Build a DataFrame summarising accuracy by module and level
    records = []
    for module, levels in results.items():
        for level, tasks in levels.items():
            total = len(tasks)
            correct = sum(1 for v in tasks.values() if v)
            accuracy = correct / total if total else 0
            records.append({"Module": module, "Level": level, "Total Tasks": total, "Correct": correct, "Accuracy": round(accuracy * 100, 2)})
    df = pd.DataFrame(records)
    st.dataframe(df)
    # Plot accuracy by module
    if not df.empty:
        chart_data = df.pivot_table(index="Module", values="Accuracy", aggfunc="mean")
        st.bar_chart(chart_data)


def main() -> None:
    """Main function to control app flow."""
    st.set_page_config(page_title="English Learning Platform", layout="wide")
    st.title("Advanced English Learning Platform")
    init_session_state()
    level = st.sidebar.selectbox("Select your CEFR level", LEVELS)
    module = st.sidebar.radio("Choose a module", MODULES)
    # Show information about AI status
    api_key = get_api_key()
    if not api_key:
        st.sidebar.warning("AI features disabled (no OPENAI_API_KEY found)")
    else:
        st.sidebar.success("AI features enabled")
    # Render selected module
    if module == "Vocabulary":
        vocabulary_module(level)
    elif module in ("Grammar", "Reading", "Listening"):
        generic_quiz_module(level, module)
    elif module == "Writing":
        writing_module(level)
    elif module == "Speaking":
        speaking_module()
    elif module == "Progress":
        progress_module()


if __name__ == "__main__":
    main()
