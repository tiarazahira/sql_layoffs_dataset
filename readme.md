
# 📊 Tech‑Layoffs Data Warehouse

> **A miniature star‑schema data mart for exploring global tech‑industry layoffs, built with plain SQL.**  
> Load the public **`layoffs.csv`** dataset → drill, slice & dice layoff trends by date 🗓️, company 🏢, and location 🌎 in your favourite BI tool.

---

## 🚀 Why this repo?

1. **Hands‑on dimensional modelling**  
   All tables follow the *star‑schema* playbook from Kimball & the “08 Logical Design” module:
   - One **fact** table (`fact_layoffs`)
   - Three **conformed dimensions** (`dim_date`, `dim_company`, `dim_location`)
2. **Pure SQL, zero dependencies**  
   Copy‑paste into MySQL **or** PostgreSQL, run `LOAD DATA`/`COPY`, and you’re ready to query.
3. **Crystal‑clear DDL**  
   👉 Surrogate PKs, well‑named FKs, sensible referential policies, plus helper indexes.

---

## 🏗️ Schema at a glance

```
                     ┌───────────────┐
                     │  dim_date     │
                     │  date_key PK  │
                     └──────┬────────┘
                            │
┌─────────────┐      ┌──────▼─────────┐      ┌──────────────┐
│ dim_company │      │  fact_layoffs  │      │ dim_location │
│ company_key │◄─────┤ layoff_key PK  ├─────►│ location_key │
└─────────────┘      │ date_key  FK   │      └──────────────┘
                     │ company_key FK │
                     │ location_keyFK │
                     │ total_laid_off │
                     │ perc_laid_off  │
                     └───────────────┘
```

*Granularity: **1 layoff event per company • per date • per location**.*

---

## 🗄️ Quick‑look DDL

```sql
CREATE TABLE fact_layoffs (
  layoff_key     BIGINT PRIMARY KEY,
  date_key       INT  NOT NULL,
  company_key    INT  NOT NULL,
  location_key   INT  NOT NULL,
  total_laid_off INT,
  perc_laid_off  DECIMAL(5,2),
  CONSTRAINT fk_fact_date
    FOREIGN KEY (date_key)
      REFERENCES dim_date(date_key)
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_fact_company
    FOREIGN KEY (company_key)
      REFERENCES dim_company(company_key)
      ON UPDATE CASCADE ON DELETE NO ACTION,
  CONSTRAINT fk_fact_location
    FOREIGN KEY (location_key)
      REFERENCES dim_location(location_key)
      ON UPDATE CASCADE ON DELETE NO ACTION
);
```

Full script lives in **`schema.sql`**.

---

## ⚡ Getting started

```bash
# 1. Clone
git clone https://github.com/<your‑user>/tech‑layoffs‑dw.git
cd tech‑layoffs‑dw

# 2. Start a local MySQL 8 container (shortcut)
docker compose up -d db

# 3. Create schema
mysql -h127.0.0.1 -uroot -p < schema.sql

# 4. Load dimensions
mysql -h127.0.0.1 -uroot -p < etl/load_dim_date.sql
mysql -h127.0.0.1 -uroot -p < etl/load_dim_company.sql
mysql -h127.0.0.1 -uroot -p < etl/load_dim_location.sql

# 5. Load fact table
mysql -h127.0.0.1 -uroot -p < etl/load_fact_layoffs.sql
```

> **Tip:** PostgreSQL fan? Remove `ENGINE=InnoDB`, swap `TINYINT`→`SMALLINT`, and use `COPY` instead of `LOAD DATA`.

---

## 🔍 Sample OLAP queries

```sql
/* 1. Total layoffs by industry in 2024 */
SELECT c.industry,
       SUM(f.total_laid_off) AS layoffs_2024
FROM   fact_layoffs f
JOIN   dim_date    d ON f.date_key    = d.date_key
JOIN   dim_company c ON f.company_key = c.company_key
WHERE  d.year = 2024
GROUP  BY c.industry
ORDER  BY layoffs_2024 DESC;

/* 2. Monthly trend in SF Bay Area vs Bangalore */
SELECT d.year, d.month_name,
       SUM(CASE WHEN l.city_region='SF Bay Area' THEN f.total_laid_off END) AS sf_layoffs,
       SUM(CASE WHEN l.city_region='Bangalore'   THEN f.total_laid_off END) AS blr_layoffs
FROM   fact_layoffs f
JOIN   dim_date     d ON f.date_key     = d.date_key
JOIN   dim_location l ON f.location_key = l.location_key
GROUP  BY d.year, d.month
ORDER  BY d.year, d.month;
```

---

## 📝 Data source & licence

- **Dataset**: [Layoffs.fyi](https://layoffs.fyi/) public spreadsheet (snapshot Mar 2025).  
- **SQL & ETL**: MIT Licence (see [`LICENSE`](./LICENSE)).  
- Dataset files inherit the original CC‑BY licence.

---

## 🌱 Ideas to extend

| 💡 | Learn |
|----|-------|
| Add **`dim_funding_round`** to relate layoffs to funding events | Slowly changing dimensions |
| Build **dbt** models & snapshots | Modern ELT |
| Connect to **Metabase / Superset** dashboards | BI & storytelling |
| Port to **BigQuery** & enable column partitioning | Cloud warehousing |

PRs welcome — happy querying & may your drill‑downs be fast! 🚀
