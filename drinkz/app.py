#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import jinja2
import db
import recipes

import sys
loader = jinja2.FileSystemLoader('../drinkz/templates')
env = jinja2.Environment(loader=loader)
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

import os

#db.load_db('../bin/drinkz.txt')
#db.load_db('drinkz.txt')
dispatch = {
    '/' : 'index',
    '/recipeContent' : 'recipeFile',
    '/inventoryContent' : 'inventoryFile',
    '/liquorTypesContent' : 'liquorTypesFile',
    '/mlForm' : 'mlFormPage',
    '/submit' : 'mlSubmit',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/form_liquor_types': 'form_liquor_types',
    '/form_liquor_inventory': 'form_liquor_inventory',
    '/form_recipe': 'form_recipe',
    '/recvML' : 'recvML',
    '/recvLiquorTypes' : 'recvLiquorTypes',
    '/recvLiquorInventory': 'recvLiquorInventory',
    '/recvRecipe': 'recvRecipe',
    '/recv' : 'recv',
    '/rpc'  : 'dispatch_rpc',
    '/rpcml' : 'rpc_convert_units_to_ml',
    '/rpcrecipes' : 'rpc_get_recipe_names',
    '/rpcinventory' : 'rpc_get_liquor_inventory',
    '/rpcenterliquor' : 'rpc_enter_liquor_type',
    '/rpcenterinventory' : 'rpc_enter_inventory',
    '/rpcenterrecipe' : 'rpc_enter_recipe'
}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = """<html>
    <head>
        <title>HW4 Index</title>
        <style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
<h1>Index:</h1>
<script>
function myFunction()
{
alert("I am an alert box!");
}
</script>    
</head>
        <body>
	Visit:
        <p>
	<a href='recipeContent'>recipe file</a>,
	<p>
	<a href='inventoryContent'>inventory file</a>,
	<p>
	<a href='liquorTypesContent'>liquor types file</a>,
	<p>
	<a href='mlForm'>convert to ml (form)</a>
	<p>
	<a href='form_liquor_types'>Enter a Liquor type (form) </a>
	<p>
        <a href='form_liquor_inventory'>Enter a Liquor inventory (form) </a>
	<p>
        <a href='form_recipe'>Enter a Recipe (form) </a>
<p>
<input type="button" onclick="myFunction()" value="Show alert box" />    
</body>
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]
        
    #def somefile(self, environ, start_response):
    #    content_type = 'text/html'
    #    data = open('somefile.html').read()
    #
    #    start_response('200 OK', list(html_headers))
    #    return [data]
    def recipeFile(self, environ, start_response):
        content_type = 'text/html'
        data = recipes()
        start_response('200 OK', list(html_headers))
        return [data]
    
    def inventoryFile(self, environ, start_response):
        content_type = 'text/html'
        data = inventory()
        start_response('200 OK', list(html_headers))
        return [data]

    def liquorTypesFile(self, environ, start_response):
        content_type = 'text/html'
        data = liquorTypes()
        start_response('200 OK', list(html_headers))
        return [data]

    def mlFormPage(self, environ, start_response):
        data = mlFormPageFunction()

	start_response('200 OK', list(html_headers))
        return [data]
    #def mlSubmit(self, environ, start_response):
#	content_type = 'text/html'
 #       data = liquorTypes()
#	start_response('200 OK', list(html_headers))
#	return[data]

    def form_liquor_types(self, environ, start_response):
	data = form_liquor_types_function()
        start_response('200 OK', list(html_headers))
        return [data]

    def form_liquor_inventory(self, environ, start_response):
        data = form_liquor_inventory_function()
        start_response('200 OK', list(html_headers))
        return [data]

    def form_recipe(self, environ, start_response):
        data = form_recipe_function()
        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
    def recvML(self, environ, start_response):
	formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        amount = results['amount'][0]

        content_type = 'text/html'
        #data = "amount: "
        amount = str(db.convert_to_ml(amount))
	data = "<html><head><title>ML display page</title><style type='text/css'>h1 {color:red;}body {font-size: 14px;}</style><h1>The ML Display Page:</h1></head><body>amount: %s ml. <a href= './'>return to index</a></body></html>" %(amount)
        
	start_response('200 OK', list(html_headers))
	return [data]

    def recvLiquorTypes(self, environ, start_response):
	formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        type = results['type'][0]
        type = str(type)

        vars = dict(entry=type, entryName = 'LIQUOR TYPE')
        template = env.get_template('hw5template.html')
        content_type = 'text/html'

	data = str(template.render(vars))
	print template.render(vars)
        #data = "amount: "
        #data = "<html><head><title>Liquor Type display page</title><style type='text/css'>h1 {color:red;}body {font-size: 14px;}</style><h1>The Liquor Type Display Page:</h1></head><body>Liquor type: %s. <a href= './'>return to index</a></body></html>" %(type)
        start_response('200 OK', list(html_headers))
        return [data]

    def recvLiquorInventory(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        inventory = results['inventory'][0]
        inventory = str(inventory)
        
        vars = dict(entry=inventory, entryName = 'LIQUOR INVENTORY')
        template = env.get_template('hw5template.html')
        content_type = 'text/html'
        
        data = str(template.render(vars))
        print template.render(vars)
        #data = "amount: "
        #data = "<html><head><title>Liquor Type display page</title><style type='text/css'>h1 {color:red;}body {font-size: 14px;}</style><$
        start_response('200 OK', list(html_headers))
        return [data]

    def recvRecipe(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        recipe = results['recipe'][0]
        recipe = str(recipe)
        
        vars = dict(entry=recipe, entryName = 'RECIPE')
        template = env.get_template('hw5template.html')
        content_type = 'text/html'
        
        data = str(template.render(vars))
        print template.render(vars)
        #data = "amount: "
        #data = "<html><head><title>Liquor Type display page</title><style type='text/css'>h1 {color:red;}body {font-size: 14px;}</style><$
        start_response('200 OK', list(html_headers))
        return [data]

   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        firstname = results['firstname'][0]
        lastname = results['lastname'][0]

        content_type = 'text/html'
        data = "First name: %s; last name: %s.  <a href='./'>return to index</a>" % (firstname, lastname)

        start_response('200 OK', list(html_headers))
        return [data]

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)
 
    def rpc_convert_units_to_ml(self,amount):
        newAmount = str(db.convert_to_ml(amount))	
        return newAmount

    def rpc_get_recipe_names(self):
        nameList = []
	for r in db.get_all_recipes():     
            nameList.append(r.name)
	return nameList

    def rpc_get_liquor_inentory(self):	
	inventoryList = []
        for m, l in db.get_liquor_inventory():
	    inventoryList.append((m,l))
	return inventoryList	

    def rpc_enter_liquor_types(self,mfg,liquor,typ):
        db.add_bottle_type(mfg,liquor,typ);
        return 1;

    def rpc_enter_liquor_inventory(self,mfg,liquor,amount):
	db.add_to_inventory(mfg,liquor,amount)
        return 1;

    def rpc_enter_recipe(self,r):
        db.add_recipe(r)
        return 1;


def form():
    return """
<form action='recv'>
Your first name? <input type='text' name='firstname' size'20'>
Your last name? <input type='text' name='lastname' size='20'>
<input type='submit'>
</form>
"""

def mlFormPageFunction():
    return """<html>
<head>
<title>ML form page</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
<h1>The ML Form Page</h1>

</head>
<body>
<form action ='recvML'>
Enter an amount to be converted to ml <input type='text' name = 'amount' size='20'>
<input type='submit'>
<p>
<p>
<a href= './'>return to index</a>
</form>
</body>
</html>
"""

def form_liquor_types_function():

    return """<html"
<head>
<title>Liquor types form page</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
<h1>The Liquor Types Form Page</h1>

</head>
<body>
<form action ='recvLiquorTypes'>
Enter a liquor type<input type='text' name = 'type' size='20'>
<input type='submit'>
<p>
<p>
<a href= './'>return to index</a>
</form>
</body>
</html>
"""

def form_liquor_inventory_function():
    return """<html"
<head>
<title>Liquor types form page</title>
<style type='text/css'> 
h1 {color:red;}
body {      
font-size: 14px;
}
</style>        
<h1>The Liquor Inventory Form Page</h1>
        
</head>
<body>
<form action ='recvLiquorInventory'>
Enter a liquor inventory<input type='text' name = 'inventory' size='20'>
<input type='submit'>
<p>
<p>
<a href= './'>return to index</a>
</form>
</body>
</html>
"""

def form_recipe_function():
    return """<html"
<head>
<title>Liquor types form page</title>
<style type='text/css'> 
h1 {color:red;}
body {      
font-size: 14px;
}
</style>        
<h1>The Recipe Form Page</h1>
        
</head>
<body>
<form action ='recvRecipe'>
Enter a Recipe<input type='text' name = 'recipe' size='20'>
<input type='submit'>
<p>
<p>
<a href= './'>return to index</a>
</form>
</body>
</html>
"""



def recipes():

#    return """     
#here is some RECIPE stuff   
#"""

    newData = """  """
    #newData += '<ul> <li> newData  </li> <li> this is a test </li> <li> i hope it works </li></ul>'
    #print newData
    newData += "<html><head><title>recipes page</title><style type='text/css'>h1 {color:red;}body {font-size: 14px;}</style><h1>The Recipes Page</h1></head><body>"
    newData += 'Recipes: <p>'
    newData += '<ul>'
    for r in db.get_all_recipes():
        newData += '<li>'
        newData += r.name
        newData += '<ul>'
        for name, amount in r.ingredients:
	    newData += '<li>'
            newData+= name
	    newData += ' - '
            newData += amount
	newData += '</ul>'
    newData += '</ul>'
    newData += "<a href= './'>return to index</a>"
    newData += '</body></html>'

    return newData

def inventory():

    newData = """ """
    newData += "<html><head><title>inventory page</title><style type='text/css'>h1 {color:red;}body {font-size: 14px;}</style><h1>The Inventory Page:</h1></head><body>"
    newData += 'Inventory: <p>'
    newData += '<ul>'
    for m, l in db.get_liquor_inventory():
	amount = db.get_liquor_amount(m, l)
	newData += '<li>'
	newData += m
	newData += '--'
	newData += l
	newData += '--'
	newData += str(amount)
        newData += ' ml'
    newData += '</ul>'
    newData += "<a href= './'>return to index</a>"
    newData += '</body></html>'
    return newData

def liquorTypes():

    newData = """ """
    newData += "<html><head><title>liquor types page</title><style type='text/css'>h1 {color:red;}body {font-size: 14px;}</style><h1>Liquor Types Page:</h1></head><body>"
    newData += 'Liquor Types: <p>'
    newData += '<ul>'
    for m, l, g in db._bottle_types_db:
	newData += '<li>'
	newData += m
	newData += '--'
	newData += l
	newData += '--'
	newData += g
    newData += '</ul>'
    newData += "<a href= './'>return to index</a>"
    newData += '</body></html>'
    return newData

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
