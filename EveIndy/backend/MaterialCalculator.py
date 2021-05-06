import math
from collections import defaultdict
from dataclasses import dataclass

from EveDB import db


class Blueprint:
    def __init__(self, name, runs=1, copies=1, me=1, te=0):
        self.name = name
        self.id = db.get_item_info(name)
        self.runs = runs
        self.copies = copies
        self.me = me
        self.te = te

        self.mats = defaultdict(int)

        self.time_taken = 0


@dataclass
class MatInfo:
    mat_id: int
    name: str
    group_id: int
    quantity: int


class MaterialCalculator:
    def __init__(self):
        # MatInfo = namedtuple('MatInfo', ['mat_id', 'mat_name', 'group_id', 'mat_quantity'])
        self.selection = []
        # self.mats = defaultdict(int)
        self.mats = {}

    def add_bp(self, bp):
        self.selection.append(bp)
        self.__get_mats(bp)

    def remove_bp(self, index):
        # delete the items from the main mats dict
        for item, quantity in self.selection[index].mats.items():

            self.mats[item].quantity -= quantity
            if self.mats[item].quantity == 0:
                self.mats.pop(item, None)

        # remove the bp from the selection
        del self.selection[index]

    def print_mats(self):
        print(f"{'typeID':<10}"
              f"{'Material':<40}"
              f"{'Quantity':<10}")
        for k, v in self.mats.items():
            print(f'{v.mat_id:<10}'
                  f'{k:<40}'
                  f'{v.quantity:<10,d}')

    # fetch materials from database
    def __get_mats(self, item):
        all_mats = db.get_mats2(item.id)
        for i in all_mats:
            adj_mats = modified_mats(i.quantity, item.me, item.runs, item.copies)
            item.mats[i.name] = adj_mats
            # self.mats[i.name] += adj_mats

            if i.name in self.mats:
                self.mats[i.name].quantity += adj_mats
            else:
                self.mats[i.name] = MatInfo(i.mat_id, i.name, i.group_id, adj_mats)


def me_mod(x=1, rig_bonus=4.2, role_bonus=1.0):
    structure_rig = rig_bonus
    structure_role = role_bonus
    return (1 - (structure_rig / 100.0)) * (1 - (structure_role / 100.0)) * (1 - (x / 100.0))


def modified_mats(quantity, me, runs, copies=1):
    return math.ceil(max(1, quantity * me) * runs) * copies
