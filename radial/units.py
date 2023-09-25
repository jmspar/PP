if __name__ == "__main__":
	print("main.py should be started instead")
	exit()

import scipy.constants as cst

print('Electron in quantum dot')

# units
print('Length unit = nm')
print('Energy unit = eV')

h2m = cst.hbar**2/2/cst.m_e/cst.e*1e18 # hbar**2/2 m_e (eV nm**2)

print('hbar**2/2m_e=', h2m, 'eV nm**2')
