use blinkit_db;
select * from sales;
SELECT SUM(Sales) AS Total_Sales
FROM sales;
SELECT AVG(Sales) AS Avg_Sales
FROM sales;
SELECT COUNT(Item_Identifier) AS Total_Items
FROM sales;
SELECT AVG(Rating) AS Avg_Rating
FROM sales;
SELECT Item_Type, SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Item_Type
ORDER BY Total_Sales DESC;
SELECT Item_Fat_Content, SUM(Sales) AS Sales
FROM sales
GROUP BY Item_Fat_Content;
SELECT Outlet_Type, SUM(Sales) AS Sales
FROM sales
GROUP BY Outlet_Type;
SELECT Outlet_Location_Type, SUM(Sales) AS Sales
FROM sales
GROUP BY Outlet_Location_Type;
SELECT Outlet_Size, SUM(Sales) AS Sales
FROM sales
GROUP BY Outlet_Size;
SELECT Outlet_Establishment_Year, SUM(Sales) AS Sales
FROM sales
GROUP BY Outlet_Establishment_Year
ORDER BY Outlet_Establishment_Year;