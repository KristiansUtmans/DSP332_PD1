from anytree import RenderTree, ContRoundStyle, NodeMixin
from collections import deque

# Heiristiskās funkcijas koeficienti

# Punktu izmaiņas koeficients
SCORE_DIFFERENCE_COEFFICIENT = 8
# Labo pāru koeficients
GOOD_PAIR_COEFFICIENT = 2
# Kopējā skaitļu koeficients
TOTAL_SUM_COEFFICIENT = 1
# Paredzamas labas spēles beigu koeficients
BENEFICIAL_ENDGAME_COEFFICIENT = 15

# Realizē gājiena punktu izmaiņas nosacījumus
def updatePoints(number, points):
    if number < 6:
        return number, points - 1
    else:
        return number - 6, points + 1

""" 
Koka virsotne, tiek mantota no NodeMixin
params:
name - Simbolu virkne, virsotnes nosaukums, tiek izmantota universālā adrešu sistēma
playerPoints - Skaitlis, Spēlētāja punkti šajā koka virsotnē
computerPoints - Skaitlis, Datora punkti šajā koka virsotnē
computerTurn - Būla vērtība, Vai šajā virsotnē ir datora gājiens
value - Skaitlis, heiristiskā virsotnes vērtība
parent - Atsauce uz vecāka virsotni
NodeMixin parametri, to ietvarā: children - Kopums ar virsotnēm, kas ir šīs virsotnes bērni
"""
class GameNode(NodeMixin):
    def __init__(self, name, setOfNumbers = None, computerTurn = True, playerPoints = 0, computerPoints = 0, value = None, parent = None):
        super().__init__()

        if setOfNumbers is None:
            setOfNumbers = []

        self.name = name
        self.setOfNumbers = setOfNumbers.copy()
        self.playerPoints = playerPoints
        self.computerPoints = computerPoints
        self.computerTurn = computerTurn
        self.parent = parent
        self.value = value

    def evaluate_node(self):
        # Heiristiskā novērtējuma funkcija
        goodPairs = 0
        badPairs = 0
        totalSum = self.setOfNumbers[0]

        # Ja
        if len(self.setOfNumbers) == 1:
            computerWin = self.computerPoints > self.playerPoints
            computerLoss = self.computerPoints < self.playerPoints
            print(self.computerPoints)
            print(self.playerPoints)
            if computerWin:
                return float('inf')
            elif computerLoss:
                return float('-inf')
            else:
                return 0

        for i in range(len(self.setOfNumbers) - 1):
            if self.setOfNumbers[i] + self.setOfNumbers[i + 1] > 6:
                goodPairs += 1
            else:
                badPairs += 1
            totalSum += self.setOfNumbers[i + 1]

        heuristicValue = (SCORE_DIFFERENCE_COEFFICIENT * (self.computerPoints - self.playerPoints) +
                GOOD_PAIR_COEFFICIENT * (goodPairs - badPairs) +
                TOTAL_SUM_COEFFICIENT * totalSum)

        if len(self.setOfNumbers) <= 3 and goodPairs == 1:
            heuristicValue = heuristicValue + BENEFICIAL_ENDGAME_COEFFICIENT

        return heuristicValue

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getSetOfNumbers(self):
        return self.setOfNumbers

    def getPlayerPoints(self):
        return self.playerPoints

    def getComputerPoints(self):
        return self.computerPoints

    def isComputerTurn(self):
        return self.computerTurn

    def isEndOfGame(self):
        return len(self.setOfNumbers) == 1

    # Minmax algoritms
    def minmax(self, depth, maximizingPlayer):
        # Ja ir sasniegts strupceļš vai maksimālais dziļums,
        # tad tiek noteikta virsotnes vērtība izmantojot heiristisko funkciju
        if depth == 0 or self.isEndOfGame():
            self.value = self.evaluate_node()
            return self.value

        # Ja spēlētājs ir maksimizētājs, tiek dabūta maksimālā heiristiskā vērtība
        if maximizingPlayer:
            maxNodeValue = float('-inf')
            for childNode in self.children:
                nodeValue = childNode.minmax(depth - 1, False)
                maxNodeValue = max(maxNodeValue, nodeValue)
            self.setValue(maxNodeValue)
            return maxNodeValue

        # Ja spēlētājs ir minimizētājs, tiek dabūta minimālā heiristiskā vērtība
        else:
            minNodeValue = float('inf')
            for childNode in self.children:
                nodeValue = childNode.minmax(depth - 1, True)
                minNodeValue = min(minNodeValue, nodeValue)
            self.setValue(minNodeValue)
            return minNodeValue

    # Alfa-Beta algoritms:
    # Principā strādā tāpat kā min-max algoritms,
    # tikai loki uz virsotnēm, kuru vērtējums neietekmēs virsotnes vērtējumu tiek nogriezti
    def alphaBeta(self, depth, alpha, beta, maximizingPlayer):
        # Ja ir sasniegts strupceļš vai maksimālais dziļums,
        # tad tiek noteikta virsotnes vērtība izmantojot heiristisko funkciju
        if depth == 0 or self.isEndOfGame():
            self.value = self.evaluate_node()
            return self.value

        # Ja spēlētājs ir maksimizētājs, tiek dabūta maksimālā heiristiskā vērtība
        if maximizingPlayer:
            maxNodeValue = float('-inf')
            for childGameNode in self.children:
                nodeValue = childGameNode.minmax(depth - 1, False)
                maxNodeValue = max(maxNodeValue, nodeValue)
                alpha = max(alpha, nodeValue)
                if beta <= alpha:
                    break
            self.value = maxNodeValue
            return maxNodeValue

        # Ja spēlētājs ir minimizētājs, tiek dabūta maksimālā heiristiskā vērtība
        else:
            minNodeValue = float('inf')
            for childGameNode in self.children:
                nodeValue = childGameNode.minmax(depth - 1, True)
                minNodeValue = min(minNodeValue, nodeValue)
                beta = min(beta, nodeValue)
                if beta <= alpha:
                    break
            self.value = minNodeValue
            return minNodeValue


class GameTree:
    # Saknes virsotne arī darbojas
    def __init__(self, root = GameNode("1", parent=None), maxDepth = 0):
        self.root = root
        self.maxDepth = maxDepth

    def getRoot(self):
        return self.root

    # Koka ģenerēšana līdz noteiktam dziļumam
    def generateGameTree(self):
        print("Generating tree")

        # Pārlūkošana izmantojot BFS algoritmu, izmantojot deku(rinda no abām pusēm pārlūkojama)
        queue = deque([[self.root, 0]])

        while queue:
            # Pievienotās virsotnes apskatām no deka kreisās puses
            currentNode, currentDepth = queue.popleft()

            # Ja ir sasniegts dziļums vai spēles beigas šajā ceļā, tad izlaist šo virsotni
            if currentDepth >= self.maxDepth or len(currentNode.getSetOfNumbers()) == 1:
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
                newNode = GameNode(newName, newSetOfNumbers, not computerTurn, newPlayerPoints, newComputerPoints,
                         parent=currentNode)

                # Pievienot virsotni deka beigās, labajā pusē, lai vēlāk caurskatītu tālāk
                queue.append([newNode, currentDepth + 1])

    def updateTreeWithMinMaxValues(self):
        self.root.minmax(self.maxDepth, self.root.isComputerTurn())

    def updateTreeWithAlphaBetaValues(self):
        self.root.alphaBeta(self.maxDepth, float('-inf'), float('inf'), self.root.isComputerTurn())


    # Pārlūko koka saknes tuvākās virsotnes un atgriež labākā gājiena(priekš datora) skaitļa virkni
    def getMinMaxBestMove(self):
        bestMove = None
        bestValue = float('-inf')
        for child in self.root.children:
            if child.getValue() > bestValue:
                bestMove = child

        return bestMove.getSetOfNumbers()

startNode = GameNode("1", [1,2,3,4,5,6,5,3,2,1], True)
tree = GameTree(startNode, 4)
tree.generateGameTree()
# print(RenderTree(startNode, style=ContRoundStyle()).by_attr(attrname="name"))
# print(tree.getRoot().children[0].evaluate_node())
# print(tree.getRoot().minmax(tree.maxDepth, tree.getRoot().isComputerTurn()))
tree.updateTreeWithMinMaxValues()
print(RenderTree(startNode, style=ContRoundStyle()).by_attr(attrname="value"))

print(tree.getMinMaxBestMove())