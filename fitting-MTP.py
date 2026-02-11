from pymatgen.core import Structure
from monty.serialization import loadfn

train_data = loadfn('MTP_lammps/json_files/train.json')
train_structures = [d['structure'] for d in train_data]
train_energies = [d['outputs']['energy'] for d in train_data]
train_forces = [d['outputs']['forces'] for d in train_data]
#train_stresses = [d['outputs']['stress'] for d in data]

#vasp_stress_order = ['xx','yy','zz','xy','yz','xz']
#snap_stress_order = ['xx','yy','zz','yz','xz','xy']
#train_stresses = []
#for d in data:
#	virial_stress = d['outputs']['stress']
#	print(virial_stress[vasp_stress_order.index(n)] for n in snap_stress_order)
#	train_stresses.append([virial_stress[vasp_stress_order.index(n)]*0.1 for n in snap_stress_order])

from maml.apps.pes import MTPotential

mtp = MTPotential()

mtp.train(train_structures=train_structures, train_energies=train_energies,
          train_forces=train_forces, train_stresses = None, max_dist=5,radial_basis_size=12, stress_weight=0)

test_data = loadfn('MTP_lammps/json_files/test.json')
test_structures = [t['structure'] for t in test_data]
test_energies = [t['outputs']['energy'] for t in test_data]
test_forces = [t['outputs']['forces'] for t in test_data]

df_orig, df_predict = mtp.evaluate(test_structures=test_structures, 
                                   test_energies=test_energies,
                                   test_forces=test_forces, test_stresses=None)


from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd

E_p = np.array(df_predict[df_predict['dtype'] == 'energy']['y_orig'])/df_predict[df_predict['dtype'] == 'energy']['n']
E_o = np.array(df_orig[df_orig['dtype'] == 'energy']['y_orig'])/df_orig[df_orig['dtype'] == 'energy']['n']
pd.DataFrame(E_p).to_csv('Energe_pre.csv')
pd.DataFrame(E_o).to_csv('Energe_ori.csv')
print("MAE of training energy prediction is {} meV/atom".format(mean_absolute_error(E_o,E_p)*1000))

F_p = np.array(df_predict[df_predict['dtype'] == 'force']['y_orig'])/df_predict[df_predict['dtype'] == 'force']['n']
F_o = np.array(df_orig[df_orig['dtype'] == 'force']['y_orig'])/df_orig[df_orig['dtype'] == 'force']['n']
pd.DataFrame(F_p).to_csv('Force_pre.csv')
pd.DataFrame(F_o).to_csv('Force_ori.csv')
print("MAE of training force prediction is {} eV/Å".format(mean_absolute_error(F_o,F_p)))

mtp.write_param(fitted_mtp='fitted.mtp')

#mtp_loaded = MTPotential.from_config(filename='fitted.mtp', elements=["Li", "H", "S"])
#print(mtp_loaded)

#from pymatgen.core import Lattice

#LiSHS = Structure.from_file('./CONTCAR')
#from maml.apps.pes import LatticeConstant

#lc_calculator = LatticeConstant(ff_settings=mtp_loaded)
#a, b, c = lc_calculator.calculate([LiSHS])[0]
#print('LiSHS', 'Lattice a: {}, Lattice b: {}, Lattice c: {}'.format(a, b, c))
