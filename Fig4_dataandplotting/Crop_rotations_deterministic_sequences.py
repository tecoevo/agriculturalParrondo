#!/usr/bin/env python
# coding: utf-8

# **Code**

import numpy as np, random as rd, itertools



def gameA(p, K, a, Sq, X):
        coin=rd.uniform(0,1)
        if(coin<p):
            X=X+1
        else:
            X=X-1
        if(0<=Sq<=K-a):
            Sq=Sq+a
        elif((K-a)<Sq<=K):
            Sq=K
        return X, Sq;     


def gameB(p1,p2,K,th,b,Sq,X):
        if(Sq<=th):
            coin1=rd.uniform(0,1)
            if(coin1<p1):
                X=X+1
            else:
                X=X-1
        else:
            coin2=rd.uniform(0,1)
            if(coin2<p2):
                X=X+1
            else:
                X=X-1
        if(0<=Sq<=b):
            Sq=0
        elif(b<Sq<=K):
            Sq=Sq-b
        return X, Sq; 



##Generating sequences to be scanned 
strg_len=2           #string length               
size=5               #max size per bit
z=[]
for i in range(strg_len):
    z.append(np.arange(0,size))
sequences = list(itertools.product(*z))
#print (np.shape(sequences))
#print(sequences)
#np.savetxt("Deterministic_sequences/Sequences",sequences)


p=0.4    #probability of winning when cover crop is grown
p1=0.0    #probability of winning when cash crop is grown plus soil quality is below threshold
p2=0.8    #probability of winning when cash crop is grown plus soil quality is above threshold
K=10
th=9      #threshold

a=1       #increase in soil quality when cover crop is grown
b=np.arange(0.5,2.1,0.1)       #decrease in soil quality when cover crop is grown

Trials=1000
T_max=1100




for bval in b:
    X_av=np.zeros((np.shape(sequences)[0],T_max))
    Sq_av=np.zeros((np.shape(sequences)[0],T_max))
    for i in range(np.shape(sequences)[0]):
        X=np.zeros((Trials,T_max))
        Sq=np.zeros((Trials,T_max))
        for trial in range(Trials):
            Sq[trial,0]=rd.randint(0, K)    # intial condition for a soil quality
            #Sq[trial,0]=int(K/2)    # intial condition for a soil quality
            time=0
            count=0
            for j in range(strg_len):
                if(sequences[i][j]==0):
                    count=count+1
            while(time<T_max-1 and count!=strg_len):
                for j in range(strg_len):
                    if(sequences[i][j]==0):
                        continue  
                    if(j%2==0): 
                        for A in range(sequences[i][j]): 
                            X[trial,time+1]=gameA(p,K,a,Sq[trial,time],X[trial,time])[0]
                            Sq[trial,time+1]=gameA(p,K,a,Sq[trial,time],X[trial,time])[1]
                            time=time+1
                            if (time>=T_max-1):
                                 break
                    if (time>=T_max-1):
                                break
                    elif(j%2!=0):
                        for B in range(sequences[i][j]):
                            X[trial,time+1]=gameB(p1, p2,K,th,bval,Sq[trial,time],X[trial,time])[0]
                            Sq[trial,time+1]=gameB(p1, p2,K,th,bval,Sq[trial,time],X[trial,time])[1]
                            time=time+1
                            if (time>=T_max-1):
                                break
                    if (time>=T_max-1):
                                break            
        for k in range(T_max):
            X_av_t=0
            Sq_av_t=0
            for l in range(Trials):
                X_av_t=X_av_t+X[l][k]
                Sq_av_t=Sq_av_t+Sq[l][k]
            X_av[i][k]=(X_av_t)/Trials    
            Sq_av[i][k]=(Sq_av_t)/Trials
    p_win=np.zeros(np.shape(sequences)[0])
    t=np.linspace(0,T_max,T_max)
    for m in range(np.shape(sequences)[0]):
        slope, intercept = np.polyfit(t[(T_max-100):T_max], X_av[m][(T_max-100):T_max], 1)
        p_win[m]=(slope+1)/2        
    #np.savetxt("Deterministic_sequences/Deterministic_sequences_p_{}_p1_{}_p2_{}_K_{}_th_{}_a_{}_b_{}_Tmax_{}_Trials_{}".format(p,p1,p2,K,th,a,bval,T_max,Trials),p_win)
    #print(bval)
     
