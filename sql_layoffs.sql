/* ───────────  DIMENSION TABLES  ─────────── */

CREATE TABLE dim_date (
  date_key         INT PRIMARY KEY,          -- surrogate YYYYMMDD
  full_date        DATE        NOT NULL,
  day              TINYINT,
  month            TINYINT,
  month_name       VARCHAR(15),
  quarter          TINYINT,
  year             SMALLINT,
  is_weekend       BOOLEAN
) ENGINE=InnoDB;

CREATE TABLE dim_company (
  company_key      INT PRIMARY KEY,
  company_name     VARCHAR(120) NOT NULL,
  industry         VARCHAR(60),
  funding_stage    VARCHAR(40),
  funds_raised_usd DECIMAL(15,2)
) ENGINE=InnoDB;

CREATE TABLE dim_location (
  location_key     INT PRIMARY KEY,
  city_region      VARCHAR(120),
  country          VARCHAR(60)
) ENGINE=InnoDB;

/* ───────────  FACT TABLE  ─────────── */

CREATE TABLE fact_layoffs (
  layoff_key        BIGINT PRIMARY KEY,
  date_key          INT  NOT NULL,
  company_key       INT  NOT NULL,
  location_key      INT  NOT NULL,
  total_laid_off    INT,
  perc_laid_off     DECIMAL(5,2),

  /* ────  EXPLICIT FOREIGN-KEY CONSTRAINTS  ──── */
  CONSTRAINT fk_fact_date
    FOREIGN KEY (date_key)
      REFERENCES dim_date (date_key)
      ON UPDATE CASCADE
      ON DELETE NO ACTION,

  CONSTRAINT fk_fact_company
    FOREIGN KEY (company_key)
      REFERENCES dim_company (company_key)
      ON UPDATE CASCADE
      ON DELETE NO ACTION,

  CONSTRAINT fk_fact_location
    FOREIGN KEY (location_key)
      REFERENCES dim_location (location_key)
      ON UPDATE CASCADE
      ON DELETE NO ACTION
) ENGINE=InnoDB;

/* ───────────  OPTIONAL PERFORMANCE INDEXES  ───────────
   (membantu join & agregasi umum di DW)                  */

CREATE INDEX idx_fact_date       ON fact_layoffs (date_key);
CREATE INDEX idx_fact_company    ON fact_layoffs (company_key);
CREATE INDEX idx_fact_location   ON fact_layoffs (location_key);
