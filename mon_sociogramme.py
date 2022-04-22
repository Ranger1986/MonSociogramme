#importation des modules
from tkinter import *
from tkinter import ttk
import sqlite3
from math import sin, cos, pi
import os.path
from os import mkdir

#mise en place des variables globales
global cur
global conn

#le graphique
def cercle(x, y,label,r = 30,coul ='black'):
    "tracé d'un cercle de centre (x,y) et de rayon r"
    can.create_oval(x-r, y-r, x+r, y+r,fill='white', outline=coul)
    can.create_text(x,y,text=str(label),font =FONT)

def drawline(x1, y1, x2, y2,couleur):    
    "Tracé d'une ligne dans le canevas can1"
    can.create_line(x1,y1,x2,y2,width=2,fill=couleur)

def figure_1():
    #actualisation des personnages et de leurs liens
    global cur
    global conn
    cur.execute('SELECT * FROM perso')
    conn.commit()
    info = cur.fetchall()
    L_pers = [] 
    for i in range(0, len(info)): 
        L_pers.append(info[i][1]+'\n'+ info[i][2])
    cur.execute('SELECT * FROM relation')
    conn.commit()
    infolien = cur.fetchall()
    idnum = []
    for i in range(0, len(info)): 
        idnum.append(info[i][0])
    R=140
    teta =0
    L = []
    # Effacer d'abord tout dessin préexistant :
    can.delete(ALL)
    for i in range(len(L_pers)):
        x = 200 + R*cos(teta)
        y = 200 + R*sin(teta)
        teta = teta + 2*pi/len(L_pers)
        L.append((x,y,L_pers[i]))   
    for i in range(len(infolien)):
        drawline(L[idnum.index(infolien[i][0])][0],L[idnum.index(infolien[i][0])][1],L[idnum.index(infolien[i][4])][0],L[idnum.index(infolien[i][4])][1],infolien[i][2])        
    for i in range(len(L)):
        cercle(L[i][0],L[i][1],L[i][2])

#fonction associes aux boutons
def fctcp():
    global Ent
    global cp
    cp = Tk()
    Ent = [0, 1, 2, 3]
    Lab_nom=Label(cp,text='Nom:', font=FONT)
    Lab_nom.grid(row=1, column=1, padx=15, pady=5)
    Ent[0] = Entry(cp, bg='white', font=FONT)
    Ent[0].grid(row=1, column=2, padx=15, pady=5)

    Lab_prenom=Label(cp, text= 'Prenom:', font=FONT)
    Lab_prenom.grid(row=2, column=1, padx=15, pady=5)
    Ent[1] = Entry(cp, bg='white', font=FONT)
    Ent[1].grid(row=2, column=2, padx=15, pady=5)

    Lab_age=Label(cp, text='Age:', font=FONT)
    Lab_age.grid(row=3, column=1, padx=15, pady=5)
    Ent[2] =Entry(cp, bg='white', font=FONT)
    Ent[2].grid(row=3, column=2, padx=15, pady=5)

    Lab_info=Label(cp, text='Informations Complémentaires', font=FONT)
    Lab_info.grid(row=4, column=1, padx=15, pady=5)
    Ent[3] = Entry(cp, bg='white', font=FONT)
    Ent[3].grid(row=4, column=2, padx=15, pady=5)

    bouton=Button(cp,bg='white', font=('Helvetia', 18),text="Valider", command=fctcpvalid)
    bouton.grid(row=5, column=1, columnspan=2)
    
    cp.mainloop()

def fctcpvalid():
    global cur
    global conn
    global Ent
    global cp
    cur.execute("INSERT INTO perso(nom, prenom, age, info) VALUES('"+Ent[0].get()+"','"+Ent[1].get()+"','"+Ent[2].get()+"','"+Ent[3].get()+"')")
    figure_1()
    figure_1()
    cp.destroy()

def fctmp():
    global cur
    global conn
    global mp
    global perso
    mp = Tk()
    
    Lab_sel=Label(mp,text='personnage a supprimer', font=FONT)
    Lab_sel.grid(row=1, column=1, padx=15, pady=5)

    cur.execute('SELECT nom, prenom FROM perso')
    conn.commit()
    char = cur.fetchall()
    plist = []
    for i in range(0, len(char)): 
        plist.append(char[i][0]+'\n '+ char[i][1])
    perso = ttk.Combobox(mp, values = plist)
    perso.grid(row=1, column=2, padx=15, pady=5)

    bouton=Button(mp,bg='white', font=('Helvetia', 18),text="Rechercher", command=fctmpsearch)
    bouton.grid(row=1, column=3)
    mp.mainloop()
    
def fctmpsearch():
    global cur
    global conn
    global mp
    global Ent
    global perso
    global I
    #partie structure
    Ent = [0, 1, 2, 3]
    
    Lab_nom=Label(mp,text='Nom:', font=FONT)
    Lab_nom.grid(row=2, column=1, padx=15, pady=5)
    Ent[0] = Entry(mp, bg='white', font=FONT)
    Ent[0].grid(row=2, column=2, padx=15, pady=5)

    Lab_prenom=Label(mp, text= 'Prenom:', font=FONT)
    Lab_prenom.grid(row=3, column=1, padx=15, pady=5)
    Ent[1] = Entry(mp, bg='white', font=FONT)
    Ent[1].grid(row=3, column=2, padx=15, pady=5)

    Lab_age=Label(mp, text='Age:', font=FONT)
    Lab_age.grid(row=4, column=1, padx=15, pady=5)
    Ent[2] =Entry(mp, bg='white', font=FONT)
    Ent[2].grid(row=4, column=2, padx=15, pady=5)

    Lab_info=Label(mp, text='Informations Complémentaires', font=FONT)
    Lab_info.grid(row=5, column=1, padx=15, pady=5)
    Ent[3] = Entry(mp, bg='white', font=FONT)
    Ent[3].grid(row=5, column=2, padx=15, pady=5)

    bouton=Button(mp,bg='white', font=('Helvetia', 18),text="Valider", command=fctmpvalid)
    bouton.grid(row=6, column=1, columnspan=2)

    #partie BD
    nomprenom = []
    for x in perso.get().split('\n '):
        nomprenom.append(x)
    cur.execute("SELECT * FROM perso WHERE nom='"+nomprenom[0]+"' AND prenom='"+nomprenom[1]+"'")
    conn.commit()
    I=cur.fetchall()[0]
    Ent[0].insert(0,str(I[1]))
    Ent[1].insert(0,str(I[2]))
    Ent[2].insert(0,str(I[3]))
    Ent[3].insert(0,str(I[4]))
    
def fctmpvalid():
    global cur
    global conn
    global mp
    global Ent
    global I
    cur.execute("UPDATE perso SET nom ='"+Ent[0].get()+"', prenom ='"+Ent[1].get()+"', age ="+Ent[2].get()+", info ='"+Ent[3].get()+"'WHERE id="+str(I[0]))
    conn.commit()
    figure_1()
    figure_1()
    mp.destroy()
                
def fctsp():
    global cur
    global conn
    global perso
    global sp
    sp = Tk()
    Lab_sel=Label(sp,text='personnage a supprimer', font=FONT)
    Lab_sel.grid(row=1, column=1, padx=15, pady=5)

    cur.execute('SELECT nom, prenom FROM perso')
    conn.commit()
    char = cur.fetchall()
    plist = []
    for i in range(0, len(char)): 
        plist.append(char[i][0]+'\n '+ char[i][1])
    perso = ttk.Combobox(sp, values = plist)
    perso.grid(row=1, column=2, padx=15, pady=5)

    bouton=Button(sp,bg='white', font=('Helvetia', 18),text="Valider", command=fctspvalid)
    bouton.grid(row=1, column=3)
    
    sp.mainloop()
    
def fctspvalid():
    global cur
    global conn
    global perso
    global sp
    nomprenom = []
    for x in perso.get().split('\n '):
        nomprenom.append(x)
    cur.execute("SELECT id FROM perso WHERE nom='"+nomprenom[0]+"' AND prenom='"+nomprenom[1]+"'")
    conn.commit()
    id1=cur.fetchall()[0][0]
    cur.execute("DELETE FROM perso WHERE nom='"+nomprenom[0]+"' AND prenom='"+nomprenom[1]+"'")
    conn.commit()
    cur.execute("DELETE FROM relation WHERE id1="+str(id1)+" OR id2="+str(id1)+"")
    conn.commit()
    figure_1()
    figure_1()
    sp.destroy()

def fctcr():
    global cur
    global conn
    global Ent
    global cr
    cr = Tk()
    Ent=[0,1,2,3,4]
    cur.execute('SELECT nom, prenom FROM perso')
    conn.commit()
    char = cur.fetchall()
    plist = []
    for i in range(0, len(char)): 
        plist.append(char[i][0]+'\n '+ char[i][1])
    Ent[0] = ttk.Combobox(cr, values = plist)
    Ent[0].grid(row=2, column=1, padx=15, pady=5)
    Lab1 = Label(cr,text='personnage 1', bg='white', font=FONT)
    Lab1.grid(row=1, column=1, padx=15, pady=5)
    
    Ent[1] = Entry(cr, bg='white', font=FONT)
    Ent[1].grid(row=2, column=2, padx=15, pady=5)
    Lab2 = Label(cr, text='vision de la relation par P1', bg='white', font=FONT)
    Lab2.grid(row=1, column=2, padx=15, pady=5)
    
    clist=["black","red","blue","yellow","green","grey"]
    Ent[2] = ttk.Combobox(cr, values = clist)
    Ent[2].grid(row=2, column=3, padx=15, pady=5)
    Lab3 = Label(cr, text="couleur", bg='white', font=FONT)
    Lab3.grid(row=1, column=3, padx=15, pady=5)
    
    Ent[3] = Entry(cr, bg='white', font=FONT)
    Ent[3].grid(row=2, column=4, padx=15, pady=5)
    Lab4 = Label(cr, text='vision de la relation par P2', bg='white', font=FONT)
    Lab4.grid(row=1, column=4, padx=15, pady=5)
    
    Ent[4] = ttk.Combobox(cr, values = plist)
    Ent[4].grid(row=2, column=5, padx=15, pady=5)
    Lab5 = Label(cr, text='personnage 2', bg='white', font=FONT)
    Lab5.grid(row=1, column=5, padx=15, pady=5)
    
    bouton=Button(cr,bg='white', font=('Helvetia', 18),text="Valider", command=fctcrvalid)
    bouton.grid(row=3, column=1, columnspan=5)

def fctcrvalid():
    global cur
    global conn
    global Ent
    global cr
    nomprenom = []
    for x in Ent[0].get().split('\n '):
        nomprenom.append(x)
    cur.execute("SELECT id FROM perso WHERE nom='"+nomprenom[0]+"' AND prenom='"+nomprenom[1]+"'")
    conn.commit()
    id1=str(cur.fetchall()[0][0])
    for x in Ent[4].get().split('\n '):
        nomprenom.append(x)
    cur.execute("SELECT id FROM perso WHERE nom='"+nomprenom[2]+"' AND prenom='"+nomprenom[3]+"'")
    conn.commit()
    id2=str(cur.fetchall()[0][0])
    cur.execute("INSERT INTO relation(id1, desc1, couleur, desc2, id2) VALUES("+id1+",'"+Ent[1].get()+"','"+Ent[2].get()+"','"+Ent[3].get()+"',"+id2+")")
    figure_1()
    figure_1()
    cr.destroy()
    
def fctmr():
    global cur
    global conn
    global mr
    global perso
    mr = Tk()
    

    cur.execute('SELECT nom, prenom FROM perso')
    conn.commit()
    char = cur.fetchall()
    plist = []
    perso = [ 0, 1]
    for i in range(0, len(char)): 
        plist.append(char[i][0]+'\n '+ char[i][1])
        
    Lab_sel=Label(mr,text='personnage1', font=FONT)
    Lab_sel.grid(row=1, column=1, padx=15, pady=5)
    
    perso[0] = ttk.Combobox(mr, values = plist)
    perso[0].grid(row=2, column=1, padx=15, pady=5)
    
    Lab_sel1=Label(mr,text='personnage2', font=FONT)
    Lab_sel1.grid(row=1, column=2, padx=15, pady=5)
    perso[1] = ttk.Combobox(mr, values = plist)
    perso[1].grid(row=2, column=2, padx=15, pady=5)
    
    bouton=Button(mr,bg='white', font=('Helvetia', 18),text="Rechercher", command=fctmrsearch)
    bouton.grid(row=1, column=3, rowspan=2)
    mr.mainloop()

def fctmrsearch():
    global cur
    global conn
    global Ent
    global perso
    global I
    global mr
    #partie structure
    Ent = [0, 1, 2]
    
    Lab_nom=Label(mr,text='personnage1', font=FONT)
    Lab_nom.grid(row=3, column=1, padx=15, pady=5)
    P1=Label(mr,text=str(perso[0].get()), font=FONT)
    P1.grid(row=4, column=1, padx=15, pady=5)

    Lab_d1=Label(mr, text= 'vision de la relation par P1', font=FONT)
    Lab_d1.grid(row=3, column=2, padx=15, pady=5)
    Ent[0] = Entry(mr, bg='white', font=FONT)
    Ent[0].grid(row=4, column=2, padx=15, pady=5)

    Lab_coul=Label(mr, text='couleur', font=FONT)
    Lab_coul.grid(row=3, column=3, padx=15, pady=5)
    clist=["black","red","blue","yellow","green","grey"]
    Ent[1] = ttk.Combobox(mr, values = clist)
    Ent[1].grid(row=4, column=3, padx=15, pady=5)

    Lab_d2=Label(mr, text='vision de la relation par P2', font=FONT)
    Lab_d2.grid(row=3, column=4, padx=15, pady=5)
    Ent[2] =Entry(mr, bg='white', font=FONT)
    Ent[2].grid(row=4, column=4, padx=15, pady=5)

    Lab_nom1=Label(mr,text='personnage1', font=FONT)
    Lab_nom1.grid(row=3, column=5, padx=15, pady=5)
    P2=Label(mr,text=str(perso[1].get()), font=FONT)
    P2.grid(row=4, column=5, padx=15, pady=5)

    bouton=Button(mr,bg='white', font=('Helvetia', 18),text="Valider", command=fctmrvalid)
    bouton.grid(row=5, column=1, columnspan=5)

    #partie BD
    nomprenom = []
    for x in perso[0].get().split('\n '):
        nomprenom.append(x)
    for x in perso[1].get().split('\n '):
        nomprenom.append(x)
    cur.execute("SELECT id FROM perso WHERE nom='"+nomprenom[0]+"' AND prenom='"+nomprenom[1]+"'")
    conn.commit()
    id1=str(cur.fetchall()[0][0])
    cur.execute("SELECT id FROM perso WHERE nom='"+nomprenom[2]+"' AND prenom='"+nomprenom[3]+"'")
    conn.commit()
    id2=str(cur.fetchall()[0][0])
    cur.execute("SELECT * FROM relation WHERE (id1="+id1+" AND id2="+id2+") OR (id1="+id2+" AND id2="+id1+")")
    conn.commit()
    I=cur.fetchall()[0]
    Ent[1].insert(0,str(I[2]))
    if I[0] == int(id1):
        Ent[0].insert(0,str(I[1]))
        Ent[2].insert(0,str(I[3]))
    if I[0] == int(id2):
        Ent[2].insert(0,str(I[1]))
        Ent[0].insert(0,str(I[3]))
    
def fctmrvalid():
    global cur
    global conn
    global mr
    global Ent
    global I
    cur.execute("DELETE FROM relation WHERE (id1="+str(I[0])+" AND id2="+str(I[4])+") OR (id1="+str(I[4])+" AND id2="+str(I[0])+")")
    conn.commit()
    cur.execute("INSERT INTO relation(id1, desc1, couleur, desc2, id2) VALUES("+str(I[0])+",'"+Ent[0].get()+"','"+Ent[1].get()+"','"+Ent[2].get()+"',"+str(I[4])+")")
    conn.commit()
    figure_1()
    figure_1()
    mr.destroy()
    
def fctsr():
    global cur
    global conn
    global perso
    global sr
    sr = Tk()
    Lab_sel=Label(sr,text='personnage 1', font=FONT)
    Lab_sel.grid(row=1, column=1, padx=15, pady=5)

    cur.execute('SELECT nom, prenom FROM perso')
    conn.commit()
    char = cur.fetchall()
    perso = [ 0, 1]
    plist = []
    for i in range(0, len(char)): 
        plist.append(char[i][0]+'\n '+ char[i][1])
    perso[0] = ttk.Combobox(sr, values = plist)
    perso[0].grid(row=2, column=1, padx=15, pady=5)

    Lab_sel1=Label(sr,text='personnage 2', font=FONT)
    Lab_sel1.grid(row=1, column=2, padx=15, pady=5)
    
    perso[1] = ttk.Combobox(sr, values = plist)
    perso[1].grid(row=2, column=2, padx=15, pady=5)

    bouton=Button(sr,bg='white', font=('Helvetia', 18),text="Valider", command=fctsrvalid)
    bouton.grid(row=1, column=3, rowspan=2)
    
    sr.mainloop()

def fctsrvalid():
    global cur
    global conn
    global perso
    global sr
    nomprenom = []
    for x in perso[0].get().split('\n '):
        nomprenom.append(x)
    for x in perso[1].get().split('\n '):
        nomprenom.append(x)
    cur.execute("SELECT id FROM perso WHERE nom='"+nomprenom[0]+"' AND prenom='"+nomprenom[1]+"'")
    conn.commit()
    id1=str(cur.fetchall()[0][0])
    cur.execute("SELECT id FROM perso WHERE nom='"+nomprenom[2]+"' AND prenom='"+nomprenom[3]+"'")
    conn.commit()
    id2=str(cur.fetchall()[0][0])
    cur.execute("DELETE FROM relation WHERE (id1="+id1+" AND id2="+id2+") OR (id1="+id2+" AND id2="+id1+")")
    conn.commit()
    figure_1()
    figure_1()
    sr.destroy()
##### Programme principal : ############
#graphique
FONT = ('helvetic', 12) ## (FontName, FontSize)

conn = sqlite3.connect('socio.db')
cur = conn.cursor()
cur.execute("CREATE TABLE  if not exists perso(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT, prenom TEXT, age TEXT, info TEXT)")
cur.execute("CREATE TABLE  if not exists relation(id1 INT, desc1 TEXT, couleur TEXT, desc2 TEXT, id2 INT)")
conn.commit()
root = Tk()
can = Canvas(root, width =400, height =400, bg ='ivory')
can.grid(column=1, row=1)
figure_1()
figure_1()

menu = Frame(root)
menu.grid(column=2, row=1)

buttoncp = Button(menu, text = "Creation personnage", command=fctcp, width = 20)
buttoncp.grid(column=1, row=1)
buttonmp = Button(menu, text = "Modification personnage", command=fctmp, width = 20)
buttonmp.grid(column=1, row=2)
buttonsp = Button(menu, text = "Suppression personnage", command=fctsp, width = 20)
buttonsp.grid(column=1, row=3)
buttoncr = Button(menu, text = "Creation relation", command=fctcr, width = 20)
buttoncr.grid(column=1, row=4)
buttonmr = Button(menu, text = "Modification relation", command=fctmr, width = 20)
buttonmr.grid(column=1, row=5)
buttonsr = Button(menu, text = "Suppression relation", command=fctsr, width = 20)
buttonsr.grid(column=1, row=6)

root.mainloop()
