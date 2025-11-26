import streamlit as st, random
ART={
  "A1":["I like cats.","My house is small.","I drink water."],
  "B1":["Remote work saves time.","Noise makes focus harder.","Habits build skill."],
  "C2":["Precision recall beats exposure.","Prosody conveys meaning.","Input richness scales mastery."]
}
def read(level): s=random.choice(ART.get(level,[])); st.text_area("Read:",s,height=120,disabled=True); return s
