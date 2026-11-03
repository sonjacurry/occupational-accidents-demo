# Occupational Accidents in Finland

An end-to-end data analytics project analysing occupational accidents in Finland using open data from Statistics Finland.

The project demonstrates a complete analytics workflow from API-based data extraction and data engineering in Databricks to interactive reporting in Power BI.

## Project Overview

The purpose of this project is to explore occupational accident patterns in Finland between **2008 and 2024** while demonstrating practical skills in:

- Python

- REST APIs

- Pandas

- PySpark

- Databricks

- Delta Lake

- SQL

- Power BI

- Git

- GitHub

- Visual Studio Code

The data is retrieved programmatically from the **Statistics Finland StatFin PXWeb API**, transformed in Databricks using a Bronze-Silver-Gold architecture, and visualised in Power BI.

## Architecture

The project follows a medallion-style architecture:

```text

Statistics Finland

       |

       v

StatFin PXWeb API

       |

       v

Python ingestion

       |

       v

+-------------+

|   Bronze    |

|  Raw data   |

+-------------+

       |

       v

+-------------+

|   Silver    |

| Cleaned and |

| structured  |

+-------------+

       |

       v

+-------------+

|    Gold     |

| Analytics-  |

| ready data  |

+-------------+

       |

       v

   Power BI

```

Git and GitHub are used for version control, source code management and project documentation.

## Data Source

The data is retrieved from Statistics Finland's StatFin database through the PXWeb API.

**StatFin table:** `ttap/129s`

**Period:** 2008-2024

The dataset contains occupational accident information by:

- Year

- Occupational status

- Injury category

- Industry

- Age group

- Gender

The API extraction is performed using Python and the `requests` library.

To keep individual PXWeb requests manageable, the data is retrieved separately for each year and combined after extraction.

## Data Pipeline

### Bronze Layer

The Bronze layer preserves the data retrieved from the StatFin PXWeb API with minimal transformation.

The API response is converted from JSON-stat2 into a tabular structure and stored as a Delta table in Databricks.

The purpose of the Bronze layer is to retain the source data before analytical transformations are applied.

### Silver Layer

The Silver layer cleans and restructures the source data for analysis.

Key transformations include:

- Renaming technical StatFin fields

- Converting columns to appropriate data types

- Removing overlapping aggregate categories

- Creating an industry hierarchy

- Separating industry codes from industry names

- Creating custom category sort orders

- Performing data-quality checks

The resulting structure contains fields such as:

```text

year

occupational_status

injury_category

injury_category_sort

industry_code_main

industry_code_sub

industry_name_main

industry_name_sub

age_group

age_group_sort

gender

accidents

```

### Gold Layer

The Gold layer contains the analytics-ready dataset used by Power BI.

The main reporting table is:

```text

gold_occupational_accidents

```

Business and source-data modelling rules are handled upstream before the Gold layer is consumed by the report.

## Industry Modelling

The source contains both broad and detailed industry classifications.

The analytical model restructures these into a two-level hierarchy:

```text

Main industry

    |

    +-- Sub-industry

```

For example:

```text

F | Construction

    |

    +-- 41 | Construction of buildings

    +-- 42 | Civil engineering

    +-- 43 | Specialised construction activities

```

This means a Civil engineering record contains both:

```text

industry_code_main = F

industry_name_main = Construction

industry_code_sub = 42

industry_name_sub = Civil engineering

```

This design makes it possible to aggregate results at main-industry level and drill down to detailed industries without storing overlapping main-industry totals as separate observations.

Two exceptional categories are retained:

```text

S1313 | Local government -sector

Unknown | Unknown

```

For these categories, the same classification is used at both the main and sub-industry level.

## Injury Category Modelling

The analytical dataset contains the following injury categories:

```text

0-3 days

4-6 days

7-14 days

15-30 days

31-90 days

91-180 days

181 days or more

Workers' compensation pension

Fatal accidents

```

The StatFin source also contains the aggregate category:

```text

At least 4 days

```

This category is excluded from the analytical dataset because it overlaps with the more detailed injury-duration categories.

An explicit sort order is created in Databricks so the categories can be presented logically in Power BI.

## Power BI Report

The Gold-layer data is used to build an interactive Power BI report.

The report contains several analytical views.

### Overview

Provides high-level KPIs and long-term development, including:

- Total accidents

- Latest-year accidents

- Previous-year accidents

- Year-on-year change

- Accident trends from 2008 to 2024

### Industry Analysis

Explores occupational accidents using the two-level industry hierarchy:

- Main industries

- Sub-industries

- Top industries by accident count

- Industry trends over time

- Injury-category distributions by industry

Users can drill from main industries into detailed sub-industries.

### Demographics

Explores accident patterns by:

- Age group

- Gender

- Year

The report compares demographic composition and long-term trends across demographic groups.

### Injury Severity

Explores the distribution and development of different injury categories.

The analysis includes:

- Injury-category distribution

- Injury-category trends

- Longer-duration outcomes

- Workers' compensation pension cases

- Fatal accidents

- Differences in injury distributions between industries

### Occupational Status

Explores occupational accidents across:

- Wage and salary earners

- Entrepreneurs

- Farmers

The page examines both absolute accident counts and differences in occupational-status composition between industries.

## Power BI Measures

The report uses reusable DAX measures rather than directly aggregating columns in individual visuals.

Examples include:

```DAX

Total Accidents =

SUM(

    gold_occupational_accidents[accidents]

)

```

Additional measures calculate:

- Latest-year accidents

- Previous-year accidents

- Year-on-year change

- Year-on-year percentage change

- Share of accidents by age group

- Share of accidents by injury category

- Share of accidents by industry

- Share of accidents by occupational status

Custom report-page tooltips provide additional contextual information without overcrowding the main report pages.

## Repository Structure

```text

occupational-accidents-demo/

|

├── notebooks/

|   └── Databricks notebooks

|

├── src/

|   └── Reusable Python code

|

├── sql/

|   └── gold_tables.sql

|

├── powerbi/

|   ├── README.md

|   └── screenshots/

|

├── docs/

|   ├── data_dictionary.md

|   └── insights.md

|

├── .gitignore

├── requirements.txt

└── README.md

```

## Key Analytical Questions

The analysis aims to answer questions such as:

- How have occupational accident counts changed between 2008 and 2024?

- Which industries record the largest number of occupational accidents?

- Which sub-industries drive the results within the main industry groups?

- Which industries have increased or decreased the most over time?

- How do occupational accident patterns differ between age groups?

- How have demographic patterns changed over time?

- How does the injury-category distribution differ between industries?

- How have severe outcomes developed over time?

- How does occupational-status composition differ between industries?

## Key Findings

The final analytical findings are documented separately in:

```text

docs/insights.md

```

The analysis focuses on evidence observable in the data and separates descriptive findings from possible causal explanations.

## Limitations

The analysis primarily uses **occupational accident counts**.

Differences in accident counts between industries or demographic groups may partly reflect differences in the number of employees, hours worked or other measures of exposure.

For example, an industry with twice as many recorded accidents does not necessarily have twice the individual accident risk.

The results should therefore primarily be interpreted as differences in the **number and distribution of recorded occupational accidents**, rather than direct comparisons of accident risk.

Additional exposure data would be required to calculate comparable accident rates.

## Technologies

| Technology | Purpose |

|---|---|

| Python | API extraction and processing |

| Requests | StatFin PXWeb API requests |

| Pandas | JSON-stat2 processing |

| PySpark | Data transformation |

| Databricks | Data engineering and processing |

| Delta Lake | Bronze, Silver and Gold tables |

| SQL | Analytical transformations |

| Power BI | Data modelling and visualisation |

| DAX | Analytical measures |

| Git | Version control |

| GitHub | Source code and documentation |

| Visual Studio Code | Local development |

## Reproducibility

The project is designed so that the analytical dataset can be rebuilt from the original public source rather than storing a static copy of the processed data in the repository.

The intended workflow is:

```text

Run StatFin ingestion

        |

        v

Create Bronze table

        |

        v

Transform Bronze to Silver

        |

        v

Create Gold table

        |

        v

Refresh Power BI model

```

## Future Improvements

Potential next steps include:

- Automating the pipeline with Databricks Workflows

- Automatically ingesting newly published years

- Moving more reusable API logic into Python modules

- Adding automated data-quality tests

- Creating additional analytical Gold tables

- Adding exposure data to calculate accident rates

- Expanding the analysis of long-term trends

- Documenting the final analytical insights