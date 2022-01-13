# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 15:29:48 2022

@author: mathi
"""
import numpy as np
import warnings
import IHMpy

def Simplex(type, A, B, C, D, BigM):

    (Cont, Var)= A.shape

    fZ = ''
    for j in range(0,Var):
        fZ += '+'+str(C[j][0]) if (C[j][0])>0 else str(C[j][0]) 
        fZ += 'x'+str(j) + ' '
    print(' Voici la fonction objectif: Z =',fZ)

    print(' Voici les contraintes :', Cont)
    Contraintes = ''
    for j in range (0, Cont):
        Contraintes = ''
        Ci = '  C'+str(j+1)+':'
        for k in range (0,Var):
            Constantes = '+'+str(A[j][k]) if A[j][k] > 0  else str(A[j][k])
            Contraintes += Constantes+'x'+str(k)+' '
        Contraintes += D[j][0] + str(B[j][0])
        print(Ci,Contraintes)

    VarBasique = []
    
    
    Compteur = Var
    

    R = np.eye(Cont)

    Btemp = B

    ValArt= []	

    for i in range(Cont):
        if D[i] == '<=':	
            C = np.vstack((C, [[0]]))

            Compteur = Compteur + 1
            VarBasique = VarBasique + [Compteur-1]

            ValArt = [ValArt, 0]

        elif D[i] == '=':
            if type == 'min':
                C = np.vstack((C, [[BigM]]))
            else:
                C = np.vstack((C, [[-BigM]]))

            Compteur = Compteur + 1
            VarBasique = VarBasique + [Compteur-1]

            ValArt = [ValArt, 1]
        elif D[i] == '>=':  # >=
            if type == 'min':
                C = np.vstack((C, [[0], [BigM]]))
            else:
                C = np.vstack((C, [[0], [-BigM]]))

            R = ColonneNegative(R, Compteur + 1 - Var)
            Btemp = ColonneNulle(Btemp, Compteur + 1 - Var)

            Compteur = Compteur + 2
            VarBasique = VarBasique + [Compteur-1]

            ValArt = [ValArt, 0, 1]
        else:
            print("Cas impossoble")

    X = np.vstack((np.zeros((Var, 1)), Btemp))

    A = np.hstack((A, R))

    st = np.vstack((np.hstack((-np.transpose(C), np.array([[0]]))), np.hstack((A, B))))

    (Lignes, Colonnes) = st.shape

    print('\n ----------- Tableau Initial ----------- \n')
    print(st)
    print('\nValeurs basiques actuelles : \n')
    print(VarBasique)
    print('\nPoint Optimal : \n')
    print(X)

    OptiZ = np.matmul(np.transpose(C), X)

    print('\nZ : \n\n', OptiZ)

    if OptiZ != 0:
        for i in range(Cont):
            if D[i] == '=' or D[i] == '>=':
                if type == 'min':
                    st[0,:]= st[0,:] + BigM * st[1+i,:]
                else:
                    st[0,:]= st[0,:] - BigM * st[1+i,:]

        print('\Tableau Incorrect\n')
        print(st)

    Ite = 0
    while True:
        if type == 'min':
            w = np.amax(st[0, 0:Colonnes-1])
            iw = np.argmax(st[0, 0:Colonnes-1])
        else:
            w = np.amin(st[0, 0:Colonnes-1])
            iw = np.argmin(st[0, 0:Colonnes-1])

        if w <= 0 and type == 'min':
            print('\nPoint Optimum Final: \n')
            break
        elif w >= 0 and type == 'max':
            print('\nPoint Optimal Final: \n')
            break
        else:
            Ite = Ite + 1

            print('\n\n ----------- Itération-----------',Ite )

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                bi = st[1:Lignes, Colonnes-1] 
                ColPivot = st[1: Lignes, iw]
                Tarr = []
                for i in range(len(ColPivot)):
                    if(ColPivot[i]) <=0:
                        Tarr.append(np.inf)
                    else:
                        Tarr.append(bi[i]/ColPivot[i])
                T = np.array(Tarr)
            
            R = np.logical_and(T != np.inf, T >= 0)
            
            (k, ik) = Min(T, R)

            cz = st[[0],:]

            Pivot = st[ik+1, iw]

            LignePivot = st[ik+1,:] / Pivot
            st = st - st[:, [iw]] * LignePivot

            st[ik+1,:]= LignePivot

            
            VarBasique[ik] = iw

            print('\n *Voici les valeurs basiques actuelles : ', VarBasique)

            Base = st[:, Colonnes-1]
            X = np.zeros((Compteur, 1))

            t = np.size(VarBasique)

            for k in range(t):
                X[VarBasique[k]] = Base[k+1]

            print('\n Point optimal : ')
            print(X)

            C = -np.transpose(cz[[0], 0:Compteur])

            OptiZ = cz[0, Colonnes-1] + np.matmul(np.transpose(C), X)
            st[0, Colonnes-1] = OptiZ

            print('\nTableau de simplex: \n')
            print(st)

            print('\n Valeur de Z : ', OptiZ)

    tv = np.size(ValArt)
    for i in range(tv):
        if ValArt[i] == 1:
            if X[Var + i] > 0:
                print('\nSolution Incorrecte\n')
                break

    return (OptiZ[0, 0], X)


def Min(x, Masque):
    
    min = 0
    imin = 0

    Var = np.size(x)

    for i in reversed(range(Var)):
        if Masque[i] == 1:
            if min == 0:
                min = x[i]
                imin = i
            else:
                if min > x[i]:
                    min = x[i]
                    imin = i
    return (min, imin)


def ColonneNegative(Mat, h):
    (r, c) = Mat.shape
    Mat = np.hstack((Mat[:, 0:h-1], -Mat[:, [h-1]], Mat[:, h-1:c]))

    return Mat


def ColonneNulle(Col, h):
    kpos = np.size(Col)
    Col = np.vstack((Col[0:h-1, [0]], np.array([[0]]), Col[h-1:kpos, [0]]))

    return Col

if __name__ == '__main__':
    print('\n ----------- Tableau de simplex avec Big M -----------\n')
    np.set_printoptions(suppress=True)
    
    #Question 1
    #(z, x) = Simplex('max', np.array([[1, 2, 1.5], [2/3, 2/3, 1], [0.5, 1/3, 0.5]]), 
     #                       np.array([[12000], [4600], [2400]]),                                            
      #                      np.array([[11], [16], [15]]),                                 
       #                     np.array([['<='], ['<='], ['<=']]),
        #          0)                                   
    
    #Question 2
    #(z, x) = Simplex('min', np.array([[400, 300], [300, 400], [200, 500]]), 
    #                        np.array([[25000], [27000], [30000]]),                                            
    #                        np.array([[20000], [25000]]),                                 
    #                        np.array([['=>'], ['=>'], ['=>']]),
    #              0)                                   

    #Question 3
    #(z, x) = Simplex('min', np.array([[1, 1, 0,0], [0, 0, 1, 1], [1, 0, 1, 0], [0,1,0,1]]), 
    #                        np.array([[200], [300], [400], [300]]),                                            
    #                        np.array([[30], [36], [25], [30]]),                                 
    #                        np.array([['='], ['='], ['<='], ['<=']]),
    #             0)                                   