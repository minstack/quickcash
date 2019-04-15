# quickcash
The confluence page describes what quick cash is and the 3 main reasons why the current quick cash algorithm is accurate by ~64%.
Please refer to the page where the query to pull the data is provided.

This is my attempt at trying to increase that accuracy to around ~80%. The following outlines some of the logic behind my implementation. The implementation here does not address 'smart change' (4.05 -> 5.05) because looking at data, paying with much larger denominations for smaller totals (6.50 -> 20 or 50) had a greater percentage.

The old and new algorithms implemented in python does not use any rounding rules. It assumes that the total provided is the final amount.

### TL;DR 
New algorithm is more accurate but is incomplete to my initial intention of using the heuristic approach - paying based on denonimation. Why? Because the algorithm does not implement multiples of bills ($20 * n). Adding these multiples in the denomination list did increase the accuracy without increasing the complexity of the algorithm. 

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

The intention of using custom lists of denominations corresponding to the country/region may not be necessary in the end but the ability to pass different lists of denominations will be better (probably).

## Test Results
The following initial tests were done with the dataset pulled - this includes all cash transactions (see raw test results that only include non-exact amounts).

Initial sample of 68k records from Australia - **84%**
- Including the 40 in the list increased this by a percent

UK past 10 day sales (38k records) - **86%**

US, Canada, New Zealand, Australia, UK for the past 10 days (600k records) - **79%**

More will be done - the above is with a maximum of 4 suggestions.  I will post a table with the maximum of 3 suggestions as that seems to still be more accurate than the current implementation for quick cash.

### Raw Test Output
I modified the datasets to only include records where `amount - sale_total > 0`. This will elimate the suggestion of the exact total and will test purely on the suggestion's accuracy. This also excluded cash amounts that would not involve quick cash - total is $200 but the amount paid is $5.

The following raw test outputs will include results of the old, new with max 2 sugguestions and new with max 3 suggestions (exluding exact amount). The results are sectioned by the different denomination lists I tested.

#### [1, 5, 10, 20, 50, 100]
```qc_summary_nonexact.csv
Old:	30970 / 43190 = 71.70641352164853
New 2:	29542 / 43190 = 68.40009261403102	Denominations:	[1, 5, 10, 20, 50, 100]
New 3:	34978 / 43190 = 80.9863394304237	Denominations:	[1, 5, 10, 20, 50, 100]

qc_ausnzuscan4daysago_nonexact.csv
Old:	62914 / 100921 = 62.33984998166883
New 2:	62173 / 100921 = 61.60561231061919	Denominations:	[1, 5, 10, 20, 50, 100]
New 3:	72650 / 100921 = 71.98699973246401	Denominations:	[1, 5, 10, 20, 50, 100]

qc_ausnzuscan10daysago_nonexact.csv
Old:	193489 / 311923 = 62.03101406436845
New 2:	191449 / 311923 = 61.37700650481048	Denominations:	[1, 5, 10, 20, 50, 100]
New 3:	223721 / 311923 = 71.72314962346476	Denominations:	[1, 5, 10, 20, 50, 100]

qc_ausnzuscanuk10daysago_nonexact.csv
Old:	252582 / 388624 = 64.99392729218988
New 2:	244519 / 388624 = 62.9191712297748	Denominations:	[1, 5, 10, 20, 50, 100]
New 3:	288864 / 388624 = 74.32994359586644	Denominations:	[1, 5, 10, 20, 50, 100]
```
#### [1, 5, 10, 20, 40, 50, 100]
```
qc_summary_nonexact.csv
Old:	30970 / 43190 = 71.70641352164853
New 2:	26859 / 43190 = 62.188006482982175	Denominations:	[1, 5, 10, 20, 40, 50, 100]
New 3:	33942 / 43190 = 78.58763602685806	Denominations:	[1, 5, 10, 20, 40, 50, 100]

qc_ausnzuscan4daysago_nonexact.csv
Old:	62914 / 100921 = 62.33984998166883
New 2:	65744 / 100921 = 65.14402354316744	Denominations:	[1, 5, 10, 20, 40, 50, 100]
New 3:	76835 / 100921 = 76.13380763171193	Denominations:	[1, 5, 10, 20, 40, 50, 100]

qc_ausnzuscan10daysago_nonexact.csv
Old:	193489 / 311923 = 62.03101406436845
New 2:	203445 / 311923 = 65.2228274285641	Denominations:	[1, 5, 10, 20, 40, 50, 100]
New 3:	237307 / 311923 = 76.07871173334445	Denominations:	[1, 5, 10, 20, 40, 50, 100]

qc_ausnzuscanuk10daysago_nonexact.csv
Old:	252582 / 388624 = 64.99392729218988
New 2:	257961 / 388624 = 66.37804150026761	Denominations:	[1, 5, 10, 20, 40, 50, 100]
New 3:	304009 / 388624 = 78.22702663757256	Denominations:	[1, 5, 10, 20, 40, 50, 100]
```
#### [1, 5, 10, 20, 40, 50, 60, 100]
```
qc_summary_nonexact.csv
Old:	30970 / 43190 = 71.70641352164853
New 2:	26884 / 43190 = 62.245890252373236	Denominations:	[1, 5, 10, 20, 40, 50, 60, 100]
New 3:	33941 / 43190 = 78.58532067608243	Denominations:	[1, 5, 10, 20, 40, 50, 60, 100]

qc_ausnzuscan4daysago_nonexact.csv
Old:	62914 / 100921 = 62.33984998166883
New 2:	66350 / 100921 = 65.74449321746712	Denominations:	[1, 5, 10, 20, 40, 50, 60, 100]
New 3:	77711 / 100921 = 77.0018132995115	Denominations:	[1, 5, 10, 20, 40, 50, 60, 100]

qc_ausnzuscan10daysago_nonexact.csv
Old:	193489 / 311923 = 62.03101406436845
New 2:	205397 / 311923 = 65.84862289731761	Denominations:	[1, 5, 10, 20, 40, 50, 60, 100]
New 3:	240311 / 311923 = 77.04176992398764	Denominations:	[1, 5, 10, 20, 40, 50, 60, 100]

qc_ausnzuscanuk10daysago_nonexact.csv
Old:	252582 / 388624 = 64.99392729218988
New 2:	260319 / 388624 = 66.9847976450245	Denominations:	[1, 5, 10, 20, 40, 50, 60, 100]
New 3:	307452 / 388624 = 79.11297295071843	Denominations:	[1, 5, 10, 20, 40, 50, 60, 100]
```
