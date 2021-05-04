import mysql.connector


# TODO: CHOOSE industryactivitymaterials FOR A BETTER QUERY, remove index from invtypes (typename)
class EveDB:
    def __init__(self):
        self.eve_db = mysql.connector.connect(user='root', password='root', host='localhost', database="evetest")
        self.cursor = self.eve_db.cursor(named_tuple=True)

    def get_item_info(self, name):
        self.cursor.execute(f"SELECT typeID FROM invtypes WHERE typeName=\"{str(name)}\"")

        data = self.cursor.fetchone()
        return data[0]

    def get_name(self, item_id):
        self.cursor.execute(f"SELECT typeName FROM invtypes WHERE typeID={item_id}")
        data = self.cursor.fetchone()

        return data[0]

    def get_print(self, item_id, activity_id=11):
        query = f"SELECT r.typeName AS print_name, l.typeID AS print_id,  l.quantity AS output_quantity " \
                f"FROM industryactivityproducts l INNER JOIN invtypes r ON l.typeID = r.typeID " \
                f"WHERE l.activityID = {activity_id} AND r.published = 1 AND l.productTypeID = {item_id}"

        self.cursor.execute(query)
        data = self.cursor.fetchone()

        return data

    def get_reactions(self, item_id):
        query = f"SELECT r.typeName AS input_name, l.materialTypeID AS input_id, l.quantity " \
                f"FROM industryactivitymaterials l INNER JOIN invtypes r ON l.materialTypeID = r.typeID " \
                f"WHERE l.activityID = 11 AND l.typeID = {item_id}"

        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data

    def get_id(self, item_name):
        self.cursor.execute(f"SELECT typeID FROM invtypes WHERE typeName=\"{str(item_name)}\"")

        data = self.cursor.fetchone()

        return data[0]

    def get_mats2(self, item):
        query = f"SELECT materialTypeID AS mat_id, typeName AS name, groupID AS group_id, quantity AS quantity " \
                f"FROM eve.industryactivitymaterials l JOIN eve.invtypes r " \
                f"WHERE l.materialTypeID=r.typeID AND activityID=1 AND l.typeID={item} " \
                f"ORDER BY materialTypeID "

        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data

    def get_adv(self, item):
        query = f"SELECT r.typeName as mat_name, materialTypeID as mat_id, quantity as mat_quantity " \
                f"FROM evetest.invtypematerials l " \
                f"JOIN evetest.invtypes r " \
                f"WHERE materialTypeID=r.typeID AND l.typeID={item};"

        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data

    def get_time(self, item):
        item_id = self.get_id(item)
        query = f"SELECT time FROM industryactivity WHERE activityID=1 AND typeID={item_id}"
        self.cursor.execute(query)

        data = self.cursor.fetchone()

        return data[0]

    def get_t1_variant(self, item_name):
        self.cursor.execute(
            f"SELECT parentTypeID "
            f"FROM eve.invmetatypes AS l JOIN eve.invtypes as r "
            f"WHERE l.typeID = r.typeID AND r.typeName=\"{item_name}\"")

        data = self.cursor.fetchone()
        return data[0]

    def get_mats(self, item):
        item_id = self.get_id(item)
        query = f"SELECT * FROM invtypematerials WHERE typeID={item_id}"
        self.cursor.execute(query)

        data = self.cursor.fetchall()

        return data

    def get_meta_lvl(self, item_name):
        self.cursor.execute(
            f"SELECT metaGroupID FROM eve.invmetatypes AS l JOIN eve.invtypes as r WHERE l.typeID = r.typeID AND r.typeName=\"{item_name}\"")

        data = self.cursor.fetchone()
        return data[0]

def percent(x):
    return 1 - (x / 100)


db = EveDB()
# res = d.get_mats("vexor")
# res2 = d.get_mats2(971)
#
# res = [(d.get_name(i[0]), i[1]) for i in res]
# res2 = [(d.get_name(i[0]), i[1]) for i in res2]
# print(res)
# print(res2)
# # print(d.get_meta_lvl("vexor"))
# print(d.get_t1_variant("Ishtar"))
# print(d.get_id("Dual Giga Pulse Laser II"))
# print(d.get_mats("Ferox"))


# te = (percent(20.0)*percent(42.0)*percent(20.0)*percent(20.0)*percent(15.0))
# sec = d.get_time("Bantam Blueprint") * 7 * te
# ty_res = time.gmtime(sec)
# res = time.strftime("%H:%M:%S", ty_res)
# print(res)
