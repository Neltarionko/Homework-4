#библиотеки
import random
import matplotlib.pyplot as plt
from operator import itemgetter
import math
import heapq

# Функция пересечения окружностей
def intersections(circle1, radius1, circle2, radius2):
    
    d = math.sqrt((circle2[0] - circle1[0])**2 + (circle2[1] - circle1[1])**2)
    if d > radius1 + radius2:
        return None
    elif d < abs(radius1 - radius2):
        return None
    elif d == 0 and radius1 == radius2:
        return None
    else:
        a = (radius1**2 - radius2**2 + d**2)/(2*d)
        h = math.sqrt(radius1**2-a**2)
        x2 = circle1[0] + a*(circle2[0] - circle1[0])/d   
        y2 = circle1[1] + a*(circle2[1] - circle1[1])/d   
        int_x1 = x2 + h*(circle2[1] - circle1[1])/d     
        int_y1 = y2 - h*(circle2[0] - circle1[0])/d 
        int_x2 = x2 - h*(circle2[1] - circle1[1])/d
        int_y2 = y2 + h*(circle2[0] - circle1[0])/d
        
        return [[int_x1, int_y1], [int_x2, int_y2]]

# Функция списка пересечения окружностей
def list_of_intersections(radiobeacons, pseudorange):
    
    list_of_inter = []
    
    for i in range(len(radiobeacons)):
        for k in range(len(radiobeacons)):
            if i != k:
                try:
                    if intersections(radiobeacons[i], pseudorange[i], radiobeacons[k], pseudorange[k]) != None:
                        list_of_inter.append(intersections(radiobeacons[i], pseudorange[i], radiobeacons[k], pseudorange[k])[0])
                        list_of_inter.append(intersections(radiobeacons[i], pseudorange[i], radiobeacons[k], pseudorange[k])[1])
                except:
                    continue
    return list_of_inter

# Функция main
def main(radiobeacons, pseudorange):
    x = []
    y = []
    for i in range(len(radiobeacons)):
        x.append(radiobeacons[i][0])
        y.append(radiobeacons[i][1])

    # Поиск пересечений окружностей    
    list_of_inter = list_of_intersections(radiobeacons, pseudorange)
    x1 = []
    y1 = []
    sumx = 0
    sumy = 0
    for i in range(len(list_of_inter)):
        sumx += list_of_inter[i][0]
        sumy += list_of_inter[i][1]
        x1.append(list_of_inter[i][0])
        y1.append(list_of_inter[i][1])

    xx = sumx/len(list_of_inter)
    yy = sumy/len(list_of_inter)

    # Поиск пересечений окружностей     
    list_of_inter_new = []
    for i in range(0, len(list_of_inter)-1, 2):
        a = list_of_inter[i]
        b = list_of_inter[i+1]
        if math.sqrt((xx - a[0])**2 + (yy - a[1])**2) < math.sqrt((xx - b[0])**2 + (yy - b[1])**2):
            list_of_inter_new.append(a)
        else:
            list_of_inter_new.append(b)

    # Выбор точек для поиска (х0, у0)   
    list1 = []
    list2 = []
    for i in range (len(list_of_inter_new)):
        a = list_of_inter_new[i]
        for k in range (len(list_of_inter_new) - 1, i, -1):
            if math.sqrt((list_of_inter_new[k][0] - a[0])**2 + (list_of_inter_new[k][1] - a[1])**2) < 2:
                list2.append(list_of_inter_new[k])
        if a not in list2:
            list1.append(a)
            list2.append(a)

    # Выбор 4-х оптимальных точек для нахождения (х0, у0)       
    len_inter = []           
    for i in range (len(list1)):
        len_inter.append(math.sqrt((xx - list1[i][0])**2 + (yy - list1[i][1])**2))
    l1, l2, l3, l4 = heapq.nsmallest(4, range(len(len_inter)), key = len_inter.__getitem__)
    data_new = [list1[l1], list1[l2], list1[l3], list1[l4]]

    x2 = []
    y2 = []
    for i in range(len(data_new)):
        x2.append(data_new[i][0])
        y2.append(data_new[i][1])

    sumx = 0
    sumy = 0
    for i in range(len(data_new)):
        sumx += data_new[i][0]
        sumy += data_new[i][1]  

    # Координаты приеменика
    x0 = sumx/len(data_new)
    y0 = sumy/len(data_new) 

    # Нахождение шума измерений+погрешности часов
    noise_tau = []
    for i in range(len(pseudorange)):
        noise_tau.append(math.sqrt((x0 - radiobeacons[i][0])**2 + (y0 - radiobeacons[i][1])**2) - pseudorange[i])
    print(noise_tau)
    
    # Построение графиков
    plt.figure(figsize = (10, 8))
    plt.scatter(x, y)
    #plt.scatter(x1, y1)
    #plt.scatter(x2, y2)
    plt.scatter(x0, y0)
    for i in range(len(radiobeacons)):
        globals()['circle%s' % i] = plt.Circle(radiobeacons[i], pseudorange[i], color='b', fill=False)
        plt.gca().add_artist(globals()['circle%s' % i])
        globals()['circle_%s' % i] = plt.Circle(radiobeacons[i], pseudorange[i]+noise_tau[i], color='b', fill=False, linestyle='--')
        plt.gca().add_artist(globals()['circle_%s' % i])
        #globals()['circle__%s' % i] = plt.Circle(radiobeacons[i], pseudorange[i]+noise[i]+tau, color='b', fill=False, linestyle='-.')
        #plt.gca().add_artist(globals()['circle__%s' % i])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis([-1000, 1000, -1000, 1000])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
    