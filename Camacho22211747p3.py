"""
Práctica 3: Sistema Musculoesqueletico

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Nicole Zoe Camacho Quezada
Número de control: 22211747
Correo institucional: L22211747@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot
import control

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import matplotlib.pyplot as plt



x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1

def musculo(Cs,R,Cp,alpha):
    num = [Cs*R,0.75]
    den = [R*(Cp+Cs),1]
    sys = control.tf(num,den)
    return sys


# Funcion de transferencia: Fs(t): control
Cs,R,Cp,alpha = 10E-6,100,100E-6,0.25
syscontrol = musculo(Cs,R,Cp,alpha)
print(f'Control: {syscontrol}')

# Funcion de transferencia: Fs(t): caso
Cs,R,Cp,alpha = 10E-6,10E3,100E-6,0.25
syscaso = musculo(Cs,R,Cp,alpha)
print(f'Caso: {syscaso}')


# Respuestas en lazo abierto
_, Fs1 = control.forced_response(syscontrol,t,u2,x0)
_, Fs2 = control.forced_response(syscaso,t,u2,x0)


clr1 = np.array([119, 190, 240])/255
clr2 = np.array([255, 203, 97])/255
clr3 = np.array([255, 137, 79])/255
clr4 = np.array([138, 166, 36])/255
clr5 = np.array([92, 47, 194])/255
clr6 = np.array([234, 91, 111])/255

fg1 = plt.figure();
plt.plot(t,u2,'-', linewidth = 1, color = clr3, label = 'Fs(t)') 
plt.plot(t, Fs1,'-', linewidth = 1, color = clr1, label ='Fs(t): Control')
plt.plot(t,Fs2,'-', linewidth = 1, color = clr2, label ='Fs(t):Caso)')

plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.2,0.1))
plt.xlabel('t[s]')
plt.ylabel('Fs(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('sistema musculoesqueletico python.png',dpi=600,bbox_inches='tight')
fg1.savefig('sistema musculoesqueletico python.pdf',bbox_inches='tight')

def controlador(kP,kI):
    Cr = 1E-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    numPI = [Rr*Cr,1]
    denPI = [Re*Cr,0]
    PI = control.tf(numPI,denPI)
    return PI

PI = controlador(0.0219712691125975,41303.6112882169)
X = control.series(PI,syscaso)
sysPID = control.feedback(X,1,sign=-1)


_, Fs3 = control.forced_response(sysPID,t,Fs1,x0)


#Respuestas en lazo cerrado
fg2 = plt.figure();
plt.plot(t,u2,'-', linewidth = 1, color = clr3, label = 'Fs(t)') 
plt.plot(t,Fs1,'-', linewidth = 1, color = clr1, label ='Fs(t): Control')
plt.plot(t,Fs2,'-', linewidth = 1, color = clr2, label ='Fs(t): Caso')
plt.plot(t,Fs3,'--', linewidth = 2, color = clr4, label ='Fs(t): Tratamiento')


plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.2,0.1))
plt.xlabel('t[s]')
plt.ylabel('Fs(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=4)
plt.show()
fg2.set_size_inches(w,h)
fg2.tight_layout()
fg2.savefig('sistema musculoesqueletico PI python.png',dpi=600,bbox_inches='tight')
fg2.savefig('sistema musculoesqueletico PI python.pdf',bbox_inches='tight')


