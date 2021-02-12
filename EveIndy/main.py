from collections import defaultdict
from EveDB import EveDB
from MaterialCalculator import MaterialCalculator, Blueprint, me_mod
from T2Decomposition import T2Decomposition


# print contents of the Blueprint's materials
def matprinter(item):
    print("Printing item: " + item.name)
    print(f"{'typeID':<10}"
          f"{'Material':<40}"
          f"{'Quantity':<10}")
    for i in item.mats:
        print(f''
              f'{i.mat_id:<10}'
              f'{i.mat_name:<40}'
              f'{i.mat_quantity:<10,d}')


import time

start = time.process_time()
db = EveDB()
mat_calc = MaterialCalculator()

# add chosen items to the dict
selection = {
    "Paladin Blueprint": Blueprint(name="Paladin Blueprint", runs=1, copies=1, me=me_mod(5), te=0)
}
mat_calc.fill_mats(selection)

materials = defaultdict(int)
comp_filter = [334]
for i in selection.values():
    for mat in i.mats:
        if mat.group_id in comp_filter:
            materials[mat.mat_id] += mat.mat_quantity

print(materials)
t2decomp = T2Decomposition(materials)
print("\n\n\nNEW VALUES\n\n\n")
t2decomp.change_adv_moon(11539, 7)

# print(f"time taken: {time.process_time() - start}")
