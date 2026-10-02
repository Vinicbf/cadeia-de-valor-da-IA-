from pathlib import Path

import pandas as pd
import streamlit as st

from textos import ROTULOS, TEXTOS

D = Path(__file__).parent / "dados"
CORES = {"Infra Física": "#888780", "Chips & Hardware": "#D85A30", "Cloud & Compute": "#378ADD",
         "Modelos de IA": "#7F77DD", "Software & Aplicação": "#1D9E75"}
CAMS = list(CORES)
PER = ["Até 1999", "2000-04", "2005-09", "2010-14", "2015-19", "2020-25"]
REF = ["Google", "TSMC", "IBM", "Apple", "Microsoft", "Amazon", "NVIDIA", "Meta", "Samsung", "Intel"]


def _versao():
    """Muda sempre que algum arquivo da pasta dados/ é atualizado — invalida o cache sozinho."""
    return max(f.stat().st_mtime for f in D.glob("*.csv"))


@st.cache_data
def _ler(nome, versao):
    return pd.read_csv(D / f"{nome}.csv")


def ler(nome):
    return _ler(nome, _versao())


# ---------------------------------------------------------------- idioma
def idioma():
    """'pt' ou 'en'. Na primeira visita, respeita o link ?lang=en."""
    if "idioma" not in st.session_state:
        st.session_state.idioma = "en" if st.query_params.get("lang", "pt").lower() == "en" else "pt"
    return st.session_state.idioma


def seletor_idioma():
    """Botão PT | EN no topo da barra lateral. Chamar no início de cada página."""
    atual = idioma()

    def _muda():
        st.session_state.idioma = st.session_state._lang or st.session_state.idioma

    st.session_state._lang = atual
    st.sidebar.segmented_control("Idioma · Language", ["pt", "en"], key="_lang", on_change=_muda,
                                 format_func=lambda x: {"pt": "Português", "en": "English"}[x])
    st.query_params["lang"] = st.session_state.idioma
    return st.session_state.idioma


def t(chave, **kw):
    """Texto da chave no idioma atual; {campos} são preenchidos com kw."""
    s = TEXTOS[chave][0 if idioma() == "pt" else 1]
    return s.format(**kw) if kw else s


def rot(x):
    """Traduz rótulos que vêm dos dados (camadas, períodos, 'Base total'...)."""
    return ROTULOS.get(x, x) if idioma() == "en" else x


def cores():
    return {rot(k): v for k, v in CORES.items()}


def cams():
    return [rot(c) for c in CAMS]


def pers():
    return [rot(p) for p in PER]


def traduz(df, *cols):
    """Cópia do DataFrame com as colunas indicadas traduzidas para exibição."""
    df = df.copy()
    for c in cols:
        df[c] = df[c].map(rot)
    return df


def br(x, casas=0):
    """Número formatado no padrão do idioma: 1.234,5 (pt) ou 1,234.5 (en)."""
    s = f"{x:,.{casas}f}"
    return s if idioma() == "en" else s.replace(",", "X").replace(".", ",").replace("X", ".")


def ordena(df):
    """Ordena as linhas pela sequência cronológica dos períodos."""
    return df.assign(_o=df.periodo.map({p: i for i, p in enumerate(PER)})).sort_values("_o").drop(columns="_o")


# (coluna, maior é melhor?) — o rótulo de cada métrica vem de textos.py (chave "col_<coluna>")
METRICAS = [("total", True), ("cit_recebidas", True), ("cit_feitas", True), ("pct_dom", True),
            ("conv_razao", True), ("cruz_feitas_pct", True), ("cruz_recebidas_pct", True),
            ("pct_feitas", True), ("pct_recebidas", True), ("camadas_elite", True),
            ("rede_media", False), ("chips_pct_topo", False), ("delta_componentes", True),
            ("isoladas", True), ("auto_recebidas_pct", True)]


def metricas():
    """Rótulo traduzido -> (coluna, maior é melhor?)."""
    return {t(f"col_{c}"): (c, maior) for c, maior in METRICAS}


def tabela_mestra():
    """Uma linha por organização do núcleo com as métricas-resumo de todos os níveis."""
    return _tabela_mestra(_versao())


@st.cache_data
def _tabela_mestra(versao):
    emp, cit, uni, prk = ler("empresas"), ler("citacoes"), ler("universidades"), ler("pagerank")
    fr, au = ler("fragmentacao"), ler("autocitacao")
    t = cit[cit.camada == "Total"].set_index("org")[["cruz_feitas_pct", "cruz_recebidas_pct"]]
    u = uni[uni.periodo == "Total"].set_index("org")[["pct_feitas", "pct_recebidas"]]
    f = fr[fr.camada == "Modelos de IA"].set_index("org")[["delta_componentes", "isoladas"]]
    m = emp.set_index("org").join([t, u, f, au.set_index("org")])
    m[["delta_componentes", "isoladas"]] = m[["delta_componentes", "isoladas"]].fillna(0)
    p = prk[prk.periodo == "2020-25"].pivot(index="org", columns="camada", values="pct_topo").reindex(m.index)[CAMS]
    m["camadas_elite"] = (p <= 1).sum(axis=1)
    m["rede_media"] = p.mean(axis=1)
    m["chips_pct_topo"] = p["Chips & Hardware"]
    return m