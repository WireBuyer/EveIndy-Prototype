import math
from collections import Counter, namedtuple, defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Any

from EveDB import db
from MaterialCalculator import modified_mats, me_mod

# holds
@dataclass
class ParentMat:
    # change parent str to parent int for mat id
    parent_name: Any
    parent_id: Any
    quantity: int
    owned: int = 10
    used: int = 2

    def runs_per(self):
        return math.ceil(self.quantity / self.used)


# Ask user runs per comp bpo first, then store that in an object and use for runs
class T2Decomposition:
    def __init__(self, materials):
        self.comps = {}
        self.adv_moon_mat = None

        # create objects for comp BPOs
        for comp_id, comp_quantity in materials.items():
            used = 3
            self.comps[comp_id] = ParentMat(db.get_name(comp_id), comp_id, comp_quantity, used=used)
        # self.print_adv_moon()

        self.fill_adv()

    def fill_adv(self):
        self.adv_moon_mat = defaultdict(int)
        for comp in self.comps.values():
            for i in db.get_adv(comp.parent_id):
                runs = comp.runs_per()
                bps = comp.used
                self.adv_moon_mat[i.mat_name] += modified_mats(i.mat_quantity, me_mod(10), runs, bps)
        # print the contents
        for k, v in self.adv_moon_mat.items():
            print(f"{k:<35}{v:<10,d}")

    def change_adv_moon(self, item_id, new_used):
        self.comps[item_id].used = new_used
        self.fill_adv()
        # self.print_adv_moon()

    # debugging
    def print_comps(self):
        print(f"\n{'Name':<40} {'Quantity':<15} {'Used':<15} {'Runs per':<10}")
        for i in self.comps.values():
            print(f"{i.parent_name:<40} {i.quantity:<15} {i.used:<15} {i.runs_per():<10}")


