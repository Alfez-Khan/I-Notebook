'''Text Editor with python using modules->tkinter,filedialog.
It opens a Tkinter based gui which has a text widget(with scrollbar) and 
menu buttons to perform different operations
It can do basic functions like creating new text files,
opening already existing files and saving changes in them.
And other text-editing work like cut, copy and paste.

Created by Alfez Khan Class XII A  Roll No. 08
''' 

# Importing tkinter module(for gui) and other modules
# filedialog for open and save as file dialog
from tkinter import *
from tkinter import filedialog


#creating the main window
root=Tk()
root.title("untitled- INotebook") #giving title to window
root.state('zoomed') #making initial state of window maximized


#creating a label at the top)
my_lab=Label(root,text='INotebook')


#creating work space where all text editing takes place
w_frame=Frame(master=root)

x_scroll=Scrollbar(w_frame,orient='horizontal')

y_scroll=Scrollbar(w_frame)
w_space=Text(w_frame, width=1000, height=4500, undo=True,
wrap='none',xscrollcommand=x_scroll.set,yscrollcommand=y_scroll.set)

y_scroll.pack(side=RIGHT,fill=Y)
x_scroll.pack(side=BOTTOM,fill=X)
y_scroll.config(command=w_space.yview)
x_scroll.config(command=w_space.xview)
w_space.pack(side=TOP)


currentfile='untitled' # currently opened file
cont=True #The program checks it value before making changes to a file or 
          #the text box will be used further in master() function


#functions of File menu
def save_file(s):
    '''open save file dialog and saves the file.
    Directly save changes to pre-existing files'''
    global currentfile   
    wdata=w_space.get('1.0','end')
    if currentfile=='untitled':
        root.filename=filedialog.asksaveasfilename(filetypes =(
            ("Text files","*.txt"),("all files","*.*")))
        try:
            with open(root.filename,'w+') as fobject:
                fobject.write(wdata)
                w_space.edit_modified(False)
            currentfile=root.filename
        except:
            pass
    else:
        with open(currentfile,'w+') as fobject:
            fobject.write(wdata)
            w_space.edit_modified(False)
def tell_save(arg):
    '''tell the program to save file
     make cont False if user press cancel or 
     close the save_window(see ask_save())'''
    global cont
    global currentfile
    save_window.destroy()
    if arg=='save':
        save_file(None)
        currentfile='untitled'
    elif arg=='notsave':
        return
    else:
        cont=False
def ask_save():
    '''open a window asking user to save the file. 
    Calls the tell_save() function 
    with an argument telling about the button clicked by the user'''
    global save_window
    save_window=Toplevel(root)
    save_window.title('ALERT!')
    save_window.grab_set()
    save_window.resizable(width=False,height=False)
    save_window.protocol('WM_DELETE_WINDOW',lambda:tell_save('cancel'))
    save_label=Label(save_window,text="Do you want save changes to \n {} ?".
    format(currentfile),
    bg='white',fg='blue',font='Times')
    savebutton=Button(save_window,text='Save',command=lambda:tell_save('save'))
    notsavebutton=Button(save_window,text='Don\'t Save',
    command=lambda:tell_save('notsave'))
    cancelbutton=Button(save_window,text='Cancel',
    command=lambda:tell_save('cancel'))
    save_label.grid(row=0,column=0,columnspan=3)
    savebutton.grid(row=1,column=0)
    notsavebutton.grid(row=1,column=1)
    cancelbutton.grid(row=1,column=2)
def new_file(s):
    '''close current file and open a new file'''
    global currentfile 
    w_space.delete("1.0", "end")
    currentfile='untitled'
    w_space.edit_modified(False)
def open_file(s):
    '''open an already existing file
    opens open file dialogbox and opens the chosen file'''
    global currentfile
    root.filename=filedialog.askopenfilename(filetypes = (("Text files","*.txt"),
    ("all files","*.*")))
    try:
        with open(root.filename,'r') as fobject:
            fdata=fobject.read()
            w_space.delete("1.0", "end") 
            w_space.insert('1.0',fdata)
            w_space.edit_modified(False)
        currentfile=root.filename    

    except:
        pass    
def saveas_file(s):
    '''opens 'save as' file dialog box and save the file as the user tell'''
    wdata=w_space.get('1.0','end')
    global currentfile
    root.filename=filedialog.asksaveasfilename(filetypes =(("Text files","*.txt"),
    ("all files","*.*")))
    try:    
        with open(root.filename,'w+') as fobject:
            fobject.write(wdata)
            w_space.edit_modified(False)
        currentfile=root.filename
    except:
        pass
def exit_file(s):
    '''exit the main window. Program is closed'''
    root.destroy()
def master(x):
    '''calls all the functions of file menu
    prevent data loss whenever a file is closed by asking user to save the file
    by calling ask_save function(which opens a window asking user to save file)'''
    global cont
    wdata=w_space.get('1.0','end')
    if x in ('new','open','exit'):
        if (w_space.edit_modified()):
            ask_save()
            root.wait_window(save_window)
    if cont==True:
        command=x+'_file(None)'
        eval(command)
        new_title=currentfile+'- INotebook'
        root.title(new_title)
    else:
        cont=True


# functions of Edit menu
def cut():
    '''Deletes the selected text
    If nothing selected does nothing'''
    try:
        w_space.delete('sel.first','sel.last')
    except:
        pass
def copy():
    '''copy the selected text to the clipboard
    If nothing selected does nothing'''
    try:
        copied=root.selection_get()
        root.clipboard_clear()
        root.clipboard_append(copied)
    except:
        pass
def paste():
    '''Paste the copied text from the clipboard
    If something selected, replace the selected text with the copied text
    If clipboaard is empty does nothing'''
    try:
        w_space.delete('sel.first','sel.last')
    except:
        pass
    try:
        copied=root.clipboard_get()
        index=w_space.index(INSERT)
        w_space.insert(index,copied)
    except:
        pass


#creating a menu bar
menubar=Menu(root)

#adding File menu to menu bar
File=Menu(menubar, tearoff=0 )
File.add_command(label='New File',command=lambda:master('new'),accelerator='Ctrl+N')
File.add_command(label='Open',command=lambda:master('open'),accelerator='Ctrl+O')
File.add_command(label='Save',command=lambda:master('save'),accelerator='Ctrl+S')
File.add_command(label='Save As',command=lambda:master('saveas'))
File.add_separator()
File.add_command(label='Exit',command=lambda:master('exit'))
menubar.add_cascade(label='File',menu=File)

#adding Edit menu to menu bar
Edit=Menu(menubar, tearoff=0 )
Edit.add_command(label='Cut',command=cut,accelerator='Ctrl+X')
Edit.add_command(label='Copy',command=copy,accelerator='Ctrl+C')
Edit.add_command(label='Paste',command=paste,accelerator='Ctrl+V')
Edit.add_separator()
Edit.add_command(label='Undo',command=w_space.edit_undo,accelerator='Ctrl+Z')
Edit.add_command(label='Redo',command=w_space.edit_redo,accelerator='Ctrl+Y')
menubar.add_cascade(label='Edit',menu=Edit)


# binding shortcuts of new,open and save buton
root.bind('<Control-Key-N>',lambda x:master('new'))
root.bind('<Control-Key-n>',lambda x:master('new'))
root.bind('<Control-Key-O>',lambda x:master('open'))
root.bind('<Control-Key-o>',lambda x:master('open'))
root.bind('<Control-Key-S>',lambda x:master('save'))
root.bind('<Control-Key-s>',lambda x:master('save'))


#getting all the elements together
root.config(menu=menubar)
my_lab.pack()
w_frame.pack()


# the following line puts the program in a loop and keep the window running
# and wait for user interaction with the window or program 
root.mainloop()