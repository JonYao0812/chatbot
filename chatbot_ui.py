#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 20:53:38 2019

@author: Jon Yao
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import qa_chat
import time


bubbles = []
class CahtbotGUI:
    
    def __init__(self,master):

##        bot = ChatBot
        
        
        master.resizable(False,False)
        master.configure(background = 'white')
        self.style = self.get_style()
        self.topFrame = tk.Frame(master,width=50, height=30,borderwidth = 1,highlightbackground = "Orange",highlightthickness=1,highlightcolor="Orange")
        self.btmFrame = tk.Frame(master,width=50, height=50)
        
##  Display box
        messages = StringVar()
        scrollbar = tk.Scrollbar(self.topFrame, orient=VERTICAL)
        scrollbar.pack( side = RIGHT, fill = Y )
        self.display= tk.Canvas(self.topFrame,yscrollcommand=scrollbar.set, width = 500, height=500,bg="white")
        self.display.pack(side = LEFT)
        scrollbar.config(command=self.display.yview)
        self.topFrame.pack(side = TOP)
        
##  Text box
        self.question = tk.Text(self.btmFrame,width = 31,height=3,relief = GROOVE, 
        	wrap = WORD,highlightbackground = "Orange",highlightcolor= "Orange",highlightthickness=1)
        self.question.pack(side = LEFT)
        self.question.insert(1.0,"Type your question here.")
        self.send = Button(self.btmFrame, text = "Send",height = 3, width = 6,
        	relief = RAISED, command = self.get_message,background = "lightblue")
        self.send.pack(side = RIGHT)
        self.question.bind("<Button-1>",self.delete_text)
        self.btmFrame.pack(side=BOTTOM)
        self.display_message(qa_chat.chat("Hi")[0], "abc")
    
    def get_message(self):
        quest = self.question.get(1.0,'end-1c')
        self.display_message(quest,"user")

        if not quest.strip():
            self.display_message("Could you try again with more words?\n","pte")
           
        else:
            self.question.delete(1.0,END)
            answers = qa_chat.chat(quest)
            for ans in answers:
                self.display_message(ans,"abc")
           
    def display_message(self, text, who):
        if who.lower() == "user":
            bubble = Label(self.display, text=text +": YOU", fg='black', 
                bg='lightgreen',anchor='e',wraplength=240)
            bubble.pack(side = RIGHT)
            self.display.create_window(500,0,window=bubble ,anchor='se',width = 240)

        else:
            bubble = Label(self.display, text="ABC: "+text, fg='black', 
                bg='lightblue',anchor='w',wraplength=240)
            bubble.pack(side = LEFT)
            self.display.create_window(0,0,window=bubble, anchor='sw',width = 240)

        self.display.move('all', 0, -50)
        self.display.configure(scrollregion = self.display.bbox("all"))





        
    def delete_text(self,event):
        self.question.delete(1.0,END)

        
    def get_style(self):
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.style.configure('TFrame', background = 'yellow')
        self.style.configure('TButton', background = '#ffe6e6')
        self.style.configure('TLabel', background = '#ffff1a', font = ('Arial','12'))
        self.style.configure('Des.TLabel',  font = ('Arial','12','italic'),foreground='blue')
        return self.style
        
root = Tk()
app = CahtbotGUI(root)
root.mainloop()
    


