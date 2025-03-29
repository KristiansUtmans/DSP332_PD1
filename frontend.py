import tkinter as tk
from tkinter import messagebox
from main import GameNode, GameTree, evaluate_node  # Ja izmainās file nosaukums šo vajag update!!!!!
import random

def show_rules_page():
    input_frame.pack_forget()
    game_frame.pack_forget()
    final_frame.pack_forget()
    algorithm_frame.pack_forget()
    rules_frame.pack(pady=20)

def show_input_page():
    rules_frame.pack_forget()
    game_frame.pack_forget()
    final_frame.pack_forget()
    algorithm_frame.pack_forget()
    input_frame.pack(pady=20)

def show_algorithm_page():
    rules_frame.pack_forget()
    game_frame.pack_forget()
    final_frame.pack_forget()
    algorithm_frame.pack(pady=20)
    input_frame.pack_forget()

def show_game_page():
    rules_frame.pack_forget()
    input_frame.pack_forget()
    final_frame.pack_forget()
    algorithm_frame.pack_forget()
    game_frame.pack(pady=20)

    # Notīra vecās pogas
    for widget in sequence_frame.winfo_children():
        widget.destroy()

    # Create buttons for the current sequence
    global sequence_buttons
    sequence_buttons = []  # Reset the sequence_buttons list

    # Izveido pogas no ģenerētas virknes
    if current_sequence:  # Veido pogas ja virkne nav tukša
        for i, num in enumerate(current_sequence):
            btn = tk.Button(sequence_frame, text=str(num), width=4, height=2, command=lambda i=i: handle_button_click(i))
            btn.pack(side="left", padx=4, pady=4)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            sequence_buttons.append(btn)
    # Display current scores
    score_label.config(text=f"Player: {player_score}  |  Opponent: {opponent_score}")
    
def show_final_page():
    rules_frame.pack_forget()
    input_frame.pack_forget()
    game_frame.pack_forget()
    algorithm_frame.pack_forget()
    final_frame.pack(pady=20)

# Function to handle button click
def handle_button_click(index):
    global current_sequence, selected_indices,selected_buttons, player_score, opponent_score, turn

    if len(selected_indices) < 2:
        selected_indices.append(index)
        sequence_buttons[index].config(bg="yellow")
        selected_buttons.add(sequence_buttons[index])  # Store selected button

    if len(selected_indices) == 2:
        i1, i2 = selected_indices
        if abs(i1 - i2) == 1 and (min(i1, i2) % 2 == 0):  # Ensures pairs are 1st-2nd, 3rd-4th, etc.
            num1 = current_sequence[i1]
            num2 = current_sequence[i2]
            combined_value = num1 + num2 if num1 + num2 <= 6 else (num1 + num2 - 6)
            current_sequence = current_sequence[:min(i1, i2)] + [combined_value] + current_sequence[max(i1, i2) + 1:]

            if turn == "player":
                player_score += 1
            else:
                opponent_score += 1

            turn = "opponent" if turn == "player" else "player"
            selected_indices.clear()
            selected_buttons.clear()  # Reset selected buttons set
            show_game_page()
            #check_game_end()

            if len(current_sequence) == 1:
                check_game_end()  # Call game over function **immediately**
            elif turn == "opponent":
                window.after(500, computer_move)
        else:
            messagebox.showinfo("Error", "Please select a valid adjacent pair (1st-2nd, 3rd-4th, etc.).")
            selected_indices.clear()
            selected_buttons.clear()  # Clear selected button tracking
            show_game_page()

def computer_move():
    global current_sequence, player_score, opponent_score, turn

    if len(current_sequence) == 1:
        check_game_end()
        return

    for i in range(0, len(current_sequence) - 1, 2):
        num1 = current_sequence[i]
        num2 = current_sequence[i + 1]
        combined_value = num1 + num2 if num1 + num2 <= 6 else (num1 + num2 - 6)
        current_sequence = current_sequence[:i] + [combined_value] + current_sequence[i + 2:]
        opponent_score += 1
        break  # Only make one move per turn

    # Remove unpaired number if necessary
    if len(current_sequence) % 2 != 0:
        current_sequence.pop()
        player_score -= 1  # Penalize the opponent (player)

    turn = "player"
    show_game_page()
    window.after(500, check_game_end)
# Initialize selected_buttons as a set
selected_buttons = set()


# Function to check if the game should end
def check_game_end():
    if len(current_sequence) == 1:
        winner = "Player" if player_score > opponent_score else "Opponent"
        messagebox.showinfo("Game Over", f"Game Over!\n{winner} wins!")
        score_label2.config(text=f"Player: {player_score}  |  Opponent: {opponent_score}")
        show_final_page()

# Function to process and update the sequence (combining pairs, removing unpaired)
def process_sequence():
    global current_sequence, player_score, opponent_score

    new_sequence = []
    # Process pairs
    for i in range(0, len(current_sequence) - 1, 2):
        num1 = current_sequence[i]
        num2 = current_sequence[i + 1]
        combined_value = num1 + num2
        if combined_value > 6:
            combined_value = combined_value - 6
        new_sequence.append(combined_value)
        player_score += 1  # Player gets 1 point for combining pairs

    # If there is an unpaired number, remove it and subtract from opponent's score
    if len(current_sequence) % 2 != 0:
        new_sequence.append(current_sequence[-1])
        opponent_score -= 1  # Subtract 1 point from the opponent

    current_sequence = new_sequence
    show_game_page()  # Refresh the game view

def on_enter(e):
  if e.widget not in selected_buttons:
    e.widget.config(bg="lightblue")  # Krāsa uz pogas hover

def on_leave(e):
  if e.widget not in selected_buttons:
    e.widget.config(bg="SystemButtonFace")  # Reset pogas krāsai kad nav hover

def submit_algorithm_settings():
    try:
        depth = int(depth_input.get())
        user_value = int(user_input.get())
        if user_value > 18:
            if depth > 3:
                messagebox.showerror("Virknēm virs 18, maksimālais dziļums 3.")
                return
        else:
            if depth > 5:
                messagebox.showerror("Virknēm 18 vai mazāk, maksimālais dziļums 5.")
                return

        if algorithm_choice.get() == -1:
               
                messagebox.showerror("Kļūda", "Nav izvēlēts algoritms")
                algorithm_frame.pack(pady=20)
                return

        show_game_page() 

    except ValueError:
        messagebox.showerror("Nepareizs skaitlis", "Lūdzu ievadiet pareizu skaitli priekš algoritma dziļuma")



def submit_input():
    global current_sequence, player_score, opponent_score, turn

    rules_frame.pack_forget()
    input_frame.pack_forget() 
    try:
        # Pārveido ievadīto uz int vērtību
        user_value = int(user_input.get())  
        if 15 <= user_value <= 25:  # Pārbauda vai pārveidotā ievadītā vērtiba ir iekš (15-25)
            if selected_choice.get() == -1:
                print("Spēlētājs: Nav izvēlēts")
                messagebox.showerror("Kļūda", "Nav izvēlēts spēlētājs")
                input_frame.pack(pady=20)
                return
            
            # Ģenerē random spēles virkni
            global current_sequence
            current_sequence = [random.randint(1, 6) for _ in range(user_value)]  # Generate random sequence
            print(f"Initial sequence: {current_sequence}")
            
            # You could call a function from your main.py to start the game with this sequence
            initial_state = GameNode("1", current_sequence)
            game_tree = GameTree(initial_state)
            game_tree.generateGameTree(2)
            # JA VAJAG IZVADĪT MIN-MAX ŠIS JĀSATAISA!!!:
            #minimax_result = main.minimax(main.Node(initial_state), depth=3, maximizing_player=True)
            #print(f"Minimaksa vērtējums: {minimax_result}")
            
            # Izvada min-max līmeni ekrānā(nezinu vai vajadzīgs?)
             #result_label.config(text=f"Minimaksa vērtējums: {minimax_result}")

            # Pārbauda un izvada vai ir ievadīts spēlētājs
            if selected_choice.get() == 2:
                print("Spēlētājs: Dators")
                player_score = 0
                opponent_score = 0
                turn = "opponent"  # Opponent starts first
                show_algorithm_page()
                window.after(500, computer_move)  # Delay to let the UI update
            else:
                print("Spēlētājs: Spēlētājs")
                player_score = 0
                opponent_score = 0
                turn = "player"
                show_algorithm_page()
        else:
            # Parāda error, ja ievade nebija (15-25)
            messagebox.showerror("Nepareizs skaitlis", "Ievadiet skaitli starp 15 un 25!")
            user_input.delete(0, tk.END)  # Notīra ievades lauku un sāk no jauna
            input_frame.pack(pady=20)
            
    except ValueError:
        # Parāda error, ja tiek ievadīta vērtība kas nav skaitlis
        messagebox.showerror("Nepareizs ievads", "Ievadiet derīgu skaitli!")
        user_input.delete(0, tk.END)  # Notīra ievades lauku un sāk no jauna
        input_frame.pack(pady=20)

window = tk.Tk()
window.title("1.praktiskais darbs")
window.geometry("1000x400")

# -----Pirmā lapa(Noteikumi)-----
rules_frame = tk.Frame(window)

rules_text = """Spēles noteikumi:

1. Ievadīt virknes garumu robežās (15-25)
2. Izvēlies, kurš spēlē pirmais — spēlētājs vai dators.
3. Spēles sākumā ir dota ģenerētā skaitļu virkne.Spēlētāji izpilda gājienus pēc kārtas.
   Katram spēlētājam ir 0 punktu. 
   Gājiena laikā spēlētājs var:  
        1.askaitīt skaitļu pāri (pirmo ar otro, trešo ar ceturto, piekto ar sesto)
            un summu ierakstīt saskaitīto skaitļu pāra vieta vietā 
            (ja summa ir lielāka par 6, tad notiek aizvietošanas: 7 = 1, 8 = 2, 9 = 3, 10 = 4, 11=5, 12=6),
            kā arī pieskaitīt savam punktu skaitam 1 punktu, vai 
        2.nodzēst to skaitli, kas ir palicis bez pāra un atņemt vienu punktu no pretinieka punktu skaita.  
4.Spēle beidzas, kad skaitļu virknē paliek viens skaitlis. Uzvar spēlētājs, kam ir vairāk punktu. 


                                Spied 'Sapratu', lai turpinātu.
"""

rules_label = tk.Label(rules_frame, text=rules_text, justify="left", wraplength=700, anchor="n")
rules_label.pack(pady=20)

accept_button = tk.Button(rules_frame, text="Sapratu", command=show_input_page)
accept_button.pack(pady=10)
accept_button.bind("<Enter>", on_enter)
accept_button.bind("<Leave>", on_leave)

rules_frame.pack(pady=20)


# -----Otrā lapa(Spēles izveide)-----
input_frame = tk.Frame(window)

# Virsraksts virs iesnieguma
input_label = tk.Label(input_frame, text="Ievadi virknes garumu (15-25):")
input_label.pack(pady=5)

# Ievades lauks
user_input = tk.Entry(input_frame, width=30)
user_input.pack(pady=5)

# Izvēlētais pirmais spēlētājs = selected_choice

selected_choice = tk.IntVar(value=-1)


# Spēlētāja izvēle (Spēlētājs vai dators)
radio_button_1 = tk.Radiobutton(input_frame, text="Spēlētājs", variable=selected_choice, value=1)
radio_button_1.pack(pady=5)
radio_button_1.bind("<Enter>", on_enter)
radio_button_1.bind("<Leave>", on_leave)


radio_button_2 = tk.Radiobutton(input_frame, text="Dators", variable=selected_choice, value=2)
radio_button_2.pack(pady=5)
radio_button_2.bind("<Enter>", on_enter)
radio_button_2.bind("<Leave>", on_leave)


# Iesniegšanas poga
submit_button = tk.Button(input_frame, text="Next", command=submit_input)
submit_button.pack(pady=5)
submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)

# Min-max izvade 
 #result_label = tk.Label(window, text="")
 #result_label.pack(pady=10)

# -----Trešā lapa(Algoritma un dzilima izvēle)-----
algorithm_frame = tk.Frame(window)
algorithm_label = tk.Label(algorithm_frame, text="Ievadi algoritma dziļumu:")
algorithm_label.pack(pady=5)

# Algoritma dziļuma ievade (pagaidām tik skaitļi jāuztaisa pārbaude vai nav burti!!!!!!!!!)
depth_input = tk.Entry(algorithm_frame, width=30)
depth_input.pack(pady=5)


algorithm_label_2 = tk.Label(algorithm_frame, text="Izvēlies algoritmu:")
algorithm_label_2.pack(pady=5)

algorithm_choice = tk.IntVar(value=-1)

radio_button_1 = tk.Radiobutton(algorithm_frame, text="Min-Max", variable=algorithm_choice, value=1)
radio_button_1.pack(pady=5)
radio_button_1.bind("<Enter>", on_enter)
radio_button_1.bind("<Leave>", on_leave)


radio_button_2 = tk.Radiobutton(algorithm_frame, text="Alpha-Beta", variable=algorithm_choice, value=2)
radio_button_2.pack(pady=5)
radio_button_2.bind("<Enter>", on_enter)
radio_button_2.bind("<Leave>", on_leave)

submit_algorithm_button = tk.Button(algorithm_frame, text="Apstiprināt", command=submit_algorithm_settings)
submit_algorithm_button.pack(pady=10)




# -----Ceturtā lapa(Spēle)-----
game_frame = tk.Frame(window)
sequence_frame = tk.Frame(game_frame)
sequence_frame.pack(pady=20)

current_sequence = []  # Initialize the sequence as empty initially

selected_indices = []  # To track selected button indices
sequence_buttons = []  # To store the button references for updating

# For displaying score
score_label = tk.Label(game_frame, text="Player: 0  |  Opponent: 0", font=("Arial", 16))
score_label.pack(pady=10)

# -----Fināla lapa(Izvadīti rezultāti un atkārtot spēli)-----
final_frame = tk.Frame(window)

header_label = tk.Label(final_frame, text="Gala rezultāti:", font=("Arial", 20))
header_label.pack(pady=5)

score_label2 = tk.Label(final_frame, text="Player: 0  |  Opponent: 0", font=("Arial", 16))
score_label2.pack(pady=20)

def reset():
    show_input_page()
    user_input.delete(0, tk.END)
    selected_choice.set(-1) 

next_button = tk.Button(final_frame, text="Next Game", command=reset)
next_button.pack(pady=5, fill="x")
next_button.bind("<Enter>", on_enter)
next_button.bind("<Leave>", on_leave)

finish_button = tk.Button(final_frame, text="Finish", command=window.quit)
finish_button.pack(pady=5, fill="x")
finish_button.bind("<Enter>", on_enter)
finish_button.bind("<Leave>", on_leave)


window.mainloop()
