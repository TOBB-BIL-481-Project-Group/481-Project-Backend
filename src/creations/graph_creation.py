import random
from utils import adjustVariableBoundaries
import heapq

fa = []


def isSymbol(str):
    return (
        type(str) == type("str") and len(str) == 1 and str[0] >= "a" and str[0] <= "z"
    )


def create_tree(n, l, r, index, isWeighted, dict, array, isDirected, is_cycle=False):
    list1 = []
    list2 = []
    mpp = {}
    findNum = {}
    for i in range(0, n):
        findNum[array[i]] = i
    for i in range(0, n - 2):
        randomNumber = random.randint(0, n - 1)
        randomNumber = array[randomNumber]
        list1.append(randomNumber)
        if randomNumber in mpp:
            mpp[randomNumber] += 1
        else:
            mpp[randomNumber] = 1

    for i in range(0, n):
        if array[i] in mpp:
            continue
        list2.append(array[i])
    heapq.heapify(list2)
    resList = []
    for i in range(0, n - 2):
        x = list1[i]
        y = heapq.heappop(list2)
        order = random.randint(0, 1)
        if isWeighted == 0:
            if is_cycle:
                if findNum[x] < findNum[y]:
                    resList.append((x, y))
                    dict[(x, y)] = 1
                    if isDirected == 0:
                        dict[(y, x)] = 1
                else:
                    resList.append((y, x))
                    dict[(y, x)] = 1
                    if isDirected == 0:
                        dict[(x, y)] = 1
            else:
                if order == 0:
                    resList.append((x, y))
                    dict[(x, y)] = 1
                    if isDirected == 0:
                        dict[(y, x)] = 1
                else:
                    resList.append((y, x))
                    dict[(y, x)] = 1
                    if isDirected == 0:
                        dict[(x, y)] = 1
        else:
            val = random.randint(l, r)
            if is_cycle:
                if findNum[x] < findNum[y]:
                    resList.append((x, y, val))
                    dict[(x, y)] = 1
                    if isDirected == 0:
                        dict[(y, x)] = 1
                else:
                    resList.append((y, x, val))
                    dict[(y, x)] = 1
                    if isDirected == 0:
                        dict[(x, y)] = 1
            else:
                if order == 0:
                    resList.append((x, y, val))
                    dict[(x, y)] = 1
                    if isDirected == 0:
                        dict[(y, x)] = 1
                else:
                    resList.append((y, x, val))
                    dict[(y, x)] = 1
                    if isDirected == 0:
                        dict[(x, y)] = 1

        mpp[x] -= 1
        if mpp[x] == 0:
            heapq.heappush(list2, x)

    x = list2[0]
    y = list2[1]
    order = random.randint(0, 1)
    if isWeighted == 0:
        if is_cycle:
            if findNum[x] < findNum[y]:
                resList.append((x, y))
                dict[(x, y)] = 1
                if isDirected == 0:
                    dict[(y, x)] = 1
            else:
                resList.append((y, x))
                dict[(y, x)] = 1
                if isDirected == 0:
                    dict[(x, y)] = 1
        else:
            if order == 0:
                resList.append((x, y))
                dict[(x, y)] = 1
                if isDirected == 0:
                    dict[(y, x)] = 1
            else:
                resList.append((y, x))
                dict[(y, x)] = 1
                if isDirected == 0:
                    dict[(x, y)] = 1
    else:
        val = random.randint(l, r)
        if is_cycle:
            if findNum[x] < findNum[y]:
                resList.append((x, y, val))
                dict[(x, y)] = 1
                if isDirected == 0:
                    dict[(y, x)] = 1
            else:
                resList.append((y, x, val))
                dict[(y, x)] = 1
                if isDirected == 0:
                    dict[(x, y)] = 1
        else:
            if order == 0:
                resList.append((x, y, val))
                dict[(x, y)] = 1
                if isDirected == 0:
                    dict[(y, x)] = 1
            else:
                resList.append((y, x, val))
                dict[(y, x)] = 1
                if isDirected == 0:
                    dict[(x, y)] = 1
    random.shuffle(resList)
    return resList


def create_string(resList, isWeighted):
    arraySize = len(resList)
    random.shuffle(resList)
    myGraph = ""
    for i in resList:
        if isWeighted:
            myGraph += str(i[0]) + " " + str(i[1]) + " " + str(i[2])
        else:
            myGraph += str(i[0]) + " " + str(i[1])
        arraySize -= 1
        if arraySize != 0:
            myGraph += "\n"
    return myGraph


def dsu(x):
    if x == fa[x]:
        return x
    tut = dsu(fa[x])
    fa[x] = tut
    return fa[x]


def create_graph(value, variables):
    printType = value["type"]
    nodeCount = value["nodeCountSymbol"]
    edgeCount = value["edgeCountSymbol"]
    indexStyle = value["indexStyle"]
    isDirected = value["isDirected"]
    isWeighted = value["isWeighted"]
    features = value["features"]
    print(value)
    n = int(adjustVariableBoundaries.get_variable_boundaries(variables, nodeCount)[0])
    m = int(adjustVariableBoundaries.get_variable_boundaries(variables, edgeCount)[0])
    if n <= 0:
        raise Exception("Node Count must be positive: graph_creation")
    if m <= 0:
        raise Exception("Edge Count must be positive: graph_creation")
    if n > 1000000:
        raise Exception("Node Count must be less than 1e6+1: graph_creation")
    if m > 1000000:
        raise Exception("Edge Count must be less than 1e6+1: graph_creation")

    l = None
    r = None
    try:
        if isWeighted:
            l = (
                int(value["leftLimit"])
                if not isSymbol(value["leftLimit"])
                else adjustVariableBoundaries.get_variable_boundaries(
                    variables, value["leftLimit"]
                )[0]
            )
            r = (
                int(value["rightLimit"])
                if not isSymbol(value["rightLimit"])
                else adjustVariableBoundaries.get_variable_boundaries(
                    variables, value["rightLimit"]
                )[1]
            )
    except Exception as e:
        raise e

    index = 0
    myGraph = ""
    if indexStyle == "1-indexed":
        index = 1
    if printType == "tree":
        bosMap = {}
        array = []
        for i in range(index, index + n):
            array.append(i)
        resList = create_tree(n, l, r, index, isWeighted, bosMap, array, isDirected)
        return create_string(resList, isWeighted)
    ###################################################################################
    multEdge = 1
    selfLoop = 1
    cycle = 1
    connected = 0
    for i in features:
        if i == "Acyclic":
            cycle = 0
        if i == "No Self Loop":
            selfLoop = 0
        if i == "No Multiple Edges":
            multEdge = 0
        if i == "Connected":
            connected = 1
    if connected == 1 and m < n - 1:
        raise Exception(
            "The graph which has less than nodeCount-1 edges, cannot be connected!: graph_creation"
        )

    fa.append(0)
    for i in range(1, index + n):  # indexti 1 yaptim.
        fa.append(i)
        # fa[i] = i

    if cycle == 0:
        if isDirected == 0:
            if connected == 1:
                if n - 1 != m:
                    raise Exception(
                        "Not possible to generate testcase under given constraints: graph_creation"
                    )
                bosMap = {}
                array = []
                for i in range(index, index + n):
                    array.append(i)
                resList = create_tree(
                    n, l, r, index, isWeighted, bosMap, array, isDirected
                )
                return create_string(resList, isWeighted)
            ########################## Undirected Cycle yok Bagli durumu bitti ######################
            if connected == 0:
                cnt = 0
                group_count = n
                while m > 0:
                    x = random.randint(index, index + n - 1)
                    y = random.randint(index, index + n - 1)
                    cnt = cnt + 1
                    if group_count == 1:
                        raise Exception(
                            "There is not any graph with these constraints!: graph_creation"
                        )
                    if cnt == 40000001:
                        raise Exception(
                            "The suitable graph cannot found in many iterations: graph_creation"
                        )
                    if dsu(x) == dsu(y):
                        continue

                    fa[dsu(x)] = dsu(y)
                    myGraph += str(x) + " " + str(y)
                    group_count -= 1
                    m = m - 1
                    if isWeighted:
                        val = random.randint(l, r)
                        myGraph += " " + str(val)
                    if m != 0:
                        myGraph += "\n"
            ##################### Undirected Cycle yok Bagli degil durumu bitti #########################
        if isDirected == 1:
            myList = []
            mpp = {}
            resList = []
            for i in range(index, index + n):
                myList.append(i)
            random.shuffle(myList)
            if connected == 1:
                ##BURAYI UPDATELE CONNECTED 1 OLANLARI DA UPDATELE
                resList = create_tree(
                    n, l, r, index, isWeighted, mpp, myList, isDirected, True
                )
                m -= n - 1
                ###############################TREE OLUSTU#####################################
                if multEdge == 1:
                    while m > 0:
                        x = random.randint(
                            index, index + n - 2
                        )  # burayi da index+n-2 yaptim
                        y = random.randint(
                            x + 1, index + n - 1
                        )  # index+n i index+n-1 yaptim
                        x = myList[x - index]  # -index ekledim
                        y = myList[y - index]  # -index ekledim
                        if isWeighted == 0:
                            resList.append((x, y))
                        if isWeighted:
                            val = random.randint(l, r)
                            resList.append((x, y, val))
                        m = m - 1
                    return create_string(resList, isWeighted)
                if multEdge == 0:
                    if n < 5000:
                        edgeList = []
                        for i in range(index, index + n):
                            for j in range(i + 1, index + n):
                                if not (
                                    (myList[i - index], myList[j - index]) in mpp
                                ):  # -index ekledim ikisine de
                                    edgeList.append(
                                        (myList[i - index], myList[j - index])
                                    )  # -index ekledim ikisine de
                        random.shuffle(edgeList)
                        if len(edgeList) < m:
                            raise Exception(
                                "The suitable graph cannot found in many iterations: graph_creation"
                            )
                        for i in range(0, m):
                            if isWeighted == 0:
                                resList.append((edgeList[i][0], edgeList[i][1]))
                            if isWeighted:
                                val = random.randint(l, r)
                                resList.append((edgeList[i][0], edgeList[i][1], val))
                        return create_string(resList, isWeighted)
                    else:
                        while m > 0:
                            x = random.randint(
                                index, index + n - 2
                            )  # burayi index+n-2 yaptim
                            y = random.randint(
                                x + 1, index + n - 1
                            )  # index + n i index+n-1 yaptim
                            x = myList[x - index]  # -index ekledim
                            y = myList[y - index]  # -index ekledim
                            if (x, y) in mpp:
                                continue
                            mpp[(x, y)] = 1
                            if isWeighted == 0:
                                resList.append((x, y))
                            if isWeighted:
                                val = random.randint(l, r)
                                resList.append((x, y, val))
                            m = m - 1
                        return create_string(resList, isWeighted)
            if connected == 0:
                mpp = {}
                if multEdge == 1:  # burayi 1 e esitse asagiyi da 0 a esitse yaptim
                    while m > 0:
                        x = random.randint(
                            index, index + n - 2
                        )  # index+n-1 di index+n-2 yaptim
                        y = random.randint(
                            x + 1, index + n - 1
                        )  # index+n i index+n-1 yaptim
                        x = myList[x - index]  # -index ekledim
                        y = myList[y - index]  # -index ekledim
                        myGraph += str(x) + " " + str(y)
                        if isWeighted:
                            val = random.randint(l, r)
                            myGraph += " " + str(val)
                        m = m - 1
                        if m != 0:
                            myGraph += "\n"
                    return myGraph
                if multEdge == 0:  # burayi ==1 seden ==0 sa yaptim.
                    if n < 5000:
                        edgeList = []
                        for i in range(index, index + n):
                            for j in range(i + 1, index + n):
                                if not (
                                    (myList[i - index], myList[j - index]) in mpp
                                ):  # i-index, j-index yaptim
                                    edgeList.append(
                                        (myList[i - index], myList[j - index])
                                    )  # i-index j-index yaptim

                        random.shuffle(edgeList)
                        if len(edgeList) < m:
                            raise Exception(
                                "The suitable graph cannot found in many iterations: graph_creation"
                            )
                        for i in range(0, m):
                            myGraph += str(edgeList[i][0]) + " " + str(edgeList[i][1])
                            if isWeighted:
                                val = random.randint(l, r)
                                myGraph += " " + str(val)
                            if m - 1 != i:
                                myGraph += "\n"
                        return myGraph
                    else:
                        while m > 0:
                            x = random.randint(
                                index, index + n - 2
                            )  # index+n-1 di index+n-2
                            y = random.randint(
                                x + 1, index + n - 1
                            )  # index+n i index+n-1 yaptim
                            x = myList[x - index]  # -index ekledim
                            y = myList[y - index]  # -index ekledim
                            if (x, y) in mpp:
                                continue
                            mpp[(x, y)] = 1
                            myGraph += str(x) + " " + str(y)
                            if isWeighted:
                                val = random.randint(l, r)
                                myGraph += " " + str(val)
                            m = m - 1
                            if m != 0:
                                myGraph += "\n"
                        return myGraph

    if cycle == 1:
        mpp = {}  # ben ekledim.
        at = 0
        array = []
        resList = []
        for i in range(index, index + n):
            array.append(i)
        if selfLoop == 0:  # ==1 ise idi ==0 sa yaptim.
            at = 1
        if connected == 1:
            resList = create_tree(n, l, r, index, isWeighted, mpp, array, isDirected)
            m -= n - 1
        if multEdge == 0:
            if n <= 5000:
                edgeList = []
                for i in range(index, index + n):
                    for j in range(i + at, index + n):
                        if not ((i, j) in mpp):
                            edgeList.append((i, j))
                            mpp[(i, j)] = 1
                            if isDirected == 0:
                                mpp[(j, i)] = 1
                        if not ((j, i) in mpp):
                            edgeList.append((j, i))
                            mpp[(j, i)] = 1
                            if isDirected == 0:
                                mpp[(i, j)] = 1
                random.shuffle(edgeList)
                if len(edgeList) < m:
                    raise Exception(
                        "The suitable graph cannot found in many iterations: graph_creation"
                    )
                for i in range(0, m):  # burayi m+1 idi m yaptim
                    if isWeighted == 0:
                        resList.append((edgeList[i][0], edgeList[i][1]))
                    if isWeighted:
                        val = random.randint(l, r)
                        resList.append((edgeList[i][0], edgeList[i][1], val))
                return create_string(resList, isWeighted)
            else:
                while m > 0:
                    x = random.randint(index, index + n - 1)  # n-1
                    y = random.randint(index, index + n - 1)  # n-1 yaptim.
                    if (x, y) in mpp:
                        continue
                    if x == y and at == 1:
                        continue
                    if isWeighted == 0:
                        resList.append((x, y))
                    mpp[(x, i)] = 1
                    if isDirected == 0:
                        mpp[(i, x)] = 1
                    if isWeighted:
                        val = random.randint(l, r)
                        resList.append((x, y, val))
                    m = m - 1
                return create_string(resList, isWeighted)
        else:
            while m > 0:
                x = random.randint(index, index + n - 1)  # n-1
                y = random.randint(index, index + n - 1)  # n-1 yaptim
                if x == y and at == 1:
                    continue
                if isWeighted == 0:
                    resList.append((x, y))
                if isWeighted:
                    val = random.randint(l, r)
                    resList.append((x, y, val))
                m = m - 1
            return create_string(resList, isWeighted)
