import pandas as pd
import plotly.express as px
import streamlit as st

from comum import CAMS, CORES, PER, br, ler, ordena

st.set_page_config(page_title="Perfil da empresa", layout="wide")

emp = ler("empresas").set_index("org")
comp, cl, conv, comb = ler("composicao"), ler("camadas"), ler("convergencia"), ler("combos")
cit, flx = ler("citacoes"), ler("fluxo_camadas")
uni, parc, prk = ler("universidades"), ler("parceiros_academicos"), ler("pagerank")

lista = list(emp.index)
org = st.sidebar.selectbox("Empresa", lista, index=lista.index("Intel") if "Intel" in lista else 0)
e = emp.loc[org]
ct = cit[(cit.org == org) & (cit.camada == "Total")].iloc[0]
ut = uni[(uni.org == org) & (uni.periodo == "Total")].iloc[0]

# ---------------------------------------------------------------- cabeçalho
st.title(org)
st.caption(f"{e.tipo} · {e.ano_ini}–{e.ano_fim} · camada dominante: {e.camada_dom} ({br(e.pct_dom, 1)}%) "
           f"· #{e['rank']} do núcleo por nº de patentes")
k = st.columns(5)
k[0].metric("Patentes", br(e.total))
k[1].metric("Convergência", f"{br(e.conv_pct, 2)}%", f"{br(e.conv_razao, 2)}× a base", delta_color="off")
k[2].metric("Citações feitas que cruzam camada", f"{br(ct.cruz_feitas_pct, 1)}%")
k[3].metric("Citações recebidas que cruzam camada", f"{br(ct.cruz_recebidas_pct, 1)}%")
k[4].metric("Citações feitas à academia", f"{br(ut.pct_feitas, 2)}%")

abas = st.tabs(["Panorama", "Composição", "Convergência", "Citações", "Universidades", "Posição na rede", "Em breve"])

# ---------------------------------------------------------------- Nível 1
with abas[0]:
    a, b = st.columns([1, 2])
    x = cl[cl.org == org]
    fig = px.bar(x, x="n", y="camada", orientation="h", color="camada", color_discrete_map=CORES,
                 category_orders={"camada": CAMS}, text=x.pct.map(lambda v: br(v, 1) + "%"),
                 labels={"n": "Patentes", "camada": ""}, title="Patentes por camada")
    fig.update_layout(showlegend=False)
    a.plotly_chart(fig, width="stretch")
    y = comp[comp.org == org]
    fig = px.bar(y, x="periodo", y="n", color="camada", color_discrete_map=CORES,
                 category_orders={"periodo": PER, "camada": CAMS},
                 labels={"n": "Patentes (por camada)", "periodo": "", "camada": ""}, title="Trajetória por período")
    fig.update_xaxes(type="category")
    b.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- Nível 2
with abas[1]:
    base = st.toggle("Comparar com a base total (linhas tracejadas)")
    y = ordena(comp[comp.org == org])
    fig = px.line(y, x="periodo", y="pct", color="camada", markers=True, color_discrete_map=CORES,
                  category_orders={"camada": CAMS}, labels={"pct": "% da carteira", "periodo": "", "camada": ""},
                  title="Como a mistura de camadas muda no tempo")
    if base:
        bt = ordena(comp[comp.org == "Base total"])
        for c in CAMS:
            s = bt[bt.camada == c]
            fig.add_scatter(x=s.periodo, y=s.pct, mode="lines", line=dict(dash="dot", color=CORES[c]),
                            name=f"{c} (base)", showlegend=False)
    fig.update_xaxes(type="category", categoryorder="array", categoryarray=PER)
    st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- Nível 3
with abas[2]:
    a, b = st.columns(2)
    z = conv[conv.org.isin([org, "Base total"])].copy()
    z["ncam"] = z.ncam.astype(str) + " camada(s)"
    fig = px.bar(z, x="ncam", y="pct", color="org", barmode="group",
                 color_discrete_map={org: "#185FA5", "Base total": "#B4B2A9"},
                 labels={"pct": "% das patentes", "ncam": "", "org": ""}, title="Patentes por nº de camadas")
    a.plotly_chart(fig, width="stretch")
    w = comb[comb.org == org].sort_values("n")
    fig = px.bar(w, x="n", y="combo", orientation="h", labels={"n": "Patentes", "combo": ""},
                 title="Combinações convergentes mais comuns")
    b.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- Nível 4
with abas[3]:
    a, b = st.columns(2)
    x = cit[(cit.org == org) & (cit.camada != "Total")].melt(
        id_vars="camada", value_vars=["feitas", "recebidas"], var_name="sentido", value_name="n")
    fig = px.bar(x, x="camada", y="n", color="sentido", barmode="group", category_orders={"camada": CAMS},
                 labels={"n": "Citações", "camada": "", "sentido": ""}, title="Citações feitas × recebidas")
    a.plotly_chart(fig, width="stretch")
    f = flx[flx.org == org].pivot(index="cam_ct", columns="cam_cd", values="n").reindex(index=CAMS, columns=CAMS).fillna(0)
    f = f.div(f.sum(axis=1).replace(0, pd.NA), axis=0) * 100
    fig = px.imshow(f.astype(float), text_auto=".0f", color_continuous_scale="Blues",
                    labels={"x": "camada citada", "y": "camada citante", "color": "%"},
                    title="Para onde vão as citações feitas (% da linha)")
    b.plotly_chart(fig, width="stretch")
    st.dataframe(cit[cit.org == org].drop(columns="org").round(2), hide_index=True)

# ---------------------------------------------------------------- Nível 4.5
with abas[4]:
    a, b = st.columns(2)
    x = ordena(uni[(uni.org == org) & (uni.periodo != "Total")]).melt(
        id_vars="periodo", value_vars=["pct_feitas", "pct_recebidas"], var_name="sentido", value_name="pct")
    x["sentido"] = x.sentido.map({"pct_feitas": "Feitas → academia", "pct_recebidas": "Recebidas ← academia"})
    fig = px.line(x, x="periodo", y="pct", color="sentido", markers=True,
                  labels={"pct": "% das citações", "periodo": "", "sentido": ""}, title="Vínculo com a academia")
    fig.update_xaxes(type="category")
    a.plotly_chart(fig, width="stretch")
    p = parc[parc.org == org].head(10).copy()
    p["parceiro"] = p.parceiro.where(p.parceiro != p.parceiro.str.lower(), p.parceiro.str.title())
    p = p.melt(id_vars="parceiro", value_vars=["feitas", "recebidas"], var_name="sentido", value_name="n")
    fig = px.bar(p, x="n", y="parceiro", color="sentido", orientation="h",
                 labels={"n": "Citações", "parceiro": "", "sentido": ""}, title="Maiores parceiros acadêmicos")
    fig.update_yaxes(autorange="reversed")
    b.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- Nível 5
with abas[5]:
    r = prk[prk.org == org]
    h = r.pivot(index="camada", columns="periodo", values="pct_topo").reindex(index=CAMS, columns=PER)
    fig = px.imshow(h, text_auto=".2f", color_continuous_scale="Blues_r", zmin=0, zmax=5, aspect="auto",
                    labels={"color": "% do topo", "x": "", "y": ""},
                    title="% do topo no ranking de PageRank (menor é melhor)")
    fig.update_xaxes(type="category")
    st.plotly_chart(fig, width="stretch")
    u = r[r.periodo == "2020-25"].set_index("camada").reindex(CAMS)
    for col, (cam, l) in zip(st.columns(5), u.iterrows()):
        if pd.isna(l["rank"]):
            col.metric(cam, "—")
        else:
            col.metric(cam, f"#{int(l['rank'])} de {br(l['pool'])}", f"top {br(l['pct_topo'], 2)}%", delta_color="off")

with abas[6]:
    st.info("Em cálculo: Redes de patente (5.5 — autocitação e pureza de comunidade), "
            "Patentes de virada (6.5) e Influência estrutural (fragmentação ao remover a empresa).")