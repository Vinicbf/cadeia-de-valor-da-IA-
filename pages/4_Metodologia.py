import json

import streamlit as st

from comum import CAMS, D, br, ler, rot, t

res = json.load(open(D / "resumo.json"))
cl = ler("camadas")
bt = cl[cl.org == "Base total"].set_index("camada")

st.title(t("mt_titulo"))
st.caption(t("mt_caption"))
abas = st.tabs(t("mt_abas").split("|"))

with abas[0]:
    st.markdown(t("mt_fontes", patentes=br(res["patentes"]), orgs=br(res["organizacoes"])))

with abas[1]:
    st.markdown(t("mt_tax_intro"))
    desc = t("mt_desc").split("|")
    linhas = "\n".join(f"| {rot(c)} | {d} | {br(bt.loc[c, 'n'])} | {br(bt.loc[c, 'pct'], 1)}% |"
                       for c, d in zip(CAMS, desc))
    st.markdown(t("mt_tax_cab") + "\n|---|---|---:|---:|\n" + linhas)
    st.markdown(t("mt_tax_resto", conv=br(res["conv_base"], 2)))

with abas[2]:
    st.markdown(t("mt_base", nucleo=res["nucleo"], n80=br(res["n80"])))

with abas[3]:
    st.markdown(t("mt_consol"))

with abas[4]:
    st.markdown(t("mt_ind"))

with abas[5]:
    st.markdown(t("mt_val"))

with abas[6]:
    st.markdown(t("mt_lim"))