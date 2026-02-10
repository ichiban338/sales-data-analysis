-- ==========================================
-- SQL QUERIES FOR SALES DATA ANALYSIS
-- Author: Juan Esteban Agudelo Alonso
-- Project: Sales Data Analysis Portfolio
-- Database: MySQL/PostgreSQL Compatible
-- ==========================================

-- ==========================================
-- QUERY 1: Top 10 Products by Revenue
-- ==========================================
-- Business Use: Identify bestsellers for inventory prioritization

SELECT 
    product,
    COUNT(transaction_id) AS total_transactions,
    SUM(quantity) AS total_units_sold,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_transaction_value
FROM 
    sales_transactions
GROUP BY 
    product
ORDER BY 
    total_revenue DESC
LIMIT 10;


-- ==========================================
-- QUERY 2: Monthly Revenue Summary
-- ==========================================
-- Business Use: Track monthly performance trends

SELECT 
    DATE_FORMAT(sale_date, '%Y-%m') AS year_month,
    COUNT(transaction_id) AS transactions,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value
FROM 
    sales_transactions
GROUP BY 
    DATE_FORMAT(sale_date, '%Y-%m')
ORDER BY 
    year_month;


-- ==========================================
-- QUERY 3: Top 20 Customers by Revenue
-- ==========================================
-- Business Use: Identify VIP customers for retention programs

SELECT 
    customer_id,
    COUNT(transaction_id) AS purchase_frequency,
    SUM(quantity) AS total_items_purchased,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value,
    MIN(sale_date) AS first_purchase_date,
    MAX(sale_date) AS last_purchase_date
FROM 
    sales_transactions
GROUP BY 
    customer_id
ORDER BY 
    total_revenue DESC
LIMIT 20;


-- ==========================================
-- QUERY 4: Revenue by Product Category
-- ==========================================
-- Business Use: Category-level performance dashboard

SELECT 
    product_category,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(transaction_id) AS total_transactions,
    SUM(quantity) AS total_units_sold,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_transaction_value,
    ROUND(AVG(quantity), 2) AS avg_items_per_transaction
FROM 
    sales_transactions
GROUP BY 
    product_category
ORDER BY 
    total_revenue DESC;


-- ==========================================
-- QUERY 5: Daily Revenue for Recent Period
-- ==========================================
-- Business Use: Monitor recent performance trends

SELECT 
    sale_date,
    COUNT(transaction_id) AS daily_transactions,
    SUM(revenue) AS daily_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value
FROM 
    sales_transactions
WHERE 
    sale_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY 
    sale_date
ORDER BY 
    sale_date DESC;


-- ==========================================
-- QUERY 6: Product Performance Within Categories
-- ==========================================
-- Business Use: Identify top performers within each category

SELECT 
    product_category,
    product,
    COUNT(transaction_id) AS transactions,
    SUM(revenue) AS product_revenue
FROM 
    sales_transactions
GROUP BY 
    product_category, 
    product
ORDER BY 
    product_category, 
    product_revenue DESC;


-- ==========================================
-- QUERY 7: Customer Segmentation by Purchase Value
-- ==========================================
-- Business Use: Segment customers for targeted marketing

SELECT 
    CASE 
        WHEN total_revenue >= 5000 THEN 'VIP'
        WHEN total_revenue >= 2000 THEN 'High-Value'
        WHEN total_revenue >= 500 THEN 'Regular'
        ELSE 'Occasional'
    END AS customer_segment,
    COUNT(customer_id) AS customer_count,
    SUM(total_revenue) AS segment_revenue,
    ROUND(AVG(total_revenue), 2) AS avg_customer_value
FROM (
    SELECT 
        customer_id,
        SUM(revenue) AS total_revenue
    FROM 
        sales_transactions
    GROUP BY 
        customer_id
) AS customer_stats
GROUP BY 
    customer_segment
ORDER BY 
    segment_revenue DESC;


-- ==========================================
-- QUERY 8: Quarterly Revenue Summary
-- ==========================================
-- Business Use: Board reporting and strategic planning

SELECT 
    CONCAT('Q', QUARTER(sale_date), ' ', YEAR(sale_date)) AS quarter,
    COUNT(transaction_id) AS total_transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(revenue) AS quarterly_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value
FROM 
    sales_transactions
GROUP BY 
    YEAR(sale_date),
    QUARTER(sale_date)
ORDER BY 
    YEAR(sale_date),
    QUARTER(sale_date);


-- ==========================================
-- QUERY 9: Single vs Multi-Item Transactions
-- ==========================================
-- Business Use: Identify upselling opportunities

SELECT 
    CASE 
        WHEN quantity = 1 THEN 'Single Item'
        WHEN quantity BETWEEN 2 AND 3 THEN '2-3 Items'
        ELSE '4+ Items'
    END AS basket_size,
    COUNT(transaction_id) AS transaction_count,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value
FROM 
    sales_transactions
GROUP BY 
    basket_size
ORDER BY 
    transaction_count DESC;


-- ==========================================
-- QUERY 10: Year-to-Date Performance Summary
-- ==========================================
-- Business Use: Executive dashboard and KPI tracking

SELECT 
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(transaction_id) AS total_transactions,
    SUM(quantity) AS total_items_sold,
    SUM(revenue) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value,
    MIN(sale_date) AS first_transaction_date,
    MAX(sale_date) AS last_transaction_date
FROM 
    sales_transactions;