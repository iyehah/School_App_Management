import tkinter as tk
from tkinter import ttk

class Settings:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill='both')
