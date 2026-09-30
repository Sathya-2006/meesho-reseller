-- Q1: Monthly revenue by category

select month,category,SUM(quantity * unit_price) as revenue, count(order_id) as n_orders from orders 
group by month,category order by 
                    case month 
                        when 'April' then 1 
                        when 'May' then 2 
                        when 'June' then 3 
                    END;


-- Q2: Region revenue
select r.region, SUM(o.quantity * o.unit_price) as revenue from orders o join resellers r 
on o.reseller_id = r.reseller_id group by r.region order by r.region;

-- Q3: Top 5 resellers

select r.reseller_id,r.reseller_name,SUM(o.quantity * o.unit_price) as total_spend from orders o join resellers r on o.reseller_id = r.reseller_id 
group by r.reseller_id having total_spend >50000 order by total_spend desc limit 5;


-- Q4: Zero-order resellers

SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(o.order_id) AS order_count
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id
HAVING COUNT(o.order_id) = 0;

select r.reseller_id,r.reseller_name,count(*) as count_star,count(o.order_id) as count_order_id  from resellers r left join orders o on r.reseller_id = o.reseller_id 
where r.reseller_id = 'RS024' group by r.reseller_id;

-- Q5: June Delivered AOV

select ROUND(sum(quantity*unit_price)/count(order_id),2) as AOV from orders where month = 'June' and status = 'Delivered';