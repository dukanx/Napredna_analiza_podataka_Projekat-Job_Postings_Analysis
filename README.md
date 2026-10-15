<img src="assets/analiza-it-trzista-rounded-512.png" width="88" alt="Analiza IT tržišta">

# Analiza IT tržišta rada primenom velikih jezičkih modela i mrežnih metoda

Kod uz završni rad na Fakultetu organizacionih nauka u Beogradu (mentor prof. dr Jelena Jovanović). Rad je nastao iz projekta za predmet Napredna analiza podataka.

[English version](README_en.md)

Pitanje: kandidat zna nekoliko tehnologija, šta vredi da uči sledeće? Odgovor se traži u oglasima za posao. Iz slobodnog teksta oglasa veliki jezički model izdvaja tražene tehnologije. Nad njima se gradi mreža tehnologija koje se traže zajedno, a na kraju se porede modeli koji kandidatu predlažu sledeću tehnologiju.

## Podaci

Skup [LinkedIn Job Postings (2023 - 2024)](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) sa Kaggle-a, licenca CC BY-SA 4.0. Ima 123.849 oglasa, gotovo svi iz aprila 2024. godine, za tržište SAD.

| Korak | Oglasa |
|---|---:|
| Svi oglasi | 123.849 |
| Posle filtera po LinkedIn oznaci i nazivu pozicije | 15.306 |
| Posle uklanjanja identičnih kopija | 14.156 |
| Posle odluke jezičkog modela da je oglas IT posao | 11.713 |

## Rezultati ukratko

- Jezički model je `gpt-oss-20b` preko servisa Groq, sa odgovorom u zadatoj šemi (Pydantic, structured output). Obrada svih oglasa koštala je 3,01 $.
- Ručna provera filtera na 50 nasumičnih oglasa: preciznost 0,902, odziv 1,000.
- Mreža ima 189 tehnologija i 1.260 veza, a težina veze je lift. Louvain je dao 14 klastera, uz modularnost 0,640. Podela je izabrana kao tipičan ishod 100 pokretanja.
- Habovi (Python, AWS, Java, SQL) povezani su sa gotovo svim oblastima. Mostovi sa malo veza (Cisco, Active Directory, DB2) povezuju po jednu usku oblast sa ostatkom mreže.
- Preporuka je proverena tako što se iz oglasa sakrije jedna tehnologija i gleda da li je model vraća među deset predloga. Skup je podeljen po firmama, pa nijedna firma nije i u učenju i u proveri.

| Model | recall@10 | Pokrivenost spiska |
|---|---:|---:|
| popularnost | 0,348 | 7,3 % |
| Apriori | 0,565 | 33,1 % |
| sličnost po lift-u | 0,355 | 99,3 % |
| hibridni model | 0,600 | 97,6 % |

![Podmreža od 50 najčešćih tehnologija](figures/mreza_top50.png)

## Sveske

| Sveska | Sadržaj |
|---|---|
| [01_ekstrakcija.ipynb](01_ekstrakcija.ipynb) | filtriranje IT oglasa, izbor modela, izdvajanje tehnologija, uticaj dužine opisa, ručna provera filtera |
| [02_analiza.ipynb](02_analiza.ipynb) | kanonizacija naziva, mreža tehnologija, centralnost, habovi i mostovi, klasteri |
| [03_preporuka.ipynb](03_preporuka.ipynb) | popularnost, Apriori, sličnost po lift-u, hibridni model, provera na pet podela po firmama |
| [04_plate.ipynb](04_plate.ipynb) | dodatna analiza plata po tehnologijama, nije deo završnog rada |

Sveske se pokreću redom, jer svaka čita ono što je prethodna upisala u `data/interim/`.

## Ostali folderi

- `figures/`: sve slike iz svezaka.
- `validacija/`: uzorak od 50 oglasa sa ručnom ocenom i uputstvo po kom je ocenjivan.
- `data/interim/`: sačuvani odgovori jezičkog modela (`ekstrakcija_*.jsonl`), pa sveske ne moraju ponovo da pozivaju model.
- `arhiva/`: prva verzija projekta za predmet Napredna analiza podataka, sa modelom `llama-3.3-70b` i uzorkom od 1.460 oglasa.

## Pokretanje

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

CSV fajlove sa Kaggle-a treba staviti direktno u `data/raw/`, bez podfoldera. Sveske koriste `postings.csv`, `job_skills.csv`, `salaries.csv` i `companies.csv`.

Odgovori modela su već u `data/interim/`, pa sveska 01 ne šalje nove zahteve i pravi Groq ključ nije potreban. Ključ u `.env` treba upisati samo za obradu oglasa koji nisu u kešu.
