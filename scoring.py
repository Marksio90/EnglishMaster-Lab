def overall_score(text_answer: str) -> dict:
    base = 50
    return {
        "grammar": base,
        "vocab": base,
        "speaking": base,
        "writing": base,
        "listening": base,
        "reading": base,
        "overall": base
    }