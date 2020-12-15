#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:24:00 2020

@author: stepka
"""
import tkinter as tk
import pickle, random

def main(filename, subset):
    f = open(filename, 'rb')
    scrambles = pickle.load(f)
    f.close() 
    
    groups = list(scrambles.keys())
    auf = ("", "U", "U'", "U2")
    
    global root
    root = tk.Tk()
    root.title("2x2 trainer. " + subset)
    root.geometry('530x300')
    root.resizable(0, 0)
    root.configure(bg='white')
    
    main_menu = tk.Menu(root, bg='white', activebackground='#93c7eb')
    root.config(menu=main_menu)
    set_menu = tk.Menu(main_menu, bg='white', activebackground='#93c7eb')
    main_menu.add_cascade(label="Subsets", menu=set_menu) 
    set_menu.add_command(label="CLL", command = lambda: refresh('cll.pickle', "CLL"))
    set_menu.add_command(label="EG-1", command = lambda: refresh('eg1.pickle', "EG1"))
    set_menu.add_command(label="EG-2", command = lambda: refresh('eg2.pickle', "EG2"))
    set_menu.add_separator()
    set_menu.add_command(label="TCLL", command = lambda: refresh('tcll.pickle', "TCLL"))
    set_menu.add_command(label="LS1", command = lambda: refresh('ls1.pickle', "LS1"))
    set_menu.add_command(label="LS2", command = lambda: refresh('ls2.pickle', "LS2"))
    set_menu.add_command(label="LS3", command = lambda: refresh('ls3.pickle', "LS3"))
    
    
    vars_dict = dict()
    c = 0
    for group in groups:
        var = tk.IntVar()
        tk.Checkbutton(root, text=group, variable=var, bg='white', activebackground='#93c7eb').grid(row=c//2, column=c%2,sticky='w')
        vars_dict[group] = var
        c += 1
    def state(l):
        s = dict()
        for i in l:
            if l[i].get() == 1:
                s[i] = l[i].get()
        return s
    
    l = tk.Label(root, bg='white')
    prev_scr = None
    
    
    def generate_scr(lbl, selection):
        nonlocal prev_scr
        if selection:
            random_type = random.choice(list(selection.keys()))
            scr = prev_scr
            while scr == prev_scr:
                scr = random.choice(scrambles[random_type])

            prev_scr = scr
            
            pre_auf = random.choice(auf)
            if pre_auf:
                pre_auf += " "
            post_auf = random.choice(auf)
            if post_auf:
                post_auf = " "+post_auf
            lbl['text'] = "        " + pre_auf + scr + post_auf
        else:
            lbl['text'] = "        " + 'nothing is selected'
    
    def select_all():
        nonlocal vars_dict
        for g in vars_dict:
            vars_dict[g].set(1)
        
    def deselect_all():
        nonlocal vars_dict
        for g in vars_dict:
            vars_dict[g].set(0)
    
    def key_events(e):
        if e.char == ' ':
            generate_scr(l, state(vars_dict))
        if e.char == 's':
            if len(state(vars_dict)) == len(groups):
                deselect_all()
            else:
                select_all()
            
    b = tk.Button(root, text='generate scranble', command= lambda : generate_scr(l, state(vars_dict)), bg='white', activebackground='#93c7eb')
    b.grid(sticky='w')
    tk.Button(root, text='select all', command= select_all, bg='white', activebackground='#93c7eb').grid(sticky='w')
    tk.Button(root, text='deselect all', command= deselect_all, bg='white', activebackground='#93c7eb').grid(sticky='w')
    l.grid(row=0, column=2)
    
    root.bind("<KeyPress>", key_events)
    
    root.mainloop()
         
    
if __name__ == '__main__':
    
    def refresh(new_file, subset):
        root.destroy()
        main(new_file, subset)
    main('cll.pickle', "CLL")