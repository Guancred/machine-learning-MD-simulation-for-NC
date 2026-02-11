from pymatgen.core.structure import Structure, Composition
from pymatgen.io.vasp.outputs import Xdatcar
import os
import re
import pandas as pd

folder_path = 'XDAT_data'

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path,file_name)
    len_xdatcar = len(Xdatcar("{}".format(file_path)).structures)
    structures = Xdatcar("{}".format(file_path),ionicstep_start=1,ionicstep_end=len_xdatcar).structures
    for steps in range(2000,len(structures),245):
    #for steps in range(2000,2003,1):
        stru = structures[steps]
        number = re.findall(r'\d+',file_name)
        stru.to(filename='./structures/POSCAR{}{}.vasp'.format(int(float(number[0])/100),steps),fmt = 'poscar')
        




