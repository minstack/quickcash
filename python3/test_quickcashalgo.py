import quickcashalgo as qca
import JsonUtil as ju
import CsvUtil as cu


def runTest(func, totals, paids, numSuggestions=3, sortedDenom=[]):

    lines = len(totals)

    correct = 0

    wrongTotals = ['sale_total']
    wrongPaids = ['paid_amount']
    wrongqc = ['wrong_quickcash']


    i = 0
    while i < lines:
        currPaid = float(paids[i])
        currTotal = float(totals[i])

        qcash = func(currTotal, numSuggestions=numSuggestions, sortedDenomination=sortedDenom)

        #print(currTotal,currPaid, qcash)

        if currPaid in qcash:
            correct += 1
        # else:
        #     wrongTotals.append(currTotal)
        #     wrongPaids.append(currPaid)
        #     wrongqc.append(qcash)

        i += 1

    return (correct, i)




if __name__ == '__main__':

    testjson = ju.loadJsonFile('test.json')
    testfiles = testjson['testfiles']
    denominations = testjson['denominations']

    results = []

    for denomination in denominations:
        results.append([str(denomination)])
        for testfile in testfiles:

            print(f"Running {testfile} : {denomination}...")

            totals = cu.getColumn(testfile, 'sale_total')
            paids = cu.getColumn(testfile, 'amount')


            newAlgo3 = runTest(qca.getQuickCash, totals, paids, numSuggestions=3, sortedDenom=denomination)
            newAlgo2 = runTest(qca.getQuickCash, totals, paids, numSuggestions=2, sortedDenom=denomination)
            oldAlgo = runTest(qca.getQuickCashOld, totals, paids, sortedDenom=[1, 5, 10, 20, 30, 40, 50, 100])

            result =[]
            result.append(testfile)
            result.append(f'Old:\t{oldAlgo[0]} / {oldAlgo[1]} = {oldAlgo[0]/oldAlgo[1] * 100}')
            result.append(f'New 2:\t{newAlgo2[0]} / {newAlgo2[1]} = {newAlgo2[0]/newAlgo2[1] * 100}\tDenominations:\t{denomination}')
            result.append(f'New 3:\t{newAlgo3[0]} / {newAlgo3[1]} = {newAlgo3[0]/newAlgo3[1] * 100}\tDenominations:\t{denomination}')

            results.append(result)


    print("\nRESULTS:")
    print("=============================================================")

    for r in results:
        for line in r:
            print(line)
        print()

    #cu.writeListToCSV(output=zip(wrongTotals, wrongPaids, wrongqc), title='qcwrong', prefix='')
