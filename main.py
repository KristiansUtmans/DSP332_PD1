class GameState:
    def __init__(self, sequence, score_player=0, score_opponent=0):
        self.sequence = sequence  # piemēram, [3, 1, 4, 2, 6, 5, ...]
        self.score_player = score_player
        self.score_opponent = score_opponent

    def is_terminal(self):
        # Spēle beidzas, ja ir viens skaitlis
        return len(self.sequence) == 1

    def get_possible_moves(self):
        moves = []
        # Piemērs: ja ir pāri skaitļu, var veikt saskaitīšanu vai dzēšanu
        # Šeit jāievieto loģika, kā veidot gājienus
        # Piemēram:
        if len(self.sequence) >= 2:
            # Gājiens: saskaitīt pirmo un otro skaitli
            new_sequence = self.sequence.copy()
            summed = new_sequence[0] + new_sequence[1]
            # Ja summa ir lielāka par 6, veic aizvietošanu (mod 6, vai kā definēts)
            new_sequence[0] = summed if summed <= 6 else (summed - 6)
            del new_sequence[1]
            moves.append(('sum', new_sequence))
        # Pievieno arī dzēšanas variantu, ja ir nepāru skaitlis
        if len(self.sequence) % 2 != 0:
            new_sequence = self.sequence.copy()
            # Dzēst pēdējo skaitli
            del new_sequence[-1]
            moves.append(('delete', new_sequence))
        return moves


class Node:
    def __init__(self, state, move=None, parent=None):
        self.state = state
        self.move = move  # Kādais gājiens novedusi uz šo stāvokli
        self.parent = parent
        self.children = []

    def expand(self):
        if self.state.is_terminal():
            return
        for move, new_seq in self.state.get_possible_moves():
            # Piemērs: ja gājiena rezultātā tiek mainīts spēlētāja punkti
            # Šeit vari pielāgot atbilstoši savam spēles noteikumam
            new_state = GameState(new_seq,
                                  self.state.score_player + (1 if move == 'sum' else 0),
                                  self.state.score_opponent - (1 if move == 'delete' else 0))
            child = Node(new_state, move, self)
            self.children.append(child)


# Rekursīva minimaksa funkcija
def minimax(node, depth, maximizing_player):
    if depth == 0 or node.state.is_terminal():
        # Atgriež heuristisko vērtējumu
        return evaluate_state(node.state)

    if maximizing_player:
        max_eval = float('-inf')
        node.expand()
        for child in node.children:
            eval = minimax(child, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        node.expand()
        for child in node.children:
            eval = minimax(child, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


def evaluate_state(state):
    # Heuristiskā novērtēšanas funkcija
    return state.score_player - state.score_opponent


# Piemērs, kā sākt spēli:
import random

# Ģenerē nejaušu skaitļu virkni garumā no 15 līdz 25, skaitļi no 1 līdz 6
length = random.randint(15, 25)
initial_sequence = [random.randint(1, 6) for _ in range(length)]
initial_state = GameState(initial_sequence)
root = Node(initial_state)

print("Sākotnējā skaitļu virkne:", initial_sequence)
print("Minimaksa vērtējums:", minimax(root, depth=3, maximizing_player=True))