import math
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from MaterialCalculator import MatInfo
# from typing import Any

from EveDB import db
from MaterialCalculator import modified_mats, me_mod


# holds
@dataclass
class CompMat:
    # change parent str to parent int for mat id
    name: str
    comp_id: int
    quantity: int
    owned: int = 10
    used: int = 2

    def runs_per(self):
        return math.ceil(self.quantity / self.used)



# TODO: convert moon to tier1, tier2, etc. to allow for t3 production

# Ask user runs per comp bpo first, then store that in an object and use for runs
class Reactions:
    def __init__(self, materials):
        # pass the materials in
        self.comps = {}
        self.adv_moon_mat = None
        self.processed_moon_mat = None
        self.moon_goo = None

        # create objects for comp BPOs
        for comp_name, comp_info in materials.items():
            pass
            # print(comp_name, comp_quantity)
            used = 1
            self.comps[db.get_id(comp_name)] = CompMat(comp_name, db.get_id(comp_name), comp_info.quantity, used=used)

        self.fill_adv()

    def fill_adv(self):
        self.adv_moon_mat = defaultdict(int)
        for comp in self.comps.values():
            for i in db.get_adv(comp.comp_id):
                runs = comp.runs_per()
                bps = comp.used
                self.adv_moon_mat[i.mat_name] += modified_mats(i.mat_quantity, me_mod(10), runs, bps)
        # print the contents
        # for k, v in self.adv_moon_mat.items():
        #     print(f"{k:<35}{v:<10,d}")

    def fill_processed(self):
        print(self.adv_moon_mat)

    def change_adv_moon(self, item_id, new_used):
        self.comps[item_id].used = new_used
        self.fill_adv()
        # self.print_adv_moon()

    # debugging
    def print_comps(self):
        print(f"\n{'Name':<40} {'Quantity':<15} {'Used':<15} {'Runs per':<10}")
        for i in self.comps.values():
            print(f"{i.name:<40} {i.quantity:<15} {i.used:<15} {i.runs_per():<10}")
