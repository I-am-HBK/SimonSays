import tkinter as tk
import random
from functools import partial

class Simon:
    IDLE = ('red', 'blue', 'green', 'yellow')
    TINTED = ('maroon', 'navy', 'darkgreen', 'olive')

    FLASH_ON = 900  #ms
    FLASH_OFF = 400  #ms

    def __init__(self, title='Simon'):
        self.master = tk.Tk()
        self.master.title(title)
        self.master.resizable(False, False)
        self.title = title
        self.buttons = [
            tk.Button(
                self.master,
                height=15,
                width=25,
                background=c,
                command=partial(self.push, i))
            for i, c in enumerate(self.IDLE)]
        for i, button in enumerate(self.buttons):
            button.grid({'column': i % 2, 'row': i // 2})
        self.b=tk.Button(self.master,text="Start new game",
                         command=lambda:[self.master.title('SimonSays: New Game'),self.reset()])
        self.b.grid({'column':0,'row':2,'columnspan':2})
        
        
    def reset(self):
        self.sequence = []
        self.new_color()

    def push(self, index):
        if index == self.current:
            try:
                self.current = next(self.iterator)
            except StopIteration:
                self.master.title('{} - Score: {}'
                                  .format(self.title, len(self.sequence)))
                self.new_color()
        else:
            self.master.title('{} - Game Over! | Final Score: {}'
                              .format(self.title, len(self.sequence)))
            self.reset()

    def new_color(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        color = random.randrange(0, len(self.buttons))
        self.sequence.append(color)
        self.iterator = iter(self.sequence)
        self.show_tile()

    def show_tile(self):
        try:
            id = next(self.iterator)
        except StopIteration:
            # No more tiles to show, start waiting for user input
            self.iterator = iter(self.sequence)
            self.current = next(self.iterator)
            for button in self.buttons:
                button.config(state=tk.NORMAL)
        else:
            self.buttons[id].config(background=self.TINTED[id])
            self.master.after(self.FLASH_ON, self.hide_tile)

    def hide_tile(self):
        for button, color in zip(self.buttons, self.IDLE):
            button.config(background=color)
        self.master.after(self.FLASH_OFF, self.show_tile)

    def run(self):
        self.reset()
        self.master.mainloop()


if __name__ == '__main__':    
    game = Simon()
    game.run()