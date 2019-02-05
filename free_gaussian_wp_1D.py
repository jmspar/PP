# free Gaussian wave packet time evolution
# to run, type "python3 simon_1D.py" in command line
# (after installing Python 3 with required libraries and downloading the file!)
# original Python 3 code by BA2 student Corentin Simon (2017-2018), to be improved!
# Jean-Marc Sparenberg

from math import sin, pi,cos
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import matplotlib.cm as cm
from matplotlib.widgets import Slider
from matplotlib.widgets import CheckButtons



fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

plt.subplots_adjust(left=0.12, bottom=0.35)

k0 = 6 #nombre d'onde central du packet gaussien
a = 1 #	facteur de distribution de la gaussienne
srx = 50 #range de la position en x

x = np.linspace(-srx/3, 2*srx/3, srx*20) #absisse de la simulation
x2 = np.linspace(0, 20, 1000)#absisse de l'espace des fréquences




alpha = 1 ## alpha = hbar/m => v = alpha*k
is_color = False 


def psi(t): #calcul de la fonction d'onde en fonction du temps
	global x
	v = alpha*k0
	w = (a**4 + ((alpha*t)**2)/4)
	wComplex = a**2 + 1j*alpha*t/2
	omega = (k0**2)*alpha/2
	probCompl = np.exp(1j*(k0*x - t*omega))*((pi/wComplex)**0.5)*np.exp(-((x - v*t)**2)/(4*wComplex))
	return probCompl


#-- Creation des sliders --



ax_a = plt.axes([0.1, 0.05, 0.8, 0.03])
a_slider = Slider(ax_a, '$t$', 0, 10, valinit=0) #slider tu temps
a_slider.label.set_size(20)

ax_b = plt.axes([0.1, 0.15, 0.8, 0.03])
b_slider = Slider(ax_b, '$a$', 0.01, 5, valinit=a) #slider de a
b_slider.label.set_size(20)


ax_c = plt.axes([0.1, 0.25, 0.8, 0.03])
c_slider = Slider(ax_c, '$k_0$', 1, 15, valinit=k0)#slider de k0
c_slider.label.set_size(20)


rax = plt.axes([0.01, 0.45, 0.08, 0.1]) #bouton de control de la couleur
check = CheckButtons(rax, ['Couleur'], [False])



def update_phase(val_):
	global a
	a = b_slider.val
	y = np.exp(- (a**2)*(k0-x2)**2) #distribution des fréquences
	ax1.clear()
	ax1.set_title('Transformée de Fourier')
	ax1.plot(x2, y)
	
	fig.canvas.draw_idle()
	update_temps(0) 

def update_temps(val_): #dessin de la fonction d'onde

	probCompl = psi(a_slider.val)
	ax2.clear()
	ax2.set_xlim([-srx/3,2*srx/3])
	ax2.set_ylim([-4, 4])
	ax2.set_title('Fonction d\'onde')

	if(is_color): #affichage en couleur
		X = np.array([x,x])
		y0 = np.zeros(len(x))
		y = [abs(i) for i in probCompl]
		Y = np.array([y0,y])
		Z = np.array([probCompl,probCompl])
		C = np.angle(Z)
		ax2.pcolormesh(X, Y, C, cmap=cm.hsv, vmin=-np.pi, vmax=np.pi)
		ax2.plot(x, np.abs(probCompl), label = '$|\psi|$', color='black')

	else: #affichage des parties reels et complexe
		ax2.plot(x, np.real(probCompl), label = '$\operatorname{Re}(\psi)$')
		ax2.plot(x, np.imag(probCompl), label = '$\operatorname{Im}(\psi)$')
		ax2.plot(x, np.absolute(probCompl)**2, label = '$\psi \psi^{\dag} $')
	
	ax2.legend(fontsize=15)
	fig.canvas.draw_idle()

def update_k(val_): #lorsqu'on chnage k0
	global k0
	k0 = c_slider.val
	update_phase(0)
	update_temps(0)

def on_check(label): #quand on clic sur le bouton
	global is_color
	is_color = not is_color
	update_temps(0)


update_phase(0) #creation de la première frame

#association des fonctions aux sliders 


a_slider.on_changed(update_temps)
b_slider.on_changed(update_phase)
c_slider.on_changed(update_k)

check.on_clicked(on_check)



plt.show()
