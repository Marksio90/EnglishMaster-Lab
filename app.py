import streamlit as st
from database import init_db
from ui_components import nav, metric_block
from lessons import read
from analytics import show_stats
from srs_logic import SRS

init_db()
st.title("EnglishMaster Lab")
u = st.selectbox("User",["Demo – student A1","Demo – student B1","Demo – student C2"])
level = u.split()[-1]
m = nav()

if m=="Learn": txt=read(level); st.button("Answer (Voice/Text next modules)");
elif m=="SRS": s=SRS(); for cid,it,tp,d in s.due(1): st.button(f"Review {it}");
elif m=="Stats": show_stats();