-- ============================================================
-- ANALYSIS VIEWS
-- ============================================================

CREATE VIEW IF NOT EXISTS v_launches_modern AS
SELECT * FROM launches
WHERE year_launch >= 2010;

CREATE VIEW IF NOT EXISTS v_provider_summary AS
SELECT 
    organisation,
    COUNT(*) as total_launches,
    SUM(success_flag) as successful,
    ROUND(100.0 * SUM(success_flag) / COUNT(*), 2) as reliability_pct,
    ROUND(AVG(cost_million), 2) as avg_cost_million,
    MIN(year_launch) as first_launch,
    MAX(year_launch) as last_launch
FROM launches
GROUP BY organisation;

CREATE VIEW IF NOT EXISTS v_yearly_trends AS
SELECT 
    year_launch,
    COUNT(*) as launches,
    SUM(success_flag) as successes,
    ROUND(100.0 * SUM(success_flag) / COUNT(*), 2) as reliability_pct,
    ROUND(AVG(cost_million), 2) as avg_cost,
    COUNT(DISTINCT organisation) as active_providers
FROM launches
GROUP BY year_launch
ORDER BY year_launch;
