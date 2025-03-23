'''
Ignorēt šo failu pagaidām, tas ir eksemplārs, vienkārši min-max algoritma piemērs
'''

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
    # Heiristiskā novērtēšanas funkcija
    return state.score_player - state.score_opponent


# Piemērs, kā sākt spēli:
import random

# Ģenerē nejaušu skaitļu virkni garumā no 15 līdz 25, skaitļi no 1 līdz 6

# User input:
length = random.randint(15, 25)
initial_sequence = [random.randint(1, 6) for _ in range(length)]