if __name__ == "__main__":
	print("main.py should be started instead")
	exit()

import scipy.constants as cst

print('Select unit system')
print('1. Atomic physics')
print('2. Nuclear physics')
n_pb = int(input('   please enter unit system number: '))

m1 = float(input('   enter mass of particle 1: '))
m2 = float(input('   enter mass of particle 2: '))
mu = m1*m2/(m1+m2)

if n_pb == 1:
	print('Atomic physics')

	# units
	print('Length unit = nm')
	print('Energy unit = eV')
	print('Mass unit = electron mass')

	h2m = cst.hbar**2 / 2 / mu / cst.m_e / cst.e*1e18 # hbar**2/2 m_e (eV nm**2)

	print('hbar**2/2mu=', h2m, 'eV nm**2')

elif n_pb == 2:
	print('Nuclear physics')

	# units
	print('Length unit = fm')
	print('Energy unit = MeV')
	print('Mass unit = atomic mass unit')

	h2m = cst.hbar ** 2 / 2 / mu / cst.atomic_mass / cst.e * 1e24  # hbar**2/2 m_e (MeV fm**2)

	print('hbar**2/2mu=', h2m, 'MeV fm**2')

else :
	print('Wrong choice')
	exit()