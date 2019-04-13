# quickcash
The confluence page describes what quick cash is and the 3 main reasons why the current quick cash algorithm is accurate by ~64%.
Please refer to the page where the query to pull the data is provided.

This is my attempt at trying to increase that accuracy to around ~80%. The following outlines some of the logic behind my implementation.

## Approach
Using the sample size of around 68K records of sales, I initially attempted to find any patterns by doing some calculations on the `sale_total` and `amount` paid without any progress.

### Denominations
I noticed from my support role, that I encounter situations where the suggestions included amounts that did not really make sense. For example, the total is less than $20 but one of the suggestions would be $30.  If I have a $10 and $20 bill, I would just pay with the single $20 bill. Naturally, I decided to approach the problem using lists of denominations.

If we consider the US, this would consist of [1, 5, 10, 20, 50, 100].
