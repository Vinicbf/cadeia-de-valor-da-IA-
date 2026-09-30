import pandas as pd
import plotly.express as px
import streamlit as st

from comum import CAMS, CORES, PER, br, ler, ordena

st.set_page_config(page_title="Camadas", layout="wide")
prk, cl, comp, flx = ler("pagerank"), ler("camadas"), ler("composicao"), ler("fluxo_camadas")
nucleo = set(ler("empresas").org)


def nome(o):
    """Nomes fora do núcleo estão em minúsculas: formata para exibição."""
    return o if o != o.lower() else o.title()


st.title("Camadas da cadeia")
cam = st.pills("Escolha a camada", CAMS, default="Chips & Hardware", key="cam") or "Chips & Hardware"
cor = CORES[cam]

# ---------------------------------------------------------------- indicadores
bt = cl[cl.org == "Base total"].set_index("camada")
b = comp[comp.org == "Base total"].set_index(["camada", "periodo"]).pct
variacao = b[(cam, "2020-25")] - b[(cam, "2000-04")]
pool = prk[(prk.camada == cam) & (prk.periodo == "2020-25")].pool.iloc[0]
k = st.columns(4)
k[0].metric("Patentes na camada", br(bt.loc[cam, "n"]))
k[1].metric("Peso na base (1976–2025)", f"{br(bt.loc[cam, 'pct'], 1)}%")
k[2].metric("Peso em 2020-25", f"{br(b[(cam, '2020-25')], 1)}%",
            f"{'+' if variacao >= 0 else ''}{br(variacao, 1)} p.p. desde 2000-04")
k[3].metric("Organizações na rede (2020-25)", br(pool))

# ---------------------------------------------------------------- liderança na rede
st.subheader("Quem lidera a rede nesta camada")
p = prk[prk.camada == cam]
top10 = p[p.periodo == "2020-25"].nsmallest(10, "rank").org.tolist()
a, c = st.columns([2, 1])
with a:
    st.caption("Posição no PageRank, período a período, das 10 organizações mais centrais em 2020-25 (1 = topo).")
    bump = ordena(p[p.org.isin(top10)]).assign(nome=lambda d: d.org.map(nome))
    fig = px.line(bump, x="periodo", y="rank", color="nome", markers=True, log_y=True,
                  category_orders={"nome": [nome(o) for o in top10]},
                  labels={"rank": "Posição (escala log)", "periodo": "", "nome": ""})
    fig.update_yaxes(autorange="reversed", tickvals=[1, 2, 5, 10, 20, 50, 100, 200, 500])
    fig.update_xaxes(type="category", categoryorder="array", categoryarray=PER)
    fig.update_layout(height=460)
    st.plotly_chart(fig, width="stretch")
with c:
    st.caption("Top 15 em 2020-25")
    t = p[p.periodo == "2020-25"].nsmallest(15, "rank")
    st.dataframe(pd.DataFrame({"#": t["rank"].values, "Organização": t.org.map(nome).values,
                               "% do topo": t.pct_topo.map(lambda z: br(z, 2)).values,
                               "Núcleo": t.org.isin(nucleo).map({True: "sim", False: "—"}).values}),
                 hide_index=True, height=460)

# ---------------------------------------------------------------- volume x dependência
st.subheader("Volume × dependência (organizações do núcleo)")
x = cl[(cl.camada == cam) & (cl.org != "Base total")]
a, c = st.columns(2)
with a:
    v = x.nlargest(15, "n")
    fig = px.bar(v, x="org", y="n", text=v.pct.map(lambda z: br(z, 0) + "%"), color_discrete_sequence=[cor],
                 labels={"n": "Patentes na camada", "org": ""}, title="Quem mais patenteia aqui")
    fig.update_xaxes(type="category", tickangle=-45)
    st.plotly_chart(fig, width="stretch")
    st.caption("Rótulo = peso da camada na carteira da própria organização.")
with c:
    d = x.nlargest(15, "pct")
    fig = px.bar(d, x="org", y="pct", text=d.pct.map(lambda z: br(z, 0) + "%"), color_discrete_sequence=[cor],
                 labels={"pct": "% da carteira", "org": ""}, title="Para quem esta camada mais pesa")
    fig.update_traces(textposition="outside")
    fig.update_xaxes(type="category", tickangle=-45)
    st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- conexões
st.subheader("Como a camada se conecta às outras")
st.caption("Citações feitas pelas organizações do núcleo, pela matriz camada citante × camada citada.")
f = flx.groupby(["cam_ct", "cam_cd"]).n.sum().reset_index()
saida = f[f.cam_ct == cam].assign(pct=lambda z: z.n / z.n.sum() * 100)
entrada = f[f.cam_cd == cam].assign(pct=lambda z: z.n / z.n.sum() * 100)
a, c = st.columns(2)
for col, dados, eixo, titulo, rot in [
        (a, saida, "cam_cd", f"Patentes de {cam} citam…", "% das citações feitas"),
        (c, entrada, "cam_ct", f"Patentes de {cam} são citadas por…", "% das citações recebidas")]:
    fig = px.bar(dados, x="pct", y=eixo, orientation="h", color=eixo, color_discrete_map=CORES,
                 category_orders={eixo: CAMS}, text=dados.pct.map(lambda z: br(z, 1) + "%"),
                 labels={"pct": rot, eixo: ""}, title=titulo)
    fig.update_layout(showlegend=False)
    col.plotly_chart(fig, width="stretch")