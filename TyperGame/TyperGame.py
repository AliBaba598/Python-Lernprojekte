import random
import tkinter as tk
import time as time

# zufälliger_buchstabe()

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ä', 'ö', 'ü']
word=[]
numbers=[1, 2, 3, 4, 5]
punkte=0

fenster=tk.Tk()
fenster.title("Random")

# Set the dimensions of the window
window_width = 400
window_height = 400

# Get the screen width and height
screen_width = fenster.winfo_screenwidth()
screen_height = fenster.winfo_screenheight()

# Calculate the x and y coordinates to center the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
fenster.geometry(f"{window_width}x{window_height}+{x}+{y}")

txt_ausgabe=tk.Entry(fenster, width=15, font=("Arial", 16), background="lightblue", state="readonly")
txt_ausgabe.pack(padx=20, pady=20, anchor="n")

txt_eingabe=tk.Entry(fenster, width=15, font=("Arial", 16))
txt_eingabe.pack(padx=20, pady=20, anchor="n")

txt_punkte=tk.Label(fenster,width=15, font=("Arial", 16), background="yellow", text=0)
txt_punkte.pack(padx=20, pady=20, anchor="n")

txt_timer=tk.Label(fenster, width=15, font=("Arial", 16), background="white", text=60)
txt_timer.pack(padx=20, pady=20, anchor="n")

# def timer():
#     for x in range(60):
#         time.after(1)
#         timerIndex=60
#         timerIndex-=1
#         txt_timer.config(text=timerIndex)
        

def generator():
    txt_ausgabe.config(state="normal")
    for letter in range(random.choice(numbers)):
        letter=random.choice(alphabet)
        word.append(letter)
    word_string=''.join(word)
    txt_ausgabe.insert(tk.END, word_string)
    txt_ausgabe.config(state="readonly")
generator()
    
def check():
    txt_ausgabe.config(state="normal")
    if txt_eingabe.get().strip()==txt_ausgabe.get().strip():
        word.clear()
        txt_ausgabe.delete(0, tk.END)
        generator()
        txt_eingabe.delete(0, tk.END)
        global punkte
        punkte+=1
        txt_punkte.config(text=punkte)
    else:
        eingabe=txt_eingabe.get().strip()
        txt_eingabe.delete(0, tk.END)
        txt_eingabe.insert(0, str(eingabe))
    txt_ausgabe.config(state="readonly")

fenster.bind('<space>', lambda event: check())
fenster.bind('<Return>', lambda event: check())
# fenster.bind('KeyPress', lambda event: timer())

def focus():
    txt_eingabe.focus()
    fenster.after(100, focus)
focus()

fenster.mainloop()