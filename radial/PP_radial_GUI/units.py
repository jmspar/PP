if __name__ == "__main__":
	print("main.py should be started instead")
	exit()

import scipy.constants as cst

print('Select unit system')
print('1. Atomic physics')
print('2. Nuclear physics')
n_us = int(input('   please enter unit system number: '))
#n_us = 2

if n_us == 1:
	print('Atomic physics')

	lu = 'nm'
	Eu = 'eV'
	print('Mass unit = electron mass')

	h2m = cst.hbar**2 / 2 / cst.m_e / cst.e * 1e18 # hbar**2/2 m_e (eV nm**2)

elif n_us == 2:
	print('Nuclear physics')

	lu = 'fm'
	Eu = 'MeV'
	print('Mass unit = atomic mass unit')

	h2m = cst.hbar ** 2 / 2 / cst.atomic_mass / cst.e * 1e24  # hbar**2/2 m_e (MeV fm**2)

else :
	print('Wrong choice')
	exit()

print('Length unit = ', lu)
print('Energy unit = ', Eu)

#m1 = float(input('   enter mass of particle 1: '))
m1 = float(16)
#m2 = float(input('   enter mass of particle 2: '))
m2 = float(4)
mu = m1*m2/(m1+m2)

h2m = h2m / mu

print('hbar**2/2mu=', h2m, Eu, lu, '**2')
