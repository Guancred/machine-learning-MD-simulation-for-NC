from glob import glob
import json
from pymatgen.io.vasp.outputs import Vasprun
import random

def get_document(index,vrun) -> dict:
    """
    Parse the vasprun into a dictionary
    
    Args:
        vrun (Vasprun object): the vasprun object from pymatgen
        
    Returns:
        dict of mliap data
    """
    structure = vrun.ionic_steps[index]['structure'].as_dict()
    energy = vrun.ionic_steps[index]['e_wo_entrp']
    forces = vrun.ionic_steps[index]['forces']
    stress = vrun.ionic_steps[index]['stress']
    return {"structure": structure, 
           "outputs": {"energy": energy,
                      "forces": forces,
                      "stress": stress}}

def data_split(full_list,ratio,shuffle=False):
    n_total = len(full_list)
    offset = int(n_total * ratio)
    if n_total == 0 or offset < 1:
        return [],full_list
    if shuffle:
        random.shuffle(full_list)
    sublist_1 = full_list[:offset]
    sublist_2 = full_list[offset:]
    return sublist_1,sublist_2



vasprun_files = glob("MTP_lammps/vasprun_files/vasprun*")
test_vasprun,train_vasprun = data_split(vasprun_files,ratio=0.2,shuffle=True)


train_data = []
test_data = []

for vrun_file in train_vasprun:
    vrun = Vasprun(vrun_file)
    for i in range(0,len(vrun.ionic_steps)):
            mliap_doc = get_document(i,vrun)
            train_data.append(mliap_doc)

for vrun_t in test_vasprun:
     vrun2 = Vasprun(vrun_t)
     for j in range(0,len(vrun2.ionic_steps)):
            mliap_doc_t = get_document(j,vrun2)
            test_data.append(mliap_doc_t)

                 
    # you can add some tags, groups etc to the mliap doc 
#	mliap_data.append(mliap_doc)	
print("train_data长度为：{}".format(len(train_data)))
print("test_data长度为{}".format(len(test_data)))
with open("MTP_lammps/json_files/train.json", "w") as f:
    json.dump(train_data, f)
with open("MTP_lammps/json_files/test.json", "w") as f:
     json.dump(test_data,f)
