import tkinter as tk
from tkinter import messagebox

from anytree import RenderTree, ContRoundStyle

from gameTree import GameNode, GameTree  # Ja izmainās file nosaukums šo vajag update!!!!!
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

    # Izveido pogas priekš current_sequence
    global sequence_buttons
    sequence_buttons = []  # Notīra sequence_buttons sarakstu

    # Izveido pogas no ģenerētas virknes
    if current_sequence:  # Veido pogas ja virkne nav tukša
        for i, num in enumerate(current_sequence):
            btn = tk.Button(sequence_frame, text=str(num), width=4, height=2, command=lambda i=i: handle_button_click(i))
            btn.pack(side="left", padx=4, pady=4)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            sequence_buttons.append(btn)
    # Parāda šobrīdējos rezultātus
    score_label.config(text=f"Player: {player_score}  |  Opponent: {opponent_score}")
    
def show_final_page():
    rules_frame.pack_forget()
    input_frame.pack_forget()
    game_frame.pack_forget()
    algorithm_frame.pack_forget()
    final_frame.pack(pady=20)


def computer_move():
    global current_sequence, player_score, opponent_score, turn, user_input
    
    if len(current_sequence) <= 1:
        return  # Pārtrauc spēli ja virkne ir <=1
        
    # No spēlētāja ievadītā dabū algoritma parmeklēšanas dziļumu
    search_depth = int(depth_input.get())  

   
    # Izveido GameNode ar ģenerēto virkni
    start_node = GameNode("1", current_sequence, True, player_score, opponent_score)
    
    # Uztaisa un ģenerē spēles koku
    game_tree = GameTree(start_node, search_depth)
    game_tree.generateGameTree()

    
    # Izmanto atbilstoši izvēlēto spēlētāja pārmeklēšanas algoritmu
    if algorithm_choice.get() == 1:  # Min-Max
        game_tree.updateTreeWithMinMaxValues()
    elif algorithm_choice.get() == 2:  # Alpha-Beta
        game_tree.updateTreeWithAlphaBetaValues()
    else:
        messagebox.showerror("Kļūda", "Nav izvēlēts pārmeklēšanas algoritms.")
        return

    print(RenderTree(game_tree.getRoot(), style=ContRoundStyle()).by_attr(attrname="heuristicValue"))

    # Dabū labāko gājienu priekš daotra
    new_sequence = game_tree.getBestMove()
    
    if new_sequence:
        # Atjauno spēles gaitu
        opponent_score += 1  # Pieskaita datoram punktu par gājiena veikšanu
        current_sequence = new_sequence
        turn = "player"
        
        show_game_page()
        
        # Pārbaude spēles beigas
        if len(current_sequence) == 1:
            check_game_end()
    else:
        messagebox.showinfo("Kļūda", "Dators nevar atrast nevienu gājienu.")
        turn = "player"  # Ja dators nevar veikt gājienu, gājiens tiek atdots spēlētājam

def handle_button_click(index):
    global current_sequence, selected_indices,selected_buttons, player_score, opponent_score, turn

    if len(selected_indices) < 2:
        selected_indices.append(index)
        sequence_buttons[index].config(bg="yellow")
        #selected_buttons.add(sequence_buttons[index])  # Saglabā atzīmētās pogas

    if len(selected_indices) == 2:
        i1, i2 = selected_indices
        if abs(i1 - i2) == 1 and (min(i1, i2) % 2 == 0):  # Pārliecinās lai būtu atzīmēti pāri būtu 1-2, 3-4, 5-6,...
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
            #selected_buttons.clear()  # Atzīmēto pogu notīrīšana
            show_game_page()

            if len(current_sequence) == 1:
                check_game_end()  # Izsauc end game fukciju
            elif turn == "opponent":  # Datora gājiens pēc aizkaves
                window.after(500, computer_move)
        else:
            messagebox.showinfo("Nepareizs pāris", "Lūdzu izvēlaties pārus (1-2, 3-4, 5-6,...).")
            selected_indices.clear()
            #selected_buttons.clear()  # Atzīmēto pogu notīrīšana
            show_game_page()


# Funkcija lai pārbaudītu spēles beigas 
def check_game_end():
    if len(current_sequence) == 1:
        winner = "Player" if player_score > opponent_score else "Opponent"
        messagebox.showinfo("Game Over", f"Game Over!\n{winner} wins!")
        score_label2.config(text=f"Player: {player_score}  |  Opponent: {opponent_score}")
        show_final_page()

def on_enter(e):
  #if e.widget not in selected_buttons:
    e.widget.config(bg="lightblue")  # Krāsa uz pogas hover

def on_leave(e):
 # if e.widget not in selected_buttons:
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

        if turn == "opponent":
            window.after(500, computer_move)  # Aizkave priekš AI gājiena

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
            print(f"Initial sequence: {current_sequence}")  # Izvada random virki
            
            

            # Pārbauda un izvada vai ir ievadīts spēlētājs
            if selected_choice.get() == 2:
                print("Spēlētājs: Dators")
                player_score = 0
                opponent_score = 0
                turn = "opponent"  # Opponent starts first
                show_algorithm_page()
                #window.after(500, computer_move)  # Delay to let the UI update
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

# ----------Pirmā lapa(Noteikumi)----------
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


# ----------Otrā lapa(Spēles izveide)----------
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

# ----------Trešā lapa(Algoritma un dzilima izvēle)----------
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

# ----------Ceturtā lapa(Spēle)----------
game_frame = tk.Frame(window)
sequence_frame = tk.Frame(game_frame)
sequence_frame.pack(pady=20)

current_sequence = []  # Inicializē atzīmēto pogu skaitu kā tukšu (sākotnēji)

selected_indices = []  # Atzīmēto pogu glabāšana
sequence_buttons = []  # Saglabā atzīmētās pogas priekš spēles gaitas atjaunošanas

# Rezultātu parādīšana ekrānā
score_label = tk.Label(game_frame, text="Player: 0  |  Opponent: 0", font=("Arial", 16))
score_label.pack(pady=10)

# ----------Fināla lapa(Izvadīti rezultāti un atkārtot spēli)----------
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
