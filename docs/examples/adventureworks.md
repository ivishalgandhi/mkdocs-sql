# SQL Server AdventureWorks Example

## Configuration

First, configure your databases in `mkdocs.yml`:

```yaml
plugins:
  - sql:
      databases:
        adventureworks:
          type: mssql
          server: localhost
          database: AdventureWorks2022
          username: sa
          password: ${MSSQL_PASSWORD}
          trust_server_certificate: yes
```

## SQL Server Queries

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

### Total Sales by Year

```sql[adventureworks]
SELECT YEAR(OrderDate) AS Year, SUM(TotalDue) AS [Total Sales]
FROM Sales.SalesOrderHeader
GROUP BY YEAR(OrderDate)
ORDER BY Year DESC
```


