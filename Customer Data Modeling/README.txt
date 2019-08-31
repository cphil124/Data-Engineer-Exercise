So I conducted this exercise primarily using SQL Server, and SSMS. The initial data upload was done via SQL Server Import Wizard. Each time the source was the .csv files read in using an SSIS 
Wizard Flat File wizard, and the destination was the local master database. I have included the SQL Scripts I was initially using to try and read in the data. While the BULK INSERT worked for the 
Customers table, due to the presence of some commas in the data, which BULK INSERT is not able to handle when reading in a comma delimited file, I resorted to SSIS but included the script anyway,
as with a data source formatted differently, this would work, and jus to show my work.

I imported the data entirely as the varchar datatype, due to the lack of easy repeatability, and poor error messaging from the wizard, and once they were inserted as such, then used SELECT INTO to create
the new tables with proper type aliasing, pulled from the raw source tables.

At this point, I began creating the output tables.

For the Master Customer List, I joined the customer and order lists by the email address as instructed and coalesced the customer ids together to get the master id. However, in order to get an individual record for 
each customer account, I partitioned the query results by each unique email address, and then took the first instance of each as a representative record. Because the rest of the data in the table would be uniform across
customer accounts, this would not impact the accuracy of results.

For the Master Order List, I just did a simple join from the raw orders against the newly made master customer list on the email address once again, as we've previously established that email can serve as a key for this purpose.
However, it was also necessary at this point to implement the aliases I referenced earlier in order to make the numerical data be treated as such in SQL, and to allow for the aggregation functions which are to be done for the 
customer facts table.

Pulling from the new master order table, I used MIN and MAX functions on the created date to find the first and last order dates for each customer, and for lifetime gross revenue and lifetime discounts, I summed the subtotal and total 
discount columns respectively. The aggregating these totals as well as subtracting the sum of the giftcert amount, gets the lifetime net revenue, equivalent to the grand total column. I left a line of code I used to verify this math
in the script but commented out. Finally, by grouping by the customer_ID and using the COUNT function on the distinct order_id's, I was able to get the lifetime # orders count. 