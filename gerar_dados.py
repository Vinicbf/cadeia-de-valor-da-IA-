"""
gerar_dados.py — reconstrói todas as tabelas do painel a partir dos arquivos brutos.

Uso (terminal, dentro da pasta painel_ia):   python gerar_dados.py
Lê os arquivos brutos da pasta-mãe (uspto) e grava:
  painel_ia/dados/          -> tabelas lidas pelo Streamlit
  painel_ia/intermediario/  -> base consolidada, citações, rede, dicionários
"""
import json
import re
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

# ------------------------------------------------------------------ configuração
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
DADOS, INTER = AQUI / "dados", AQUI / "intermediario"
for d in (DADOS, INTER):
    d.mkdir(exist_ok=True)

ARQ_BASE = RAIZ / "patentes_join_completo_v2.csv"
ARQ_CIT = RAIZ / "citacoes_recebidas_corpus.csv"
ARQ_SEL = RAIZ / "organizacoes_selecionadas_corte_80pct_citacoes.csv"

CORTE_NUCLEO = 0.50       # núcleo = grupos que somam 50% das patentes
ANO_MIN_CIT = 1995        # janela das citações nos Níveis 4 e 4.5 (1976 = sem janela)

CAM = {"0_infra_fisica": "Infra Física", "1_chips_hardware": "Chips & Hardware",
       "2_cloud_compute": "Cloud & Compute", "3_modelos_ia": "Modelos de IA",
       "4_5_software_aplicacao": "Software & Aplicação"}
PER = ["Até 1999", "2000-04", "2005-09", "2010-14", "2015-19", "2020-25"]
REF = {"Google": 14607, "TSMC": 23180, "IBM": 60387, "Apple": 9750, "Microsoft": 21751,
       "Amazon": 10983, "NVIDIA": 2962, "Meta": 5284, "Samsung": 33296, "Intel": 20000}

SUF = {"inc", "incorporated", "corp", "corporation", "co", "company", "ltd", "limited", "llc", "plc",
       "gmbh", "ag", "sa", "nv", "bv", "kk", "se", "lp", "llp", "srl", "spa", "oy", "ab", "as"}

ACAD = (r"univ|college|institut|regents|research foundation|school|academ|commissariat|fraunhofer|"
        r"max planck|polytechnic|trustees|kaist|national laborator|cnrs|^etri$")
ACAD_EXCLUI = {"sas institute"}

# ------------------------------------------------------------------ consolidação de nomes
# Regra: fundir holdings de PI, subsidiárias da mesma marca e renomeações;
# manter aquisições e empresas independentes de mesma marca separadas.
GRUPOS = {
    "IBM": ["international business machines"],
    "TSMC": ["taiwan semiconductor manufacturing"],
    "Intel": ["intel", "intel ip"],
    "Google": ["google", "google technology holdings"],
    "Microsoft": ["microsoft", "microsoft technology licensing"],
    "Apple": ["apple", "apple computer"],
    "NVIDIA": ["nvidia"],
    "Meta": ["facebook", "facebook technologies", "meta platforms", "meta platforms technologies"],
    "Toshiba": ["kabushiki kaisha toshiba", "tokyo shibaura denki kabushiki kaisha", "tokyo shibaura electric",
                "toshiba tec kabushiki kaisha", "toshiba medical systems", "toshiba electronic devices & storage"],
    "Kioxia": ["toshiba memory", "kioxia"],
    "SK Hynix": ["sk hynix", "hyundai electronics industries"],
    "HP": ["hewlett packard development", "hewlett packard"],
    "HPE": ["hewlett packard enterprise development"],
    "Dell": ["dell products", "dell usa"],
    "EMC": ["emc", "emc ip holding"],
    "Broadcom": ["broadcom", "avago technologies general ip singapore pte",
                 "avago technologies international sales pte"],
    "BlackBerry": ["blackberry", "research in motion"],
    "Baidu": ["beijing baidu netcom science technology", "baidu online network technology beijing", "baidu usa"],
    "Adobe": ["adobe", "adobe systems"],
    "Accenture": ["accenture global solutions", "accenture global services"],
    "Amkor": ["amkor technology", "amkor technology singapore holding pte"],
    "Applied Materials": ["applied materials", "applied materials israel"],
    "ASM International": ["asm ip holding", "asm international", "asm america"],
    "ASML": ["asm lithography"],
    "AT&T": ["at&t intellectual property i", "at&t mobility ii", "at&t", "at&t bell laboratories"],
    "Canon": ["canon kabushiki kaisha", "canon medical systems"],
    "Fujifilm": ["fujifilm", "fujifilm business innovation", "fuji xerox"],
    "Fujitsu": ["fujitsu", "fujitsu semiconductor"],
    "GlobalFoundries": ["globalfoundries", "globalfoundries singapore pte", "globalfoundries us"],
    "General Motors": ["gm global technology operations", "general motors", "gm cruise holdings"],
    "Hon Hai": ["hon hai precision industry", "hon hai precision ind"],
    "Honeywell": ["honeywell international", "honeywell"],
    "Huawei": ["huawei technologies", "huawei digital power technologies"],
    "Infineon": ["infineon technologies", "infineon technologies austria"],
    "KLA": ["kla tencor", "kla", "kla tencor technologies"],
    "Philips": ["koninklijke philips", "koninklijke philips electronics", "us philips"],
    "Kyocera": ["kyocera", "kyocera document solutions"],
    "Lenovo": ["lenovo singapore pte", "lenovo beijing", "lenovo enterprise solutions singapore pte"],
    "LSI": ["lsi logic", "lsi"],
    "Mitsubishi Electric": ["mitsubishi electric", "mitsubishi electric research laboratories"],
    "Motorola": ["motorola", "motorola solutions"],
    "NEC": ["nec", "nec electronics"],
    "NXP": ["nxp", "nxp usa"],
    "Oki": ["oki electric industry", "oki semiconductor"],
    "Red Hat": ["red hat", "red hat israel"],
    "Renesas": ["renesas electronics", "renesas technology"],
    "SanDisk": ["sandisk technologies", "sandisk", "sandisk 3d"],
    "Sharp": ["sharp kabushiki kaisha", "sharp laboratories of america"],
    "Shin-Etsu": ["shin etsu chemical", "shin etsu handotai"],
    "SMIC": ["semiconductor manufacturing international shanghai",
             "semiconductor manufacturing international beijing"],
    "STATS ChipPAC": ["stats chippac", "stats chippac pte"],
    "STMicroelectronics": ["stmicroelectronics", "stmicroelectronics rousset sas", "stmicroelectronics crolles 2 sas"],
    "Tencent": ["tencent technology shenzhen", "tencent america"],
    "Toyota": ["toyota jidosha kabushiki kaisha", "toyota motor engineering & manufacturing north america",
               "toyota research institute"],
    "Kia": ["kia motors", "kia"],
    "Salesforce": ["salesforcecom", "salesforce"],
    "Snap": ["snap", "snapchat"],
    "LG Electronics": ["lg electronics", "goldstar"],
    "Denso": ["denso", "nippondenso", "nippon denso"],
}
# famílias inteiras por prefixo (nome == prefixo ou começa com "prefixo ")
PREFIXOS = {
    "Samsung": ["samsung"], "Hitachi": ["hitachi"], "Sony": ["sony"], "Siemens": ["siemens"],
    "Panasonic": ["panasonic", "matsushita"], "Amazon": ["amazon"], "Oracle": ["oracle"],
    "Nokia": ["nokia"], "Verizon": ["verizon"], "Capital One": ["capital one"], "SAP": ["sap"],
    "ASML": ["asml"], "Ford": ["ford"], "SK Hynix": ["hynix"],
}
# nomes de exibição para organizações do núcleo sem grupo
NOMES = {"micron technology": "Micron", "texas instruments": "Texas Instruments", "qualcomm": "Qualcomm",
         "tokyo electron": "Tokyo Electron", "advanced micro devices": "AMD", "general electric": "GE",
         "cisco technology": "Cisco", "sumitomo electric industries": "Sumitomo Electric",
         "winbond electronics": "Winbond", "semiconductor energy laboratory": "Semiconductor Energy Lab",
         "vmware": "VMware", "ricoh": "Ricoh", "seiko epson": "Seiko Epson", "nikon": "Nikon", "xerox": "Xerox",
         "telefonaktiebolaget lm ericsson publ": "Ericsson", "bank of america": "Bank of America",
         "robert bosch": "Bosch", "honda motor": "Honda", "boe technology group": "BOE",
         "electronics and telecommunications research institute": "ETRI", "boeing": "Boeing",
         "lam research": "Lam Research"}


def norm(s):
    t = re.sub(r"[^\w&]+", " ", str(s).lower().replace(".", "")).split()
    if t and t[0] == "the":
        t = t[1:]
    while t and t[-1] in SUF:
        t.pop()
    return " ".join(t)


def montar_dicionario(normalizados):
    dic = {}
    for g, ns in GRUPOS.items():
        for n in ns:
            dic[n] = g
    for g, ps in PREFIXOS.items():
        for n in normalizados:
            if any(n == p or n.startswith(p + " ") for p in ps):
                dic[n] = g
    return dic


def curva(base):
    po = base.drop_duplicates(["patent_id", "org"])[["patent_id", "org"]].copy()
    ordem = po.org.value_counts()
    po["rk"] = po.org.map(pd.Series(np.arange(1, len(ordem) + 1), index=ordem.index))
    m = po.groupby("patent_id").rk.min()
    cob = (m.value_counts().sort_index().cumsum() / len(m)).reindex(range(1, len(ordem) + 1)).ffill()
    return ordem, cob


# ------------------------------------------------------------------ 1. base e consolidação
print("1/7 base de patentes e consolidação de nomes")
df = pd.read_csv(ARQ_BASE, usecols=["patent_id", "camada", "disambig_assignee_organization", "ano"])
df = df.rename(columns={"disambig_assignee_organization": "org_bruto"}).dropna(subset=["org_bruto"])
brutos = df.org_bruto.unique()
norm_map = {b: norm(b) for b in brutos}
dic = montar_dicionario(set(norm_map.values()))
fin_map = {b: NOMES.get(dic.get(n, n), dic.get(n, n)) for b, n in norm_map.items()}
df["org"] = df.org_bruto.map(fin_map)

pc = df.drop_duplicates(["patent_id", "org", "camada"])[["patent_id", "org", "camada", "ano"]].copy()
pc["camada"] = pd.Categorical(pc.camada.map(CAM), categories=list(CAM.values()), ordered=True)
pc["periodo"] = pd.cut(pc.ano, [0, 1999, 2004, 2009, 2014, 2019, 2100], labels=PER)
pc.to_csv(INTER / "base_consolidada.csv", index=False)
json.dump({"grupos": GRUPOS, "prefixos": PREFIXOS, "nomes": NOMES}, open(INTER / "dicionario.json", "w",
          encoding="utf-8"), ensure_ascii=False, indent=1)
del df

tot = pc.drop_duplicates(["patent_id", "org"]).groupby("org").size()
val = pd.DataFrame({"painel": tot.reindex(list(REF)), "dossie": pd.Series(REF)})
val["dif%"] = (val.painel / val.dossie - 1) * 100
print(val.round(2).to_string())

ordem, cob = curva(pc)
k50 = int((cob >= CORTE_NUCLEO).idxmax())
nucleo = list(ordem.index[:k50])
print(f"núcleo: {k50} grupos | 80%: {int((cob >= .8).idxmax())} grupos")
sem_nome = [o for o in nucleo if o == o.lower()]
if sem_nome:
    print("ATENÇÃO — núcleo com nome sem formatação (acrescente em NOMES):", sem_nome)

# ------------------------------------------------------------------ 2. Níveis 1 a 3
print("2/7 composição e convergência")
pl = pc.drop_duplicates(["patent_id", "camada"])[["patent_id", "camada", "periodo"]]
ncam = pl.groupby("patent_id").size()
combo = pl.sort_values("camada").groupby("patent_id").camada.agg(lambda s: " + ".join(map(str, s)))
base_conv = (ncam > 1).mean() * 100

N = pc[pc.org.isin(nucleo)]
up = N.drop_duplicates(["patent_id", "org"]).copy()
up["ncam"] = up.patent_id.map(ncam)
up["combo"] = up.patent_id.map(combo)

BT = pl.assign(org="Base total")
comp = pd.concat([N, BT]).groupby(["org", "periodo", "camada"], observed=True).size().rename("n").reset_index()
comp["pct"] = comp.n / comp.groupby(["org", "periodo"], observed=True).n.transform("sum") * 100
cl = pd.concat([N, BT]).groupby(["org", "camada"], observed=True).size().rename("n").reset_index()
cl["pct"] = cl.n / cl.groupby("org").n.transform("sum") * 100
dom = cl.loc[cl.groupby("org").n.idxmax()].set_index("org")

g = up.groupby("org")
emp = pd.DataFrame({"total": g.size(), "ano_ini": g.ano.min(), "ano_fim": g.ano.max(),
                    "conv_pct": g.ncam.agg(lambda s: (s > 1).mean() * 100)})
emp["conv_razao"] = emp.conv_pct / base_conv
emp["camada_dom"] = dom.camada
emp["pct_dom"] = dom.pct
emp["tipo"] = np.where(emp.index.str.contains(ACAD, case=False, regex=True), "Instituto", "Empresa")
emp = emp.sort_values("total", ascending=False)
emp["rank"] = range(1, len(emp) + 1)

conv = (pd.concat([up, pd.DataFrame({"org": "Base total", "ncam": ncam})])
        .groupby(["org", "ncam"]).size().rename("n").reset_index())
conv["pct"] = conv.n / conv.groupby("org").n.transform("sum") * 100
comb = (up[up.ncam > 1].groupby(["org", "combo"]).size().rename("n").reset_index()
        .sort_values(["org", "n"], ascending=[True, False]).groupby("org").head(10))

emp.rename_axis("org").reset_index().to_csv(DADOS / "empresas.csv", index=False)
comp.to_csv(DADOS / "composicao.csv", index=False)
cl.to_csv(DADOS / "camadas.csv", index=False)
conv.to_csv(DADOS / "convergencia.csv", index=False)
comb.to_csv(DADOS / "combos.csv", index=False)

# ------------------------------------------------------------------ 3. citações
print("3/7 citações (arquivo grande, pode demorar)")
ib = pl.patent_id.unique()
D = pd.read_csv(ARQ_CIT, usecols=["patent_id", "citation_patent_id"], dtype=str)
D.columns = ["citante", "citada"]
for c in D.columns:
    D[c] = pd.to_numeric(D[c], errors="coerce")
D = D.dropna().astype("int64")
D = D[D.citante.isin(ib) & D.citada.isin(ib)].drop_duplicates()
D.to_csv(INTER / "citacoes_base.csv", index=False)
anos = pc.drop_duplicates("patent_id").set_index("patent_id").ano
D95 = D[(D.citante.map(anos) >= ANO_MIN_CIT) & (D.citada.map(anos) >= ANO_MIN_CIT)]
print(f"   citações na base: {len(D):,} | janela {ANO_MIN_CIT}+: {len(D95):,}")

# ------------------------------------------------------------------ 4. Nível 4 (matriz camada x camada)
print("4/7 Nível 4 — citações por camada")
L = pl[["patent_id", "camada"]].assign(camada=lambda x: x.camada.astype(str))
P = (D95.merge(L.rename(columns={"patent_id": "citante", "camada": "cam_ct"}), on="citante")
        .merge(L.rename(columns={"patent_id": "citada", "camada": "cam_cd"}), on="citada"))
P["cruza"] = P.cam_ct != P.cam_cd
PO = up[["patent_id", "org"]]


def resumo(X, nome):
    a = X.groupby(["org", "camada"]).cruza.agg(["size", "mean"])
    b = X.groupby("org").cruza.agg(["size", "mean"]).assign(camada="Total").set_index("camada", append=True)
    t = pd.concat([a, b])
    t.columns = [nome, f"cruz_{nome}_pct"]
    t[f"cruz_{nome}_pct"] *= 100
    return t


Pf, Pr = P.rename(columns={"cam_ct": "camada"}), P.rename(columns={"cam_cd": "camada"})
FO = pd.concat([Pf.merge(PO, left_on="citante", right_on="patent_id"), Pf.assign(org="Base total")])
RO = pd.concat([Pr.merge(PO, left_on="citada", right_on="patent_id"), Pr.assign(org="Base total")])
cit = resumo(FO, "feitas").join(resumo(RO, "recebidas"), how="outer").fillna(0).reset_index()
cit.to_csv(DADOS / "citacoes.csv", index=False)
mat = (P.merge(PO, left_on="citante", right_on="patent_id")
        .groupby(["org", "cam_ct", "cam_cd"]).size().rename("n").reset_index())
mat.to_csv(DADOS / "fluxo_camadas.csv", index=False)
del P, Pf, Pr, FO, RO

# ------------------------------------------------------------------ 5. Nível 4.5 (academia)
print("5/7 Nível 4.5 — universidade x empresa")
PA = pc[["patent_id", "org"]].drop_duplicates()
PA = PA[PA.org.str.contains(ACAD, case=False, regex=True) & ~PA.org.isin(ACAD_EXCLUI)]
ids_acad = set(PA.patent_id)
per = pc.drop_duplicates("patent_id").set_index("patent_id").periodo


def acad(ponta, outra, nome):
    X = D95.merge(PO, left_on=ponta, right_on="patent_id")
    X["periodo"] = X[ponta].map(per)
    proprio = X.merge(PO.rename(columns={"patent_id": outra}), on=[outra, "org"],
                      how="left", indicator=True)["_merge"].eq("both").values
    X["acad"] = X[outra].isin(ids_acad).values & ~proprio
    tot_ = X.groupby("org").acad.mean().mul(100).rename(f"pct_{nome}").reset_index().assign(periodo="Total")
    porp = X.groupby(["org", "periodo"], observed=True).acad.mean().mul(100).rename(f"pct_{nome}").reset_index()
    parc_ = (X[X.acad].merge(PA.rename(columns={"patent_id": outra, "org": "parceiro"}), on=outra)
             .groupby(["org", "parceiro"]).size().rename(nome))
    return pd.concat([tot_, porp]), parc_


uf, pf = acad("citante", "citada", "feitas")
ur, pr = acad("citada", "citante", "recebidas")
univ = uf.merge(ur, on=["org", "periodo"], how="outer")
parc = pd.concat([pf, pr], axis=1).fillna(0).astype(int)
parc["total"] = parc.feitas + parc.recebidas
parc = parc.reset_index().sort_values(["org", "total"], ascending=[True, False]).groupby("org").head(15)
univ.to_csv(DADOS / "universidades.csv", index=False)
parc.to_csv(DADOS / "parceiros_academicos.csv", index=False)

# ------------------------------------------------------------------ 6. Nível 5 (PageRank)
print("6/7 Nível 5 — PageRank por camada e período")
sel = pd.read_csv(ARQ_SEL)
sel = sel[sel.dentro_do_corte_80pct_citacoes]
sel["grupo"] = sel.disambig_assignee_organization.map(
    lambda r: fin_map.get(r) or NOMES.get(dic.get(norm(r), norm(r)), dic.get(norm(r), norm(r))))
sel["cam"] = sel.camada.map(CAM).fillna(sel.camada)
chaves = set(zip(sel.cam, sel.grupo))
glob_sel = set(sel.grupo)

U = pc[pc.org.isin(glob_sel)]
uids = U.patent_id.unique()
Da = D[D.citante.isin(uids) & D.citada.isin(uids)]
ct = U[["patent_id", "org", "camada"]].astype({"camada": str}).rename(
    columns={"patent_id": "citante", "org": "org_ct"})
cd = U[["patent_id", "org"]].drop_duplicates().rename(columns={"patent_id": "citada", "org": "org_cd"})
E = Da.merge(ct, on="citante").merge(cd, on="citada")
E = E[[k in chaves for k in zip(E.camada, E.org_ct)]]
E["periodo"] = E.citante.map(per).astype(str)
A = E.groupby(["camada", "periodo", "org_ct", "org_cd"]).size().rename("n").reset_index()
A.to_csv(INTER / "rede_orgs_camada_periodo.csv", index=False)

linhas = []
for (cam, p), grp in A.groupby(["camada", "periodo"]):
    G = nx.from_pandas_edgelist(grp, "org_ct", "org_cd", "n", create_using=nx.DiGraph)
    s = pd.Series(nx.pagerank(G, weight="n")).sort_values(ascending=False)
    linhas.append(pd.DataFrame({"org": s.index, "pagerank": s.values, "rank": range(1, len(s) + 1),
                                "pool": len(s), "camada": cam, "periodo": p}))
prk = pd.concat(linhas)
prk["pct_topo"] = prk["rank"] / prk.pool * 100
prk.to_csv(DADOS / "pagerank.csv", index=False)

# ------------------------------------------------------------------ 6b. Extra (fragmentação) e autocitação
print("6b/7 Extra — fragmentação ao remover cada organização; autocitação")
# Regra do script 22: rede NÃO direcionada entre organizações, citações internas à camada
# (as duas patentes na camada, as duas de ANO_MIN_CIT em diante), sem autocitação, todas as organizações.
Lc = pl[["patent_id", "camada"]].assign(camada=lambda x: x.camada.astype(str))
Pc = pc[["patent_id", "org"]].drop_duplicates()
frag = []
for cam in CAM.values():
    ids = set(Lc.patent_id[Lc.camada == cam])
    E2 = D95[D95.citante.isin(ids) & D95.citada.isin(ids)]
    E2 = (E2.merge(Pc.rename(columns={"patent_id": "citante", "org": "a"}), on="citante")
            .merge(Pc.rename(columns={"patent_id": "citada", "org": "b"}), on="citada"))
    E2 = E2.loc[E2.a != E2.b, ["a", "b"]].drop_duplicates()
    G = nx.from_pandas_edgelist(E2, "a", "b")
    comp_base = nx.number_connected_components(G)
    nos = set(G)
    for org in nucleo:
        if org not in G:
            continue
        isoladas = sum(1 for v in G[org] if G.degree(v) == 1)    # vizinhos cuja única ligação era a empresa
        comp = nx.number_connected_components(G.subgraph(nos - {org}))
        frag.append({"org": org, "camada": cam, "delta_componentes": comp - comp_base,
                     "isoladas": isoladas, "nos_rede": len(nos)})
    print(f"   {cam}: {len(nos):,} organizações, {G.number_of_edges():,} ligações")
frag = pd.DataFrame(frag)
frag.to_csv(DADOS / "fragmentacao.csv", index=False)


def auto(ponta, outra, nome):
    X = D95.merge(PO, left_on=ponta, right_on="patent_id")
    X["auto"] = X.merge(PO.rename(columns={"patent_id": outra}), on=[outra, "org"],
                        how="left", indicator=True)["_merge"].eq("both").values
    g = X.groupby("org").auto
    return pd.concat([g.mean().mul(100).rename(f"auto_{nome}_pct"),
                      g.size().rename(f"cit_{nome}")], axis=1)          # citações únicas (sem expandir por camada)


autoc = pd.concat([auto("citante", "citada", "feitas"), auto("citada", "citante", "recebidas")], axis=1)
autoc.rename_axis("org").reset_index().to_csv(DADOS / "autocitacao.csv", index=False)

# ------------------------------------------------------------------ 7. resumo e validação
print("7/7 resumo")
cv = pd.DataFrame({"k": cob.index, "cobertura": cob.values * 100})
cv[cv.k <= 20000].to_csv(DADOS / "curva_concentracao.csv", index=False)
json.dump({"patentes": int(pl.patent_id.nunique()), "organizacoes": int(len(ordem)), "nucleo": k50,
           "n80": int((cob >= .8).idxmax()), "conv_base": round(base_conv, 2)},
          open(DADOS / "resumo.json", "w"))

print("\n=== validação (Intel) ===")
print(f"convergência base {base_conv:.2f}% (esperado 8,40) | Intel {emp.loc['Intel', 'conv_pct']:.2f}% (11,86)")
print(prk.query("org == 'Intel' and periodo == '2020-25'")[["camada", "rank", "pool"]].to_string(index=False))

print("\n=== fragmentação em Modelos de IA — dossiês: IBM +139/131, Amazon +76/74, Google +50/46, "
      "Samsung +46/43, Microsoft +41/40, Meta +16/16, Intel +11/11, NVIDIA +9/9, Apple +8/7, TSMC +1/1 ===")
print(frag[(frag.camada == "Modelos de IA") & frag.org.isin(list(REF))].set_index("org")
      [["delta_componentes", "isoladas"]].sort_values("delta_componentes", ascending=False).to_string())
print("\n=== autocitação (% das recebidas que vêm da própria organização) ===")
print(autoc.reindex(list(REF)).round(1).sort_values("auto_recebidas_pct", ascending=False).to_string())
print("\nPronto. Rode: streamlit run app.py")
