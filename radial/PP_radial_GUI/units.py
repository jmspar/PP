if __name__ == "__main__":
	print("main.py should be started instead")
	exit()

import scipy.constants as cst

print('Select physical problem')
print('1. Electron in spherical quantum dot')
print('2. Nucleus-nucleus central interaction')
n_pb = int(input('   please enter problem number: '))

if n_pb == 1:
	print('Electron in quantum dot')

	# units
	print('Length unit = nm')
	print('Energy unit = eV')

	h2m = cst.hbar**2/2/cst.m_e/cst.e*1e18 # hbar**2/2 m_e (eV nm**2)

	print('hbar**2/2m_e=', h2m, 'eV nm**2')

elif n_pb == 2:
	print('Nucleus-nucleus central interaction')

	# units
	print('Length unit = fm')
	print('Energy unit = MeV')

	h2m = cst.hbar ** 2 / 2 / cst.m_p / cst.e * 1e24  # hbar**2/2 m_e (MeV fm**2)

	print('hbar**2/2mu=', h2m, 'MeV fm**2')

else :
	print('Wrong choice')
	exit()