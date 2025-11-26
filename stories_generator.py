import random
def gen_story():
    titles=["A Strange Day","Market Adventure","Lost on a Train","The Algorithm"]
    tones=["funny","mysterious","dramatic","chaotic"]
    levels=["A1","B1","B2","C1","C2"]
    scripts={
        "A1":"I went to the shop. I saw a cat. The cat was big. I bought milk.",
        "B1":"I missed my train because I didn’t hear my alarm. A group of tourists helped me find the right platform. We still keep in touch.",
        "B2":"The meeting ran overtime, and decisions had to be made under pressure. Despite minor misunderstandings, we delivered the prototype before the deadline.",
        "C1":"The research paper challenged prior assumptions; anomalous data patterns pointed toward a paradigm shift rather than experimental noise.",
        "C2":"Through deliberate linguistic calibration of multi‑modal pedagogical strategies, mastery emerged not from exposure volume, but from precision recall density."
    }
    t=random.choice(titles); tone=random.choice(tones); cefr=random.choice(levels); stxt=scripts[cefr[0]] if cefr.startswith("A") else scripts[cefr]
    return {"title":t,"tone":tone,"cefr":cefr,"story":stxt}