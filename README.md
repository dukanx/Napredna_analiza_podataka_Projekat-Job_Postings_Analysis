# Analiza Dinamike IT Tržišta Rada

LLM ekstrakcija i mrežna analiza tehnologija na osnovu LinkedIn oglasa za posao.

| | |
|---|---|
| **Kurs** | Napredna Analiza Podataka |
| **Autor** | Nikola Dukić |
| **Dataset** | LinkedIn Job Postings 2023/2024 (Kaggle) |
| **Obim** | 1.460 IT pozicija |

---

## Sadržaj

- [Cilj projekta](#cilj-projekta)
- [Istraživačka pitanja](#istraživačka-pitanja)
- [Metodologija](#metodologija)
- [Rezultati](#rezultati)
- [Ograničenja](#ograničenja)
- [Tech stack](#tech-stack)
- [Pokretanje](#pokretanje)

---

## Cilj projekta

Analiza IT tržišta rada kroz tri komplementarna pristupa:

1. **LLM Ekstrakcija** — automatsko izvlačenje implicitnih karakteristika oglasa (tehnologije, ton, benefiti)
2. **Mrežna Analiza** — mapiranje ekosistema tehnologija kroz co-occurrence grafove
3. **Korelaciona Analiza** — ispitivanje veze između širine znanja i plate, i uticaja tona oglasa na angažovanje kandidata

---

## Istraživačka pitanja

1. **Tehnološki ekosistem** — Kako su tehnologije međusobno povezane? Koji su dominantni klasteri?
2. **Plata vs. veštine** — Da li šira raznolikost tehnologija donosi višu platu?
3. **Ton oglasa** — Da li red/green flags utiču na broj aplikacija?

---

## Metodologija

### LLM ekstrakcija

Llama 3.3 70B (Groq API) korišćen za ekstrakciju strukturisanih podataka iz slobodnog teksta oglasa:

- prepoznavanje tehnologija i alata
- klasifikacija tona (red/green flags)
- ekstrakcija benefita

### Mrežna analiza

Na osnovu ekstraktovanih tehnologija izgrađen je co-occurrence graf:

- čvor = tehnologija
- grana = zajedničko pojavljivanje u istom oglasu
- **Louvain Community Detection** za otkrivanje klastera
- metrike centralnosti za identifikaciju ključnih tehnologija

### Korelaciona analiza

- Pearsonova korelacija između broja tehnoloških oblasti i plate
- korelacija između tone score-a i conversion rate-a (broj aplikacija / pregledi)
- poređenje tehničkih i netehničkih pozicija kao kontrolna varijabla

---

## Rezultati

### 1. Tehnološki ekosistem

- identifikovano **7 jasnih tehnoloških klastera**
- **Python** i **AWS** su centralne tehnologije — pojavljuju se unutar svih klastera
- Modularity score: **0.28** — validna podela uz očekivana preklapanja (full-stack pozicije)

### 2. Plata i širina znanja

| Skup podataka | Pearsonov r | Interpretacija |
|---|---|---|
| Sve pozicije | 0.13 | slaba pozitivna korelacija |
| Samo tehničke pozicije | -0.08 | zanemarljivo |

**Ključni nalaz — "Cluster 0 efekat":**

Prividna pozitivna korelacija potiče isključivo iz razlike između netehničkih pozicija (0 klastera, niža plata) i tehničkih pozicija (1+ klastera, viša plata). Unutar tehničkih pozicija, širina znanja nema značajan uticaj na platu.

> Tržište ne nagrađuje generaliste. Specijalizacija i seniority su važniji faktori od breadth-a znanja.

### 3. Ton oglasa i angažovanje kandidata

| Faktor | Korelacija s conversion rate-om | Interpretacija |
|---|---|---|
| Red flags | -0.09 | zanemarljiva negativna |
| Green flags | -0.07 | zanemarljivo (suprotno očekivanju) |
| Vibe score | 0.00 | nema uticaja |

**Ključni nalaz:**

Kandidati ignorišu retoriku oglasa. Odluke o apliciranju se donose na osnovu strukturnih faktora — naziv pozicije, kompanija, plata, lokacija — a ne na osnovu tona ili benefits marketinga.

### Praktične implikacije

**Za kandidate:**
- fokus na specijalizaciju unutar jedne oblasti umesto "svaštarenja"
- Python i AWS su "passport" tehnologije — otvaraju vrata u svim oblastima
- marketing speak u oglasima nije signal kvaliteta kompanije

**Za poslodavce:**
- ton oglasa ne utiče na broj aplikacija — fokus na jasnoću pozicije i benefita
- transparentnost oko plate je ključna

---

## Ograničenja

- **LLM ekstrakcija** — Llama 3.3 70B nije perfektan; detekcija tona je subjektivna i sklona greškama bez fine-tuninga
- **Dataset** — samo LinkedIn oglasi (nedostaju startup oglasi, direktne aplikacije, domaći oglasi)
- **Conversion rate** — broj aplikacija nije idealna mera angažovanja; nedostaju podaci o daljim fazama selekcije

---

## Tech stack

| Kategorija | Tehnologije |
|---|---|
| LLM | Llama 3.3 70B Versatile (Groq API) |
| Mrežna analiza | NetworkX, python-louvain |
| Analiza podataka | Pandas, SciPy |
| Vizualizacija | Seaborn, Matplotlib |
| Dataset | [LinkedIn Job Postings 2023–2024 (Kaggle)](https://www.kaggle.com/) |

---

## Pokretanje

### Preduslovi

```bash
pip install pandas scipy seaborn networkx python-louvain groq
```

### Konfiguracija

U notebook-u postaviti svoj Groq API key:

```python
GROQ_API_KEY = "your_api_key_here"
```

### Analiza

Otvoriti i pokrenuti `ProjekatNAP.ipynb` u celini. Ćelije su organizovane redom: ekstrakcija → mrežna analiza → korelaciona analiza.

> LLM ekstrakcija nad celim datasetom može trajati duže — preporučuje se pokretanje nad podskupom za testiranje.

