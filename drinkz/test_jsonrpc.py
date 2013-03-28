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
from . import db, recipes
from drinkz.app import SimpleApp
from wsgiref.simple_server import make_server
import urlparse
import simplejson

def test_rpc_convert_units_to_ml():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

    db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

    db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

    r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                            '4 oz')])
    db.add_recipe(r)
    r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),
                                     ('vermouth', '1.5 oz')])
    db.add_recipe(r)
    r = recipes.Recipe('vomit inducing martini', [('orange juice',
                                               '6 oz'),
                                              ('vermouth',
                                               '1.5 oz')])

    db.add_recipe(r)

    db.add_recipe(r)

    environ = {}
    environ['PATH_INFO'] = '/rpcml'
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']

    #assert text.find('Recipes: <p><ul><li>scotch on the rocks<ul><li>blended scotch - 4 oz</ul><li>vomit inducing martini<ul><li>orange juice - 6 oz<li>ver$
    #assert ('Content-type', 'text/html') in headers
    #assert status == '200 OK'
    liquorAmount = app_obj.rpc_convert_units_to_ml('27 ml')
    assert liquorAmount == '27.0'

def test_rpc_get_recipe_names():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

    db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

    db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

    r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                            '4 oz')])
    db.add_recipe(r)
    r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),  
                                     ('vermouth', '1.5 oz')])
    db.add_recipe(r)
    r = recipes.Recipe('vomit inducing martini', [('orange juice',
                                               '6 oz'),
                                              ('vermouth',
                                               '1.5 oz')])

    db.add_recipe(r)

def test_rpc_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

    db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

    db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

    r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                            '4 oz')])
    db.add_recipe(r)
    r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),  
                                     ('vermouth', '1.5 oz')])
    db.add_recipe(r)
    r = recipes.Recipe('vomit inducing martini', [('orange juice',
                                               '6 oz'),
                                              ('vermouth',
                                               '1.5 oz')])

    db.add_recipe(r)
