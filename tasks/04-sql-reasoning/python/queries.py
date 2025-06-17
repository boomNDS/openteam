# tasks/04‑sql‑reasoning/python/queries.py
from pathlib import Path

# --- path to donations.db --------------------------------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "donations.db"

# --- Task A ---------------------------------------------------------------
SQL_A = """
SELECT
	p.campaign_id,
	SUM(p.amount_thb) AS total_thb,
	ROUND(NULLIF(SUM(p.amount_thb), 0) / CAST(c.target_thb AS REAL), 4) AS pct_of_target
FROM
	pledge AS p
	LEFT JOIN campaign AS c ON p.campaign_id = c.id
GROUP BY
	p.campaign_id;
"""

# --- Task B ---------------------------------------------------------------
SQL_B = """
SELECT
	(ceil(0.9 * SUM(p.amount_thb))) AS p90_thb,
	CASE
		WHEN d.country = 'Thailand' THEN 'thailand'
		ELSE 'global'
	END AS country
FROM
	pledge p
	LEFT JOIN donor d ON p.donor_id = d.id
GROUP BY
	CASE
		WHEN d.country = 'Thailand' THEN 'thailand'
		ELSE 'global'
	END
ORDER BY
	p90_thb;
"""

# --- (skipped) indexes -----------------------------------------------------
INDEXES: list[str] = []        # left empty on purpose
