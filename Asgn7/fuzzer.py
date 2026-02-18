

def simpleCalculator(v1, v2, operation):
    res=0
    if(operation == '+'):
        res=v1+v2
    elif operation == '-':
        res = v1-v2
    elif operation == '*':
        res = v1*v2
    elif operation == '/':
        res = v1/v2
    elif operation == '%':
        res = v1%v2
    
    return res

def simpleFuzzer():
    #complete the following methods
    blns_samples = [
        '\\',
        '\\\\',
        '1.00',
        '$1.00',
        '1/2',
        '1E+02',
        '-1',
        '-1.00',
        '-$1.00',
        '-1/2'
    ]
    for s in blns_samples:
        try:
            print(f"Trying: simpleCalculator({s}, 2, '+')")
            result = simpleCalculator(s, 2, '+')  # Test string as v1
            print(f"Result: {result}")
        except Exception as e:
            print(f"Crash: {e}")

        try:
            print(f"Trying: simpleCalculator(2, {s}, '-')")
            result = simpleCalculator(2, s, '-')  # Test string as v2
            print(f"Result: {result}")
        except Exception as e:
            print(f"Crash: {e}")

if __name__ == '__main__':
    simpleFuzzer()