import tkinter

class Card(tkinter.Tk):
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value