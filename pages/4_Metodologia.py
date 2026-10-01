import json

import pandas as pd
import streamlit as st

from comum import CAMS, D, br, ler

st.set_page_config(page_title="Metodologia", layout="wide")
res = json.load(open(D / "resumo.json"))
cl = ler("camadas")
bt = cl[cl.org == "Base total"].set_index("camada")

st.title("Metodologia")
st.caption("Como os dados foram construídos, que decisões foram tomadas e o que os indicadores não mostram.")

abas = st.tabs(["Taxonomia", "Base e núcleo", "Consolidação de nomes", "Indicadores", "Validação", "Limitações"])

# ---------------------------------------------------------------- taxonomia
with abas[0]:
    st.markdown("""
Cada patente é classificada numa **taxonomia de cinco camadas** da cadeia de valor da IA, a partir dos seus
códigos de classificação tecnológica (CPC):
""")
    desc = {"Infra Física": "fábricas, materiais e equipamentos de manufatura",
            "Chips & Hardware": "semicondutores, processadores e memória",
            "Cloud & Compute": "data centers e infraestrutura de nuvem",
            "Modelos de IA": "aprendizado de máquina e inteligência artificial",
            "Software & Aplicação": "software, aplicações e produtos finais"}
    linhas = "\n".join(f"| {c} | {desc[c]} | {br(bt.loc[c, 'n'])} | {br(bt.loc[c, 'pct'], 1)}% |" for c in CAMS)
    st.markdown("| Camada | Abrange | Patentes | Peso |\n|---|---|---:|---:|\n" + linhas)
    st.markdown(f"""
Uma mesma patente pode tocar **mais de uma camada**; chamamos isso de **convergência**. Na base inteira,
**{br(res['conv_base'], 2)}%** das patentes são convergentes, e esse valor serve de referência para a razão de
convergência de cada organização.

Os indicadores usam **contagem integral**: uma patente convergente conta uma vez em cada camada que toca. Por isso,
a soma das camadas é maior que o número de patentes únicas.
""")

# ---------------------------------------------------------------- base e núcleo
with abas[1]:
    st.markdown(f"""
**Fonte.** Patentes concedidas pelo USPTO, com titulares desambiguados pelo PatentsView
(`disambig_assignee_organization`) e citações da tabela `g_us_patent_citation`.

**Recorte.** {br(res['patentes'])} patentes únicas entre 1976 e 2025, de {br(res['organizacoes'])} organizações
(após a consolidação de nomes).

**Núcleo de análise.** A inovação patenteada é extremamente concentrada:

| Parcela das patentes | Organizações necessárias |
|---|---:|
| 50% | {res['nucleo']} |
| 80% | {br(res['n80'])} |

O painel detalha as **{res['nucleo']} organizações que concentram metade das patentes**. O corte de 50% foi preferido
ao de 80% por dois motivos: com ~1.900 organizações seria inviável revisar os nomes manualmente, e metade delas
teria menos de 100 patentes, o que torna instáveis indicadores como a taxa de convergência.

**Como a concentração é medida.** As organizações são ordenadas pelo total de patentes, e cada patente é contada
**uma única vez**, para a primeira de suas titulares no ranking. Isso evita dupla contagem de patentes com mais de
um titular.

**Períodos.** Até 1999, 2000-04, 2005-09, 2010-14, 2015-19 e 2020-25, pelo ano de concessão.
""")

# ---------------------------------------------------------------- consolidação
with abas[2]:
    st.markdown("""
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
""")

# ---------------------------------------------------------------- indicadores
with abas[3]:
    st.markdown("""
| Nível | Indicador | Definição |
|---|---|---|
| 1 | Panorama | Total de patentes únicas, período de atividade e camada dominante (maior participação na contagem por camada). |
| 2 | Composição | Participação de cada camada na carteira, por período. |
| 3 | Convergência | % de patentes em 2 ou mais camadas; **razão** = % da organização ÷ % da base. |
| 4 | Citações por camada | Citações feitas e recebidas por camada. Uma citação **cruza camada** quando a camada da patente citante difere da camada da citada (matriz camada × camada, com contagem integral nas duas pontas). |
| 4.5 | Universidade × empresa | % das citações feitas a patentes de titulares acadêmicos e % das recebidas deles. Autocitações não contam, mesmo quando a patente citada tem um cotitular acadêmico. |
| 5 | Posição na rede | PageRank ponderado na rede de citações entre organizações, por camada e período. **% do topo** = posição ÷ nº de organizações na rede; **elite** = até 1%. |

**Janela das citações.** Os Níveis 4 e 4.5 usam citações entre patentes da base em que as **duas** pontas são de
1995 a 2025, o mesmo recorte dos estudos de caso originais. O Nível 5 usa todas as citações, de 1976 a 2025.

**Titulares acadêmicos.** Identificados por palavras-chave no nome: universidade, college, instituto, regents,
research foundation, trustees, academia, polytechnic, além de CEA, Fraunhofer, Max Planck, CNRS, KAIST e ETRI.
A lista foi revisada manualmente (por exemplo, o SAS Institute, empresa de software, foi excluído).

**Rede do PageRank.** Cada citação liga a organização citante à citada. A camada é a da patente citante; o
período, o ano da patente citante. Participam as organizações dentro do corte de 80% das citações feitas em cada
camada (seleção do estudo original, traduzida para os grupos consolidados).

**Em construção:** Redes de patente (5.5: autocitação e pureza de comunidade), Patentes de virada (6.5) e
Influência estrutural (fragmentação da rede ao remover a organização).
""")

# ---------------------------------------------------------------- validação
with abas[4]:
    st.markdown("""
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

**Demais níveis**

| Nível | Resultado da validação |
|---|---|
| 2 e 3 | Idênticos: convergência da base 8,40%; Intel 11,89% (estudo: 11,86%), Chips 37,6% (37,7%). |
| 4 | Volume interno idêntico. O cruzamento fica 6–10 p.p. acima do estudo por usar a matriz camada × camada, mas a **ordem entre as empresas é preservada** (correlação de postos: 1,0 nas feitas e 0,93 nas recebidas). |
| 4.5 | Parceiros acadêmicos coincidem (Intel: ITRI 291 × 284; CEA 200 × 197; MIT 181 × 174). Os percentuais diferem porque a lista de instituições é própria. |
| 5 | Intel em 2020-25: #2, #3, #5, #8 e #12 nas cinco camadas (estudo: #2, #3, #6, #7 e #14). |
""")

# ---------------------------------------------------------------- limitações
with abas[5]:
    st.markdown("""
- **Citações restritas à base.** Só entram citações entre patentes da base. Citações a patentes fora da cadeia de
  valor da IA ou a literatura não patentária ficam de fora.
- **Cruzamento entre camadas observado de forma parcial.** O arquivo de citações por camada dos estudos originais
  continha apenas citações internas a cada camada; aqui se usa a tabela completa, e o cruzamento depende da regra
  de contagem adotada (ver Indicadores).
- **Classificação acadêmica por palavras-chave.** Pode deixar de fora instituições com nomes atípicos ou incluir
  entidades ambíguas. Os percentuais do Nível 4.5 não são diretamente comparáveis aos dos estudos de caso.
- **Desambiguação herdada.** A qualidade dos nomes depende da desambiguação do PatentsView, que tem falhas
  pontuais (como o rótulo "Samsung Display").
- **Aquisições não consolidadas.** As trajetórias refletem a entidade que depositou a patente, e não o grupo
  econômico atual.
- **Último período.** 2020-25 inclui patentes concedidas até 2025; o atraso entre depósito e concessão faz com
  que os anos mais recentes estejam sub-representados.
""")