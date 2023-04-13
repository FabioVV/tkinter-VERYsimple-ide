from tkinter import *
from tkinter import filedialog as fd
from tkinter import font, messagebox
from tkinter.colorchooser import askcolor
import subprocess

gpath = ''

def main():
    win = Tk()
    win.title("Simple text/code IDE") 
    win.geometry("1200x700")
    win.resizable(False,False)
    textfont = font.Font(family='Bell Gothic Std Black', size='12')
    
    def new_file():

        if text.compare("end-1c", "==", "1.0"):
            text.delete("1.0",END)
            lb.config(text = "New file")
        else:
            rsp = messagebox.askyesno("Are you sure to preceed?","Create new file")
            if rsp:
                text.delete("1.0",END)
                lb.config(text = "New file")
            else:
                pass

    
    def save_file():
        fil = fd.asksaveasfilename(filetypes=[('Python Files','*.py')])
       
        
        with open(f'{fil}', '+a') as file:
            content = text.get("1.0", END)
            file.write(str(content))

        global gpath
        gpath = fil
        lb.config(text = str(fil))


    def open_file():
        global gpath

        if text.compare("end-1c", "==", "1.0"):
            fil = fd.askopenfilename(title='Open File', filetypes=[('Python Files','*.py')])
            with open(f'{fil}', 'r') as file:
                content = file.read()
                #print(content)
                text.insert("1.0", content)

            
            gpath = fil
            lb.config(text = str(fil))
        else:
            rsp = messagebox.askyesno("Are you sure to preceed?","Opening a file will overwrite all of the content")
            if rsp:
                fil = fd.askopenfilename(title='Open File', filetypes=[('Python Files','*.py')])
                text.delete("1.0",END)
                with open(f'{fil}', 'r') as file:
                    content = file.read()
                    #print(content)
                    text.insert("1.0", content)

                
                gpath = fil
                lb.config(text = str(fil))
                
            else:
                pass


    def font_color_chooser():
        val = askcolor()
        text.config(fg=val[1])

    def background_color_chooser():
        val = askcolor()
        text.config(bg=val[1])
   
    def creator():
        new= Toplevel(win)
        new.geometry("500x100")
        new.title("New Window")
        new.title("Creator") 
        new.resizable(False,False)
        Label(new, text="Fábio Varela", font=('Helvetica 25 bold')).pack(pady=30)

    


    def run_python():
        global gpath
        if gpath == '':
            rsp = messagebox.askokcancel("Save file first","Click ok to save the file and run")
            if rsp:
                fil = fd.asksaveasfilename(filetypes=[('Python Files','*.py')])
        
                with open(f'{fil}', '+a') as file:
                    content = text.get("1.0", END)
                    file.write(str(content))

                gpath = fil
                lb.config(text = str(fil))


                code = gpath.replace('"\"','\\')
                cmd = f'python "{code}"'
                #print(cmd)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                outputResult, error = process.communicate()
                output.insert('1.0',outputResult)
                output.insert('1.0',error)

            else:
                pass
        else:
           
            code = gpath.replace('"\"','\\')
            cmd = f'python "{code}"'
            #print(code)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            outputResult, error = process.communicate()
            output.insert('1.0',outputResult)
            output.insert('1.0',error)
    





    # Menus

    menu = Menu(win)
    filemenu = Menu(menu, tearoff=0)
    filemenu.add_command(label="New", command=new_file)
    filemenu.add_command(label="Open", command=open_file)
    filemenu.add_command(label="Save", command=save_file)
    filemenu.add_command(label="Exit",command=win.destroy)
    filemenu.add_separator()
    filemenu.add_command(label="Run python script",command=run_python)
    menu.add_cascade(label="File", menu=filemenu)

    optionsmenu = Menu(menu, tearoff=0)
    optionsmenu.add_command(label="Change background color...", command=background_color_chooser)
    optionsmenu.add_command(label="Change font color...", command=font_color_chooser)
    menu.add_cascade(label="Options", menu=optionsmenu)

    about = Menu(menu, tearoff=0)
    about.add_command(label="Creator", command=creator)
    about.add_command(label="Made with love...")
    menu.add_cascade(label="About...", menu=about)




    scroll = Scrollbar(win, orient='vertical')
    scroll.pack(side=RIGHT, fill="y")



    lb = Label(win, text="New file*")


    lb.pack()


    text = Text(win,height=30, yscrollcommand=scroll.set, bg='black', fg='white', insertbackground='white', font=textfont)
    text.pack(fill="both")
    text.config(tabs=4*4)

    output = Text(height=10, width=150 , bg='black', fg='green')
    output.pack()

    # Running the windown and adding the menu
    win.config(menu=menu)
    win.mainloop()
    #


main()