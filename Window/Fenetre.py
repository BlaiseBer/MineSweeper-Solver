import tkinter as tk
from PIL import Image
from PIL import ImageTk
import os

class Fenetre(tk.Tk):
    def __init__(self, n, N, game):
        tk.Tk.__init__(self)

        self.n = n
        self.N = N
        self.game = game
        self.grid_frame = tk.Frame(self)

        #Dict to easily access images from their number
        self.images = {}
        filename = os.path.dirname(__file__)
        dir = os.path.join(filename, "minesweeper_icons")
        with os.scandir(dir) as d:
            for dirEntry in d:
                image = Image.open(dirEntry.path)
                image = image.resize((20, 20), Image.Resampling.LANCZOS)
                image = ImageTk.PhotoImage(image)
                self.images[os.path.basename(dirEntry.path)] = image

        self.init_widget()

    def init_widget(self):

        label = tk.Label(self, text="Grille")
        bouton = tk.Button(self, text="Suivant", command=lambda: (self.game.step(), self.update_grid()))
        bouton2 = tk.Button(self, text="Auto", command=lambda: (self.auto_solve(), self.update_grid()))
        label.pack()
        bouton.pack()
        bouton2.pack()

        #We chose options of the grid and update it for the first time
        self.grid_frame.configure(background="white")
        for i in range(self.N):
            for j in range(self.N):
                self.grid_frame.columnconfigure(i, weight=1)
                self.grid_frame.rowconfigure(i, weight=1)
        self.update_grid()

    def update_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Redraw images with current game state
        for i in range(self.N):
            for j in range(self.N):
                key = str(self.game.found.grid.get(i, j)) + '.jpg'
                label = tk.Label(self.grid_frame, image=self.images[key], padx=0, pady=0)
                label.grid(column=i, row=j, padx=0, pady=0, ipadx=0, ipady=0)
        self.grid_frame.pack()

    def auto_solve(self):
        if len(self.game.pile) > 0:
            self.after(0, self.game.step)
            self.after(0,self.update_grid)
            self.after(300, self.auto_solve)
        else:
            print("plus rien à jouer !")