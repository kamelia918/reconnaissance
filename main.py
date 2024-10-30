import tkinter
import customtkinter
from system_info import get_system_info_f1, display_system_info_f1
from memory_info import  get_memory_info_f2, display_memory_info_f2
from cpu_info import get_cpu_info, display_system_cpu_info_f3
from peripherals import get_system_perif, display_system_perif_f4

def create_scrollable_frame(parent, bg_color):
    canvas = tkinter.Canvas(parent, bg=bg_color)
    scrollable_frame = tkinter.Frame(canvas, bg=bg_color)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollbar = tkinter.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    return scrollable_frame

app = customtkinter.CTk()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}")  
app.title("Reconnaissance")
customtkinter.set_appearance_mode("system")
app.resizable(width=True, height=True)

top_frame = tkinter.Frame(master=app)
top_frame.pack(side="top", fill="both", expand=True)

bottom_frame = tkinter.Frame(master=app)
bottom_frame.pack(side="top", fill="both", expand=True)

frame1 = create_scrollable_frame(top_frame,"gray")
frame2 = create_scrollable_frame(top_frame, "gray")
frame3 = create_scrollable_frame(bottom_frame, "gray")
frame4 = create_scrollable_frame(bottom_frame, "gray")

display_system_info_f1(frame1)
display_memory_info_f2(frame2)
display_system_cpu_info_f3(frame3)
display_system_perif_f4(frame4)

app.mainloop()
