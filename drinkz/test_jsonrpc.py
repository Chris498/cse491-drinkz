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

def call_remote(base, method, params, id):
    # determine the URL to call
    url = base + 'rpc'

    # encode things in a dict that is then converted into JSON
    d = dict(method=method, params=params, id=id)
    encoded = simplejson.dumps(d)

    # specify appropriate content-type
    headers = { 'Content-Type' : 'application/json' }

    # call remote server
    req = urllib2.Request(url, encoded, headers)

    # get response
    response_stream = urllib2.urlopen(req)
    json_response = response_stream.read()

    # decode response
    response = simplejson.loads(json_response)

    # return result
    return response['result']

def test_rpc_convert_units_to_ml():
    db._reset_db()

    #server_base = 

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

  #  liquorAmount = call_remote(server_base, method='conver_units_to_ml',params=['27 oz'], id=1)
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
