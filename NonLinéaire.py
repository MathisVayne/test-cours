# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 17:02:52 2022

@author: mathi
"""
import pandas as pd


#PasSimple
s=0.05
x1=0.0

def x_PasSimple(n):
    if n>0:
        return x1+(n-1)*s
    else:
        return x1+(n+1)*s


def f_PasSimple(n):
    return x_PasSimple(n)**5-5*(x_PasSimple(n)**3)-20*(x_PasSimple(n))+5

def PasSimple():
    n=1
    if f_PasSimple(2)<f_PasSimple(1) :
        while f_PasSimple(n+1)<f_PasSimple(n): 
            n+=1
        a=x_PasSimple(n-1)
        b=x_PasSimple(n)
    elif f_PasSimple(2)>f_PasSimple(1):
        while f_PasSimple(n+1)>f_PasSimple(n):
            n-=1
        a=x_PasSimple(n-1)
        b=x_PasSimple(n)
    elif f_PasSimple(2)==f_PasSimple(3):
        a=x_PasSimple(1)
        b=x_PasSimple(2)
    elif f_PasSimple(2)>f_PasSimple(1) and f_PasSimple(2)>f_PasSimple(1):
        a=x_PasSimple(-2)
        b=x_PasSimple(2)
    return n,a,b


#Pas accéléré 

def x_PasAccel(n,s,x1):
    if n>0:
        return x1+(n-1)*s
    else:
        return x1+(n+1)*s


def f_PasAccel(n,s,x1):
    return x_PasAccel(n,s,x1)**5-5*(x_PasAccel(n,s,x1)**3)-20*(x_PasAccel(n,s,x1))+5

def PasAccel():
    x1=0.0
    s=0.05
    n=1
    if f_PasAccel(2,s,x1)<f_PasAccel(1,s,x1) :
        while f_PasAccel(n+1,s,x1)<f_PasAccel(n,s,x1): 
            n+=1
            s=2*s
        a=x_PasAccel(n-1,s,x1)
        b=x_PasAccel(n,s,x1)
    if f_PasAccel(2,s,x1)>f_PasAccel(1,s,x1):
        while f_PasAccel(n+1,s,x1)>f_PasAccel(n,s,x1):
            n-=1
            s=2*s
        a=x_PasAccel(n-1,s,x1)
        b=x_PasAccel(n,s,x1)
    elif f_PasAccel(2,s,x1)==f_PasAccel(3,s,x1):
        a=x_PasAccel(1,s,x1)
        b=x_PasAccel(2,s,x1)
    elif f_PasAccel(2,s,x1)>f_PasAccel(1,s,x1) and f_PasAccel(2,s,x1)>f_PasAccel(1,s,x1):
        a=x_PasAccel(-2,s,x1)
        b=x_PasAccel(2,s,x1)
    return n,a,b,s

#Bissection


def f_Bis(x_Bis):
    return x_Bis**5-5*(x_Bis**3)-20*(x_Bis)+5

def Méthode(L,method):
    x0 = (L[0]+L[1])/2
    x1 = (L[0]+x0)/2
    x2 = (x0+L[1])/2
    X = [x1,x0,x2]
    f0 = f_Bis(x0)
    f1 = f_Bis(x1)
    f2 = f_Bis(x2)
    F = [f1,f0,f2]
    if method == 'min':
        if f1 == min(F):
            return [L[0],x0]
        elif f0 == min(F):
            return [x1,x2]
        else:
            return [x0,L[1]]

def Bissection(L0,method,e):
    if method == 'min':
        m = 'minimum'
    else:
        m= 'maximum'
    Min = [L0[0]]
    Max = [L0[1]]
    L = list(L0)
    while (L[1]-L[0]) > (L0[1]-L0[0])*e:
        L = Méthode(L,method)
        Min.append(L[0])
        Max.append(L[1])
    df = pd.DataFrame(list(zip(Min,Max)),columns=['min','max'])
    x_Final = (L[0]+L[1])/2
    f_Final = f_Bis(x_Final)
    print(df)
    print(f'Le {m} trouvé pour la fonction f(x) est {f_Final} à x = {x_Final}.')


#NewtonRaphson

def f_NR(x):
    return x**3-(7*(x**2))+(8*(x-3))

def df(x):
    return (3*(x**2))-14*x+8

def ddf(x):
    return 6*x-14

x0=5
Epsilon=0.001

def x(i,df,ddf,x0):
    if i==1:
        return x0
    else:
        return x(i-1,df,ddf,x0)-(df(x(i-1,df,ddf,x0))/ddf(x(i-1,df,ddf,x0)))
    
def NR(x0,Espilon):
    i=1
    while abs(df(x(i,df,ddf,x1)))>Epsilon:
        i+=1
    return x(i,df,ddf,x0)   


#Choix de la méthode
question = int(input("Quel programme choisissez-vous ? \n - 1 : Pas simple \n - 2 : Pas accéléré \n - 3 : Bissection  \n - 4 : Newton Raphson \n"))

#Réponse aux questions en fonction du choix
if question ==1:
    print("Programme 1")
    results=PasSimple()
    n=results[0]
    a=results[1]
    b=results[2]   
    print("Le point de minimum x est compris entre ",a," et ",b,". \n On a donc la fonction f(x)=",f_PasSimple(n))
    
    
if question ==2:
    print("Programme 2")
    results=PasAccel()
    n=results[0]
    a=results[1]
    b=results[2]   
    s=results[3]
    print("Le point de minimum x est compris entre ",a," et ",b,". \n On a donc la fonction f(x)=",f_PasAccel(n,s,x1))
    
    
if question ==3:
    print("Programme 3")
    Bissection([0,5], 'min', 0.1)
    
    
if question ==4:
    print("Programme 4")
    print ("Voici le point optimum pour la focntion f(x) : x =",NR(x0,Epsilon))
