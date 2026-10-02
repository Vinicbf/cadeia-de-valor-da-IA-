import pandas as pd
import plotly.express as px
import streamlit as st

from comum import CAMS, cams, cores, ler, metricas, ordena, pers, rot, t, tabela_mestra, traduz

m = tabela_mestra()
comp, prk = ler("composicao"), ler("pagerank")
MET = metricas()

# ---------------------------------------------------------------- seleção
st.title(t("cp_titulo"))
padrao = [o for o in ["Intel", "NVIDIA", "IBM", "Meta"] if o in m.index]
with st.container(border=True):
    st.markdown(t("cp_escolha"))
    sel = []
    for cam in CAMS:
        orgs = [o for o in m.index if m.loc[o, "camada_dom"] == cam]
        if orgs:
            sel += st.pills(rot(cam), orgs, selection_mode="multi",
                            default=[o for o in padrao if o in orgs], key=f"p_{cam}") or []
if len(sel) > 4:
    st.warning(t("cp_max"))
    sel = sel[:4]
if len(sel) < 2:
    st.info(t("cp_min"))
    st.stop()
COR = dict(zip(sel, ["#185FA5", "#D85A30", "#1D9E75", "#7F77DD"]))
st.caption(" · ".join(f"{o}: {rot(m.loc[o, 'camada_dom'])} ({int(m.loc[o, 'ano_ini'])}–{int(m.loc[o, 'ano_fim'])})"
                      for o in sel))

# ---------------------------------------------------------------- tabela + radar
a, b = st.columns([1, 1])
with a:
    st.subheader(t("cp_lado"))
    tab = m.loc[sel, [c for c, _ in MET.values()]].T
    tab.index = list(MET)
    st.dataframe(tab.round(2), height=560)
with b:
    st.subheader(t("cp_perfil"))
    st.caption(t("cp_perfil_leg"))
    eixos = [("conv_razao", True), ("cruz_feitas_pct", True), ("cruz_recebidas_pct", True),
             ("pct_feitas", True), ("camadas_elite", True), ("rede_media", False)]
    r = pd.DataFrame({t(f"col_{c}"): m[c].rank(pct=True, ascending=maior) * 100 for c, maior in eixos})
    rr = r.loc[sel].rename_axis("org").reset_index().melt(id_vars="org", var_name="eixo", value_name="percentil")
    fig = px.line_polar(rr, r="percentil", theta="eixo", color="org", line_close=True, range_r=[0, 100],
                        color_discrete_map=COR, labels={"org": ""})
    fig.update_traces(fill="toself", opacity=0.55)
    fig.update_layout(height=470, margin=dict(t=30, b=30))
    st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- composição
st.subheader(t("cp_comp"))
c = traduz(ordena(comp[comp.org.isin(sel)]), "periodo", "camada")
fig = px.bar(c, x="periodo", y="pct", color="camada", facet_col="org", color_discrete_map=cores(),
             category_orders={"camada": cams(), "periodo": pers(), "org": sel},
             labels={"pct": t("pf_pct_carteira"), "periodo": "", "camada": ""})
fig.update_xaxes(type="category", tickangle=-45)
fig.for_each_annotation(lambda x: x.update(text=x.text.split("=")[-1]))
fig.update_layout(height=420)
st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- rede
st.subheader(t("vg_rede_titulo"))
p = (prk[(prk.periodo == "2020-25") & prk.org.isin(sel)]
     .pivot(index="org", columns="camada", values="pct_topo").reindex(index=sel, columns=CAMS))
p.columns = cams()
fig = px.imshow(p, text_auto=".2f", color_continuous_scale="Blues_r", zmin=0, zmax=5, aspect="auto",
                labels={"color": t("ax_pct_topo"), "x": "", "y": ""})
fig.update_xaxes(type="category")
fig.update_layout(height=90 + 45 * len(sel))
st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- ranking
st.subheader(t("cp_ranking"))
rotulos = list(MET)
met = st.selectbox(t("cp_metrica"), rotulos, index=rotulos.index(t("col_conv_razao")))
col, maior = MET[met]
if not maior:
    st.caption(t("cp_menor"))
rk = m[[col]].dropna().sort_values(col, ascending=not maior).rename_axis("org").reset_index()
rk["destaque"] = rk.org.where(rk.org.isin(sel), t("cp_demais"))
fig = px.bar(rk, x="org", y=col, color="destaque", color_discrete_map={**COR, t("cp_demais"): "#D3D1C7"},
             labels={col: met, "org": ""})
fig.update_xaxes(type="category", tickangle=-60)
fig.update_layout(showlegend=False, height=460)
st.plotly_chart(fig, width="stretch")