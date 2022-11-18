import urllib.request
import scipy as sc
import numpy as np
import re
import matplotlib.pyplot as plt
import xml.etree.cElementTree as ET
import os

def h(n,x):
    return sc.special.spherical_jn(n, x) + 1j * sc.special.spherical_yn(n, x)

def a(n,x):
    return sc.special.spherical_jn(n, x)/h(n, k*r)

def b(n,x):
    return (x * sc.special.spherical_jn(n-1, x) - n * sc.special.spherical_jn(n, x)) / (x * h(n - 1, x) - n * h(n, x))

def sigma(povtor,x):
    sigm = 0
    for n in range(1,povtor):
        sigm = sigm + np.power(-1,n)*(n+0.5)*(b(n,x)-a(n,x))
        print('n= ',n)
    return sigm

if __name__=='__main__':
    url = 'https://jenyay.net/uploads/Student/Modelling/task_02.xml'
    urllib.request.urlretrieve(url, 'znachenia.xml')
    with open('znachenia.xml', 'r') as file:
        data = file.readlines()
    var = int(input('Введите ваш вариант: '))
    var +=1
    priblizhenie = int(input('Введите приближение(число шагов): '))
    print(data[var])
    print(re.findall('\d+[.]*\d*e*[-]*\d*', data[var]))
    variant = re.findall('\d+[.]*\d*e*[-]*\d*', data[var])
    D = float(variant[1])
    print('D= ',D)
    fmin = float(variant[2])
    print('fmin= ',fmin)
    fmax = float(variant[3])
    print('fmax= ',fmax)
    r = D/2
    print('r= ',r)
    f = np.linspace(fmin,fmax,priblizhenie)
    print('f= ',f)
    lamda = 3*10**8/f
    print('lamda= ',lamda)
    k = 2*np.pi/lamda
    print('k= ',k)
    result = lamda**2/np.pi*abs(sigma(70,k*r))**2
    print('sigma = ',result)
    plt.xlabel('2*pi*r/lambda')
    plt.ylabel('sigma/pi*r^2')
    plt.plot(2*np.pi*r/lamda,result/(np.pi*r**2))
    plt.show()
    plt.xlabel('f')
    plt.ylabel('sigma')
    plt.plot(f,result)
    plt.show()

    # creating xml file

    if 'results' not in os.listdir():
        os.makedirs(os.path.join(os.getcwd(), 'results'))

    root = ET.Element("data")
    freq = ET.SubElement(root, "frequencydata")

    for i in range(priblizhenie):
        ET.SubElement(freq, "f").text = "{}".format(f[i])

    lam = ET.SubElement(root, "lambdadata")

    for i in range(priblizhenie):
        ET.SubElement(lam, "lambda").text = "{}".format(lamda[i])

    rc = ET.SubElement(root, "rcsdata")

    for i in range(priblizhenie):
        ET.SubElement(rc, "rcs").text = "{}".format(result[i])

    tree = ET.ElementTree(root)
    ET.indent(tree, '  ')
    tree.write("results/results.xml", encoding="utf-8", xml_declaration=True)