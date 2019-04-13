# quickcash
The confluence page describes what quick cash is and the 3 main reasons why the current quick cash algorithm is accurate by ~64%.
Please refer to the page where the query to pull the data is provided.

This is my attempt at trying to increase that accuracy to around ~80%. The following outlines some of the logic behind my implementation. The implementation here does not address 'smart change' (4.05 -> 5.05) because looking at data, paying with much larger denominations for smaller totals (6.50 -> 20 or 50) had a greater percentage.

## Approach
Using the sample size of around 68K records of sales, I initially attempted to find any patterns by doing some calculations on the `sale_total` and `amount` paid without any progress.

### Denominations
I noticed from my support role, that I encounter situations where the suggestions included amounts that did not really make sense. For example, the total is less than $20 but one of the suggestions would be $30.  If I have a $10 and $20 bill, I would just pay with the single $20 bill. Naturally, I decided to approach the problem using lists of denominations.

I initially considered the US to test out my logic, consisting of `[1, 5, 10, 20, 50, 100]` but also wanted it so that the algorithm would accept any sorted list of denominations. This approach made sense because of cases where a suggestion would be wasted like I outlined previously.

## Logic
- Find the smallest denomination that is greater than the total sale amount
- Calculate a 'combination' of denominations that is the smallest amount greater than the total (not the same as the above but uses the index found above to to find the one before - 'one step' less)
  - A total such as $15.40 would possibly result in the customer paying $16
  - Takes the greatest denomination less than the total and increments by the lowest denomination until it is either equal or greater than the total
    - **total**: 15.40, **start**: 10, **lowest denomination increment**: by 1 (the US list above in mind)
  - This does not consider multiples of denominations which I believe would make the algo much more expensive.  TBH, I actually haven't tried this fully.
  - If this does not hit the exact amount - total being something like $14.00, add to the suggestion
- Finally, add the remaining denominations greater than the total - starting from the one found in step 1. Maximum of 4 total suggestions including the exact amount (this can be specified).

Intial run with the sample returned an accuracy of **~83%**.

## Large Cash Amounts (>$200)
The current algorithm maxes out suggestions where the total is greater than $200. My implementation will work with any amount.  From the above logic, a step is added in the beginning where I take the largest denomination to calculate a factor to be incorporated later on.
- Factor = the integer division of the total by the largest denomination
  - 245.45 / 100 = **2**
- Temporary total = total mod largest denomination
  - 245.45 % 100 = **45.45**
- Now the initial logic can process the new temporary exactly the same way it would like any other total
- Before finalizing the suggestions, add the final suggestions with the factor * largest denomination
  - suggestion += factor * largest denomination
  - suggestion += 2 * 100
- Although we do not have any data on this that would be accurate because of the current algo, I would suspect that this will add more accurate data moving forward if this were to be implemented

## Different Currencies and Regions
Although the initial intent was to have custom lists of denominations to be passed to the algorithm, initial testings show that the list `[1, 5, 10, 20, 40, 50, 100]` has the best results with the data available. Test results will be included in the following section but I will explain why I added 40 to the list.

A bank note of 40 does not exist in any major country/region Vend is used in (US, Canada, Australia, New Zealand, UK). But because this implementation (currently) does not account for multiples of the same bill (total: 38.8, paid: 40 (20 x 2)), it was added after looking at the failed suggestions. Simply adding 40 into the list of 'denominations' increased the accuracy significantly.

The intention of using custom lists of denominations corresponding to the country/region may not be necessary in the end but the ability to pass different lists of denominations will be better better for refactoring (probably).

## Test Results
Initial sample of 68k records from Australia - **84%**
- Including the 40 in the list increased this by a percent

UK past 10 day sales (38k records) - **86%**

US, Canada, New Zealand, Australia, UK for the past 10 days (600k records) - **79%**

More will be done - the above is with a maximum of 4 suggestions.  I will post a table with the maximum of 3 suggestions as that seems to still be more accurate than the current implementation for quick cash.
