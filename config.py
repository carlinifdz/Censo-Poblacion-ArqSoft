import customtkinter as ctk
from tkinter import ttk

mode = 1

if mode == 1:
    appearance = "dark"
    font_title = ("Arial", 18, "bold")
    font = ("Arial", 14)

    bg_color="#131313"
    frame_color="#282828"

    button_color = "#8500de"
    button_text_color = "#FFFFFF"

    text_color = "#ffffff"

    fg_color="#F0EEDE"

    pady = 5
    padx = 10

    corner_radius = 16
elif mode == 2:
    appearance = "light"
    font_title = ("Arial", 18, "bold")
    font = ("Arial", 14)

    bg_color="#FFFDEF"
    frame_color="#F0EEDE"

    button_color = "#d62828"
    button_text_color = "#FFFFFF"

    text_color = "#000000"

    fg_color="#F0EEDE"

    pady = 5
    padx = 10

    corner_radius = 16
