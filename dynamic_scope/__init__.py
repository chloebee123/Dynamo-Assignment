from ctypes import sizeof       
from threading import local     
from typing import Dict, Any, Iterator, Optional        
from collections import abc     
from types import FunctionType      
import inspect      
class DynamicScope(abc.Mapping):        
    def __init__(self):                                                 # creating dictionary-like object
        self.env: Dict[str, Optional[Any]] = {}     
    def __getitem__(self, key):                                         # function to get item in object
        if key in self.env:     
            return self.env[key]        
        else:                                                           
            raise NameError         
    def __setitem__(self, key, value):                                  # function for setting key value pair
        if key not in self.env:     
            self.env[key] = value       
        else:       
            return      
    def __iter__(self):                                                 # function to iterate over object
        return iter(self.env)       
    def __len__(self):                                                  # function to get length 
        return len(self.env)        
def get_dynamic_re() -> DynamicScope:       
    dictionary = DynamicScope()     
    def get_size():                                                     # function to get the size of the stack (probably a better/easier way to do this)
        size = -1                                                       # set to -1 bc the last two items in the stack are my own function calls
        stack = inspect.stack()     
        while stack != []:                                              # this is so inefficient but this loop counts how many times i can use .pop() before the stack is empty and 
            stack.pop()                                                 # incremented the size counter to get the size
            size += 1       
        return size     
    def get_locals(size):                                               # function to get the locals from the stack_info 
        stack_info = inspect.stack()        
        i = 2                                                           # i = 2 because i wanted skip the 0th and 1th index in my below loop
        while i < size:                                                 # i just realized a for loop would have been much easier but i went with the while loop
            frame = stack_info[i][0]                                    # current stack frame
            freevars = list(frame.f_code.co_freevars)                   # freevars in current stack frame
            localvars = list(frame.f_locals)                            # locals in current stack frame
            localvars2 = frame.f_locals                                 # same as localvars but in dictionary form so that i can access key/value pairs easier 
            i += 1      
            toadd = [x for x in localvars if x not in freevars]         # essentially toadd = localvars - freevars
            for keys in toadd:      
                if type(localvars2[keys]) == str:                       # for whatever reason, my freevars variable didn't list all the freevars (no idea what 
                    dictionary.__setitem__(keys, localvars2[keys])      # I wrote or didn't write to cause it) so this was me double checking that each local 
        return None                                                     # in my list was supposed to be added to my dictionary
    get_locals(get_size())                                              
    return dictionary                                                   