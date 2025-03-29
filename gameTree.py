from anytree import RenderTree, ContRoundStyle, NodeMixin
from collections import deque

# Heiristiskās funkcijas koeficienti

# Punktu izmaiņas koeficients
SCORE_DIFFERENCE_COEFFICIENT = 3
# Labo pāru koeficients
GOOD_PAIR_COEFFICIENT = 0.5
# Kopējā skaita koeficients
TOTAL_SUM_COEFFICIENT = 0.1

# Realizē gājiena punktu izmaiņas nosacījumus
def updatePoints(number, points):
    if number < 6:
        return number, points - 1
    else:
        return number - 6, points + 1

# Koka virsotne
class GameNode(NodeMixin):
    def __init__(self, name, setOfNumbers = None, playerPoints = 0, computerPoints = 0, computerTurn = True, parent = None):
        super().__init__()

        if setOfNumbers is None:
            setOfNumbers = []

        self.name = name
        self.setOfNumbers = setOfNumbers.copy()
        self.playerPoints = playerPoints
        self.computerPoints = computerPoints
        self.computerTurn = computerTurn
        self.parent = parent

    def evaluate_node(self):
        # Heiristiskā novērtējuma funkcija
        goodPairs = 0
        badPairs = 0
        totalSum = self.setOfNumbers[0]

        for i in range(len(self.setOfNumbers) - 1):
            if self.setOfNumbers[i] + self.setOfNumbers[i + 1] > 6:
                goodPairs += 1
            else:
                badPairs += 1
            totalSum += self.setOfNumbers[i + 1]

        return (SCORE_DIFFERENCE_COEFFICIENT * (self.computerPoints - self.playerPoints) +
                GOOD_PAIR_COEFFICIENT * (goodPairs - badPairs) +
                TOTAL_SUM_COEFFICIENT * totalSum)

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

# TODO: Spēles koks, kad depth <= 15 - 7 -> ģenerēt pilnu koku
class GameTree:
    # Saknes virsotne arī darbojas
    def __init__(self, root = GameNode("1", parent=None)):
        self.root = root

    def getRoot(self):
        return self.root

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

            # Simulē iespējamos spēles gājienus - Iterē pāri katram ciparam spēles virknē, ņemts nākošais, saskaita un pievieno spēles kokam
            for i in range(len(currentNumbers) - 1):
                currentNumber = currentNumbers[i]
                nextNumber = currentNumbers[i + 1]

                # Piešķir jaunā skaitļu virknes skaitļa vērtību un
                # Piešķir vai atņem attiecīgajam spēlētājam punktus atkarībā no skaitļu summas rezultāta
                if computerTurn:
                    newNumber, newComputerPoints = updatePoints(currentNumber + nextNumber, currentComputerPoints)
                    newPlayerPoints = currentPlayerPoints
                else:
                    newNumber, newPlayerPoints = updatePoints(currentNumber + nextNumber, currentPlayerPoints)
                    newComputerPoints = currentComputerPoints

                # Tikai priekš šīs virsotnes izdzēš apskatāmo ciparu un nākamo ciparu, to vietā ieliekot to summu
                newSetOfNumbers = currentNumbers.copy()
                newSetOfNumbers[i + 1] = newNumber
                newSetOfNumbers.pop(i)

                newName = f"{latestName}.{i}"

                # Uzģenerē jauno virsotni. Iestatot tās vecāku, nav nepieciešams to saglabāt
                newNode = GameNode(newName, newSetOfNumbers, newPlayerPoints, newComputerPoints, not computerTurn,
                         parent=currentNode)

                # Pievienot virsotni deka beigās, labajā pusē, lai vēlāk caurskatītu tālāk
                queue.append([newNode, currentDepth + 1])

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
print(tree.getRoot().children[0].evaluate_node())

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