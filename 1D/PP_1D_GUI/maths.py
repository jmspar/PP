if __name__ == "__main__":
	print("main.py should be started instead")
	exit()

import numpy as np

# Calculation range (nm)
x_min = -8
x_max = 10
calculations = 1000

# Potential
default_V_0 = 0  # (eV)
V_0 = default_V_0
default_V_barrier = 1
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
E_limit = 0.0

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
default_k_0 = 6
k_0 = default_k_0
k_0_min = 1
k_0_max = 15
alpha = 1
omega = k_0**2 * alpha / 2
default_a = 1
a = default_a
a_min = 0.5
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
	potential[0] = [x_min, barrier_start, barrier_start, barrier_end, barrier_end, x_max]
	potential[1] = [V_0, V_0, V_barrier, V_barrier, V_1, V_1]


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
	global k_s, k_b, K_b, k_e, A, B, R, T, E
	if E - V_0 <= 0:
		return

	k_s = np.sqrt((E - V_0) / E) * k_0
	k_b = np.sqrt((E - V_barrier) / E) * k_0
	K_b = np.sqrt((V_barrier - E) / E) * k_0
	k_e = np.sqrt((E - V_1) / E + 0j) * k_0  # + Oj added to allow square root calculation for negative numbers
	x_s = barrier_start
	x_e = barrier_end

	# Preventing division by 0 (good enough for plotting)
	if k_e == 0:
		k_e = 0.000001
	if k_s == k_b:
		k_s = k_b + 0.000001

	if E - V_barrier > 0:  # Case 1
		A = 1 / \
			((k_b / k_e - 1) / (k_b / k_e + 1) * np.exp(2 * 1j * k_b * x_e) + (1 + k_b / k_s) / (1 - k_b / k_s) * np.exp(2 * 1j * k_b * x_s)) \
			* (2 * np.exp(1j * k_s * k_b * x_s)) / (1 - k_b / k_s)
		B = (k_b / k_e - 1) / (k_b / k_e + 1) * A * np.exp(2 * 1j * k_b * x_e)
		R = np.exp(1j * k_s * x_s) * (A * np.exp(1j * k_b * x_s) + B * np.exp(-1j * k_b * x_s) - np.exp(1j * k_s * x_s))
		T = np.exp(-1j * k_e * x_e) * (A * np.exp(1j * k_b * x_e) + B * np.exp(-1j * k_b * x_e))
	elif E - V_barrier < 0:  # Case 2
		A = 1 / \
			(
					(1j * k_e * np.sinh(K_b * x_e) - K_b * np.cosh(K_b * x_e)) / (
						K_b * np.sinh(K_b * x_e) - 1j * k_e * np.cosh(K_b * x_e))
					+ (1j * k_s * np.sinh(K_b * x_s) + K_b * np.cosh(K_b * x_s)) / (
								1j * k_s * np.cosh(K_b * x_s) + K_b * np.sinh(K_b * x_s))
			) \
			* 2 * 1j * k_s * np.exp(1j * k_s * x_s) / \
			(1j * k_s * np.cosh(K_b * x_s) + K_b * np.sinh(K_b * x_s))
		B = A * \
			(1j * k_e * np.sinh(K_b * x_e) - K_b * np.cosh(K_b * x_e)) / \
			(K_b * np.sinh(K_b * x_e) - 1j * k_e * np.cosh(K_b * x_e))
		R = np.exp(1j * k_s * x_s) * (A * np.sinh(K_b * x_s) + B * np.cosh(K_b * x_s) - np.exp(1j * k_s * x_s))
		T = np.exp(-1j * k_e * x_e) * (A * np.sinh(K_b * x_e) + B * np.cosh(K_b * x_e))
	else:  # E - V_barrier == 0  # Case 3
		A = 2 * np.exp(1j * k_s * x_s) / \
			(x_s - x_e + 1 / (1j * k_s) + 1 / (1j * k_e))
		B = A * (1 / (1j * k_e) - x_e)
		R = np.exp(1j * k_s * x_s) * (np.exp(1j * k_s * x_s) - A / (1j * k_s))
		T = A / (1j * k_e * np.exp(1j * k_e * x_e))


def gaussian(x, x_start, direction=1):
	if wave_packet:
		k = k_0
		v = alpha * k
		w = a ** 2 + 1j * alpha * t / 2
		x = x - x_start
		return np.exp(-((direction * x - v*t)**2)/(4*w))
	else:
		return 1


def wave_function_value(x):
	""" Returns value of the wave function at a x value """
	if E - V_0 <= 0:
		return 0
	else:  # E - V_0 > 0
		if x < barrier_start:
			return gaussian(x, barrier_start + delta_start, 1) * np.exp(1j * k_s * x) + gaussian(x, barrier_start - delta_start, -1) * R * np.exp(-1j * k_s * x)
		elif barrier_start <= x <= barrier_end:
			if E - V_barrier > 0:
				return gaussian(x, barrier_start + delta_start, 1) * (A * np.exp(1j * k_b * x) + B * np.exp(-1j * k_b * x))
			elif E - V_barrier < 0:
				return gaussian(x, barrier_start + delta_start, 1) * (A * np.sinh(K_b * x) + B * np.cosh(K_b * x))
			else:  # E - V_barrier = 0
				return gaussian(x, barrier_start + delta_start, 1) * (A * x + B)
		else:  # x > barrier_end
			return gaussian(x, barrier_start + delta_start, 1) * T * np.exp(1j * k_e * x)
