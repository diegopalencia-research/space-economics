-- ============================================================
-- BUSINESS INTELLIGENCE QUERIES
-- Launch Economics & Reliability Intelligence
-- ============================================================

-- QUERY 1: PROVIDER RELIABILITY BY ORBIT CLASS
SELECT 
    organisation,
    orbit_class,
    COUNT(*) as total_launches,
    SUM(success_flag) as successful_launches,
    ROUND(100.0 * SUM(success_flag) / COUNT(*), 2) as reliability_pct,
    ROUND(AVG(cost_million), 2) as avg_cost_million,
    ROUND(AVG(CASE WHEN success_flag = 1 THEN cost_million END), 2) as avg_success_cost
FROM launches
WHERE year_launch >= 2010
GROUP BY organisation, orbit_class
HAVING COUNT(*) >= 5
ORDER BY organisation, reliability_pct DESC;

-- QUERY 2: COST EFFICIENCY TREND (SpaceX vs Industry)
WITH yearly_stats AS (
    SELECT 
        year_launch,
        CASE WHEN organisation = 'SpaceX' THEN 'SpaceX' ELSE 'Industry Average' END as provider_group,
        COUNT(*) as launches,
        ROUND(AVG(cost_million), 2) as avg_cost,
        ROUND(AVG(CASE WHEN success_flag = 1 THEN cost_million END), 2) as success_cost,
        ROUND(100.0 * SUM(success_flag) / COUNT(*), 1) as reliability
    FROM launches
    WHERE year_launch BETWEEN 2012 AND 2024
      AND cost_million IS NOT NULL
    GROUP BY year_launch, provider_group
)
SELECT * FROM yearly_stats
ORDER BY year_launch, provider_group;

-- QUERY 3: LAUNCH SITE LATITUDE EFFICIENCY
SELECT 
    CASE 
        WHEN location LIKE '%Guiana%' OR location LIKE '%Kourou%' THEN 'Equatorial (5°N)'
        WHEN location LIKE '%Cape Canaveral%' OR location LIKE '%Kennedy%' THEN 'Low (28°N)'
        WHEN location LIKE '%Vandenberg%' THEN 'Mid (34°N)'
        WHEN location LIKE '%Baikonur%' THEN 'Mid-High (46°N)'
        WHEN location LIKE '%Plesetsk%' THEN 'High (63°N)'
        ELSE 'Other'
    END as latitude_band,
    orbit_class,
    COUNT(*) as launches,
    ROUND(AVG(cost_million), 2) as avg_cost,
    ROUND(100.0 * SUM(success_flag) / COUNT(*), 1) as reliability
FROM launches
WHERE year_launch >= 2000
GROUP BY latitude_band, orbit_class
HAVING COUNT(*) >= 3
ORDER BY 
    CASE latitude_band
        WHEN 'Equatorial (5°N)' THEN 1
        WHEN 'Low (28°N)' THEN 2
        WHEN 'Mid (34°N)' THEN 3
        WHEN 'Mid-High (46°N)' THEN 4
        WHEN 'High (63°N)' THEN 5
        ELSE 6
    END,
    orbit_class;

-- QUERY 4: REUSABILITY PREMIUM / DISCOUNT ANALYSIS
WITH falcon_launches AS (
    SELECT 
        year_launch,
        CASE 
            WHEN detail LIKE '%Block 5%' THEN 'Falcon 9 Block 5 (Reusable)'
            WHEN detail LIKE '%Block 4%' THEN 'Falcon 9 Block 4 (Limited Reuse)'
            WHEN detail LIKE '%Block 3%' OR detail LIKE '%v1.1%' THEN 'Falcon 9 v1.1 (Expendable)'
            ELSE 'Other Falcon'
        END as variant,
        cost_million,
        success_flag
    FROM launches
    WHERE rocket_family = 'Falcon 9'
      AND year_launch >= 2015
)
SELECT 
    variant,
    COUNT(*) as launches,
    ROUND(AVG(cost_million), 2) as avg_cost,
    ROUND(MIN(cost_million), 2) as min_cost,
    ROUND(MAX(cost_million), 2) as max_cost,
    ROUND(100.0 * SUM(success_flag) / COUNT(*), 1) as reliability
FROM falcon_launches
GROUP BY variant
ORDER BY avg_cost;

-- QUERY 5: MARKET CONCENTRATION (HHI proxy)
WITH yearly_share AS (
    SELECT 
        year_launch,
        organisation,
        COUNT(*) as launches,
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY year_launch) as market_share
    FROM launches
    WHERE year_launch >= 2015
    GROUP BY year_launch, organisation
)
SELECT 
    year_launch,
    ROUND(SUM(market_share * market_share / 100), 2) as hhi_index,
    COUNT(DISTINCT organisation) as num_providers
FROM yearly_share
WHERE market_share >= 5
GROUP BY year_launch
ORDER BY year_launch DESC;
