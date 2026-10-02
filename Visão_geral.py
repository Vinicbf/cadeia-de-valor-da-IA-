"""
Visão_geral.py — ponto de entrada do painel (o Streamlit Cloud aponta para este arquivo).
Configura a página, desenha o seletor de idioma e monta o menu com os nomes no idioma escolhido.
O conteúdo de cada página está na pasta pages/.
"""
import streamlit as st

from comum import seletor_idioma, t

st.set_page_config(page_title="Cadeia de valor da IA · AI value chain", layout="wide")
seletor_idioma()

pg = st.navigation([
    st.Page("pages/0_Visao_geral.py", title=t("nav_visao"), default=True),
    st.Page("pages/1_Perfil_da_empresa.py", title=t("nav_perfil"), url_path="perfil"),
    st.Page("pages/2_Comparar.py", title=t("nav_comparar"), url_path="comparar"),
    st.Page("pages/3_Camadas.py", title=t("nav_camadas"), url_path="camadas"),
    st.Page("pages/4_Metodologia.py", title=t("nav_metodologia"), url_path="metodologia"),
])
pg.run()