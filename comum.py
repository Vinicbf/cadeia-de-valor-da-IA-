from pathlib import Path

import pandas as pd
import streamlit as st

D = Path(__file__).parent / "dados"
CORES = {"Infra Física": "#888780", "Chips & Hardware": "#D85A30", "Cloud & Compute": "#378ADD",
         "Modelos de IA": "#7F77DD", "Software & Aplicação": "#1D9E75"}
CAMS = list(CORES)
PER = ["Até 1999", "2000-04", "2005-09", "2010-14", "2015-19", "2020-25"]
REF = ["Google", "TSMC", "IBM", "Apple", "Microsoft", "Amazon", "NVIDIA", "Meta", "Samsung", "Intel"]


@st.cache_data
def ler(nome):
    return pd.read_csv(D / f"{nome}.csv")


def br(x, casas=0):
    """Número no formato brasileiro: 1.234,5"""
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ordena(df):
    """Ordena as linhas pela sequência cronológica dos períodos."""
    return df.assign(_o=df.periodo.map({p: i for i, p in enumerate(PER)})).sort_values("_o").drop(columns="_o")


# rótulo -> (coluna, maior é melhor?)
METRICAS = {
    "Patentes": ("total", True),
    "% na camada dominante": ("pct_dom", True),
    "Convergência (× base)": ("conv_razao", True),
    "Cruzamento — feitas (%)": ("cruz_feitas_pct", True),
    "Cruzamento — recebidas (%)": ("cruz_recebidas_pct", True),
    "Academia — feitas (%)": ("pct_feitas", True),
    "Academia — recebidas (%)": ("pct_recebidas", True),
    "Camadas na elite (≤1%)": ("camadas_elite", True),
    "Posição média na rede (% do topo)": ("rede_media", False),
    "Chips: % do topo": ("chips_pct_topo", False),
}


@st.cache_data
def tabela_mestra():
    """Uma linha por organização do núcleo com as métricas-resumo de todos os níveis."""
    emp, cit, uni, prk = ler("empresas"), ler("citacoes"), ler("universidades"), ler("pagerank")
    t = cit[cit.camada == "Total"].set_index("org")[["cruz_feitas_pct", "cruz_recebidas_pct"]]
    u = uni[uni.periodo == "Total"].set_index("org")[["pct_feitas", "pct_recebidas"]]
    m = emp.set_index("org").join([t, u])
    p = prk[prk.periodo == "2020-25"].pivot(index="org", columns="camada", values="pct_topo").reindex(m.index)[CAMS]
    m["camadas_elite"] = (p <= 1).sum(axis=1)
    m["rede_media"] = p.mean(axis=1)
    m["chips_pct_topo"] = p["Chips & Hardware"]
    return m