'''
Effat Farhana
'''

def simpleCalculator(v1, v2, operation):

   if isinstance(v1, str) and v1.isnumeric()== False:
      return "At least one input is non-numeric"

   if isinstance(v2, str) and v2.isnumeric()== False:
      return "At least one input is non-numeric"
   
   v1 = float(v1)
   v2 = float(v2)

   
   res=0
   if(operation == '+'):
      res=v1+v2
   elif operation == '-':
      res = v1-v2
   elif operation == '*':
      res = v1*v2
   elif operation == '/':
      if v2!=0:
         res = v1/v2
      else:
         return "Division by zero"
   elif operation == '%':
      res = v1%v2
    
   return res

def simpleFuzzer(): 
   fuzz_cases = [
      (None, 2, '+'),                 # NoneType 
      ([1], 2, '+'),                  # list 
      ({'a': 1}, 2, '-'),             # dict 
      (2, lambda x: x, '*'),          # function 
      (b"bytes", 2, '/'),             # bytes 
      ((3,), 2, '+'),                 # tuple 
      (set([5]), 2, '+'),             # set 
      (object(), 2, '-'),             # generic object
      (frozenset([1, 2]), 2, '+'),    # immutable set
      (Ellipsis, 2, '*')              # the literal `...` (Ellipsis object)

    ] 
   for v1, v2, op in fuzz_cases:
        try:
            print(f"Trying simpleCalculator({v1}, {v2}, '{op}')")
            result = simpleCalculator(v1, v2, op)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Crash: {e}")

if __name__=='__main__':
    simpleFuzzer()
