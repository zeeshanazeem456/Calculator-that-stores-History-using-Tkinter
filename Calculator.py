import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from math import sqrt
import os

history_file = os.path.join(os.path.dirname(__file__), "history.txt")
buttons = [
    ["AC","+/-","%","÷"],
    ["7","8","9","x"],
    ["4","5","6","-"],
    ["1","2","3","+"],
    ["0",".","√","="],
]
right_symbol = ["÷","x","-","+","=","√"]
top_symbol = ["AC","+/-","%"]

#Performing funcitonalities
A = '0'
operator = None
B = '0'

color_gray = "#D4D4D2"
color_black = 'black'
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

row_count = len(buttons)
button_in_one_row = len(buttons[0])

def update_history():
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history_text = f.read()
    except FileNotFoundError:
        history_text = ""

    history_label.config(state='normal')
    history_label.delete("1.0", tk.END)
    history_label.insert(tk.END, history_text)
    history_label.config(state='disabled')

def write_to_history(calculation):
    with open(history_file, "a", encoding="utf-8") as f:  
        f.write(calculation + "\n")
    update_history()

def ClearAll():
    global A,B,operator
    A = '0'
    operator = None
    B = '0'
    label["text"] = '0' 

def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)

def button_clicked(value):
    global right_symbols,top_symbols,label,A,B,operator

    if value == '√':
        try:
            current = float(label["text"])
            if current < 0:
                label["text"] = "Error"
                write_to_history(f"√({current}) = Error")
            else:
                result = sqrt(current)  
                cleaned_result = remove_zero_decimal(result)
                label["text"] = cleaned_result
                write_to_history(f"√({current}) = {cleaned_result}")
                A = cleaned_result
                B = '0'
                operator = None
        except Exception as e:
            label["text"] = "Error"
            write_to_history("√(Invalid Input) = Error")
        return  # Stop further logic


    if value in right_symbol:
        if value == '=':
            if A is not None and operator is not None:
                B = label["text"]
                numA = float(A)
                numB = float(B)
                if operator == "+":
                    label["text"] = str(numA + numB)
                elif operator == "-":
                    label["text"] = remove_zero_decimal(numA - numB)
                elif operator == 'x':
                    label["text"] = remove_zero_decimal(numA * numB)
                elif operator == "÷":
                    if numB != 0:
                        label["text"] = remove_zero_decimal(numA / numB)
                    else:
                        label["text"] = "Error"
                calculation = f"{A} {operator} {B} = {label['text']}"
                # Write the calculation to history.txt
                write_to_history(calculation)
                A = label["text"]  
                operator = None
                B = '0' 
        if value in "-+x÷":
            if operator is None:
                A = label["text"]
                label["text"] = "0"
                B = "0"
            operator = value

    elif value in top_symbol: 
        if value == 'AC':
            ClearAll()
            label["text"] = '0'
        elif value == '+/-':
            result = float(label['text']) * -1
            label["text"] = remove_zero_decimal(result)
        elif value == '%':
            result = float(label["text"]) / 100
            label["text"] = remove_zero_decimal(result)
    else:
        if value == '.':
            if value not in label["text"]:
                label["text"] += value
        elif value in "0123456789":
            if label["text"] == '0':
                label["text"] = value
            else:
                label["text"] += value
        if A != '0' and operator is None:
            A = label["text"]
            ClearAll()
            label["text"] = value

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Calculator")
    window.resizable(False,False)

    #Frame
    frame = tk.Frame(window)
    label = tk.Label(frame,text = "0",font = ("Comicsans",45),bg = color_black,fg=color_white,anchor='e',width=button_in_one_row)
    label.grid(row=0,column=0,columnspan=button_in_one_row,sticky='we')

    #Adding buttons in the calculator
    for row in range(row_count):
        for column in range(button_in_one_row):
            value = buttons[row][column]
            button = tk.Button(frame,text= value,font = ("Comicsans",30),width = button_in_one_row - 1,height = 1,command=lambda value=value: button_clicked(value))
            #Adding colors to the buttons
            if value in top_symbol:
                button.config(bg=color_gray,fg=color_black)
            elif value in right_symbol:
                button.config(background=color_orange,foreground=color_white)
            else:
                button.config(fg=color_white,background=color_dark_gray)
            button.grid(row = row+1,column = column)
    frame.pack(side=tk.LEFT)

    # History frame
    history_frame = tk.Frame(window, bg="white")
    history_label_title = tk.Label(history_frame, text="History", font=("Comicsans", 18, "bold"), bg="white", fg="black")
    history_label_title.pack(pady=(10, 0))

    history_label = ScrolledText(history_frame, width=30, height=20, font=("Comicsans", 14), bg="white", state='disabled')
    history_label.pack(padx=10, pady=10)

    history_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

    window.update()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_x = int((screen_width/2)-(window_width/2))
    window_y = int((screen_height/2) - (window_height/2))

    window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    update_history()
    window.mainloop()