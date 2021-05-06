import math
from collections import defaultdict
from dataclasses import dataclass, field

from EveDB import db
from MaterialCalculator import modified_mats, me_mod


@dataclass
class CompInfo:
    name: str
    mat_id: int
    quantity: int
    used: int = 1
    runs_per: int = field(init=False)
    total_runs: int = field(init=False)

    def __post_init__(self):
        self.update_runs_per()
        self.update_total()

    def update_runs_per(self):
        self.runs_per = math.ceil(self.quantity / self.used)

    def update_total(self):
        self.total_runs = math.ceil(self.runs_per * self.used)


@dataclass
class ReactionInfo:
    mat_name: str
    mat_id: int
    quantity: int
    print_name: str
    print_id: int
    output: int = 2
    used: int = 1
    total_runs: int = field(init=False)
    runs_per: int = field(init=False)

    def __post_init__(self):
        self.update_all()

    # function to make it easier to update the object's fields
    def update_all(self):
        self.update_total_runs()
        self.update_runs_per()

    def update_total_runs(self):
        self.total_runs = math.ceil(self.quantity / self.output)

    def update_runs_per(self):
        self.runs_per = math.ceil(self.total_runs / self.used)

    def change_used(self, new_used):
        self.used = new_used
        self.update_all()


# TODO: convert moon to tier1, tier2, etc. to allow for t3 production
# TODO: store and get used amounts from db

fuel_filter = [1136, 1137]


class Reactions:
    def __init__(self):
        # prints for editing used amount

        self.comps = {}  # contains CompInfo objects
        self.adv_moon_print = {}
        self.processed_prints = {}
        self.fuel = defaultdict(int)
        self.moon_goo = defaultdict(int)

    def set_comps(self, comps):
        # create objects for comp BPOs
        for comp in comps:
            used = 1
            self.comps[comp.mat_id] = CompInfo(comp.name, comp.mat_id, comp.quantity, used)

    def change_comps(self, item_id, new_used):
        """
        :param item_id: id of the formula
        :param new_used: new amount of formulas to use
        """
        self.comps[item_id].used = new_used
        self.comps[item_id].update_runs_per()

    def set_adv(self):
        self.adv_moon_print = {}
        for comp in self.comps.values():
            for i in db.get_adv(comp.mat_id):
                print_name, print_id, output_quantity = db.get_print(i.mat_id)
                runs = comp.runs_per
                bps = comp.used
                quantity = modified_mats(i.mat_quantity, me_mod(10), runs, bps)
                if print_id in self.adv_moon_print:
                    self.adv_moon_print[print_id].quantity += quantity
                    self.adv_moon_print[print_id].update_all()
                else:
                    self.adv_moon_print[print_id] = ReactionInfo(i.mat_name, i.mat_id, quantity, print_name, print_id,
                                                                 output_quantity)
        self.set_processed()

    def change_adv(self, item_id, new_used):
        """
        :param item_id: id of the formula
        :param new_used: new amount of formulas to use
        """
        self.adv_moon_print[item_id].used = new_used
        self.adv_moon_print[item_id].update_all()
        self.set_processed()

    def set_processed(self):
        self.processed_prints = {}
        for reaction in self.adv_moon_print.values():
            for i in db.get_reactions(reaction.print_id):
                quantity = modified_mats(i.mat_quantity, me_mod(0, 0, 2.64), reaction.runs_per, reaction.used)
                if i.group_id in fuel_filter:
                    self.fuel[db.get_name(i.mat_id)] += quantity
                else:
                    print_name, print_id, output_quantity = db.get_print(i.mat_id)
                    if print_id in self.processed_prints:
                        self.processed_prints[print_id].quantity += quantity
                        self.processed_prints[print_id].update_all()
                    else:
                        self.processed_prints[print_id] = ReactionInfo(i.mat_name, i.mat_id, quantity, print_name,
                                                                       print_id,
                                                                       output_quantity)
        self.set_goo()

    def change_processed(self, item_id, new_used):
        """
        :param item_id: id of the formula
        :param new_used: new amount of formulas to use
        """
        self.processed_prints[item_id].used = new_used
        self.processed_prints[item_id].update_all()
        self.set_goo()

    def set_goo(self):
        self.moon_goo = defaultdict(int)
        for reaction in self.processed_prints.values():
            for i in db.get_reactions(reaction.print_id):
                quantity = modified_mats(i.mat_quantity, me_mod(0, 0, 2.64), reaction.runs_per, reaction.used)
                if i.group_id in fuel_filter:
                    self.fuel[db.get_name(i.mat_id)] += quantity
                else:
                    self.moon_goo[i.mat_name] += quantity
