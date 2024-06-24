import tkinter
from tkinter import filedialog

def select_folder():
   root = tkinter.Tk()
   root.withdraw()
   folder_path = filedialog.askdirectory(master=root)
   root.destroy()
   return folder_path
