"""
Database functionality for drinkz information.
"""

from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes = {}
_music = {}
def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes = {}
    _music = {}

def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipes)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipes
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipes) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class DuplicateRecipeName(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    # just add it to the inventory database as a tuple, for now.
    key = (mfg, liquor)
    _inventory_db[key] = _inventory_db.get(key, 0.0) + convert_to_ml(amount)
    
def add_to_music(request):

    #if request.name in _music:
    #    _music[request.name].append(request)
    #else:        
    _music[request.name] = request

def get_all_music():
     return _music.values()

def check_inventory(mfg, liquor):
    return ((mfg, liquor) in _inventory_db)

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."

    return _inventory_db.get((mfg, liquor), 0.0)

def convert_to_ml(amount):
    # amount is going to be in format "number units"
    num, units = amount.split()
    num = float(num)
    units = units.lower()

    if units == 'ml':
        pass
    elif units == 'liter':
        num = 1000.0 * num
    elif units == 'oz':
        num = 29.5735 * num
    elif units == 'gallon' or units == 'gallons':
        num = 3785.41 * num
    else:
        raise Exception("unknown unit %s" % units)

    return num

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."

    for m, l in _inventory_db:
        yield m, l

def add_recipe(r):
    if r.name in _recipes:
        raise DuplicateRecipeName
    _recipes[r.name] = r

def get_recipe(name):
    return _recipes.get(name)

def get_all_recipes():
    return _recipes.values()

def check_inventory_for_type(generic_type):
    matching_ml = []
    for (m, l, t) in _bottle_types_db:
        if t == generic_type:
            amount = _inventory_db.get((m, l), 0.0)
            matching_ml.append((m, l, amount))

    return matching_ml

