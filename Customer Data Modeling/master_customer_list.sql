DROP TABLE IF EXISTS dbo.master_customer_list
GO

WITH sub as 
(SELECT 
	COALESCE(cr.account_id, ord.customer_account_id) AS [customer_id]
	,cr.email AS [email address]
	,cr.fname as [first name]
	,cr.lname as [last name]
	,ROW_NUMBER() OVER (PARTITION BY cr.email ORDER BY cr.account_id) as rn
FROM [dbo].[customers_raw] as [cr]
JOIN [dbo].[orders_raw] as [ord] ON cr.email = ord.customer_email
) SELECT CAST([customer_id] AS int) AS [customer_id]
		,[email address]
		,[first name]
		,[last name]
INTO [master].[dbo].[master_customer_list]
FROM sub WHERE rn = 1
GO


SELECT *
FROM [master].[dbo].[master_customer_list]
ORDER BY customer_id desc
