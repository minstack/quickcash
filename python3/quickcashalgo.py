import CsvUtil as cu
import math

# testfile = 'quickcash_threecountries.csv'
# testfile = 'qc_summary.csv'
# testfile = 'qc_ausnzuscan4daysago.csv'
# testfile = 'qc_ausnzuscan10daysago.csv'
#testfile = 'qc_uk4daysago.csv'
testfile = 'qc_ausnzuscanuk10daysago.csv'


def getQuickCash(total, numSuggestions=3, sortedDenomination=None):

    if sortedDenomination is None:
        sortedDenomination = [1, 5, 10, 20, 40, 50, 100]

    # insert the exact at the end because of largestDfactor calc in the end
    quickcash = []

    #need to check whether total is greater than largest denomination
    # to prevent doing separate algo for this case, divide and get the int val = store
    # take mod to use that to continue with regular algo
    # this allows for all cash totals to have same amount of suggestions with consistent results
    # as smaller totals
    largeDfactor = int(total / sortedDenomination[-1])
    tempTotal = total % sortedDenomination[-1]

    # print(largeDfactor, tempTotal)

    #the index of the next highest denomination without any combo
    nextDidx = 0
    i = 0
    while i < len(sortedDenomination):
        currD = sortedDenomination[i]
        if currD > tempTotal:
            nextDidx = i
            break
        i += 1


    # previous denomination that is less than total, since it's sorted
    prevD = nextDidx - 1

    # use the lowest denomination to keep adding to the combo until it is
    # greater than the amount.  the lowest should be a factor of any greater
    # denomination so the combo suggestion will include combinations that may
    # consist of other denominations higher than the lowest
    combo = sortedDenomination[prevD]
    smart = round(combo + (tempTotal % 10), 2)
    exact = False
    # combo = math.floor(tempTotal) + sortedDenomination[0]
    #
    # exact = (combo == tempTotal)
    # print("combo: ", combo)
    while combo <= tempTotal:
        if combo == tempTotal:
            # this is exact; no need to look for next combo since first suggestion
            # is always the exact
            exact = True
            break
        combo += sortedDenomination[0]

    if not exact:
        quickcash.append(combo)

    # if tempTotal != smart:
    #     quickcash.append(smart)

    # ceil = math.ceil(tempTotal / 5) * 5
    # quickcash.append(ceil)
    # print(quickcash)
    # now add all the next higher denominations left
    while nextDidx < len(sortedDenomination) and len(quickcash) < numSuggestions:
        next = sortedDenomination[nextDidx]

        if next not in quickcash:
            quickcash.append(next)
        nextDidx += 1

    # add largeDfactor
    if largeDfactor > 0:
        i = 0
        while i < len(quickcash):
            dAdd = largeDfactor * sortedDenomination[-1]
            quickcash[i] += dAdd
            i += 1

    #print(quickcash)

    quickcash.insert(0, total)

    return quickcash

# print(getQuickCash(14))


if __name__ == '__main__':
    totals = cu.getColumn(testfile, 'sale_total')
    paids = cu.getColumn(testfile, 'amount')
    lines = len(totals)

    correct = 0

    wrongTotals = ['sale_total']
    wrongPaids = ['paid_amount']
    wrongqc = ['wrong_quickcash']


    i = 0
    while i < lines:
        currPaid = float(paids[i])
        currTotal = float(totals[i])

        qcash = getQuickCash(currTotal)

        print(currTotal,currPaid, qcash)

        if currPaid in qcash:
            correct += 1
        else:
            wrongTotals.append(currTotal)
            wrongPaids.append(currPaid)
            wrongqc.append(qcash)

        i += 1

    print(correct)
    print(correct/lines*100)

    cu.writeListToCSV(output=zip(wrongTotals, wrongPaids, wrongqc), title='qcwrong', prefix='')

'''
    - needs to check the next combo (not just next highest denomination)
    -- add that to the list for the first suggestion (apart from the exact)
    - then the next highest actual denomination
    -- repeat till 3 suggestions filled

'''
