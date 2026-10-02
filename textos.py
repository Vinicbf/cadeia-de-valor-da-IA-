"""
textos.py — todos os textos do painel em português e inglês.

Cada entrada é  "chave": ("texto em português", "texto em inglês").
Para corrigir uma frase, altere aqui; as páginas não precisam mudar.
Trechos entre chaves, como {nucleo}, são preenchidos pelo painel.
"""

# ---------------------------------------------------------------- rótulos que vêm dos dados
ROTULOS = {
    "Infra Física": "Physical Infrastructure",
    "Chips & Hardware": "Chips & Hardware",
    "Cloud & Compute": "Cloud & Compute",
    "Modelos de IA": "AI Models",
    "Software & Aplicação": "Software & Applications",
    "Até 1999": "Up to 1999",
    "Base total": "Whole base",
    "Empresa": "Company",
    "Instituto": "Institute",
    "Total": "Total",
}

TEXTOS = {
    # ------------------------------------------------------------ comuns
    "idioma": ("Idioma", "Language"),
    "como_citar": (
        """
### Como citar
FORNARI, V.C.B. **Cadeia de valor da IA pela lente das patentes**: painel interativo.
Versão 1.0. Zenodo, 2026. DOI: [10.5281/zenodo.23071792](https://doi.org/10.5281/zenodo.23071792).
Disponível em: https://cadeia-ia.streamlit.app/.
""",
        """
### How to cite
FORNARI, V.C.B. **Cadeia de valor da IA pela lente das patentes** [The AI value chain through the lens of
patents]: interactive dashboard. Version 1.0. Zenodo, 2026.
DOI: [10.5281/zenodo.23071792](https://doi.org/10.5281/zenodo.23071792).
Available at: https://cadeia-ia.streamlit.app/.
"""),
    "grupos": ("{n} grupos", "{n} groups"),

    # ------------------------------------------------------------ Visão geral
    "vg_sobre": (
        """
### Sobre o painel
Este painel usa **patentes como lente** para mapear a cadeia de valor da inteligência artificial,
da fábrica ao produto final.

Cada patente é classificada em **cinco camadas**: Infra Física, Chips & Hardware, Cloud & Compute,
Modelos de IA e Software & Aplicação. Uma mesma patente pode tocar mais de uma camada, o que
chamamos de **convergência**.

**Recorte:** {patentes} patentes (1976–2025) e as **{nucleo} organizações** que
concentram metade delas.
""",
        """
### About this dashboard
This dashboard uses **patents as a lens** to map the value chain of artificial intelligence,
from the factory to the final product.

Each patent is classified into **five layers**: Physical Infrastructure, Chips & Hardware,
Cloud & Compute, AI Models and Software & Applications. A single patent may touch more than one
layer, which we call **convergence**.

**Scope:** {patentes} patents (1976–2025) and the **{nucleo} organizations** that hold
half of them.
"""),
    "vg_titulo": ("Cadeia de valor da IA pela lente das patentes", "The AI value chain through the lens of patents"),
    "vg_subtitulo": ("Núcleo de {nucleo} organizações que concentram metade das patentes da base · 1976–2025",
                     "Core of {nucleo} organizations holding half of all patents in the database · 1976–2025"),
    "kpi_patentes": ("Patentes únicas", "Unique patents"),
    "kpi_orgs": ("Organizações", "Organizations"),
    "kpi_metade": ("Metade das patentes em", "Half of all patents in"),
    "kpi_80": ("80% das patentes em", "80% of all patents in"),
    "vg_conc_titulo": ("Poucas organizações concentram a inovação", "A few organizations concentrate innovation"),
    "ax_n_orgs": ("Nº de organizações (escala log)", "Number of organizations (log scale)"),
    "ax_pct_patentes": ("% das patentes", "% of patents"),
    "vg_comp_titulo": ("A IA explode no fim do período", "AI takes off at the end of the period"),
    "ax_pct_base": ("% da base", "% of the database"),
    "vg_disp_titulo": ("Volume de citações × convergência", "Citation volume × convergence"),
    "vg_disp_legenda": (
        "X: citações únicas recebidas de outras patentes da base (1995–2025, escala log). "
        "Y: convergência em relação à média da base (1 = média). Tamanho = nº de patentes.",
        "X: unique citations received from other patents in the database (1995–2025, log scale). "
        "Y: convergence relative to the database average (1 = average). Size = number of patents."),
    "ax_cit_recebidas": ("Citações recebidas (escala log)", "Citations received (log scale)"),
    "ax_conv_razao": ("Convergência (× média da base)", "Convergence (× database average)"),
    "leg_camada_dom": ("Camada dominante", "Dominant layer"),
    "media_base": ("média da base", "database average"),
    "vg_rede_titulo": ("Posição na rede em 2020-25 (% do topo no PageRank — menor é melhor)",
                       "Network position in 2020-25 (top % in PageRank — lower is better)"),
    "vg_slider": ("Empresas exibidas (por nº de patentes)", "Organizations shown (by number of patents)"),
    "ax_pct_topo": ("% do topo", "top %"),
    "vg_tabela_titulo": ("Tabela mestra", "Master table"),
    "vg_notas_titulo": ("Notas metodológicas", "Methodological notes"),
    "vg_notas": (
        "- **Núcleo:** grupos que somam 50% das patentes únicas, após consolidar nomes (holdings de PI, "
        "subsidiárias e renomeações fundidas; aquisições mantidas separadas).\n"
        "- **Citações:** entre patentes da base de 1995 a 2025. O cruzamento usa a matriz camada citante × "
        "camada citada.\n"
        "- **Academia:** classificação por palavras-chave (universidades, institutos, fundações de pesquisa), "
        "sem contar autocitações.\n"
        "- **PageRank:** rede de organizações por camada e período, restrita ao corte de 80% das citações feitas; "
        "percentil = posição ÷ total de nós.\n"
        "- **Fragmentação:** componentes conectados novos na rede de citação entre organizações da camada "
        "Modelos de IA quando a organização é removida.\n"
        "- **Mais detalhes:** página *Metodologia*.",
        "- **Core:** groups that together hold 50% of unique patents, after consolidating names (IP holding "
        "companies, subsidiaries and renamings merged; acquisitions kept separate).\n"
        "- **Citations:** between patents in the database, 1995 to 2025. Cross-layer citations are measured on "
        "the citing layer × cited layer matrix.\n"
        "- **Academia:** keyword-based classification (universities, institutes, research foundations), "
        "excluding self-citations.\n"
        "- **PageRank:** network of organizations by layer and period, restricted to the 80% cut of citations "
        "made; percentile = rank ÷ number of nodes.\n"
        "- **Fragmentation:** new connected components in the AI Models citation network between organizations "
        "when the organization is removed.\n"
        "- **More details:** *Methodology* page."),

    # ------------------------------------------------------------ colunas e métricas
    "col_org": ("Organização", "Organization"),
    "col_rank": ("#", "#"),
    "col_total": ("Patentes", "Patents"),
    "col_ano_ini": ("Início", "First year"),
    "col_camada_dom": ("Camada dominante", "Dominant layer"),
    "col_pct_dom": ("% dominante", "% dominant"),
    "col_conv_pct": ("Convergência %", "Convergence %"),
    "col_conv_razao": ("Converg. (× base)", "Converg. (× average)"),
    "col_cruz_feitas_pct": ("Cruz. feitas %", "Cross-layer made %"),
    "col_cruz_recebidas_pct": ("Cruz. recebidas %", "Cross-layer received %"),
    "col_pct_feitas": ("Academia feitas %", "Academia made %"),
    "col_pct_recebidas": ("Academia recebidas %", "Academia received %"),
    "col_camadas_elite": ("Camadas na elite (≤1%)", "Elite layers (≤1%)"),
    "col_chips_pct_topo": ("Chips: % do topo", "Chips: top %"),
    "col_delta_componentes": ("Fragmentação IA (+comp.)", "AI fragmentation (+comp.)"),
    "col_isoladas": ("Isoladas (IA)", "Isolated (AI)"),
    "col_auto_recebidas_pct": ("Autocitação recebida %", "Self-citation received %"),
    "col_cit_recebidas": ("Citações recebidas", "Citations received"),
}