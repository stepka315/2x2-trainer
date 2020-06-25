#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:24:00 2020

@author: stepka
"""
import tkinter as tk
import pickle, random

f = open('tcll.pickle', 'rb')
scrambles = pickle.load(f)
f.close() 



groups = list(scrambles.keys())
auf = ("", "U", "U'", "U2")

root = tk.Tk()
root.title("2x2 trainer")
root.geometry('530x300')
#root.resizable(0, 0)

vars_dict = dict()
c = 0
for group in groups:
    var = tk.IntVar()
    tk.Checkbutton(root, text=group, variable=var).grid(row=c//2, column=c%2,sticky='w')
    vars_dict[group] = var
    c += 1
def state(l):
    s = dict()
    for i in l:
        if l[i].get() == 1:
            s[i] = l[i].get()
    return s

l = tk.Label(root)
prev_scr = None


def generate_scr(lbl, s):
    selection = s(vars_dict)
    global prev_scr
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
    global vars_dict
    for g in vars_dict:
        vars_dict[g].set(1)
    
def deselect_all():
    global vars_dict
    for g in vars_dict:
        vars_dict[g].set(0)


b = tk.Button(root, text='generate scranble', command= lambda : generate_scr(l, state))
b.grid(sticky='w')
tk.Button(root, text='select all', command= select_all ).grid(sticky='w')
tk.Button(root, text='deselect all', command= deselect_all ).grid(sticky='w')
l.grid(row=0, column=2)
root.mainloop()