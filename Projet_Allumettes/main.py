from functools import partial
from time import sleep
from tkinter import *
from random import *


def display_welcome(event=None):
    frame_main.pack_forget()
    menu.pack_forget()
    menu_ai.pack_forget()
    
    welcome.pack(pady=175)

    
def display_menu_ai():
    menu.pack_forget()
    
    menu_ai.pack(expand=YES)


def hide_welcome():
    welcome.pack_forget()
    
    menu.pack(expand=YES)


def create(mode):
    menu.pack_forget()
    menu_ai.pack_forget()
    
    g = Game()
    g.create_game()
    
    if mode == "easy":
        g.ai.change_mode("easy")
        g.game_ai()
        
    elif mode == "hard":
        g.ai.change_mode("hard")
        g.game_ai()
        
    elif mode == "duo":
        g.game_duo()
        g.change_mode_game("duo")



window = Tk()
#
window.geometry("1366x768+50+50")
window.resizable(width=False, height=False)
window.title("STICK NEON")
window.config(bg="#000000")
#
img_font = PhotoImage(file="Allumette_img/font.gif")
img_stick = PhotoImage(file="Allumette_img/stick.gif")
img_hide = PhotoImage(file="Allumette_img/hide.gif")
img_cadre = PhotoImage(file="Allumette_img/rectangle.gif")
#
message = StringVar()
#
window.bind('<space>', display_welcome) 


font = Canvas(window, relief=FLAT, highlightbackground="#000000")
font.create_image(685, 385, image=img_font)
font.place(x=0, y=0, relwidth=1, relheight=1)

welcome = Frame(window, bg="#000000")
welcome.pack(pady=175)

title_welcome = Label(welcome, text="STICK NEON", font=("Courier New", 100), bg="#000000", fg="#FF66FF")
title_welcome.pack()

but_welcome = Button(welcome, text="CLICK TO START", font=("Courier New", 50), bg="#000000", fg="#FF66FF", pady=200, padx=270, borderwidth=0, activebackground="#000000", activeforeground="#FF66FF", command=hide_welcome)
but_welcome.pack()


menu = Frame(window, bg="#000000")

friend_but = Button(menu, text="DUO", font=("Courier New", 74), bg="#000000", fg="#FF66FF", activebackground="#FF66FF", activeforeground="#000000", borderwidth=0, padx=31, pady=55, command=partial(create,"duo"))
friend_but.grid(row=1, column=1, padx=40, pady=40)

ia_but = Button(menu, text="AI", font=("Courier New", 74), bg="#000000", fg="#FF66FF", activebackground="#FF66FF", activeforeground="#000000", borderwidth=0, padx=61, pady=55, command=display_menu_ai)
ia_but.grid(row=1, column=2, padx=40, pady=40)

menu.grid_columnconfigure(0, weight=1)
menu.grid_columnconfigure(3, weight=1)


menu_ai = Frame(window, bg="#000000")

easy_but = Button(menu_ai, text="EASY", font=("Courier New", 74), bg="#000000", fg="#FF66FF", activebackground="#FF66FF", activeforeground="#000000", borderwidth=0, padx=15, pady=75, command=partial(create, "easy"))
easy_but.grid(row=0, column=1, padx=40, pady=40)

hard_but = Button(menu_ai, text="HARD", font=("Courier New", 74), bg="#000000", fg="#FF66FF", activebackground="#FF66FF", activeforeground="#000000", borderwidth=0, padx=0, pady=75, command=partial(create, "hard"))
hard_but.grid(row=0, column=2, padx=40, pady=40)

menu_ai.grid_columnconfigure(0, weight=1)
menu_ai.grid_columnconfigure(3, weight=1)



frame_main = Frame(window, bg="#000000")


class Game():
    def __init__(self):
        self.allumettes = Allumette()
        self.consone = Consone()
        self.ai = Ai()
        
        self.mode_game = ""

        self.player_1 = "P1"
        self.player_2 = "AI"
        
        self.play = self.player_1
        
        self.nbr = 13
    
    
    def create_game(self):
        frame_main.pack(expand=YES)
        
        frame_buttons = Frame(frame_main, bg="red")
        frame_buttons.grid(row=1, column=1)

        but1 = Button(frame_buttons, text="1", font=("Courier New", 74), bg="#000000", fg="#FF66FF", activebackground="#FF66FF", activeforeground="#000000", borderwidth=0, padx=0, pady=25, command=partial(self.jouer_all,self.player_1,1))
        but1.grid(row=0, column=0)
        but2 = Button(frame_buttons, text="2", font=("Courier New", 74), bg="#000000", fg="#FF66FF", activebackground="#FF66FF", activeforeground="#000000", borderwidth=0, padx=0, pady=25, command=partial(self.jouer_all,self.player_1,2))
        but2.grid(row=0, column=1)
        but3 = Button(frame_buttons, text="3", font=("Courier New", 74), bg="#000000", fg="#FF66FF", activebackground="#FF66FF", activeforeground="#000000", borderwidth=0, padx=0, pady=25, command=partial(self.jouer_all,self.player_1,3))
        but3.grid(row=0, column=4)
        
        self.allumettes.create_allumette()
        self.consone.create_consone()
        
        self.consone.say_rules()
    
    
    def change_mode_game(self, mode):
        self.mode_game = mode         
    
    
    def jouer_all(self, name, n):
        x = 0
        nombre = self.allumettes.get_allumette()
        if nombre > 1 :
            for i in range(n):
                m = self.allumettes.get_allumette()
                
                self.allumettes.retirer_allumette()
                
                if m != self.allumettes.get_allumette():
                    x = x + 1
            
            if nombre == 13 :
                name = self.play
                
            elif self.mode_game == "duo":
                if self.play == self.player_1 :
                    self.play = self.player_2
                    name = self.player_2
                    
                else : 
                    self.play = self.player_1
                    name = self.player_1
                
            self.consone.write_all(name, x)
            self.verif(name)

    
    def verif(self, name):
        loser = ""
        if name == self.player_1 :
            loser = self.player_2
        else :
            loser = self.player_1
            
        if self.allumettes.get_allumette() < 2 :
            self.consone.say_end(loser)
    

    def game_ai(self):
        if self.allumettes.get_allumette() > 1 :
            if self.nbr != self.allumettes.get_allumette():
                sleep(0.5)
                    
                n = self.ai.calcule_retirer(self.allumettes.get_allumette())
                self.jouer_all("AI", n)
                
                self.nbr = self.allumettes.get_allumette()
                window.after(1000,self.game_ai)
         
            else :
                window.after(1000,self.game_ai)
    
    
    def game_duo(self):
        self.consone.delete_space()

        self.player_1 = self.consone.ask_name(1).upper()

        if self.player_1 == "" or self.player_1 == " ":
            self.player_1 = "P1"
        
        self.player_2 = self.consone.ask_name(2).upper()

        if self.player_2 == "" or self.player_2 == " ":
            self.player_2 = "P2"
        
        
        self.play = self.player_1
        
        self.consone.add("SYSTEM: Let's start " + self.player_1 + " !\n")



class Allumette():
    def __init__(self):        
        self.liste_allumette = []
        self.nombre = 0
        
        self.name = ""
    
    
    def create_allumette(self):
        self.frame_allumette = Frame(frame_main, bg="#000000", pady=50)
        self.frame_allumette.grid(row=0, column=0, columnspan=2)
        
        for i in range(1,14):
            canva = Canvas(self.frame_allumette, background="#000000", width=90, height=190,  highlightthickness=0)
            canva.create_image(45,100, image=img_stick, tags="teemo")
            canva.pack(side=LEFT)
            
            self.liste_allumette.append(canva)
        
        self.nombre = len(self.liste_allumette)
    
    
    def destroy_allumette(self):
        for w in self.frame_allumette.winfo_children():
            w.pack_forget()
    
    
    def retirer_allumette(self):
        if len(self.liste_allumette) > 1 :
            stick = self.liste_allumette.pop()
            stick.itemconfigure("teemo", image=img_hide)
    
    
    def get_allumette(self):
        return len(self.liste_allumette)



class Consone():
    def __init__(self): 
        self.texte = ""
        
    
    def create_consone(self):
        self.frame_com = Frame(frame_main, bg="#000000")
        self.frame_com.grid(row=1, column=0)

        cadre = Canvas(self.frame_com, width=647, height=313, highlightthickness=0)
        cadre.create_image(323,156, image=img_cadre)
        cadre.pack()

        self.frame_consone = Frame(self.frame_com, bg="#000000")
        self.frame_consone.place(x=40, y=40)

        dial = Message(self.frame_consone, textvariable=message, font=("Courier New", 18), width=558, background="#000000", foreground="#FF66FF")
        dial.pack()
    
    
    def add(self, t):
        if len(self.texte) > 180 :
            self.texte = ""
        
        self.texte = self.texte + ">>> " + t + "\n"
        message.set(self.texte)
    
    
    def delete_space(self):
        self.texte = message.get()[:-1]
        message.set(self.texte)
    
    
    def say_rules(self):
        self.add("SYSTEM: Play a game of Stick Neon. Remove one to three neons in turn. The person who removes the last neon loses. Here we go.\n")
    
    
    def say_end(self, p):
        self.texte =">>> SYSTEM: " + p + " lost the game.\n\n>>> SYSTEM: Press <ESPACE> to return to the menu."
        message.set(self.texte)
    
    
    def write_all(self,name, n):
        self.texte = message.get() + ">>> "
        
        if len(self.texte) > 185:
            self.texte = ">>> "
        
        if n == 1 :
            self.texte = self.texte + str(name) + ": pulled out " + str(n) + " neon.\n"
            message.set(self.texte)
        else :
            self.texte = self.texte + str(name) + ": pulled out " + str(n) + " neons.\n"
            message.set(self.texte)
    
    
    def ask_name(self, n):
        self.var = StringVar()
        
        self.asker = Frame(self.frame_consone, background="#000000")
        self.asker.pack(side=LEFT)

        lab = Label(self.asker, text=">>>", font=("Courier New", 18), background="#000000", foreground="#FF66FF")
        lab.pack(side=LEFT, padx=7)

        enter = Entry(self.asker, textvariable=self.var, font=("Courier New", 18), background="#000000", foreground="#FF66FF", borderwidth=0, insertbackground="#FF66FF", takefocus=1)
        enter.pack(side=LEFT)
        
        window.bind('<Return>', self.detruit)
        
        self.texte = message.get()
        self.texte = self.texte + "\n>>> SYSTEM: What's your name, Player " + str(n) + "?"
        message.set(self.texte)
        
        enter.focus_force()
        window.wait_window(self.asker)
        
        return self.var.get()
    
    
    def detruit(self, event=None):
        self.asker.destroy()

    


class Ai():
    def __init__(self):
        self.n = 3
        self.mode = "easy"
    
    
    def change_mode(self, mode):
        self.mode = mode
    
    
    def calcule_retirer(self, m):
        if self.mode == "easy":
            n = randrange(1,4)
            return n
        
        elif self.mode == "hard":
            n = m
            
            if n == 2 :
                return 1
            elif n == 3 :
                return 2
            elif n == 4 :
                return 3
            elif n == 6 :
                return 1
            elif n == 7 :
                return 2
            elif n == 8 :
                return 3
            elif n == 10 :
                return 1
            elif n == 11 :
                return 2
            elif n == 12 : 
                return 3
            else :
                return 1



window.mainloop()

# chosir allumette
# choisir qui commence (alétoire)