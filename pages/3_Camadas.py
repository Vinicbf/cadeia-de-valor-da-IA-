import pandas as pd
import plotly.express as px
import streamlit as st

from comum import CAMS, CORES, br, cores, cams, ler, ordena, pers, rot, t, traduz

prk, cl, comp, flx = ler("pagerank"), ler("camadas"), ler("composicao"), ler("fluxo_camadas")
nucleo = set(ler("empresas").org)


def nome(o):
    """Nomes fora do núcleo estão em minúsculas: formata para exibição."""
    return o if o != o.lower() else o.title()


st.title(t("cm_titulo"))
cam = st.pills(t("cm_escolha"), CAMS, default="Chips & Hardware", format_func=rot, key="cam") or "Chips & Hardware"
cor = CORES[cam]
camr = rot(cam)

# ---------------------------------------------------------------- indicadores
bt = cl[cl.org == "Base total"].set_index("camada")
b = comp[comp.org == "Base total"].set_index(["camada", "periodo"]).pct
variacao = b[(cam, "2020-25")] - b[(cam, "2000-04")]
pool = prk[(prk.camada == cam) & (prk.periodo == "2020-25")].pool.iloc[0]
k = st.columns(4)
k[0].metric(t("cm_kpi_pat"), br(bt.loc[cam, "n"]))
k[1].metric(t("cm_kpi_peso"), f"{br(bt.loc[cam, 'pct'], 1)}%")
k[2].metric(t("cm_kpi_peso_rec"), f"{br(b[(cam, '2020-25')], 1)}%",
            t("cm_delta", x=("+" if variacao >= 0 else "") + br(variacao, 1)))
k[3].metric(t("cm_kpi_orgs"), br(pool))

# ---------------------------------------------------------------- liderança na rede
st.subheader(t("cm_lidera"))
p = prk[prk.camada == cam]
top10 = p[p.periodo == "2020-25"].nsmallest(10, "rank").org.tolist()
a, c = st.columns([2, 1])
with a:
    st.caption(t("cm_bump_leg"))
    bump = traduz(ordena(p[p.org.isin(top10)]), "periodo").assign(nome=lambda d: d.org.map(nome))
    fig = px.line(bump, x="periodo", y="rank", color="nome", markers=True, log_y=True,
                  category_orders={"nome": [nome(o) for o in top10]},
                  labels={"rank": t("cm_ax_pos"), "periodo": "", "nome": ""})
    fig.update_yaxes(autorange="reversed", tickvals=[1, 2, 5, 10, 20, 50, 100, 200, 500])
    fig.update_xaxes(type="category", categoryorder="array", categoryarray=pers())
    fig.update_layout(height=460)
    st.plotly_chart(fig, width="stretch")
with c:
    st.caption(t("cm_top15"))
    tp = p[p.periodo == "2020-25"].nsmallest(15, "rank")
    tab = pd.DataFrame({"a": tp["rank"].values, "b": tp.org.map(nome).values,
                        "c": tp.pct_topo.map(lambda z: br(z, 2)).values,
                        "d": tp.org.isin(nucleo).map({True: t("cm_sim"), False: "—"}).values})
    tab.columns = t("cm_tab").split("|")
    st.dataframe(tab, hide_index=True, height=460)

# ---------------------------------------------------------------- volume x dependência
st.subheader(t("cm_volume"))
x = cl[(cl.camada == cam) & (cl.org != "Base total")]
a, c = st.columns(2)
with a:
    v = x.nlargest(15, "n")
    fig = px.bar(v, x="org", y="n", text=v.pct.map(lambda z: br(z, 0) + "%"), color_discrete_sequence=[cor],
                 labels={"n": t("cm_kpi_pat"), "org": ""}, title=t("cm_mais_patenteia"))
    fig.update_xaxes(type="category", tickangle=-45)
    st.plotly_chart(fig, width="stretch")
    st.caption(t("cm_rot_peso"))
with c:
    d = x.nlargest(15, "pct")
    fig = px.bar(d, x="org", y="pct", text=d.pct.map(lambda z: br(z, 0) + "%"), color_discrete_sequence=[cor],
                 labels={"pct": t("pf_pct_carteira"), "org": ""}, title=t("cm_mais_pesa"))
    fig.update_traces(textposition="outside")
    fig.update_xaxes(type="category", tickangle=-45)
    st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- conexões
st.subheader(t("cm_conexoes"))
st.caption(t("cm_conexoes_leg"))
f = flx.groupby(["cam_ct", "cam_cd"]).n.sum().reset_index()
saida = traduz(f[f.cam_ct == cam].assign(pct=lambda z: z.n / z.n.sum() * 100), "cam_cd")
entrada = traduz(f[f.cam_cd == cam].assign(pct=lambda z: z.n / z.n.sum() * 100), "cam_ct")
a, c = st.columns(2)
for col, dados, eixo, titulo, rotulo in [
        (a, saida, "cam_cd", t("cm_citam", cam=camr), t("cm_pct_feitas")),
        (c, entrada, "cam_ct", t("cm_citadas", cam=camr), t("cm_pct_recebidas"))]:
    fig = px.bar(dados, x="pct", y=eixo, orientation="h", color=eixo, color_discrete_map=cores(),
                 category_orders={eixo: cams()}, text=dados.pct.map(lambda z: br(z, 1) + "%"),
                 labels={"pct": rotulo, eixo: ""}, title=titulo)
    fig.update_layout(showlegend=False)
    col.plotly_chart(fig, width="stretch")