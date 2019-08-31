DROP TABLE IF EXISTS dbo.[customer_facts]

SELECT 
	mol.[customer_id] as [Master Customer ID]
	,MIN(mol.created_at) AS [First Order Date]
	,MAX(mol.created_at) AS [Last Order Date]
	,SUM(mol.[subtotal]) AS [Lifetime Gross Revenue]
	,SUM(mol.[discount_amount]) AS [Lifetime Discounts]
	,SUM(mol.[grand_total]) AS [Lifetime Net Revenue]
	--,SUM(mol.[subtotal]) -  SUM(mol.[giftcert_amount] - mol.[discount_amount]) AS [Lifetime Net Revenue2]
	,COUNT(DISTINCT mol.id) as [Lifetime # Orders]
INTO [dbo].[customer_facts]
FROM [dbo].[master_order_list] as mol 
JOIN [dbo].[master_customer_list] as mcl ON mol.[customer_id] = mcl.[customer_id]
GROUP BY mol.[customer_id]

SELECT * FROM dbo.[customer_facts] ORDER BY [Master Customer ID] DESC