DROP TABLE IF EXISTS dbo.orders_raw
GO

DROP TABLE IF EXISTS dbo.customers_raw
GO

CREATE TABLE dbo.customers_raw (
	account_id varchar(50),
	email VARCHAR(512),
	fname VARCHAR(512),
	lname VARCHAR(512)
)
GO

BULK INSERT dbo.customers_raw
FROM 'C:\Users\Cameron Phillips\Documents\GitHub\Challenge_Site_Submissions\Interview Questions\CatchCo Exercise\customers.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
)
GO




CREATE TABLE dbo.orders_raw (
	[id] INT NOT NULL PRIMARY KEY,
	[reference_number] INT,
	[status] varchar(20),
	[subscription_id] INT, 
	[state] varchar(20),
	grand_total DECIMAL,
	subtotal DECIMAL,
	tax_amount DECIMAL,
	total_due DECIMAL,
	total_invoiced DECIMAL,
	total_item_count INT,
	total_paid decimal,
	total_qty_ordered int, 
	total_refunded int,
	discount_amount decimal,
	order_currency_code varchar(5),
	giftcert_amount int,
	coupon_code varchar(50),
	coupon_rule_name varchar(50),
	customer_group_id bit,
	customer_account_id int,
	customer_is_guest bit,
	shipping_amount decimal, 
	shipping_description varchar(50),
	shipping_discount_amount int,
	shipping_hidden_tax_amount int,
	shipping_incl_tax decimal,
	shipping_invoiced decimal, 
	shipping_method varchar(50),
	shipping_refunded bit,
	how_did_you_hear varchar(50), -- Column contains data with commas. This would need to be reformatted for a Bulk Insert Script to work. 
	how_did_you_hear_other varchar(50),
	created_at datetime,
	updated_at datetime,
	order_has_subscription bit, 
	order_has_ecommerce bit,
	customer_email varchar(50),
	customer_fname varchar(50),
	customer_lname varchar(50)
)

BULK INSERT dbo.orders_raw
FROM 'C:\Users\Cameron Phillips\Documents\GitHub\Challenge_Site_Submissions\Interview Questions\CatchCo Exercise\orders.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
)
GO