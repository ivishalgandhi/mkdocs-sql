-- Top Selling Products
SELECT TOP 5
    p.Name AS ProductName,
    SUM(OrderQty) AS TotalQuantitySold,
    SUM(LineTotal) AS TotalRevenue
FROM Sales.SalesOrderDetail sod
JOIN Production.Product p ON sod.ProductID = p.ProductID
GROUP BY p.Name
ORDER BY TotalRevenue DESC;

-- Sales by Territory
SELECT 
    st.Name AS Territory,
    COUNT(DISTINCT soh.CustomerID) AS NumberOfCustomers,
    SUM(TotalDue) AS TotalSales,
    AVG(TotalDue) AS AverageOrderValue
FROM Sales.SalesOrderHeader soh
JOIN Sales.SalesTerritory st ON soh.TerritoryID = st.TerritoryID
GROUP BY st.Name
ORDER BY TotalSales DESC;

-- Customer Demographics
SELECT 
    pp.LastName + ', ' + pp.FirstName AS CustomerName,
    pea.EmailAddress,
    pa.City,
    pa.StateProvince,
    pc.Phone
FROM Sales.Customer c
JOIN Person.Person pp ON c.PersonID = pp.BusinessEntityID
JOIN Person.EmailAddress pea ON pp.BusinessEntityID = pea.BusinessEntityID
JOIN Person.BusinessEntityAddress bea ON pp.BusinessEntityID = bea.BusinessEntityID
JOIN Person.Address pa ON bea.AddressID = pa.AddressID
JOIN Person.PersonPhone pc ON pp.BusinessEntityID = pc.BusinessEntityID
ORDER BY pp.LastName, pp.FirstName
LIMIT 10;

-- Product Categories and Subcategories
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

-- Employee Sales Performance
SELECT 
    p.FirstName + ' ' + p.LastName AS SalesPerson,
    COUNT(soh.SalesOrderID) AS NumberOfOrders,
    SUM(soh.TotalDue) AS TotalSales,
    SUM(soh.TotalDue)/COUNT(soh.SalesOrderID) AS AverageOrderValue,
    MAX(soh.OrderDate) AS LastOrderDate
FROM Sales.SalesOrderHeader soh
JOIN Person.Person p ON soh.SalesPersonID = p.BusinessEntityID
GROUP BY p.FirstName, p.LastName
ORDER BY TotalSales DESC;
