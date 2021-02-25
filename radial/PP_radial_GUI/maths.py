if __name__ == "__main__":
	print("main.py should be started instead")
	exit()

import numpy as np
import scipy.special as sp

hbar = 1 # (to be calculated from physical constants)
h2m = 1 # hbar**2/2m (to be calculated from physical constants)
l = 2 # orbital angular momentum quantum number

# Calculation range (nm)
x_min = 0
x_max = 10
calculations = 1000

# Potential
default_V_barrier = -1.5
V_barrier = default_V_barrier
default_V_1 = 0
V_1 = default_V_1
default_barrier_start = 0  # (nm)
barrier_start = default_barrier_start
default_barrier_end = 2
barrier_end = default_barrier_end

potential = [[], []]  # Potential plot data

# Energy
default_E = 1
E = default_E
E_min = -2
E_max = 2

energy = [[x_min, x_max], []]  # Potential plot data

# Constants
k_s = 0
k_b = 0
K_b = 0
k_e = 0
A = 0
B = 0
R = 0
T = 0

# Wave function
psi_min = -4
psi_max = 4
psi = [[], []]

# Wave
wave_packet = False
alpha = 1
omega = E/hbar
default_a = 1
a = default_a
a_min = 0.1
a_max = 5
delta_start = -4

# Time
default_t = 0
t = default_t
t_min = 0
t_max = 5

def calculate_potential():
	""" Calculates the value of the potential """
	global potential
	potential[0] = [x_min, barrier_end, barrier_end, x_max]
	potential[1] = [V_barrier, V_barrier, V_1, V_1]


def calculate_effective_potential():
	""" Calculates the effective potential """
	global effective_potential

	effective_potential[0] = np.linspace(x_min, x_max, calculations)
	effective_potential[1] = []

	for x in effective_potential[0]:
            if x < barrier_end:
                effective_potential[1].append(V_barrier + l*(l+1)/x**2*h2m)
            else:
                effective_potential[1].append(V_1 + l*(l+1)/x**2*h2m)                


def calculate_energy():
	""" Calculates the value of the potential """
	global energy
	energy[1] = [E, E]


def calculate_wave_function():
	""" Calculates the wave function """
	global psi
	calculate_constants()

	psi[0] = np.linspace(x_min, x_max, calculations)
	psi[1] = []

	time_factor = np.exp(-1j * omega * t)
	for x in psi[0]:
		psi[1].append(wave_function_value(x) * time_factor)


def calculate_constants():
	""" Calculate needed constants for the wave function """
	global k_e, k_b, td

	k_e = np.sqrt(E/h2m + 0j)  # + Oj added to allow square root calculation for negative numbers
	k_b = np.sqrt((E - V_barrier) / h2m + 0j)

	x_e = barrier_end
	
	td = (k_e*sp.spherical_jn(l,k_b*x_e)*sp.spherical_jn(l+1,k_e*x_e)-k_b*sp.spherical_jn(l,k_e*x_e)*sp.spherical_jn(l+1,k_b*x_e)) \
            /(k_e*sp.spherical_jn(l,k_b*x_e)*sp.spherical_yn(l+1,k_e*x_e)-k_b*sp.spherical_yn(l,k_e*x_e)*sp.spherical_jn(l+1,k_b*x_e)) # phase-shift tangent


def gaussian(x, x_start, direction=1):
    return 1 # error in calculation by Vandentempel
	#if wave_packet:
		#k = k_0
		#v = alpha * k
		#w = a ** 2 + 1j * alpha * t / 2
		#x = x - x_start
		#return np.exp(-((direction * x - v*t)**2)/(4*w))
	#else:
		#return 1


def wave_function_value(x):
        """ Returns value of wave function in x """
        if x < barrier_end:
#            return np.sin(k_b * x)/k_b #  l=0 only
            return sp.spherical_jn(l, k_b * x) * x / k_b**l
        else:  # x > barrier_end
#            return np.sin(k_e * x) / np.sin(k_e * barrier_end) * np.sin(k_b * barrier_end)/k_b  # l=0 only
            return (sp.spherical_jn(l, k_e * x) - td * sp.spherical_yn(l, k_e * x)) \
                 / (sp.spherical_jn(l, k_e * barrier_end) - td * sp.spherical_yn(l, k_e * barrier_end)) \
                 *  sp.spherical_jn(l, k_b * barrier_end) * x/k_b**l
