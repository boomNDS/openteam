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
	p.campaign_id
ORDER BY
	pct_of_target DESC,
	campaign_id ASC;
"""

# --- Task B ---------------------------------------------------------------
SQL_B = """
WITH
	all_pledges AS (
		SELECT
			'global' AS scope,
			amount_thb
		FROM
			pledge
		UNION ALL
		SELECT
			'thailand' AS scope,
			p.amount_thb
		FROM
			pledge p
			JOIN donor d ON p.donor_id = d.id
		WHERE
			d.country = 'Thailand'
	),
	ranked AS (
		SELECT
			scope,
			amount_thb,
			ROW_NUMBER() OVER (
				PARTITION BY
					scope
				ORDER BY
					amount_thb
			) AS rankNumber,
			COUNT(*) OVER (
				PARTITION BY
					scope
			) AS cnt
		FROM
			all_pledges
	)
SELECT
	scope,
	amount_thb AS p90_thb
FROM
	ranked
WHERE
	rankNumber = CEIL(0.9 * cnt)
ORDER BY
	CASE scope
		WHEN 'global' THEN 1
		ELSE 2
	END;
"""

# --- (skipped) indexes -----------------------------------------------------
INDEXES: list[str] = []        # left empty on purpose
