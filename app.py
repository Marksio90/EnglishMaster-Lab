import streamlit as st
from srs_colloc_vocab import SRSVocabColloc
from vocab_scenes import contextual_list
e=SRSVocabColloc(); st.title("Vocab + Collocations SRS")
if st.button("Review Queue"):
    it=e.get_due(); contextual_list(it)