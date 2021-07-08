def irrigateHandler(params):
    paramIndex = [6, 4, 5, 2, 3]
    parList = []
    parDict = params[0]
    parListValues = list(parDict.values())

    for i in paramIndex:
        parList.append(parListValues[i])
    
    return parList