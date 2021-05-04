import math
from collections import defaultdict
from dataclasses import dataclass, field
from pprint import pprint
# from typing import Any

from EveDB import db
from MaterialCalculator import modified_mats, me_mod


@dataclass
class CompInfo:
    name: str
    mat_id: int
    quantity: int
    used: int = 1
    runs_per: int = field(init=False)
    total: int = field(init=False)

    def __post_init__(self):
        self.update_runs_per()
        self.update_total()

    def update_runs_per(self):
        self.runs_per = math.ceil(self.quantity / self.used)

    def update_total(self):
        self.total = math.ceil(self.runs_per * self.used)


@dataclass
class ReactionInfo:
    name: str
    print_id: int
    quantity: int
    output: int
    used: int = 1
    runs_per: int = field(init=False)

    def __post_init__(self):
        # self.__update_total()
        self.update_runs()

    # def __update_total(self):
    #     self.total_runs = math.ceil(self.quantity / self.output)

    def update_runs(self):
        self.runs_per = math.ceil(self.quantity / self.used)

    def change_used(self, new_used):
        self.used = new_used
        self.update_runs()


# TODO: convert moon to tier1, tier2, etc. to allow for t3 production
# TODO: store and get used amounts from db

# Ask user runs per comp bpo first, then store that in an object and use for runs
class Reactions:
    def __init__(self):
        # prints for editing used amount
        # mats to collect total mats
        self.comps = {}  # contains CompInfo objects
        self.adv_moon_print = {}
        self.adv_moon_mats = defaultdict(int)
        # self.processed_prints = None
        # self.moon_goo = None

    def set_comps(self, comps):
        # create objects for comp BPOs
        for comp in comps:
            used = 1
            self.comps[comp.mat_id] = CompInfo(comp.name, comp.mat_id, comp.quantity, used)

    def change_comps(self, item_id, new_used):
        self.comps[item_id].used = new_used
        self.comps[item_id].update_runs_per()

    def after(self):
        pprint(self.comps)
        pprint(self.adv_moon_print)

    def fill_adv(self):
        self.adv_moon_print = {}
        for comp in self.comps.values():
            # print(comp)
            for i in db.get_adv(comp.mat_id):
                print(i)
                break
                # if i.mat_name in self.adv_moon_print:
                #     self.adv_moon_print[i.mat_name].quantity += 1
                # else:
                #     runs = comp.runs_per
                #     bps = comp.used
                #     quantity = modified_mats(i.mat_quantity, me_mod(10), runs, bps)
                #     self.adv_moon_print[i.mat_name] = ReactionInfo(i.mat_name, i.mat_id, quantity, 100000)
                # self.adv_moon_print[i.mat_name] += modified_mats(i.mat_quantity, me_mod(10), runs, bps)
        # print the contents
        # for k, v in self.adv_moon_mat.items():
        #     print(f"{k:<35}{v:<10,d}")
    #
    # def fill_processed(self):
    #     self.processed_prints = {}
    #     for mat_name, quantity in self.adv_moon_print.items():
    #         print_name, print_id, output_quantity = db.get_print(db.get_id(mat_name))
    #         self.processed_prints[print_id] = ReactionInfo(print_name, print_id, quantity, output_quantity)
    #         # print(mat_name)
    #         # print(db.get_print(db.get_id(mat_name)))
    #         # break
    #
    #     # pprint(self.processed_moon_mat[db.get_id('Tungsten Carbide Reaction Formula')])
    #     # print(self.adv_moon_mat)
    #     # pprint(self.processed_moon_mat)
    #
    #
    # # TODO: FIX THIS
    # def change_adv_moon(self, item_id, new_used):
    #     self.comps[item_id].used = new_used
    #     self.fill_adv()
    #
    # def change_processed_moon(self, item_id, new_used):
    #     self.processed_prints[item_id].used = new_used
    #     print(self.processed_prints[item_id])
    #     self.fill_processed()

    # debugging
    def print_comps(self):
        print(f"\n{'Name':<40} {'Quantity':<15} {'Used':<15} {'Runs per':<10}")
        for i in self.comps.values():
            print(f"{i.name:<40} {i.quantity:<15,d} {i.used:<15} {i.runs_per():<10,d}")
