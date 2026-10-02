import json

import plotly.express as px
import streamlit as st

from comum import CAMS, D, REF, br, cams, cores, ler, pers, rot, seletor_idioma, t, tabela_mestra, traduz

st.set_page_config(page_title="Cadeia de valor da IA · AI value chain", layout="wide")
seletor_idioma()

m = tabela_mestra()
mf = m
comp, curva, prk = ler("composicao"), ler("curva_concentracao"), ler("pagerank")
res = json.load(open(D / "resumo.json"))
p = prk[prk.periodo == "2020-25"].pivot(index="org", columns="camada", values="pct_topo")

# ---------------------------------------------------------------- barra lateral
st.sidebar.markdown(t("vg_sobre", patentes=br(res["patentes"]), nucleo=res["nucleo"]))
st.sidebar.markdown(t("como_citar"))

# ---------------------------------------------------------------- cabeçalho e KPIs
st.title(t("vg_titulo"))
st.caption(t("vg_subtitulo", nucleo=res["nucleo"]))
k = st.columns(4)
k[0].metric(t("kpi_patentes"), br(res["patentes"]))
k[1].metric(t("kpi_orgs"), br(res["organizacoes"]))
k[2].metric(t("kpi_metade"), t("grupos", n=res["nucleo"]))
k[3].metric(t("kpi_80"), t("grupos", n=br(res["n80"])))

# ---------------------------------------------------------------- concentração + composição
c1, c2 = st.columns(2)
with c1:
    st.subheader(t("vg_conc_titulo"))
    fig = px.line(curva, x="k", y="cobertura", log_x=True,
                  labels={"k": t("ax_n_orgs"), "cobertura": t("ax_pct_patentes")})
    for y in (50, 80):
        fig.add_hline(y=y, line_dash="dot", line_color="gray")
    st.plotly_chart(fig, width="stretch")
with c2:
    st.subheader(t("vg_comp_titulo"))
    b = traduz(comp[comp.org == "Base total"], "periodo", "camada")
    fig = px.bar(b, x="periodo", y="pct", color="camada", color_discrete_map=cores(),
                 category_orders={"periodo": pers(), "camada": cams()},
                 labels={"pct": t("ax_pct_base"), "periodo": "", "camada": ""})
    fig.update_xaxes(type="category")
    st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- volume de citações x convergência
st.subheader(t("vg_disp_titulo"))
st.caption(t("vg_disp_legenda"))
destaque = (set(REF) | set(mf.nlargest(5, "cit_recebidas").index)
            | set(mf.nlargest(3, "conv_razao").index))
dd = traduz(mf.reset_index(), "camada_dom")
fig = px.scatter(dd, x="cit_recebidas", y="conv_razao", size="total", color="camada_dom",
                 color_discrete_map=cores(), category_orders={"camada_dom": cams()},
                 hover_name="org", size_max=45, log_x=True,
                 text=[o if o in destaque else "" for o in dd.org],
                 hover_data={"total": ":,", "auto_recebidas_pct": ":.1f", "delta_componentes": True},
                 labels={"cit_recebidas": t("ax_cit_recebidas"), "conv_razao": t("ax_conv_razao"),
                         "camada_dom": t("leg_camada_dom"), "total": t("col_total"),
                         "auto_recebidas_pct": t("col_auto_recebidas_pct"),
                         "delta_componentes": t("col_delta_componentes")})
fig.add_hline(y=1, line_dash="dot", line_color="gray", annotation_text=t("media_base"))
fig.update_traces(textposition="top center")
fig.update_layout(height=550)
st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- elite estrutural
st.subheader(t("vg_rede_titulo"))
n = st.slider(t("vg_slider"), 10, len(mf), min(30, len(mf)))
top = mf.sort_values("total", ascending=False).head(n).index
hm = p.reindex(top)[CAMS]
hm.columns = cams()
fig = px.imshow(hm, color_continuous_scale="Blues_r", zmin=0, zmax=5, aspect="auto", text_auto=".1f",
                labels={"color": t("ax_pct_topo"), "x": "", "y": ""})
fig.update_xaxes(type="category")
fig.update_layout(height=22 * n + 120)
st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- tabela mestra
st.subheader(t("vg_tabela_titulo"))
cols = ["rank", "total", "cit_recebidas", "ano_ini", "camada_dom", "pct_dom", "conv_pct", "conv_razao",
        "cruz_feitas_pct", "cruz_recebidas_pct", "pct_feitas", "pct_recebidas", "camadas_elite",
        "chips_pct_topo", "delta_componentes", "isoladas", "auto_recebidas_pct"]
tab = traduz(mf.reset_index()[["org"] + cols], "camada_dom")
tab.columns = [t("col_org")] + [t(f"col_{c}") for c in cols]
st.dataframe(tab.round(2), hide_index=True, height=500)

with st.expander(t("vg_notas_titulo")):
    st.markdown(t("vg_notas"))
