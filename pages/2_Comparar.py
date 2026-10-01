import pandas as pd
import plotly.express as px
import streamlit as st

from comum import CAMS, CORES, METRICAS, PER, ler, ordena, tabela_mestra

st.set_page_config(page_title="Comparar", layout="wide")
m = tabela_mestra()
comp, prk = ler("composicao"), ler("pagerank")

st.title("Comparar empresas")
padrao = [o for o in ["Intel", "NVIDIA", "IBM", "Meta"] if o in m.index]
with st.container(border=True):
    st.markdown("**Escolha de 2 a 4 organizações** (agrupadas pela camada dominante)")
    sel = []
    for cam in CAMS:
        orgs = [o for o in m.index if m.loc[o, "camada_dom"] == cam]
        if orgs:
            sel += st.pills(cam, orgs, selection_mode="multi",
                            default=[o for o in padrao if o in orgs], key=f"p_{cam}") or []
if len(sel) > 4:
    st.warning("Máximo de 4 organizações — usando as 4 primeiras da lista.")
    sel = sel[:4]
if len(sel) < 2:
    st.info("Escolha pelo menos duas organizações acima.")
    st.stop()
COR = dict(zip(sel, ["#185FA5", "#D85A30", "#1D9E75", "#7F77DD"]))
st.caption(" · ".join(f"{o}: {m.loc[o, 'camada_dom']} ({int(m.loc[o, 'ano_ini'])}–{int(m.loc[o, 'ano_fim'])})"
                      for o in sel))

# ---------------------------------------------------------------- tabela + radar
a, b = st.columns([1, 1])
with a:
    st.subheader("Indicadores lado a lado")
    tab = m.loc[sel, [c for c, _ in METRICAS.values()]].T
    tab.index = list(METRICAS)
    st.dataframe(tab.round(2), height=390)
with b:
    st.subheader("Perfil relativo")
    st.caption("Percentil entre as organizações do núcleo (100 = melhor). Na posição na rede, menor % do topo vira percentil maior.")
    eixos = ["Convergência (× base)", "Cruzamento — feitas (%)", "Cruzamento — recebidas (%)",
             "Academia — feitas (%)", "Camadas na elite (≤1%)", "Posição média na rede (% do topo)"]
    r = pd.DataFrame({e: m[METRICAS[e][0]].rank(pct=True, ascending=METRICAS[e][1]) * 100 for e in eixos})
    rr = r.loc[sel].rename_axis("org").reset_index().melt(id_vars="org", var_name="eixo", value_name="percentil")
    fig = px.line_polar(rr, r="percentil", theta="eixo", color="org", line_close=True, range_r=[0, 100],
                        color_discrete_map=COR, labels={"org": ""})
    fig.update_traces(fill="toself", opacity=0.55)
    fig.update_layout(height=430, margin=dict(t=30, b=30))
    st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- composição
st.subheader("Composição por período")
c = ordena(comp[comp.org.isin(sel)])
fig = px.bar(c, x="periodo", y="pct", color="camada", facet_col="org", color_discrete_map=CORES,
             category_orders={"camada": CAMS, "periodo": PER, "org": sel},
             labels={"pct": "% da carteira", "periodo": "", "camada": ""})
fig.update_xaxes(type="category", tickangle=-45)
fig.for_each_annotation(lambda x: x.update(text=x.text.split("=")[-1]))
fig.update_layout(height=420)
st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- rede
st.subheader("Posição na rede em 2020-25 (% do topo no PageRank — menor é melhor)")
p = (prk[(prk.periodo == "2020-25") & prk.org.isin(sel)]
     .pivot(index="org", columns="camada", values="pct_topo").reindex(index=sel, columns=CAMS))
fig = px.imshow(p, text_auto=".2f", color_continuous_scale="Blues_r", zmin=0, zmax=5, aspect="auto",
                labels={"color": "% do topo", "x": "", "y": ""})
fig.update_xaxes(type="category")
fig.update_layout(height=90 + 45 * len(sel))
st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- ranking
st.subheader("Ranking no núcleo")
met = st.selectbox("Métrica", list(METRICAS), index=2)
col, maior = METRICAS[met]
if not maior:
    st.caption("Nesta métrica, menor é melhor — as primeiras barras são as melhores posições.")
rk = m[[col]].dropna().sort_values(col, ascending=not maior).rename_axis("org").reset_index()
rk["destaque"] = rk.org.where(rk.org.isin(sel), "Demais")
fig = px.bar(rk, x="org", y=col, color="destaque", color_discrete_map={**COR, "Demais": "#D3D1C7"},
             labels={col: met, "org": ""})
fig.update_xaxes(type="category", tickangle=-60)
fig.update_layout(showlegend=False, height=460)
st.plotly_chart(fig, width="stretch")