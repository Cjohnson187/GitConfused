
def method1():
    print("called method 1 from jvpm_methods.py module")

def method2():
    print("called method 2 from jvpm_methods.py module")

def method3():
    print("called method 3 from jvpm_methods.py module")

"""DICTIONARY"""
def opcode_methods(argument):
    tokenDict = {
        "iconst_m1": method1, 
        "istore_1": method2, 
        "iinc": method3
    }
    # get the method name from the tokenDict dictionary
    method = tokenDict.get(argument, lambda: "Invalid opcode")
    # Call the Method.
    method()
                                
def get_methods(opcode):
    ''' Retrieve method name from dictionary of opcodes '''
    return tokenDict[opcode]
