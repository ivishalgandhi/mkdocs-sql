# World Population Data Analysis

This example demonstrates using SQL queries to analyze world population data. The database contains information about countries and their major cities, including population data, geographical information, and economic indicators.

## Database Schema

The database consists of two main tables:
- `countries`: Contains country-level data including population, area, GDP, and continent
- `cities`: Contains city-level data including population, coordinates, and capital city status

## Sample Queries

### Top 5 Most Populous Countries

Find the most populous countries and their GDP per capita:

```sql[default]
SELECT 
    name,
    population,
    ROUND(CAST(gdp_usd AS FLOAT) / population, 2) as gdp_per_capita
FROM countries 
ORDER BY population DESC 
LIMIT 5;
```

### Population Density Analysis

Analyze countries with the highest population density:

```sql[default]
SELECT 
    name,
    population,
    area_km2,
    ROUND(CAST(population AS FLOAT) / area_km2, 2) as density_per_km2
FROM countries 
ORDER BY density_per_km2 DESC
LIMIT 5;
```

### Cities vs Country Population

Compare city populations to their country's total population:

```sql[default]
SELECT 
    c.name as country_name,
    ci.name as city_name,
    ci.population as city_population,
    c.population as country_population,
    ROUND(CAST(ci.population AS FLOAT) / c.population * 100, 2) as percentage
FROM cities ci
JOIN countries c ON ci.country_id = c.id
ORDER BY percentage DESC
LIMIT 5;
```

### Population by Continent

Analyze population and economic indicators by continent:

```sql[default]
SELECT 
    continent,
    COUNT(*) as num_countries,
    SUM(population) as total_population,
    ROUND(AVG(CAST(gdp_usd AS FLOAT) / population), 2) as avg_gdp_per_capita
FROM countries
GROUP BY continent
ORDER BY total_population DESC;
```