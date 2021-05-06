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


# import time
# start = time.process_time()
# import tracemalloc
# tracemalloc.start()
mat_calc = MaterialCalculator()

# # add chosen items to the list
bp = Blueprint(name="Paladin Blueprint", runs=1, copies=1, me=me_mod(4), te=0)
mat_calc.add_bp(bp)
bp = Blueprint(name="Retribution Blueprint", runs=3, copies=7, me=me_mod(3), te=0)
mat_calc.add_bp(bp)
# bp = Blueprint(name="Heretic Blueprint", runs=3, copies=2, me=me_mod(3), te=0)
# mat_calc.add_bp(bp)
# mat_calc.remove_bp(2)


t2comps = []
comp_filter = [334]
for mat in mat_calc.mats.values():
    if mat.group_id in comp_filter:
        # can change this to loop over mats and pass each single one to Reactions later
        # avoids making this secondary list that will just be looped over anyway
        t2comps.append(mat)

# pprint(t2comps)

reactions = Reactions()
reactions.set_comps(t2comps)
reactions.change_comps(11543, 2)
reactions.set_adv()
# reactions.change_adv(46207, 2)
# pprint(reactions.comps)
# reactions.change_processed_moon(46208, 2)

# pprint(reactions.processed_moon_mat[46208])
# t2decomp.change_adv_moon(11539, 7)


# print(f"time taken: {time.process_time() - start}")
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage is {current / 10**3}KB; Peak was {peak / 10**3}KB; Diff = {(peak - current) / 10**3}KB")
# tracemalloc.stop()
