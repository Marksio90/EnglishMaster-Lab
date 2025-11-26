"""
utils.py
========

This module provides helper functions for the English learning platform.
It contains routines for loading task data, evaluating user answers,
managing a simple Leitner spaced‑repetition algorithm, and integrating
optional AI services for writing and speaking feedback.

The design is modular so that individual components (e.g., spaced
repetition, answer evaluation) can be reused across different Streamlit
pages. If additional functionality is needed, such as more advanced
natural language processing or database storage, extend this module
accordingly.

Note: External services like OpenAI require an API key set in the
environment variable ``OPENAI_API_KEY``. If no key is present, the
fallback implementations will be used.
"""

import json
import os
import datetime
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Tuple

try:
    import openai  # type: ignore
except ImportError:
    openai = None  # gracefully handle absence of openai package


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_tasks(module: Optional[str] = None, level: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load tasks from the JSON file and optionally filter by module and level.

    Tasks are stored in a single JSON file ``tasks.json`` located in the
    ``data`` directory. Each task has at least the keys ``id``, ``level``,
    ``module``, ``question`` and ``answer``. Some tasks include ``options``
    (for multiple choice questions), ``explanation`` and additional fields.

    Parameters
    ----------
    module : str, optional
        Name of the module to filter tasks by (e.g. ``"vocabulary"``).
    level : str, optional
        CEFR level to filter tasks by (e.g. ``"A1"``).

    Returns
    -------
    list of dict
        A list of tasks matching the specified criteria.
    """
    tasks_path = os.path.join(DATA_DIR, "tasks.json")
    if not os.path.isfile(tasks_path):
        raise FileNotFoundError(f"Task file not found: {tasks_path}")
    with open(tasks_path, "r", encoding="utf-8") as f:
        all_tasks: List[Dict[str, Any]] = json.load(f)
    filtered = []
    for task in all_tasks:
        if module is not None and task.get("module") != module:
            continue
        if level is not None and task.get("level") != level:
            continue
        filtered.append(task)
    return filtered


def evaluate_answer(task: Dict[str, Any], user_answer: str) -> Tuple[bool, float]:
    """Evaluate a user response against the expected answer.

    For multiple choice tasks, the evaluation is a simple string comparison.
    For open questions, the evaluation uses a ratio of similarity between
    the expected answer and the user's answer. The ratio is computed
    using ``difflib.SequenceMatcher`` and must exceed 0.6 to be
    considered correct.

    Parameters
    ----------
    task : dict
        Task dictionary containing at least an ``answer`` field.
    user_answer : str
        The answer provided by the user.

    Returns
    -------
    tuple of (bool, float)
        A tuple where the first element indicates whether the answer is
        correct and the second element is the similarity score (0.0–1.0).
    """
    expected = str(task.get("answer", "")).strip().lower()
    response = user_answer.strip().lower()
    # If multiple correct options are provided as a list, accept any
    if isinstance(task.get("answer"), list):
        correct = response in [str(a).lower() for a in task["answer"]]
        return correct, 1.0 if correct else 0.0
    # Simple exact match for short answers
    if task.get("options"):
        return response == expected, 1.0 if response == expected else 0.0
    # Fuzzy match for free text answers
    ratio = SequenceMatcher(None, expected, response).ratio()
    return ratio >= 0.6, ratio


def leitner_next_interval(box: int) -> int:
    """Return the number of days until the next review based on the Leitner box.

    The classic Leitner system uses exponential intervals of 1, 2, 4, 8 and
    16 days for boxes 1 through 5 respectively. If the box number is
    outside this range, a default of 16 days is returned.

    Parameters
    ----------
    box : int
        Current Leitner box number (1–5).

    Returns
    -------
    int
        Number of days until the card should be reviewed again.
    """
    intervals = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}
    return intervals.get(box, 16)


def update_leitner(progress: Dict[str, Any], task_id: str, correct: bool) -> None:
    """Update Leitner progress for a given task.

    This function modifies the ``progress`` dictionary in place. Each
    entry for a task contains the current box (1–5) and the next review
    date. If the answer is correct, the card is moved to the next
    higher box (up to 5) and the next review date is extended. If
    incorrect, the card is reset to box 1 and scheduled for review
    tomorrow.

    Parameters
    ----------
    progress : dict
        Dictionary storing Leitner progress keyed by task ID.
    task_id : str
        Identifier of the task being reviewed.
    correct : bool
        Whether the user answered the task correctly.
    """
    today = datetime.date.today()
    task_progress = progress.get(task_id, {"box": 1, "next_review": str(today)})
    box = task_progress.get("box", 1)
    if correct:
        box = min(box + 1, 5)
    else:
        box = 1
    days = leitner_next_interval(box)
    next_review_date = today + datetime.timedelta(days=days)
    progress[task_id] = {"box": box, "next_review": str(next_review_date)}


def tasks_due(tasks: List[Dict[str, Any]], progress: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return a list of tasks that are due for review based on Leitner progress.

    Parameters
    ----------
    tasks : list of dict
        List of tasks to consider.
    progress : dict
        Leitner progress dictionary keyed by task ID.

    Returns
    -------
    list of dict
        Tasks whose next review date is today or earlier, or that haven't
        been reviewed before.
    """
    today = datetime.date.today()
    due = []
    for task in tasks:
        tid = str(task.get("id"))
        if tid not in progress:
            due.append(task)
            continue
        pr = progress[tid]
        try:
            next_date = datetime.datetime.strptime(pr.get("next_review", str(today)), "%Y-%m-%d").date()
        except ValueError:
            next_date = today
        if next_date <= today:
            due.append(task)
    return due


def evaluate_writing(text: str, api_key: Optional[str] = None, level: str = "") -> Dict[str, Any]:
    """Provide feedback on a piece of writing.

    If an OpenAI API key is available and the ``openai`` package is installed,
    the function uses ChatGPT to generate comprehensive feedback covering
    grammar, vocabulary, coherence, and suggestions for improvement. The
    prompt is tailored to the CEFR level if provided. If no API key or
    ``openai`` package is present, a basic analysis is performed based on
    word count and sentence structure.

    Parameters
    ----------
    text : str
        The user's written submission.
    api_key : str, optional
        OpenAI API key. If provided, advanced feedback will be generated.
    level : str, optional
        CEFR level of the user (e.g. ``"B2"``). Used to contextualize AI
        feedback.

    Returns
    -------
    dict
        A dictionary containing feedback information. When using the
        fallback analysis, keys include ``word_count`` and ``sentence_count``.
    """
    text = text.strip()
    if not text:
        return {"error": "No text provided."}
    # Use OpenAI if available and an API key is supplied
    if api_key and openai:
        openai.api_key = api_key
        system_prompt = (
            "You are an English teacher evaluating a learner's writing. "
            "Provide constructive feedback on grammar, vocabulary, coherence, "
            "and overall style. Suggest improvements appropriate for a CEFR "
            f"{level} level learner."
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                max_tokens=300,
                temperature=0.7,
            )
            feedback = response.choices[0].message["content"].strip()
            return {"feedback": feedback}
        except Exception as e:
            # Return fallback feedback if API call fails
            return {"error": f"AI feedback unavailable: {e}"}
    # Fallback analysis: compute basic statistics
    sentences = [s for s in text.replace("\n", " ").split(".") if s.strip()]
    words = text.split()
    feedback = {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "tips": (
            "Consider varying your sentence structure and using transition words "
            "to improve coherence. Check subject-verb agreement and verb tenses."
        ),
    }
    return feedback


def simple_chat(prompt: str, api_key: Optional[str] = None) -> str:
    """Generate a response to the user's message using OpenAI or a canned reply.

    This function attempts to use the ChatGPT API when available. If no
    API key is provided or the API call fails, a simple echo reply is
    returned, instructing the user to enable AI support.

    Parameters
    ----------
    prompt : str
        The user's input message.
    api_key : str, optional
        OpenAI API key.

    Returns
    -------
    str
        Chatbot response to the prompt.
    """
    if not prompt.strip():
        return "Please say something to start the conversation."
    if api_key and openai:
        openai.api_key = api_key
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly English conversation partner."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.7,
            )
            reply = response.choices[0].message["content"].strip()
            return reply
        except Exception as e:
            return f"AI chat unavailable: {e}"
    # Fallback response
    return "AI functionality is disabled. To enable chat, set the OPENAI_API_KEY environment variable."
