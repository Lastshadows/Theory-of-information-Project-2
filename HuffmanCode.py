
from heapq import *

class Node(object):

    # Data
    symbol = None
    prob = 0

    # Link to left and right child
    lhs = None
    rhs = None

    def __init__(self, symbol, prior):
        self.symbol = symbol
        self.prob = prior

    def setChildren(self, leftNode, rightNode):
        self.lhs = leftNode
        self.rhs = rightNode

    def getSymbol(self):
        return self.symbol

    def getFreq(self):
        return self.prob

    # Required for sorting in heapify
    def __lt__(self, a):
        return self.prob < a.prob

class HuffmanCoder:

    dict ={}
    listOfSymbols = []
    nodeQueue = []
    codes = {}

    # we have the list of symbols in the alphabet and a dictionnary that match these symbols to their frequency
    def __init__(self, listOfSymbols, dict):
        self.listOfSymbols = listOfSymbols
        self.dict = dict

        #create the nodes of the tree
        for symbol in listOfSymbols:
            #print(symbol + " was added to nodeQueue")
            node = Node(symbol, dict[symbol])
            self.nodeQueue.append(node)

        # nodes are sorted in ascending order of probability: the root is the
        # smallest frequency
        heapify(self.nodeQueue)
        while len(self.nodeQueue) > 1:
            # Get the two least frequent one
            left = heappop(self.nodeQueue)
            right = heappop(self.nodeQueue)
            node = Node(None, right.prob + left.prob)
            node.setChildren(left, right)
            heappush(self.nodeQueue, node)

    def isLeaf(self, node):
        return node.symbol is not None
    # recursive fct that will code the different symbols
    def codeIt(self, prefixCodeStr, node):

        #if we have a leaf node (item is none for non leaf nodes)
        if self.isLeaf(node):
            if prefixCodeStr is None:
                self.codes[node.symbol] = "0"
            else:
                # Transmit prefix code of parent
                self.codes[node.symbol] = prefixCodeStr
        #if internal node
        else:
            self.codeIt(prefixCodeStr + "0", node.lhs)
            self.codeIt(prefixCodeStr + "1", node.rhs)

    #starts the recursion
    def encoder(self, str):
        self.codeIt(str, self.nodeQueue[0])

    def getCode(self):
        return self.codes
