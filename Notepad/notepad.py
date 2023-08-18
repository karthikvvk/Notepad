"""
>This is an application made in python using tkinter and other required built in modules.
>It uses file handling to store the info of current file in use, what all file has been created and
    what files are deleted using this application.
>It do not access any of the users files except to separate from the app's files.
>Contains 9 global functions
"""
import os
import urllib.request

root_dir = os.getcwd()
req_mods = {"oopen" : "openeasy"}
req_mods_lnk = {"oopen" : "https://github.com/karthikvvk/make-life-easy-python-packages-oopen/raw/main/make-life-easy-python-packages-oopen/openeasy.py"}
for hi in req_mods:
    if os.path.exists(hi):
        pass
    else:
        os.mkdir(hi)
    open(f"{root_dir}\\{hi}\\__init__.py", 'w').close()
    urllib.request.urlretrieve(req_mods_lnk[hi], f"{root_dir}\\{hi}\\{req_mods[hi]}.py")
import oopen.openeasy as op
from tkinter import *
import datetime
from tkinter import ttk, filedialog


root = Tk()
bg = '#323231'
fg = '#e8e8e8'
size = f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}'
print(size)
root.geometry(size)
root.configure(bg=bg)

file = op.o_read('cur_file.txt')
files = op.o_read("cur_files.txt").split(",")
files.pop()

if file:
    pass
else:
    file = 'untitled'f'{f"{datetime.datetime.now()}".split(".")[1]}.txt'
    files.append(file)
    op.o_write('cur_file.txt', file)
    op.o_append('cur_files.txt', file+',')

root.title(file)
inp = Text(root, width=130, height=30, bg=bg, fg=fg)
inp.grid(row=5, column=5)


def load():
    """Read the data stored in the file and add insert them into the 'Text' widget. (2 usages)"""
    global file, inp
    inp.insert(END, op.o_read(file))


load()


def sav():
    """Get the text typed into 'Text' widget and writes them into the current opened file.
    """
    global file
    inp_d = inp.get("1.0", "end-1c")
    op.o_write(file, inp_d)
    a = Label(root, text='Saved', fg=fg, bg=bg)
    a.grid()


def opp():
    """Uses tkinter's filedialog module to create a WINDOWS 'open file window' and opens the file."""
    global file, files
    fl = filedialog.askopenfilename(initialdir='/', title='select a file', filetypes=[('Text files', '*.txt'), ("all types", "*.*")])
    file = fl.split("/")[-1]
    op.o_write('cur_file.txt', file)
    files.append(fl.split("/")[-1])
    for i in files:
        op.o_append('cur_files.txt', i+',')
    root.title(file)
    load()


def rena():
    """Get the file name form the user and uses 'os' module to rename the file."""
    rename_w = Tk()
    rename_w.title('Rename')
    rename_w.geometry('500x500')
    rename_w.configure(bg=bg)
    global file
    ren_v = StringVar(rename_w, value='')
    re = ttk.Entry(rename_w, textvariable=ren_v)
    re.grid()

    def sum():
        global file, files
        re_get = re.get()
        new = re_get+'.txt'
        os.rename(file, new)
        op.o_write('cur_file.txt', new)
        files[files.index(file)] = new
        op.o_replace('cur_files.txt', file, new)
        file = new
        Label(root, text='renamed', fg=fg, bg=bg).grid()
        root.title(file)
    ttk.Button(rename_w, text='submit', command=sum).grid(row=1, column=1)
    Label(root, text='Enter the new name: ', fg=fg, bg=bg).grid(row=0, column=0)
    rename_w.mainloop()


def cr_checkbox(tk_window_object, sequence, bg=bg, fg=fg, row=0, column=0):
    """Automates the checkbox widget creation."""
    len_seq = len(sequence)
    vari = []
    row_l = []

    for y in range(row, len_seq + row):
        row_l.append(y)

    for i in range(len_seq):
        vari.append('a' + str(i))
        vari[i] = IntVar(tk_window_object, value=0)

    for i in range(len_seq):
        Checkbutton(tk_window_object, text=sequence[i], variable=vari[i], bg=bg, justify='left', fg=fg).grid(
            row=row_l[i], column=column)
    return [len_seq, vari, sequence, ttk]


def dell():
    """Uses os module to rename the file such a way it is neglected while fetching the available files."""
    global file
    op.o_write('cur_file.txt', '')
    op.o_replace('cur_files.txt', file+',', '')
    os.rename(file, "$"+file)
    Label(root, text='moved to recycle bin', bg=bg, fg=fg).grid()
    root.title('Notepad')


def recy():
    """Shows which files are neglected while fetching(means recycle bin)."""
    lis_dir = []
    for t in os.listdir():
        if t.endswith('.txt') and t.startswith('$'):
            lis_dir.append(t.lstrip("$").rstrip(".txt"))

    recyclee = Tk()
    recyclee.title('Recycle Bin')
    recyclee.geometry('500x500')
    recyclee.configure(bg=bg)
    checked = cr_checkbox(recyclee, lis_dir, row=1)
    selected = []

    def subb():
        n = 0
        for i in checked[1]:
            if i:
                selected.append(lis_dir[n])
            n += 1

    def del_for():
        subb()
        for j in selected:
            os.remove("$"+j+'.txt')
        recyclee.destroy()
        Label(root, text='deleted forever', bg=bg, fg=fg).grid()

    def restore():
        subb()
        for j in selected:
            os.rename("$" + j + '.txt', j + '.txt')
        recyclee.destroy()
        Label(root, text='restored', bg=bg, fg=fg).grid()

    ttk.Button(recyclee, text='delete forever', command=del_for).grid(row=0, column=0)
    ttk.Button(recyclee, text='restore', command=restore).grid(row=0, column=1)
    
    recyclee.mainloop()


def lis():
    """Shows all the available files"""
    listing = Tk()
    for j in files:
        Label(listing, text=j, fg=fg, bg=bg).grid()
    listing.mainloop()


def ne():
    """Uses oopen module to create newfile."""
    new_file = Tk()
    new_file.title('New File')
    new_file.geometry('500x500')
    nef_v = StringVar(new_file, value='')
    nef = ttk.Entry(new_file, textvariable=nef_v)
    def cre():
        global file, files
        neff = nef.get()+'.txt'
        op.o_write('cur_file.txt', neff)
        op.o_append('cur_files.txt', neff+',')
        files[files.index(file)] = neff
        file =neff
        root.title(neff)
        new_file.destroy()
    ttk.Button(new_file, text='create new note', command=cre).grid(row=1, column=1)
    Label(new_file, text='Enter file name: ').grid(row=0, column=0)
    nef.grid(row=0, column=1)
    new_file.mainloop()


save = ttk.Button(root, text='save', command=sav)
save.grid(row=0, column=4)
opn = ttk.Button(root, text='open', command=opp)
opn.grid(row=0, column=2)
rename = ttk.Button(root, text='rename', command=rena)
rename.grid(row=2, column=4)
new = ttk.Button(root, text='new note', command=ne)
new.grid(row=4, column=0)
delete = ttk.Button(root, text='delete', command=dell)
delete.grid(row=2, column=0)
recycle = ttk.Button(root, text='recycle bin', command=recy)
recycle.grid(row=2, column=2)
lis_note = ttk.Button(root, text='list notes', command=lis)
lis_note.grid(row=0, column=0)

Label(root, text='', bg=bg).grid(row=1, column=0)
Label(root, text='', bg=bg).grid(row=3, column=0)

Label(root, text='     ', bg=bg).grid(row=0, column=1)
Label(root, text='     ', bg=bg).grid(row=0, column=3)

root.mainloop()
