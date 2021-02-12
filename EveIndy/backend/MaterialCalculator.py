import math
from collections import namedtuple
from EveDB import db


class Blueprint:
    def __init__(self, name, runs, copies, me=1, te=0):
        self.name = name
        self.id = db.get_item_info(name)
        self.runs = runs
        self.copies = copies
        self.me = me
        self.te = te

        self.mats = []

        self.time_taken = 0


class MaterialCalculator:

    # fetch materials from database
    def get_mats(self, item):
        MatInfo = namedtuple('MatInfo', ['mat_id', 'mat_name', 'group_id', 'mat_quantity'])
        all_mats = db.get_mats2(item.id)
        for i in all_mats:
            mat = MatInfo(mat_id=i.mat_id,
                          mat_name=i.mat_name,
                          group_id=i.group_id,
                          mat_quantity=modified_mats(i.mat_quantity, item.me, item.runs, item.copies))
            item.mats.append(mat)
        return

    # takes the selection and calls get_mats for all items
    def fill_mats(self, selection):
        for i in selection.values():
            self.get_mats(i)


def me_mod(x=1):
    structure_rig = 4.2
    structure_role = 1
    return (1 - (structure_rig / 100.0)) * (1 - (structure_role / 100.0)) * (1 - (x / 100.0))


def modified_mats(quantity, me, runs, copies=1):
    return math.ceil(max(1, quantity * me) * runs) * copies
