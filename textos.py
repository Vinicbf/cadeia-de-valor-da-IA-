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
    "col_cit_feitas": ("Citações feitas", "Citations made"),
    "col_rede_media": ("Posição média na rede (% do topo)", "Average network position (top %)"),

    # ------------------------------------------------------------ Perfil da empresa
    "sb_empresa": ("Empresa", "Organization"),
    "pf_caption": ("{tipo} · {ini}–{fim} · camada dominante: {cam} ({pct}%) · #{rank} do núcleo por nº de patentes",
                   "{tipo} · {ini}–{fim} · dominant layer: {cam} ({pct}%) · #{rank} in the core by number of patents"),
    "pf_conv": ("Convergência", "Convergence"),
    "pf_x_base": ("{x}× a base", "{x}× the average"),
    "pf_kpi_cruz_f": ("Citações feitas que cruzam camada", "Citations made that cross layers"),
    "pf_kpi_cruz_r": ("Citações recebidas que cruzam camada", "Citations received that cross layers"),
    "pf_kpi_acad": ("Citações feitas à academia", "Citations made to academia"),
    "pf_abas": ("Panorama|Composição|Convergência|Citações|Universidades|Posição na rede|Influência estrutural",
                "Overview|Composition|Convergence|Citations|Universities|Network position|Structural influence"),
    "pf_pat_camada": ("Patentes por camada", "Patents by layer"),
    "pf_trajetoria": ("Trajetória por período", "Trajectory by period"),
    "pf_pat_por_camada": ("Patentes (por camada)", "Patents (by layer)"),
    "pf_toggle_base": ("Comparar com a base total (linhas tracejadas)", "Compare with the whole database (dashed lines)"),
    "pf_pct_carteira": ("% da carteira", "% of portfolio"),
    "pf_mistura": ("Como a mistura de camadas muda no tempo", "How the layer mix changes over time"),
    "pf_base_sufixo": ("(base)", "(database)"),
    "pf_n_camadas": ("{n} camada(s)", "{n} layer(s)"),
    "pf_pat_ncam": ("Patentes por nº de camadas", "Patents by number of layers"),
    "pf_combos": ("Combinações convergentes mais comuns", "Most common convergent combinations"),
    "pf_citacoes": ("Citações", "Citations"),
    "pf_feitas": ("feitas", "made"),
    "pf_recebidas": ("recebidas", "received"),
    "pf_feitas_recebidas": ("Citações feitas × recebidas", "Citations made × received"),
    "pf_cam_citada": ("camada citada", "cited layer"),
    "pf_cam_citante": ("camada citante", "citing layer"),
    "pf_fluxo": ("Para onde vão as citações feitas (% da linha)", "Where citations made go (% of row)"),
    "pf_tab_cit": ("Camada|Feitas|Cruzam camada — feitas (%)|Recebidas|Cruzam camada — recebidas (%)",
                   "Layer|Made|Cross-layer — made (%)|Received|Cross-layer — received (%)"),
    "pf_acad_f": ("Feitas → academia", "Made → academia"),
    "pf_acad_r": ("Recebidas ← academia", "Received ← academia"),
    "pf_pct_cit": ("% das citações", "% of citations"),
    "pf_vinculo": ("Vínculo com a academia", "Ties with academia"),
    "pf_parceiros": ("Maiores parceiros acadêmicos", "Top academic partners"),
    "pf_pagerank": ("% do topo no ranking de PageRank (menor é melhor)", "Top % in the PageRank ranking (lower is better)"),
    "pf_rank_de": ("#{r} de {pool}", "#{r} of {pool}"),
    "pf_top": ("top {x}%", "top {x}%"),
    "pf_ax_frag": ("+ componentes ao remover", "+ components when removed"),
    "pf_frag_titulo": ("Quanto a rede de cada camada se fragmenta sem esta organização",
                       "How much each layer's network fragments without this organization"),
    "pf_frag_legenda": ("Rótulo: componentes novos e posição entre as organizações do núcleo. "
                        "Os estudos de caso originais mediram só a camada Modelos de IA.",
                        "Label: new components and rank among core organizations. "
                        "The original case studies measured only the AI Models layer."),
    "pf_isoladas": ("Organizações isoladas (IA)", "Isolated organizations (AI)"),
    "pf_auto_r": ("Autocitação — recebidas", "Self-citation — received"),
    "pf_auto_f": ("Autocitação — feitas", "Self-citation — made"),
    "pf_mediana": ("mediana do núcleo: {x}%", "core median: {x}%"),

    # ------------------------------------------------------------ Comparar
    "cp_titulo": ("Comparar empresas", "Compare organizations"),
    "cp_escolha": ("**Escolha de 2 a 4 organizações** (agrupadas pela camada dominante)",
                   "**Choose 2 to 4 organizations** (grouped by dominant layer)"),
    "cp_max": ("Máximo de 4 organizações — usando as 4 primeiras da lista.",
               "Maximum of 4 organizations — using the first 4 in the list."),
    "cp_min": ("Escolha pelo menos duas organizações acima.", "Choose at least two organizations above."),
    "cp_lado": ("Indicadores lado a lado", "Indicators side by side"),
    "cp_perfil": ("Perfil relativo", "Relative profile"),
    "cp_perfil_leg": ("Percentil entre as organizações do núcleo (100 = melhor). "
                      "Na posição na rede, menor % do topo vira percentil maior.",
                      "Percentile among core organizations (100 = best). "
                      "For network position, a lower top % becomes a higher percentile."),
    "cp_comp": ("Composição por período", "Composition by period"),
    "cp_ranking": ("Ranking no núcleo", "Ranking in the core"),
    "cp_metrica": ("Métrica", "Metric"),
    "cp_menor": ("Nesta métrica, menor é melhor — as primeiras barras são as melhores posições.",
                 "For this metric, lower is better — the first bars are the best positions."),
    "cp_demais": ("Demais", "Others"),

    # ------------------------------------------------------------ menu
    "nav_visao": ("Visão geral", "Overview"),
    "nav_perfil": ("Perfil da empresa", "Organization profile"),
    "nav_comparar": ("Comparar", "Compare"),
    "nav_camadas": ("Camadas", "Layers"),
    "nav_metodologia": ("Metodologia", "Methodology"),

    # ------------------------------------------------------------ Camadas
    "cm_titulo": ("Camadas da cadeia", "Value chain layers"),
    "cm_escolha": ("Escolha a camada", "Choose a layer"),
    "cm_kpi_pat": ("Patentes na camada", "Patents in the layer"),
    "cm_kpi_peso": ("Peso na base (1976–2025)", "Share of the database (1976–2025)"),
    "cm_kpi_peso_rec": ("Peso em 2020-25", "Share in 2020-25"),
    "cm_delta": ("{x} p.p. desde 2000-04", "{x} pp since 2000-04"),
    "cm_kpi_orgs": ("Organizações na rede (2020-25)", "Organizations in the network (2020-25)"),
    "cm_lidera": ("Quem lidera a rede nesta camada", "Who leads the network in this layer"),
    "cm_bump_leg": ("Posição no PageRank, período a período, das 10 organizações mais centrais em 2020-25 (1 = topo).",
                    "PageRank position, period by period, of the 10 most central organizations in 2020-25 (1 = top)."),
    "cm_ax_pos": ("Posição (escala log)", "Rank (log scale)"),
    "cm_top15": ("Top 15 em 2020-25", "Top 15 in 2020-25"),
    "cm_tab": ("#|Organização|% do topo|Núcleo", "#|Organization|Top %|Core"),
    "cm_sim": ("sim", "yes"),
    "cm_volume": ("Volume × dependência (organizações do núcleo)", "Volume × dependence (core organizations)"),
    "cm_mais_patenteia": ("Quem mais patenteia aqui", "Who patents the most here"),
    "cm_rot_peso": ("Rótulo = peso da camada na carteira da própria organização.",
                    "Label = share of the layer in the organization's own portfolio."),
    "cm_mais_pesa": ("Para quem esta camada mais pesa", "For whom this layer weighs the most"),
    "cm_conexoes": ("Como a camada se conecta às outras", "How the layer connects to the others"),
    "cm_conexoes_leg": ("Citações feitas pelas organizações do núcleo, pela matriz camada citante × camada citada.",
                        "Citations made by core organizations, on the citing layer × cited layer matrix."),
    "cm_citam": ("Patentes de {cam} citam…", "{cam} patents cite…"),
    "cm_citadas": ("Patentes de {cam} são citadas por…", "{cam} patents are cited by…"),
    "cm_pct_feitas": ("% das citações feitas", "% of citations made"),
    "cm_pct_recebidas": ("% das citações recebidas", "% of citations received"),

    # ------------------------------------------------------------ Metodologia
    "mt_titulo": ("Metodologia", "Methodology"),
    "mt_caption": ("De onde vêm os dados, como foram construídos, que decisões foram tomadas e o que os indicadores não mostram.",
                   "Where the data come from, how they were built, which decisions were made and what the indicators do not show."),
    "mt_abas": ("Fontes de dados|Taxonomia|Base e núcleo|Consolidação de nomes|Indicadores|Validação|Limitações",
                "Data sources|Taxonomy|Database and core|Name consolidation|Indicators|Validation|Limitations"),
    "mt_fontes": (
        """
### Origem

Todos os dados vêm das **patentes concedidas pelo Escritório de Patentes e Marcas dos Estados Unidos (USPTO)**,
obtidas pelo **PatentsView**, a plataforma de dados abertos sobre patentes apoiada pelo próprio USPTO. O PatentsView
disponibiliza as patentes em tabelas para download em massa (*bulk data*), já com os titulares e inventores
desambiguados, ou seja, com as variações de grafia de um mesmo nome unificadas.

O USPTO é a fonte mais usada em estudos de inovação tecnológica: os Estados Unidos são o principal mercado de
proteção para empresas de tecnologia de todo o mundo, o que torna a base comparável entre organizações de
diferentes países.

### Tabelas utilizadas

| Tabela do PatentsView | Uso no painel | Campos principais |
|---|---|---|
| `g_patent` | identificação, tipo e data de concessão | `patent_id`, `patent_type`, `patent_date` |
| `g_cpc_current` | classificação tecnológica, base da taxonomia de camadas | `patent_id`, `cpc_group` |
| `g_assignee_disambiguated` | titular da patente | `patent_id`, `disambig_assignee_organization` |
| `g_us_patent_citation` | citações entre patentes norte-americanas | `patent_id` (citante), `citation_patent_id` (citada), `citation_category` |

### Recorte

- **Tipo:** patentes de utilidade (*utility patents*), que protegem invenções técnicas.
- **Período:** concessões de 1976 a 2025. O ano de cada patente é o ano da data de concessão.
- **Escopo tecnológico:** patentes com pelo menos um código CPC associado a uma das cinco camadas da cadeia de
  valor da IA (aba *Taxonomia*).
- **Titular:** patentes com titular organizacional identificado (empresas, universidades, institutos);
  patentes apenas de inventores individuais ficam fora.

### Volume final

| Item | Total |
|---|---:|
| Patentes únicas | {patentes} |
| Organizações (após consolidação de nomes) | {orgs} |
| Citações entre patentes da base (1976–2025) | 7.625.966 |
| Citações entre patentes da base (1995–2025) | 6.809.332 |

### Reprodutibilidade

Todo o processamento, da base bruta às tabelas do painel, está num único script (`gerar_dados.py`), disponível no
repositório do projeto no GitHub junto com o código do painel. As tabelas exibidas aqui são agregadas; os dados
brutos podem ser obtidos diretamente no PatentsView.
""",
        """
### Origin

All data come from **patents granted by the United States Patent and Trademark Office (USPTO)**, obtained through
**PatentsView**, the open patent data platform supported by the USPTO itself. PatentsView provides patents as bulk
download tables, with assignees and inventors already disambiguated, that is, with spelling variants of the same
name unified.

The USPTO is the most widely used source in studies of technological innovation: the United States is the main
protection market for technology companies worldwide, which makes the database comparable across organizations
from different countries.

### Tables used

| PatentsView table | Use in the dashboard | Main fields |
|---|---|---|
| `g_patent` | identification, type and grant date | `patent_id`, `patent_type`, `patent_date` |
| `g_cpc_current` | technology classification, basis of the layer taxonomy | `patent_id`, `cpc_group` |
| `g_assignee_disambiguated` | patent assignee | `patent_id`, `disambig_assignee_organization` |
| `g_us_patent_citation` | citations between US patents | `patent_id` (citing), `citation_patent_id` (cited), `citation_category` |

### Scope

- **Type:** utility patents, which protect technical inventions.
- **Period:** grants from 1976 to 2025. Each patent's year is the year of its grant date.
- **Technological scope:** patents with at least one CPC code associated with one of the five layers of the AI
  value chain (*Taxonomy* tab).
- **Assignee:** patents with an identified organizational assignee (companies, universities, institutes);
  patents held only by individual inventors are excluded.

### Final volume

| Item | Total |
|---|---:|
| Unique patents | {patentes} |
| Organizations (after name consolidation) | {orgs} |
| Citations between patents in the database (1976–2025) | 7,625,966 |
| Citations between patents in the database (1995–2025) | 6,809,332 |

### Reproducibility

All processing, from the raw database to the dashboard tables, is contained in a single script (`gerar_dados.py`),
available in the project's GitHub repository together with the dashboard code. The tables shown here are
aggregated; the raw data can be obtained directly from PatentsView.
"""),
    "mt_tax_intro": (
        "Cada patente é classificada numa **taxonomia de cinco camadas** da cadeia de valor da IA, a partir dos seus "
        "códigos de classificação tecnológica (CPC):",
        "Each patent is classified into a **five-layer taxonomy** of the AI value chain, based on its technology "
        "classification codes (CPC):"),
    "mt_tax_cab": ("| Camada | Abrange | Patentes | Peso |", "| Layer | Covers | Patents | Share |"),
    "mt_desc": (
        "fábricas, materiais e equipamentos de manufatura|semicondutores, processadores e memória|"
        "data centers e infraestrutura de nuvem|aprendizado de máquina e inteligência artificial|"
        "software, aplicações e produtos finais",
        "factories, materials and manufacturing equipment|semiconductors, processors and memory|"
        "data centers and cloud infrastructure|machine learning and artificial intelligence|"
        "software, applications and end products"),
    "mt_tax_resto": (
        """
Uma mesma patente pode tocar **mais de uma camada**; chamamos isso de **convergência**. Na base inteira,
**{conv}%** das patentes são convergentes, e esse valor serve de referência para a razão de convergência de cada
organização.

Os indicadores usam **contagem integral**: uma patente convergente conta uma vez em cada camada que toca. Por isso,
a soma das camadas é maior que o número de patentes únicas.
""",
        """
A single patent may touch **more than one layer**; we call this **convergence**. Across the whole database,
**{conv}%** of patents are convergent, and this value is the benchmark for each organization's convergence ratio.

The indicators use **full counting**: a convergent patent counts once in each layer it touches. For this reason,
the sum across layers exceeds the number of unique patents.
"""),
    "mt_base": (
        """
**Núcleo de análise.** A inovação patenteada é extremamente concentrada:

| Parcela das patentes | Organizações necessárias |
|---|---:|
| 50% | {nucleo} |
| 80% | {n80} |

O painel detalha as **{nucleo} organizações que concentram metade das patentes**. O corte de 50% foi preferido ao de
80% por dois motivos: com quase 1.900 organizações seria inviável revisar os nomes manualmente, e metade delas teria
menos de 100 patentes, o que torna instáveis indicadores como a taxa de convergência.

**Como a concentração é medida.** As organizações são ordenadas pelo total de patentes, e cada patente é contada
**uma única vez**, para a primeira de suas titulares no ranking. Isso evita dupla contagem de patentes com mais de
um titular.

**Períodos.** Até 1999, 2000-04, 2005-09, 2010-14, 2015-19 e 2020-25, pelo ano de concessão.
""",
        """
**Core of the analysis.** Patented innovation is extremely concentrated:

| Share of patents | Organizations required |
|---|---:|
| 50% | {nucleo} |
| 80% | {n80} |

The dashboard details the **{nucleo} organizations that hold half of all patents**. The 50% cut was preferred over
80% for two reasons: with almost 1,900 organizations, reviewing names manually would be unfeasible, and half of them
would have fewer than 100 patents, which makes indicators such as the convergence rate unstable.

**How concentration is measured.** Organizations are ranked by total patents, and each patent is counted **only
once**, for the first of its assignees in the ranking. This avoids double counting patents with more than one
assignee.

**Periods.** Up to 1999, 2000-04, 2005-09, 2010-14, 2015-19 and 2020-25, by grant year.
"""),
    "mt_consol": (
        """
Os nomes de titulares passam por duas etapas.

**1. Normalização automática** (todas as organizações): caixa baixa, remoção de pontuação, de sufixos societários
(Inc., Corp., Ltd., LLC, GmbH, Co. etc.) e do artigo "The". Assim, "Intel Corporation" e "INTEL CORP." viram "intel".

**2. Consolidação por grupo** (revisão manual das maiores organizações). A regra:

| Situação | Tratamento | Exemplos |
|---|---|---|
| Holding de propriedade intelectual | fundida ao grupo | Microsoft Technology Licensing → Microsoft |
| Subsidiária da mesma marca | fundida ao grupo | Sony Interactive Entertainment → Sony |
| Mudança de nome | fundida ao grupo | Facebook → Meta; Matsushita → Panasonic; Nippondenso → Denso |
| Aquisição | **mantida separada** | Red Hat (IBM), Sun (Oracle), Elpida (Micron) |
| Empresa independente de mesma marca | **mantida separada** | LG Chem ≠ LG Electronics; Rohm ≠ Rohm and Haas |

Manter aquisições separadas evita anacronismos: sem essa regra, patentes da Red Hat dos anos 1990 seriam
atribuídas à IBM, que só comprou a empresa em 2019.

**Casos discutíveis e decisão tomada:** HP e HPE separadas (cisão de 2015); EMC separada da Dell (aquisição de
2016); Kioxia separada da Toshiba (cisão de 2018); Siemens Healthineers fundida à Siemens (mesma marca).

**Anomalia da base.** No PatentsView, o rótulo "Samsung Display" abrange patentes do grupo inteiro desde 1987,
embora a empresa só exista desde 2012. Todas as entidades Samsung foram tratadas como um único grupo.

**Detecção de nomes faltantes.** Um ano de "início" tardio para uma empresa antiga indica nomes antigos não
fundidos. Foi assim que se identificaram, por exemplo, Matsushita (Panasonic), GoldStar (LG) e ASM Lithography (ASML).
""",
        """
Assignee names go through two steps.

**1. Automatic normalization** (all organizations): lowercase, removal of punctuation, corporate suffixes
(Inc., Corp., Ltd., LLC, GmbH, Co. etc.) and the article "The". Thus "Intel Corporation" and "INTEL CORP." both
become "intel".

**2. Group consolidation** (manual review of the largest organizations). The rule:

| Situation | Treatment | Examples |
|---|---|---|
| Intellectual property holding company | merged into the group | Microsoft Technology Licensing → Microsoft |
| Subsidiary under the same brand | merged into the group | Sony Interactive Entertainment → Sony |
| Name change | merged into the group | Facebook → Meta; Matsushita → Panasonic; Nippondenso → Denso |
| Acquisition | **kept separate** | Red Hat (IBM), Sun (Oracle), Elpida (Micron) |
| Independent company under the same brand | **kept separate** | LG Chem ≠ LG Electronics; Rohm ≠ Rohm and Haas |

Keeping acquisitions separate avoids anachronisms: without this rule, Red Hat patents from the 1990s would be
attributed to IBM, which only acquired the company in 2019.

**Debatable cases and the decision taken:** HP and HPE kept separate (2015 split); EMC separate from Dell (2016
acquisition); Kioxia separate from Toshiba (2018 spin-off); Siemens Healthineers merged into Siemens (same brand).

**Database anomaly.** In PatentsView, the label "Samsung Display" covers patents of the whole group since 1987,
although the company has only existed since 2012. All Samsung entities were treated as a single group.

**Detecting missing names.** A late "first year" for a long-established company signals old names that were not
merged. This is how, for example, Matsushita (Panasonic), GoldStar (LG) and ASM Lithography (ASML) were identified.
"""),
    "mt_ind": (
        """
### Funil de indicadores por organização

| Nível | Indicador | Definição |
|---|---|---|
| 1 | Panorama | Total de patentes únicas, período de atividade e camada dominante (maior participação na contagem por camada). |
| 2 | Composição | Participação de cada camada na carteira, por período. |
| 3 | Convergência | % de patentes em 2 ou mais camadas; **razão** = % da organização ÷ % da base. |
| 4 | Citações por camada | Citações feitas e recebidas por camada. Uma citação **cruza camada** quando a camada da patente citante difere da camada da citada (matriz camada × camada, com contagem integral nas duas pontas). |
| 4 | Volume de citações | Citações **únicas** feitas e recebidas, sem expandir por camada. É a medida usada na Visão geral, para que o volume não seja inflado pela convergência. |
| 4.5 | Universidade × empresa | % das citações feitas a patentes de titulares acadêmicos e % das recebidas deles. Autocitações não contam, mesmo quando a patente citada tem um cotitular acadêmico. |
| 5 | Posição na rede | PageRank ponderado na rede de citações entre organizações, por camada e período. **% do topo** = posição ÷ nº de organizações na rede; **elite** = até 1%. |
| 5.5 | Autocitação | % das citações recebidas que vêm de patentes da própria organização (e % das feitas que vão para ela). Distingue estratégias de inovação mais fechadas de mais abertas. |
| Extra | Influência estrutural | Componentes conectados novos e organizações que ficam **isoladas** quando a organização é removida da rede. |

### Detalhes de construção

**Janela das citações.** Os Níveis 4, 4.5, 5.5 e Extra usam citações entre patentes da base em que as **duas**
pontas são de 1995 a 2025, o mesmo recorte dos estudos de caso originais. O Nível 5 usa todas as citações, de 1976
a 2025.

**Titulares acadêmicos.** Identificados por palavras-chave no nome: universidade, college, instituto, regents,
research foundation, trustees, academia, polytechnic, além de CEA, Fraunhofer, Max Planck, CNRS, KAIST e ETRI.
A lista foi revisada manualmente (por exemplo, o SAS Institute, empresa de software, foi excluído).

**Rede do PageRank.** Cada citação liga a organização citante à citada. A camada é a da patente citante; o
período, o ano da patente citante. Participam as organizações dentro do corte de 80% das citações feitas em cada
camada (seleção do estudo original, traduzida para os grupos consolidados).

**Rede da influência estrutural.** Rede **não direcionada** entre organizações, uma para cada camada, formada
pelas citações em que as duas patentes pertencem à camada. Entram **todas** as organizações, sem corte, e as
autocitações são descartadas. Cada organização do núcleo é removida e mede-se quantos componentes novos surgem e
quantas organizações perdem todas as suas ligações (as que dependiam exclusivamente dela). O cálculo cobre as cinco
camadas; os estudos de caso usaram a camada **Modelos de IA**.

### O que ficou nos estudos de caso

Dois indicadores dos estudos de caso individuais não foram estendidos às organizações do núcleo:

- **Pureza de comunidade (5.5):** variou pouco entre as dez empresas estudadas (de 80% a 99%), distinguindo pouco
  as organizações, e exige construir uma rede interna de patentes para cada uma.
- **Patentes de virada (6.5):** sete das dez empresas conectam todos os pares de camadas; numa amostra maior, o
  indicador tende a saturar. Seu valor está na narrativa de cada empresa (qual patente conectou cada par de
  camadas e quando), que segue nos estudos de caso.
""",
        """
### Indicator funnel for each organization

| Level | Indicator | Definition |
|---|---|---|
| 1 | Overview | Total unique patents, period of activity and dominant layer (largest share in the layer count). |
| 2 | Composition | Share of each layer in the portfolio, by period. |
| 3 | Convergence | % of patents in 2 or more layers; **ratio** = organization's % ÷ database %. |
| 4 | Citations by layer | Citations made and received by layer. A citation **crosses layers** when the layer of the citing patent differs from that of the cited patent (layer × layer matrix, with full counting at both ends). |
| 4 | Citation volume | **Unique** citations made and received, without expanding by layer. This is the measure used in the Overview, so that volume is not inflated by convergence. |
| 4.5 | University × company | % of citations made to patents held by academic assignees and % of citations received from them. Self-citations are excluded, even when the cited patent has an academic co-assignee. |
| 5 | Network position | Weighted PageRank in the citation network between organizations, by layer and period. **Top %** = rank ÷ number of organizations in the network; **elite** = up to 1%. |
| 5.5 | Self-citation | % of citations received that come from the organization's own patents (and % of citations made that go to them). Distinguishes more closed from more open innovation strategies. |
| Extra | Structural influence | New connected components and organizations left **isolated** when the organization is removed from the network. |

### Construction details

**Citation window.** Levels 4, 4.5, 5.5 and Extra use citations between patents in the database where **both**
ends are from 1995 to 2025, the same scope as the original case studies. Level 5 uses all citations, 1976 to 2025.

**Academic assignees.** Identified by keywords in the name: university, college, institute, regents, research
foundation, trustees, academy, polytechnic, plus CEA, Fraunhofer, Max Planck, CNRS, KAIST and ETRI. The list was
reviewed manually (for example, SAS Institute, a software company, was excluded).

**PageRank network.** Each citation links the citing organization to the cited one. The layer is that of the citing
patent; the period, the year of the citing patent. The network includes the organizations within the 80% cut of
citations made in each layer (selection from the original study, mapped onto the consolidated groups).

**Structural influence network.** An **undirected** network between organizations, one per layer, built from the
citations in which both patents belong to the layer. **All** organizations are included, with no cut, and
self-citations are discarded. Each core organization is removed, and we measure how many new components appear and
how many organizations lose all their links (those that depended exclusively on it). The calculation covers the five
layers; the case studies used the **AI Models** layer.

### What remained in the case studies

Two indicators from the individual case studies were not extended to the core organizations:

- **Community purity (5.5):** varied little among the ten companies studied (from 80% to 99%), so it barely
  distinguishes organizations, and it requires building an internal patent network for each one.
- **Turning-point patents (6.5):** seven of the ten companies connect every pair of layers; in a larger sample, the
  indicator tends to saturate. Its value lies in each company's narrative (which patent connected each pair of
  layers, and when), which remains in the case studies.
"""),
    "mt_val": (
        """
O pipeline foi validado contra os dez estudos de caso individuais feitos anteriormente com a mesma base.

**Total de patentes após a consolidação**

| Empresa | Painel | Estudo de caso | Diferença |
|---|---:|---:|---:|
| Google | 14.604 | 14.607 | −0,02% |
| TSMC | 23.134 | 23.180 | −0,20% |
| IBM | 60.219 | 60.387 | −0,28% |
| Apple | 9.750 | 9.750 | 0,00% |
| Microsoft | 21.724 | 21.751 | −0,12% |
| Amazon | 10.915 | 10.983 | −0,62% |
| NVIDIA | 2.946 | 2.962 | −0,54% |
| Meta | 5.284 | 5.284 | 0,00% |
| Samsung | 33.292 | 33.296 | −0,01% |
| Intel | 19.904 | 20.000 | −0,48% |

As pequenas diferenças vêm de variações menores de nome que a busca por termo dos estudos de caso capturava.

**Influência estrutural na camada Modelos de IA** (componentes novos / organizações isoladas)

| Empresa | Painel | Estudo de caso |
|---|---:|---:|
| IBM | +124 / 117 | +139 / 131 |
| Amazon | +76 / 74 | +76 / 74 |
| Google | +51 / 47 | +50 / 46 |
| Microsoft | +42 / 41 | +41 / 40 |
| Samsung | +35 / 32 | +46 / 43 |
| Meta | +16 / 16 | +16 / 16 |
| Intel | +11 / 11 | +11 / 11 |
| NVIDIA | +9 / 9 | +9 / 9 |
| Apple | +9 / 8 | +8 / 7 |
| TSMC | 0 / 0 | +1 / 1 |

Quatro valores são idênticos e a ordem é preservada, exceto pela troca entre Samsung e Microsoft. As diferenças
vêm da consolidação de nomes (cada grupo vira um único nó) e da contagem de patentes com mais de um titular.

**Demais níveis**

| Nível | Resultado da validação |
|---|---|
| 2 e 3 | Idênticos: convergência da base 8,40%; Intel 11,89% (estudo: 11,86%), Chips 37,6% (37,7%). |
| 4 | Volume interno idêntico. O cruzamento fica 6–10 p.p. acima do estudo por usar a matriz camada × camada, mas a **ordem entre as empresas é preservada** (correlação de postos: 1,0 nas feitas e 0,93 nas recebidas). |
| 4.5 | Parceiros acadêmicos coincidem (Intel: ITRI 291 × 284; CEA 200 × 197; MIT 181 × 174). Os percentuais diferem porque a lista de instituições é própria. |
| 5 | Intel em 2020-25: #2, #3, #5, #8 e #12 nas cinco camadas (estudo: #2, #3, #6, #7 e #14). |
| 5.5 | A autocitação foi redefinida sobre todas as citações recebidas (o estudo de caso usava só as 15 patentes mais citadas). A ordem dos extremos se mantém: TSMC e Apple no topo. |
""",
        """
The pipeline was validated against the ten individual case studies previously carried out with the same database.

**Total patents after consolidation**

| Company | Dashboard | Case study | Difference |
|---|---:|---:|---:|
| Google | 14,604 | 14,607 | −0.02% |
| TSMC | 23,134 | 23,180 | −0.20% |
| IBM | 60,219 | 60,387 | −0.28% |
| Apple | 9,750 | 9,750 | 0.00% |
| Microsoft | 21,724 | 21,751 | −0.12% |
| Amazon | 10,915 | 10,983 | −0.62% |
| NVIDIA | 2,946 | 2,962 | −0.54% |
| Meta | 5,284 | 5,284 | 0.00% |
| Samsung | 33,292 | 33,296 | −0.01% |
| Intel | 19,904 | 20,000 | −0.48% |

The small differences come from minor name variants that the case studies' term search captured.

**Structural influence in the AI Models layer** (new components / isolated organizations)

| Company | Dashboard | Case study |
|---|---:|---:|
| IBM | +124 / 117 | +139 / 131 |
| Amazon | +76 / 74 | +76 / 74 |
| Google | +51 / 47 | +50 / 46 |
| Microsoft | +42 / 41 | +41 / 40 |
| Samsung | +35 / 32 | +46 / 43 |
| Meta | +16 / 16 | +16 / 16 |
| Intel | +11 / 11 | +11 / 11 |
| NVIDIA | +9 / 9 | +9 / 9 |
| Apple | +9 / 8 | +8 / 7 |
| TSMC | 0 / 0 | +1 / 1 |

Four values are identical and the order is preserved, except for Samsung and Microsoft swapping places. The
differences come from name consolidation (each group becomes a single node) and from counting patents with more
than one assignee.

**Other levels**

| Level | Validation result |
|---|---|
| 2 and 3 | Identical: database convergence 8.40%; Intel 11.89% (study: 11.86%), Chips 37.6% (37.7%). |
| 4 | Internal volume identical. Cross-layer shares are 6–10 pp higher than in the study because of the layer × layer matrix, but the **ranking of companies is preserved** (rank correlation: 1.0 for citations made and 0.93 for citations received). |
| 4.5 | Academic partners match (Intel: ITRI 291 × 284; CEA 200 × 197; MIT 181 × 174). Percentages differ because the list of institutions is our own. |
| 5 | Intel in 2020-25: #2, #3, #5, #8 and #12 across the five layers (study: #2, #3, #6, #7 and #14). |
| 5.5 | Self-citation was redefined over all citations received (the case study used only the 15 most-cited patents). The extremes keep their order: TSMC and Apple at the top. |
"""),
    "mt_lim": (
        """
- **Escopo geográfico.** A base cobre apenas patentes concedidas nos Estados Unidos. Estratégias de proteção
  concentradas em outros escritórios (China, Europa, Japão, Coreia) aparecem só na parte que também foi
  depositada no USPTO.
- **Citações restritas à base.** Só entram citações entre patentes da base. Citações a patentes fora da cadeia de
  valor da IA ou a literatura não patentária ficam de fora.
- **Cruzamento entre camadas.** Depende da regra de contagem adotada (ver *Indicadores*); os valores absolutos não
  são diretamente comparáveis aos dos estudos de caso.
- **Classificação acadêmica por palavras-chave.** Pode deixar de fora instituições com nomes atípicos ou incluir
  entidades ambíguas. Os percentuais do Nível 4.5 não são diretamente comparáveis aos dos estudos de caso.
- **Desambiguação herdada.** A qualidade dos nomes depende da desambiguação do PatentsView, que tem falhas
  pontuais (como o rótulo "Samsung Display").
- **Aquisições não consolidadas.** As trajetórias refletem a entidade que depositou a patente, e não o grupo
  econômico atual.
- **Último período.** 2020-25 inclui patentes concedidas até 2025; o atraso entre depósito e concessão faz com
  que as invenções mais recentes estejam sub-representadas.
""",
        """
- **Geographic scope.** The database covers only patents granted in the United States. Protection strategies
  concentrated in other offices (China, Europe, Japan, Korea) appear only to the extent that they were also filed
  with the USPTO.
- **Citations restricted to the database.** Only citations between patents in the database are included.
  Citations to patents outside the AI value chain or to non-patent literature are excluded.
- **Cross-layer citations.** Depend on the counting rule adopted (see *Indicators*); absolute values are not
  directly comparable to those of the case studies.
- **Keyword-based academic classification.** May miss institutions with unusual names or include ambiguous
  entities. Level 4.5 percentages are not directly comparable to those of the case studies.
- **Inherited disambiguation.** Name quality depends on PatentsView's disambiguation, which has occasional flaws
  (such as the "Samsung Display" label).
- **Acquisitions not consolidated.** Trajectories reflect the entity that filed the patent, not the current
  corporate group.
- **Last period.** 2020-25 includes patents granted up to 2025; the lag between filing and grant means the most
  recent inventions are under-represented.
"""),
}