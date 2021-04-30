from collections import defaultdict
from pprint import pprint
from EveDB import db
from MaterialCalculator import MaterialCalculator, Blueprint, me_mod
from Reactions import Reactions

# print contents of the Blueprint's materials
# def matprinter(item):
#     print(item)
#     print("Printing item: " + item.name)
#     print(f"{'typeID':<10}"
#           f"{'Material':<40}"
#           f"{'Quantity':<10}")
#     for i in item.mats:
#         print(f''
#               f'{i.mat_id:<10}'
#               f'{i.mat_name:<40}'
#               f'{i.mat_quantity:<10,d}')


import time
start = time.process_time()
import tracemalloc
tracemalloc.start()
mat_calc = MaterialCalculator()

# add chosen items to the list
bp = Blueprint(name="Paladin Blueprint", runs=1, copies=1, me=me_mod(4), te=0)
mat_calc.add_bp(bp)
bp = Blueprint(name="Retribution Blueprint", runs=3, copies=7, me=me_mod(3), te=0)
mat_calc.add_bp(bp)
bp = Blueprint(name="Heretic Blueprint", runs=3, copies=2, me=me_mod(3), te=0)
mat_calc.add_bp(bp)
mat_calc.remove_bp(2)

# mat_calc.print_mats()


# pprint(mat_calc.selection[1].mats)
# pprint(mat_calc.mats)

t2comps = defaultdict(int)
comp_filter = [334]
for mat in mat_calc.mats.values():
    if mat.group_id in comp_filter:
        t2comps[mat.name] = mat

print("printing for: " + db.get_name(46207))
pprint(db.get_reactions(46207))

# t2decomp = Reactions(t2comps)
# print("\nNEW VALUES\n")
# t2decomp.change_adv_moon(11539, 7)

# print(f"time taken: {time.process_time() - start}")
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage is {current / 10**3}KB; Peak was {peak / 10**3}KB; Diff = {(peak - current) / 10**3}KB")
# tracemalloc.stop()
