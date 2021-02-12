from EveDB import EveDB
import time


class TimeCalc:
    def __init__(self, eve_db):
        self.eve_db = eve_db

    # def timer(self):
    # te = (percent(32.0) * percent(42.0) * percent(bp_te) * percent(15.0))
    # sec = self.eve_db.get_time(item_name + " blueprint") * runs * te
    # ty_res = time.gmtime(sec)
    # res = time.strftime("%H:%M:%S", ty_res)
    # print(res)


def percent(x):
    return 1 - (x / 100)


skills = {
    "science": 0,
    "industry": 0,
    "adv_industry": 0,
    "metallurgy": 0,
    "research": 0,
    "reactions": 0,
}
