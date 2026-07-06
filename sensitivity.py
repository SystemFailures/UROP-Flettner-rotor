import numpy as np
import matplotlib.pyplot as plt



w= 0.006
t = 0.00165
E = 190*1e9
H = 0.135
F = 1.6

I = (w* t**3)/12

def recalcI():
    global I
    I = (w* t**3)/12

def getSensitivity(D):
    s = (w* (t**2) * E)/(6*D*1e7)
    return s

def getDisplacement(D):
    d = F/(E*I) * (H*(D+0.01)*(H+0.5*(D+0.01)) + 1/3 * (D+0.01)**3)
    return d

def getSum(D):
    return getDisplacement(D)+getSensitivity(D)

def plot():
    D = np.linspace(0.008,0.05,200)
    s = getSensitivity(D)
    d = getDisplacement(D)
    g=s+d
    
    plt.figure()
    plt.plot(D,s,label="Sensitivity (x10^-7)")
    plt.plot(D,d,label="Displacement of rotor centre (m)")
    plt.plot(D,g)
    plt.scatter(D[np.where(g == min(g))],getSum(D[np.where(g == min(g))]),marker='x')
    

    global t
    thicknesses = np.linspace(0.0012,0.0023,20)
    optDs = np.zeros_like(thicknesses)
    optds = np.zeros_like(thicknesses)
    optss = np.zeros_like(thicknesses)
    optgs = np.zeros_like(thicknesses)

    for i in range(len(thicknesses)):
        t = thicknesses[i]
        recalcI()
        s = getSensitivity(D)
        d= getDisplacement(D)
        g=s+d

        opt_index = np.where(g == min(g))
        optDs[i] = D[opt_index]
        optds[i] = d[opt_index]
        optss[i] = s[opt_index]
        optgs[i] = g[opt_index]
    '''
    for width in widths:
        w = width
        recalcI()
        s = getSensitivity(D)
        d = getDisplacement(D)
        g=s+d

        optLoc = np.where(g == min(g))
        optDs.append(D[optLoc])
        optgs.append(min(g))
        optds.append(d[optLoc])
        optss.append(s[optLoc])'''
    
    plt.plot(optDs,optgs,label="Lowest sum for widths [4,14]mm")
    plt.plot(optDs,optss,label="Sensitivity at optimum sum")
    plt.plot(optDs,optds,label="Displacement at optimum sum")
    for i in range(len(thicknesses)):
        if i%4 == 0:
            plt.annotate(round(thicknesses[i]*1000,2),(optDs[i],optgs[i]),rotation=90)
            plt.scatter(optDs[i],optgs[i],marker='x',color='red')


    plt.legend()
    plt.show()

plot()