import pandas as pd
import plotly.express as px
import streamlit as st

from comum import CAMS, PER, br, cams, cores, ler, ordena, pers, rot, t, traduz

emp = ler("empresas").set_index("org")
comp, cl, conv, comb = ler("composicao"), ler("camadas"), ler("convergencia"), ler("combos")
cit, flx = ler("citacoes"), ler("fluxo_camadas")
uni, parc, prk = ler("universidades"), ler("parceiros_academicos"), ler("pagerank")

lista = list(emp.index)
org = st.sidebar.selectbox(t("sb_empresa"), lista, index=lista.index("Intel") if "Intel" in lista else 0)
e = emp.loc[org]
ct = cit[(cit.org == org) & (cit.camada == "Total")].iloc[0]
ut = uni[(uni.org == org) & (uni.periodo == "Total")].iloc[0]


def traduz_combo(s):
    return " + ".join(rot(x) for x in s.split(" + "))


# ---------------------------------------------------------------- cabeçalho
st.title(org)
st.caption(t("pf_caption", tipo=rot(e.tipo), ini=int(e.ano_ini), fim=int(e.ano_fim), cam=rot(e.camada_dom),
             pct=br(e.pct_dom, 1), rank=e["rank"]))
k = st.columns(5)
k[0].metric(t("col_total"), br(e.total))
k[1].metric(t("pf_conv"), f"{br(e.conv_pct, 2)}%", t("pf_x_base", x=br(e.conv_razao, 2)), delta_color="off")
k[2].metric(t("pf_kpi_cruz_f"), f"{br(ct.cruz_feitas_pct, 1)}%")
k[3].metric(t("pf_kpi_cruz_r"), f"{br(ct.cruz_recebidas_pct, 1)}%")
k[4].metric(t("pf_kpi_acad"), f"{br(ut.pct_feitas, 2)}%")

abas = st.tabs(t("pf_abas").split("|"))

# ---------------------------------------------------------------- Nível 1
with abas[0]:
    a, b = st.columns([1, 2])
    x = traduz(cl[cl.org == org], "camada")
    fig = px.bar(x, x="n", y="camada", orientation="h", color="camada", color_discrete_map=cores(),
                 category_orders={"camada": cams()}, text=x.pct.map(lambda v: br(v, 1) + "%"),
                 labels={"n": t("col_total"), "camada": ""}, title=t("pf_pat_camada"))
    fig.update_layout(showlegend=False)
    a.plotly_chart(fig, width="stretch")
    y = traduz(comp[comp.org == org], "periodo", "camada")
    fig = px.bar(y, x="periodo", y="n", color="camada", color_discrete_map=cores(),
                 category_orders={"periodo": pers(), "camada": cams()},
                 labels={"n": t("pf_pat_por_camada"), "periodo": "", "camada": ""}, title=t("pf_trajetoria"))
    fig.update_xaxes(type="category")
    b.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- Nível 2
with abas[1]:
    base = st.toggle(t("pf_toggle_base"))
    y = traduz(ordena(comp[comp.org == org]), "periodo", "camada")
    fig = px.line(y, x="periodo", y="pct", color="camada", markers=True, color_discrete_map=cores(),
                  category_orders={"camada": cams()},
                  labels={"pct": t("pf_pct_carteira"), "periodo": "", "camada": ""}, title=t("pf_mistura"))
    if base:
        bt = traduz(ordena(comp[comp.org == "Base total"]), "periodo", "camada")
        for c in cams():
            s = bt[bt.camada == c]
            fig.add_scatter(x=s.periodo, y=s.pct, mode="lines", line=dict(dash="dot", color=cores()[c]),
                            name=f"{c} {t('pf_base_sufixo')}", showlegend=False)
    fig.update_xaxes(type="category", categoryorder="array", categoryarray=pers())
    st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- Nível 3
with abas[2]:
    a, b = st.columns(2)
    z = conv[conv.org.isin([org, "Base total"])].copy()
    z["ncam"] = z.ncam.map(lambda n: t("pf_n_camadas", n=n))
    z["org"] = z.org.map(rot)
    fig = px.bar(z, x="ncam", y="pct", color="org", barmode="group",
                 color_discrete_map={org: "#185FA5", rot("Base total"): "#B4B2A9"},
                 labels={"pct": t("ax_pct_patentes"), "ncam": "", "org": ""}, title=t("pf_pat_ncam"))
    a.plotly_chart(fig, width="stretch")
    w = comb[comb.org == org].sort_values("n").copy()
    w["combo"] = w.combo.map(traduz_combo)
    fig = px.bar(w, x="n", y="combo", orientation="h", labels={"n": t("col_total"), "combo": ""},
                 title=t("pf_combos"))
    b.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- Nível 4
with abas[3]:
    a, b = st.columns(2)
    x = cit[(cit.org == org) & (cit.camada != "Total")].melt(
        id_vars="camada", value_vars=["feitas", "recebidas"], var_name="sentido", value_name="n")
    x["sentido"] = x.sentido.map({"feitas": t("pf_feitas"), "recebidas": t("pf_recebidas")})
    x = traduz(x, "camada")
    fig = px.bar(x, x="camada", y="n", color="sentido", barmode="group", category_orders={"camada": cams()},
                 labels={"n": t("pf_citacoes"), "camada": "", "sentido": ""}, title=t("pf_feitas_recebidas"))
    a.plotly_chart(fig, width="stretch")
    f = flx[flx.org == org].pivot(index="cam_ct", columns="cam_cd", values="n").reindex(index=CAMS, columns=CAMS).fillna(0)
    f = f.div(f.sum(axis=1).replace(0, float("nan")), axis=0) * 100   # camada sem citações fica em branco
    f.index, f.columns = cams(), cams()
    fig = px.imshow(f.astype(float), text_auto=".0f", color_continuous_scale="Blues",
                    labels={"x": t("pf_cam_citada"), "y": t("pf_cam_citante"), "color": "%"}, title=t("pf_fluxo"))
    b.plotly_chart(fig, width="stretch")
    tc = traduz(cit[cit.org == org].drop(columns="org"), "camada")
    tc.columns = t("pf_tab_cit").split("|")
    st.dataframe(tc.round(2), hide_index=True)

# ---------------------------------------------------------------- Nível 4.5
with abas[4]:
    a, b = st.columns(2)
    x = ordena(uni[(uni.org == org) & (uni.periodo != "Total")]).melt(
        id_vars="periodo", value_vars=["pct_feitas", "pct_recebidas"], var_name="sentido", value_name="pct")
    x["sentido"] = x.sentido.map({"pct_feitas": t("pf_acad_f"), "pct_recebidas": t("pf_acad_r")})
    x = traduz(x, "periodo")
    fig = px.line(x, x="periodo", y="pct", color="sentido", markers=True,
                  labels={"pct": t("pf_pct_cit"), "periodo": "", "sentido": ""}, title=t("pf_vinculo"))
    fig.update_xaxes(type="category")
    a.plotly_chart(fig, width="stretch")
    p = parc[parc.org == org].head(10).copy()
    p["parceiro"] = p.parceiro.where(p.parceiro != p.parceiro.str.lower(), p.parceiro.str.title())
    p = p.melt(id_vars="parceiro", value_vars=["feitas", "recebidas"], var_name="sentido", value_name="n")
    p["sentido"] = p.sentido.map({"feitas": t("pf_feitas"), "recebidas": t("pf_recebidas")})
    fig = px.bar(p, x="n", y="parceiro", color="sentido", orientation="h",
                 labels={"n": t("pf_citacoes"), "parceiro": "", "sentido": ""}, title=t("pf_parceiros"))
    fig.update_yaxes(autorange="reversed")
    b.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- Nível 5
with abas[5]:
    r = prk[prk.org == org]
    h = r.pivot(index="camada", columns="periodo", values="pct_topo").reindex(index=CAMS, columns=PER)
    h.index, h.columns = cams(), pers()
    fig = px.imshow(h, text_auto=".2f", color_continuous_scale="Blues_r", zmin=0, zmax=5, aspect="auto",
                    labels={"color": t("ax_pct_topo"), "x": "", "y": ""}, title=t("pf_pagerank"))
    fig.update_xaxes(type="category")
    st.plotly_chart(fig, width="stretch")
    u = r[r.periodo == "2020-25"].set_index("camada").reindex(CAMS)
    for col, (cam, l) in zip(st.columns(5), u.iterrows()):
        if pd.isna(l["rank"]):
            col.metric(rot(cam), "—")
        else:
            col.metric(rot(cam), t("pf_rank_de", r=int(l["rank"]), pool=br(l["pool"])),
                       t("pf_top", x=br(l["pct_topo"], 2)), delta_color="off")

# ---------------------------------------------------------------- Extra
with abas[6]:
    fr, au = ler("fragmentacao"), ler("autocitacao").set_index("org")
    fr["posicao"] = fr.groupby("camada").delta_componentes.rank(ascending=False, method="min").astype(int)
    f = fr[fr.org == org].set_index("camada").reindex(CAMS).fillna(0)
    fd = f.reset_index()
    fd["camada"] = fd.camada.map(rot)
    a, b = st.columns([2, 1])
    with a:
        fig = px.bar(fd, x="camada", y="delta_componentes", color="camada", color_discrete_map=cores(),
                     text=[f"+{int(d)} (#{int(p)})" for d, p in zip(fd.delta_componentes, fd.posicao)],
                     labels={"delta_componentes": t("pf_ax_frag"), "camada": ""}, title=t("pf_frag_titulo"))
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")
        st.caption(t("pf_frag_legenda"))
    with b:
        st.metric(t("pf_isoladas"), br(f.loc["Modelos de IA", "isoladas"]))
        if org in au.index:
            st.metric(t("pf_auto_r"), f"{br(au.loc[org, 'auto_recebidas_pct'], 1)}%",
                      t("pf_mediana", x=br(au.auto_recebidas_pct.median(), 1)), delta_color="off")
            st.metric(t("pf_auto_f"), f"{br(au.loc[org, 'auto_feitas_pct'], 1)}%",
                      t("pf_mediana", x=br(au.auto_feitas_pct.median(), 1)), delta_color="off")
