import tkinter as tk
from openai import OpenAI

root = tk.Tk()
root.geometry("340x440")
root.title("AI CHATBOT")

client = OpenAI(api_key="ENTER YOUR API KEY HERE")

inputy = 398
inputcheck = 2
userquestion = ""

def check_multiline():
    global inputy, inputcheck
    inputbox.update_idletasks()
    result = inputbox.count("1.0", "end-1c", "displaylines")
    displayed_lines = result[0] if result else 0
    displayed_lines += 1

    if displayed_lines == 8:
        inputcheck = displayed_lines + 1
    elif displayed_lines < 8:
        if displayed_lines == inputcheck:
            inputcheck = displayed_lines + 1
            inputy -= 9
            inputbox.config(height=displayed_lines)
            inputbox.place(x=132, y=inputy, anchor="center")
        elif displayed_lines < inputcheck - 1:
            inputcheck = displayed_lines + 1
            inputy = 407 - (9 * displayed_lines)
            inputbox.config(height=displayed_lines)
            inputbox.place(x=132, y=inputy, anchor="center")

def clear_inputbox():
    inputbox.delete("1.0", tk.END)
    inputbox.config(height=1)
    inputbox.place(x=132, y=398, anchor="center")

def get_userinput():
    global userquestion
    userquestion = inputbox.get("1.0", "end-1c")

def new_window(response_text):
    answerpopup = tk.Toplevel(root)
    answerpopup.title("CHATBOT RESPONSE")
    answerpopup.geometry("320x200")

    popupcanvas = tk.Canvas(answerpopup, height=200, width=300)

    scrollbar = tk.Scrollbar(answerpopup, orient="vertical", command=popupcanvas.yview)
    popupcanvas.configure(yscrollcommand=scrollbar.set)

    popupcanvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    scroll_popup = tk.Frame(popupcanvas)
    popupcanvas.create_window((0, 0), window=scroll_popup, anchor="nw")

    answertext = tk.Label(scroll_popup, text=response_text, wraplength=295)
    answertext.pack()

    def on_configure(event):
        popupcanvas.configure(scrollregion=popupcanvas.bbox("all"))

    scroll_popup.bind("<Configure>", on_configure)

    def _on_mousewheel(event):
        popupcanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    popupcanvas.bind_all("<MouseWheel>", _on_mousewheel)

def submit_question():
    global userquestion
    get_userinput()
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": userquestion}
            ]
        )
        reply = response.choices[0].message.content
        
        new_window(reply)

    except Exception as e:
        print("Error with OpenAI API:", e)

    clear_inputbox()

maincanvas = tk.Canvas(root, width=320, height=420)
maincanvas.place(relx=0.5, rely=0.5, anchor="center")

title = tk.Label(maincanvas, text="AI CHATBOT", font=("Arial", 24, "bold"), fg="#000000")
title.place(relx=0.5, rely=0.1, anchor="center")

subtitle = tk.Label(maincanvas, text="Powered by: OpenAI", font=("Arial", 9), fg="#000000")
subtitle.place(relx=0.5, rely=0.175, anchor="center")

inputbox = tk.Text(maincanvas, height=1, width=26, font=("Arial", 12), wrap="word")
inputbox.place(x=132, y=inputy, anchor="center")

submitbutton = tk.Button(maincanvas, text="Submit", font=("Arial", 8), width=6, height=1, command=submit_question)
submitbutton.place(x=290, y=398, anchor="center")

inputbox.bind("<KeyRelease>", lambda e: check_multiline())
inputbox.bind("<<Paste>>", lambda e: check_multiline())
inputbox.bind("<Return>", lambda e: check_multiline())
inputbox.bind("<Delete>", lambda e: check_multiline())

root.mainloop()
