import db

class Recipe(object):
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients
        # you could also check here for properly formatted ingredients

    def need_ingredients(self):
        needed = []
        for (generic_type, amount) in self.ingredients:
            matching = db.check_inventory_for_type(generic_type)

            max_m = ''
            max_l = ''
            max_amount = 0.0

            for (m, l, t) in matching:
                if t > max_amount:
                    max_amount = t

            amount_needed = db.convert_to_ml(amount)

            if max_amount < amount_needed:
                needed.append((generic_type, amount_needed - max_amount))

        return needed
