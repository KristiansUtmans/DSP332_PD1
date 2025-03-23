from anytree import Node, RenderTree, AsciiStyle, ContRoundStyle, NodeMixin
from collections import deque

# Heiristiskās funkcijas koeficienti

# Punktu izmaiņas koeficients
SCORE_DIFFERENCE_COEFFICIENT = 3
# Labo pāru koeficients
GOOD_PAIR_COEFFICIENT = 0.5
# Kopējā skaita koeficients
TOTAL_SUM_COEFFICIENT = 0.1

def generateNodeAddress(name):
    lastDelimiter = name.rfind('.')

    try:
        lastAddress = int(name[lastDelimiter:])
        newAddress = str(lastAddress + 1)
        return newAddress

    except ValueError:
        return name[:lastDelimiter]

# Koka virsotne
class GameNode(NodeMixin):
    def __init__(self, name, setOfNumbers = None, playerPoints = 0, computerPoints = 0, computerTurn = True, parent = None, **kwargs):
        super().__init__()

        if setOfNumbers is None:
            setOfNumbers = []

        self.name = name
        self.setOfNumbers = setOfNumbers.copy()
        self.playerPoints = playerPoints
        self.computerPoints = computerPoints
        self.computerTurn = computerTurn
        self.parent = parent

    def getName(self):
        return self.name

    def getSetOfNumbers(self):
        return self.setOfNumbers

    def getPlayerPoints(self):
        return self.playerPoints

    def getComputerPoints(self):
        return self.computerPoints

    def isComputerTurn(self):
        return self.computerTurn

# Spēles koks, kad depth <= 15 - 7 -> ģenerēt pilnu koku
class GameTree:
    # Saknes virsotne arī darbojas
    def __init__(self, root = GameNode("1", parent=None)):
        self.root = root

    def getRoot(self):
        return self.root

    def getDepth(self):
        return self.depth

    # Koka ģenerēšana līdz noteiktam dziļumam
    def generateGameTree(self, max_depth):
        print("Generating tree")

        # Pārlūkošana izmantojot BFS algoritmu, izmantojot deku(rinda no abām pusēm pārlūkojama)
        queue = deque([[self.root, 0]])

        while queue:
            # Pievienotās virsotnes apskatām no deka kreisās puses
            currentNode, currentDepth = queue.popleft()

            # Ja ir sasniegts dziļums vai spēles beigas šajā ceļā, tad izlaist šo virsotni
            if currentDepth >= max_depth or len(currentNode.getSetOfNumbers()) == 1:
                continue

            currentNumbers = currentNode.getSetOfNumbers()
            currentPlayerPoints = currentNode.getPlayerPoints()
            currentComputerPoints = currentNode.getComputerPoints()
            computerTurn = currentNode.isComputerTurn()
            latestName = currentNode.getName()
            if computerTurn:
                currentComputerPoints += 1
            else:
                currentPlayerPoints += 1

            # Simulē iespējamos spēles gājienus - Iterē pāri katram ciparam spēles virknē, ņemts nākošais, saskaita un pievieno spēles kokam
            for i in range(len(currentNumbers) - 1):
                currentNumber = currentNumbers[i]
                nextNumber = currentNumbers[i + 1]

                newNumber = currentNumber + nextNumber
                if newNumber > 6:
                    newNumber = newNumber - 6

                # Tikai priekš šīs virsotnes izdzēš apskatāmo ciparu un nākamo ciparu, to vietā ieliekot to summu
                newSetOfNumbers = currentNumbers.copy()
                newSetOfNumbers[i + 1] = newNumber
                newSetOfNumbers.pop(i)


                newName = f"{latestName}.{i}"

                # Uzģenerē jauno virsotni. Iestatot tās vecāku, nav nepieciešams to saglabāt
                newNode = GameNode(newName, newSetOfNumbers, currentPlayerPoints, currentComputerPoints, not computerTurn,
                         parent=currentNode)

                # Pievienot virsotni deka beigās, labajā pusē, lai vēlāk caurskatītu tālāk
                queue.append((newNode, currentDepth + 1))

def evaluate_node(node):
    # Heiristiskā novērtēšanas funkcija

    playerScore = node.getPlayerPoints()
    computerScore = node.getComputerPoints()
    setOfNumbers = node.getSetOfNumbers().copy()
    goodPairs = 0
    badPairs = 0
    totalSum = setOfNumbers[0]

    for i in range(len(setOfNumbers) - 1):
        if setOfNumbers[i] + setOfNumbers[i + 1] > 6:
            goodPairs += 1
        else:
            badPairs += 1
        totalSum += setOfNumbers[i + 1]

    return (SCORE_DIFFERENCE_COEFFICIENT * (computerScore - playerScore) +
            GOOD_PAIR_COEFFICIENT * (goodPairs - badPairs) +
            TOTAL_SUM_COEFFICIENT * totalSum)

    # Implement min-max and alpha-beta algorithms, anytree - PostOrderIter() can help
    # def generateWithMiniMax(self):
    #
    #     computerTurn = True
    #
    #     if computerTurn:
    #         bestScore = -999
    #
    #     self.root = GameNode("a")
    #
    # def generateWithAlphaBeta(self):
    #     self.root = GameNode("")


startNode = GameNode("1", [1,2,3,4,5,6,7])
tree = GameTree(startNode)

tree.generateGameTree(2)
print(RenderTree(startNode, style=ContRoundStyle()).by_attr(attrname="setOfNumbers"))
print(evaluate_node(tree.getRoot().children[0].children[0]))

# print(RenderTree(startNode, style=AsciiStyle()).by_attr())
#
# class Node():

#
# f = Node("f")
# b = Node("b", parent=f)
# a = Node("a", parent=b)
# d = Node("d", parent=b)
# c = Node("c", parent=d)
# e = Node("e", parent=d)
# g = Node("g", parent=f)
# i = Node("i", parent=g)
# h = Node("h", parent=i)
# print(RenderTree(f, style=AsciiStyle()).by_attr())