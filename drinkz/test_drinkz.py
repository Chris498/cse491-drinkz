"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and executed (although there are many more
rules ;).
"""

import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp

from . import db, load_bulk_data, recipes

def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'

def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'
    
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')

def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

def test_add_to_inventory_2():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass

def test_get_liquor_amount_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.0, amount

def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_inventory_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_bottle_type('a', 'b', 'xxx')
    
    data = "Johnnie Walker,Black Label,1000 ml\n   \n\n# comment\na,b,10 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 2, n

def test_bulk_load_inventory_3():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    data = "Johnnie Walker,Black Label,1000 ml\na,b\n"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.0, amount

def test_get_liquor_amount_3():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml\nJohnnie Walker,Black Label,500 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1500.0, amount

def test_get_liquor_amount_4():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml\nJohnnie Walker,Black Label,50 oz"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 2478.675, amount

def test_get_liquor_amount_5():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml\nJohnnie Walker,Black Label,50 gallons"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    try:
        amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
        assert 0
    except:
        pass                            # we expect to see an error about gallons

def test_bulk_load_bottle_types_1():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_bottle_types_2():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch\n     \na,b,c"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 2, n

def test_bulk_load_bottle_types_3():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch\n# test comment\na,b,c\n\n"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 2, n

def test_bulk_load_bottle_types_4():
    db._reset_db()

    data = "a,b"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert n == 0, n

def test_script_load_bottle_types_1():
    db._reset_db()

    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    
def test_script_load_inventory_1():
    db._reset_db()

    scriptpath = 'bin/load-liquor-inventory'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt', 'test-data/inventory-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1234.0, amount

def test_script_load_recipes_1():
    db._reset_db()

    scriptpath = 'bin/load-recipes'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/recipes-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code
    newRecipe = recipes.Recipe('sunshine', [('unflavored vodka', '100 oz')])


    for r in db.get_all_recipes():
        if(r.name == 'sunshine'):
	   assert newRecipe.ingredients == r.ingredients

def test_script_load_recipes_2():
    db._reset_db()

    scriptpath = 'bin/load-recipes'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/recipes-2.txt'])
    
    assert exit_code == 0, 'non zero exit code %s' % exit_code
    newRecipe1 = recipes.Recipe('Moon dust', [('vodka', '200 oz')])
    newRecipe2 = recipes.Recipe('Abraham Brew', [('beer','200 oz'),('gin','50 oz')])
    
    for r in db.get_all_recipes():
        if(r.name == 'Moon dust'):
            assert newRecipe1.ingredients == r.ingredients
	if(r.name =='Abraham Brew'):
	    assert newRecipe2.ingredients == r.ingredients
    
def test_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x


def test_get_recipes_from_inventory_1():
        db._reset_db()

        db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

        db.add_bottle_type('Bacardi', 'vodka', 'unflavored vodka')
        db.add_to_inventory('Bacardi', 'vodka', '20 ml')

        db.add_bottle_type('Natural Light', 'light', 'watery beer')
        db.add_to_inventory('Natural Light', 'light', '500 ml')

        r= recipes.Recipe('Natty Bomb', [('watery beer', '2 oz')])
        db.add_recipe(r)

        x = {}
        x = db.get_recipes_from_inventory()

        assert x['Natty Bomb'] == r

def test_get_recipes_from_inventory_2():
        db._reset_db()

        db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

        db.add_bottle_type('Bacardi', 'vodka', 'unflavored vodka')
        db.add_to_inventory('Bacardi', 'vodka', '200 ml')

        db.add_bottle_type('Natural Light', 'light', 'watery beer')
        db.add_to_inventory('Natural Light', 'light', '500 ml')

        recipe1= recipes.Recipe('Natty Bomb', [('watery beer', '2 oz')])
        db.add_recipe(recipe1)

	recipe2 = recipes.Recipe('Whirlpool', [('unflavored vodka', '1 oz'),('blended scotch', '2 oz')])
	db.add_recipe(recipe2)

        x = {}
        x = db.get_recipes_from_inventory()

        assert x['Natty Bomb'] == recipe1
	assert x['Whirlpool'] == recipe2
