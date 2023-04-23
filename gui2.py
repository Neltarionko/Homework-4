from tkinter import *
from gui_base2 import *

def clicked1():
    
    f = open('data2.txt', 'w')
    f.write(txt1.get())
    f.write('\n')
    f.write(txt2.get())
    f.write('\n')
    f.write(txt3.get())
    f.write('\n')
    f.write(txt4.get())
    f.close()  
    
def clicked2():
    
    f = open('data2.txt', 'r')
    data = []
    for line in f:     
        data.append([float(x) for x in line.split()])
    
    radiobeacons_x = data[0]
    radiobeacons_y = data[1]
    pseudorange = data[2]
    tau = data[3]

    radiobeacons = []
    for i in range(len(radiobeacons_x)):
        radiobeacons.append([radiobeacons_x[i], radiobeacons_y[i]]) 
        
    txt1.insert(0, radiobeacons_x)
    txt2.insert(0, radiobeacons_y)
    txt3.insert(0, pseudorange)
    txt4.insert(0, tau)
    
def clicked3(): 
    
    radiobeacons_x = [float(x) for x in txt1.get().split()] 
    radiobeacons_y = [float(x) for x in txt2.get().split()]

    radiobeacons = []
    for i in range(len(radiobeacons_x)):
        radiobeacons.append([radiobeacons_x[i], radiobeacons_y[i]])
    pseudorange = [float(x) for x in txt3.get().split()]
    tau = [float(x) for x in txt4.get().split()]
    
    main(radiobeacons, pseudorange, tau)

window = Tk()
window.title("Radiobeacons GUI")
window.geometry('900x150') 
lbl = Label(window, text="Введите значения координат маяков, псевдодальностей и погрещности часов (не менее 5):")  
lbl.grid(column=0, row=0)  

txt1= Entry(window,width=100)  
txt1.grid(column=0, row=1) 
txt2= Entry(window,width=100)  
txt2.grid(column=0, row=2) 
txt3 = Entry(window,width=100)  
txt3.grid(column=0, row=3)
txt4 = Entry(window,width=100)  
txt4.grid(column=0, row=4)

btn1 = Button(window, text="Сохранить в txt", command=clicked1) 
btn1.grid(column=1, row=5) 
btn2 = Button(window, text="Загрузить из txt", command=clicked2) 
btn2.grid(column=2, row=5) 
btn3 = Button(window, text="Расчет", command=clicked3) 
btn3.grid(column=3, row=5) 

lbl = Label(window, text="*Значения данных хранятся в файле data2.txt*")  
lbl.grid(column=0, row=6)  

window.mainloop()