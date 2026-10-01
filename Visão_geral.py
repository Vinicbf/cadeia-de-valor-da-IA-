import json

import plotly.express as px
import streamlit as st

from comum import CAMS, CORES, D, PER, REF, br, ler, tabela_mestra

st.set_page_config(page_title="Cadeia de valor da IA — patentes", layout="wide")

m = tabela_mestra()
mf = m
comp, curva, prk = ler("composicao"), ler("curva_concentracao"), ler("pagerank")
res = json.load(open(D / "resumo.json"))
p = prk[prk.periodo == "2020-25"].pivot(index="org", columns="camada", values="pct_topo")

# ---------------------------------------------------------------- barra lateral
st.sidebar.markdown(f"""
### Sobre o painel
Este painel usa **patentes como lente** para mapear a cadeia de valor da inteligência artificial,
da fábrica ao produto final.

Cada patente é classificada em **cinco camadas**: Infra Física, Chips & Hardware, Cloud & Compute,
Modelos de IA e Software & Aplicação. Uma mesma patente pode tocar mais de uma camada, o que
chamamos de **convergência**.

**Recorte:** {br(res['patentes'])} patentes (1976–2025) e as **{res['nucleo']} organizações** que
concentram metade delas.

""")
st.sidebar.markdown("""
### Como citar
FORNARI, V.C.B. **Cadeia de valor da IA pela lente das patentes**: painel interativo.
Versão 1.0. Zenodo, 2026. DOI: [10.5281/zenodo.23071792](https://doi.org/10.5281/zenodo.23071792).
Disponível em: https://cadeia-ia.streamlit.app/.
""")

# ---------------------------------------------------------------- cabeçalho e KPIs
st.title("Cadeia de valor da IA pela lente das patentes")
st.caption(f"Núcleo de {res['nucleo']} organizações que concentram metade das patentes da base · 1976–2025")
k = st.columns(4)
k[0].metric("Patentes únicas", br(res["patentes"]))
k[1].metric("Organizações", br(res["organizacoes"]))
k[2].metric("Metade das patentes em", f"{res['nucleo']} grupos")
k[3].metric("80% das patentes em", f"{br(res['n80'])} grupos")

# ---------------------------------------------------------------- concentração + composição
c1, c2 = st.columns(2)
with c1:
    st.subheader("Poucas organizações concentram a inovação")
    fig = px.line(curva, x="k", y="cobertura", log_x=True,
                  labels={"k": "Nº de organizações (escala log)", "cobertura": "% das patentes"})
    for y in (50, 80):
        fig.add_hline(y=y, line_dash="dot", line_color="gray")
    st.plotly_chart(fig, width="stretch")
with c2:
    st.subheader("A IA explode no fim do período")
    b = comp[comp.org == "Base total"]
    fig = px.bar(b, x="periodo", y="pct", color="camada", color_discrete_map=CORES,
                 category_orders={"periodo": PER, "camada": CAMS},
                 labels={"pct": "% da base", "periodo": "", "camada": ""})
    fig.update_xaxes(type="category")
    st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- influência x indispensabilidade
st.subheader("Volume de citações × convergência")
st.caption("X: citações únicas recebidas de outras patentes da base (1995–2025, escala log). "
           "Y: convergência em relação à média da base (1 = média). Tamanho = nº de patentes.")
destaque = (set(REF) | set(mf.nlargest(5, "cit_recebidas").index)
            | set(mf.nlargest(3, "conv_razao").index))
fig = px.scatter(mf.reset_index(), x="cit_recebidas", y="conv_razao", size="total", color="camada_dom",
                 color_discrete_map=CORES, hover_name="org", size_max=45, log_x=True,
                 text=[o if o in destaque else "" for o in mf.index],
                 hover_data={"total": ":,", "auto_recebidas_pct": ":.1f", "delta_componentes": True},
                 labels={"cit_recebidas": "Citações recebidas (escala log)",
                         "conv_razao": "Convergência (× média da base)", "camada_dom": "Camada dominante",
                         "total": "Patentes", "auto_recebidas_pct": "Autocitação recebida (%)",
                         "delta_componentes": "Fragmentação IA (+comp.)"})
fig.add_hline(y=1, line_dash="dot", line_color="gray", annotation_text="média da base")
fig.update_traces(textposition="top center")
fig.update_layout(height=550)
st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- elite estrutural
st.subheader("Posição na rede em 2020-25 (% do topo no PageRank — menor é melhor)")
n = st.slider("Empresas exibidas (por nº de patentes)", 10, len(mf), min(30, len(mf)))
top = mf.sort_values("total", ascending=False).head(n).index
fig = px.imshow(p.reindex(top)[CAMS], color_continuous_scale="Blues_r", zmin=0, zmax=5,
                aspect="auto", text_auto=".1f", labels={"color": "% do topo", "x": "", "y": ""})
fig.update_xaxes(type="category")
fig.update_layout(height=22 * n + 120)
st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- tabela mestra
st.subheader("Tabela mestra")
cols = {"rank": "#", "total": "Patentes", "ano_ini": "Início", "camada_dom": "Camada dominante",
        "pct_dom": "% dominante", "conv_pct": "Convergência %", "conv_razao": "Converg. (× base)",
        "cruz_feitas_pct": "Cruz. feitas %", "cruz_recebidas_pct": "Cruz. recebidas %",
        "pct_feitas": "Academia feitas %", "pct_recebidas": "Academia recebidas %",
        "camadas_elite": "Camadas na elite (≤1%)", "chips_pct_topo": "Chips: % do topo",
        "delta_componentes": "Fragmentação IA (+comp.)", "isoladas": "Isoladas (IA)",
        "auto_recebidas_pct": "Autocitação recebida %"}
tab = mf.reset_index()[["org"] + list(cols)].rename(columns={"org": "Organização", **cols})
st.dataframe(tab.round(2), hide_index=True, height=500)

with st.expander("Notas metodológicas"):
    st.markdown(
        "- **Núcleo:** grupos que somam 50% das patentes únicas, após consolidar nomes (holdings de PI, "
        "subsidiárias e renomeações fundidas; aquisições mantidas separadas).\n"
        "- **Citações (Níveis 4 e 4.5):** entre patentes da base de 1995 a 2025. O cruzamento usa a matriz "
        "camada citante × camada citada; os valores diferem dos dossiês individuais, mas a ordem é preservada "
        "(ρ = 1,0 / 0,93).\n"
        "- **Academia:** classificação por palavras-chave (universidades, institutos, fundações de pesquisa), "
        "sem contar autocitações.\n"
        "- **PageRank:** rede de organizações por camada e período, restrita ao corte de 80% das citações feitas; "
        "percentil = posição ÷ total de nós.\n"
        "- **Fragmentação:** componentes conectados novos na rede de citação entre organizações da camada "
        "Modelos de IA quando a organização é removida.\n"
        "- **Mais detalhes:** página *Metodologia*.")
