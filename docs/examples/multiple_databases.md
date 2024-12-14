# Using Multiple Databases

This example shows how to use multiple databases in your documentation.

## Configuration

Our current configuration in `mkdocs.yml`:

```yaml
plugins:
  - sql:
      databases:
        default:  # SQLite database
          type: sqlite
          path: docs/examples/population.sqlite
        adventureworks:  # SQL Server database
          type: mssql
          server: 127.0.0.1,1433
          database: AdventureWorks2022
          username: sa
          password: ${MSSQL_PASSWORD}
          encrypt: true
          trust_server_certificate: true
```

## SQLite Database Examples

Here are some example queries using our SQLite database containing world population data.

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

## SQL Server Examples

Here are some example queries using the AdventureWorks database in SQL Server.

### Top Selling Products

Find the top 5 products by revenue:

```sql[adventureworks]
SELECT TOP 5
  p.Name AS ProductName,
    SUM(OrderQty) AS TotalQuantitySold,
    SUM(LineTotal) AS TotalRevenue
FROM Sales.SalesOrderDetail sod
JOIN Production.Product p ON sod.ProductID = p.ProductID
GROUP BY p.Name
ORDER BY TotalRevenue DESC;
```

### Sales by Territory

Analyze sales performance across different territories:

```sql[adventureworks]
SELECT 
    st.Name AS Territory,
    COUNT(DISTINCT soh.CustomerID) AS NumberOfCustomers,
    SUM(TotalDue) AS TotalSales,
    AVG(TotalDue) AS AverageOrderValue
FROM Sales.SalesOrderHeader soh
JOIN Sales.SalesTerritory st ON soh.TerritoryID = st.TerritoryID
GROUP BY st.Name
ORDER BY TotalSales DESC;
```

### Product Categories

Analyze products by category and subcategory:

```sql[adventureworks]
SELECT 
    pc.Name AS Category,
    ps.Name AS Subcategory,
    COUNT(p.ProductID) AS NumberOfProducts,
    AVG(p.ListPrice) AS AveragePrice
FROM Production.Product p
JOIN Production.ProductSubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID
JOIN Production.ProductCategory pc ON ps.ProductCategoryID = pc.ProductCategoryID
GROUP BY pc.Name, ps.Name
ORDER BY Category, Subcategory;
```