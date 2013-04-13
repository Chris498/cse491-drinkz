"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db, recipes                        # import from local package

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    reader = parse_csv(fp)

    x = []
    n = 0
    for line in reader:
        try:
            (mfg, name, typ) = line
        except ValueError:
            print 'Badly formatted line: %s' % line
            continue
        
        n += 1
        db.add_bottle_type(mfg, name, typ)

    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    reader = parse_csv(fp)

    x = []
    n = 0

    for line in reader:
        try:
            (mfg, name, amount) = line
        except ValueError:
            print 'Badly formatted line: %s' % line
            continue
    
        n += 1
        db.add_to_inventory(mfg, name, amount)

    return n


def load_recipes(fp):
    
    reader = parse_csv(fp)

    x = []
    n = 0
    for line in reader:

	if(len(line) == 3):
            try:
                (name, liquorType, amount) = line
                print '\n name: %s' % name
                print '\n liquor Type: %s' % liquorType
                print '\n amount: %s' % amount

            except ValueError:
	        print 'Badly formatted line: %s' % line
	        continue
	
	    n+=1
            myTuple = (liquorType, amount)
            myList = [myTuple]
            r = recipes.Recipe(name, myList)
            print r.name
            print r.ingredients
	    db.add_recipe(r)
        if(len(line) == 5):
            try:
                (name, liquorType1, amount1,liquorType2,amount2) = line
                print '\n name: %s' % name
                print '\n liquor Type: %s' % liquorType1
                print '\n amount: %s' % amount1
    		print '\n liquor Type: %s' % liquorType2
                print '\n amount: %s' % amount2
            except ValueError:
                print 'Badly formatted line: %s' % line
                continue  

            n+=1
            myTuple1 = (liquorType1, amount1)
            myTuple2 = (liquorType2, amount2)
            myList = [myTuple1, myTuple2]
            r = recipes.Recipe(name, myList)
            print r.name
            print r.ingredients
            db.add_recipe(r)
    return n

def parse_csv(fp):
    reader = csv.reader(fp)

    for line in reader:
        if not line or not line[0].strip() or line[0].startswith('#'):
            continue

        yield line
