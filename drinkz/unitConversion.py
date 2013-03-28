    
def convert_to_ML(amount):
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
    


