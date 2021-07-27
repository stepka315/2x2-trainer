import tkinter as tk
import pickle, random


run = True
filename = "scr/cll.pickle"
subset = "CLL"

def refresh(new_file, new_subset):
    global filename, subset
    filename = new_file
    subset = new_subset
    root.destroy()

def close():
    global run, root
    root.destroy()
    run = False

while run:
    f = open(filename, 'rb')
    scrambles = pickle.load(f)
    f.close()

    groups = list(scrambles.keys())
    auf = ("", "U", "U'", "U2")

    scr_list = []
    counter = 0

    global root
    root = tk.Tk()
    root.title("2x2 trainer. " + subset)
    root.geometry('550x320')
    root.resizable(0, 0)
    root.configure(bg='white')

    main_menu = tk.Menu(root, bg='white', activebackground='#93c7eb')
    root.config(menu=main_menu)
    set_menu = tk.Menu(main_menu, bg='white', activebackground='#93c7eb')
    main_menu.add_cascade(label="Subsets", menu=set_menu)
    set_menu.add_command(label="CLL", command = lambda: refresh('scr/cll.pickle', "CLL"))
    set_menu.add_command(label="EG-1", command = lambda: refresh('scr/eg1.pickle', "EG1"))
    set_menu.add_command(label="EG-2", command = lambda: refresh('scr/eg2.pickle', "EG2"))
    set_menu.add_separator()
    set_menu.add_command(label="TCLL", command = lambda: refresh('scr/tcll.pickle', "TCLL"))
    set_menu.add_command(label="LS1", command = lambda: refresh('scr/ls1.pickle', "LS1"))
    set_menu.add_command(label="LS2", command = lambda: refresh('scr/ls2.pickle', "LS2"))
    set_menu.add_command(label="LS3", command = lambda: refresh('scr/ls3.pickle', "LS3"))


    def select_all():
        global vars_dict
        for g in vars_dict:
            vars_dict[g].set(1)
        update_scr_list()

    def deselect_all():
        global vars_dict
        for g in vars_dict:
            vars_dict[g].set(0)
        update_scr_list()

    def key_events(e):
        if e.char == ' ':
            generate_scr(l, state(vars_dict))
        if e.char == 's':
            if len(state(vars_dict)) == len(groups):
                deselect_all()
            else:
                select_all()

    def update_scr_list():
        global scr_list, counter
        selection = state(vars_dict)
        counter = 0
        scr_list = []
        for group in selection:
            scr_list.extend(scrambles[group])

    def state(l):
        s = dict()
        for i in l:
            if l[i].get() == 1:
                s[i] = l[i].get()
        return s

    def generate_scr(lbl, selection):
        global prev_scr, scr_list, counter
        if selection:
            if in_order.get() == 0:
                random_type = random.choice(list(selection.keys()))
                scr = prev_scr
                while scr == prev_scr:
                    scr = random.choice(scrambles[random_type])
            else:
                scr = scr_list[counter % len(scr_list)]
                counter += 1

            prev_scr = scr

            pre_auf = random.choice(auf)
            if pre_auf:
                pre_auf += " "
            post_auf = random.choice(auf)
            if post_auf:
                post_auf = " "+post_auf
            lbl['text'] = "        " + pre_auf + scr + post_auf
        else:
            lbl['text'] = "        nothing is selected"


    vars_dict = dict()
    c = 0
    for group in groups:
        var = tk.IntVar()
        tk.Checkbutton(root, text=group, variable=var, bg='white', activebackground='#93c7eb', command=update_scr_list).grid(row=c//2, column=c%2,sticky='w')
        vars_dict[group] = var
        c += 1

    l = tk.Label(root, bg='white')
    prev_scr = None

    b = tk.Button(root, text='generate scramble', command= lambda : generate_scr(l, state(vars_dict)), bg='white', activebackground='#93c7eb')
    b.grid(sticky='w')
    tk.Button(root, text='select all', command= select_all, bg='white', activebackground='#93c7eb').grid(sticky='w')
    tk.Button(root, text='deselect all', command= deselect_all, bg='white', activebackground='#93c7eb').grid(sticky='w')
    l.grid(row=0, column=2)

    in_order = tk.IntVar()
    tk.Checkbutton(root, text='Go in order', variable=in_order, bg='white', activebackground='#93c7eb', command=update_scr_list).grid(sticky='w')

    root.bind("<KeyPress>", key_events)

    root.protocol("WM_DELETE_WINDOW", close)

    root.mainloop()
