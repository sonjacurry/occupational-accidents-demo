CREATE OR REPLACE TABLE gold_occupational_accidents AS

SELECT
    year,
    occupational_status,
    injury_category,
    injury_category_sort,
    industry_code_main,
    industry_code_sub,
    industry_name_main,
    industry_name_sub,
    age_group,
    gender,
    accidents

FROM silver_occupational_accidents;
