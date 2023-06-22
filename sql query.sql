--/////////////////////Query1

select 
distinct ca.name category_name,
count(r.rental_id) rental_count
from category ca join film_category fc 
on ca.category_id = fc.category_id
join film f on fc.film_id = f.film_id
join inventory i on f.film_id = i.film_id
join rental r on i.inventory_id = r.inventory_id
where ca.name in(
'Animation', 'Children', 'Classics', 'Comedy', 'Family' ,'Music')
group by 1
order by category_name





---/////////////////////Query2

select 
distinct
ca.name category_name,
sum(f.rental_duration) over (partition by ca.name order by ca.name) as total_rent
from category ca join film_category fc 
on ca.category_id = fc.category_id and ca.name in ('Animation', 'Children', 'Classics', 'Comedy', 'Family' ,'Music')
join film f on fc.film_id = f.film_id
GROUP BY 1,2

---///////////////////////Query3

WITH t1 AS
(SELECT c.name category,
	NTILE(4) OVER (ORDER BY f.rental_duration) AS standard_quartile

FROM category c
JOIN film_category fc
ON c.category_id = fc.category_id
JOIN film f
ON f.film_id = fc.film_id
WHERE c.name IN ('Animation', 'Children','Classics','Comedy','Family','Music')
ORDER BY category, standard_quartile);

SELECT t1.category, t1.standard_quartile, COUNT(*)
FROM t1
GROUP BY 1,2
ORDER BY category, standard_quartile

---///////////////////////Query4

WITH t1 AS
(SELECT DATE_PART('month', rental_date) as month, DATE_PART('year', rental_date) as year, store_id, COUNT (film_id) OVER (PARTITION BY DATE_TRUNC('month', rental_date) ORDER BY store_id) as count_rentals
FROM rental r
JOIN inventory i
ON i.inventory_id = r.inventory_id);

SELECT t1.month rental_month, t1.year rental_year, t1.store_id, COUNT(count_rentals) count_rentals
FROM t1
GROUP BY 1, 2, 3
ORDER BY count_rentals DESC
