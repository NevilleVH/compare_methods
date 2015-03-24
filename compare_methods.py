#compare convergence speed of bisection and secant methods
#Neville Varney-Horwitz
#24 March 2015
import random,math

ACCURACY = 1e-6
def get_init_values(f):
    """Find starting values x_0, x_1 such that f(x_0) < 0 and f(x_1) > 0"""
    max_iter = 1e5 
    x_0 = x_1 = random.random() * 10
    i = 0  
    while (f(x_0) > 0 or f(x_1) < 0) and (i < max_iter):   
        num = random.random() * 10 # using random nums can help escape local minima
        if f(x_0) > 0 : 
            if f(x_0) > f(x_0 - num):
                x_0 -= num
            else:
                x_0 += num
        if f(x_1) < 0:
            if f(x_1) < f(x_1 - num):
                x_1 -= num
            else:
                x_1 += num
        i += 1
    if i == max_iter:
        x_0 = x_1 = None
    return x_0, x_1

def secant1(init_vals,f):
    """original secant method for finding roots"""
    count = 0
    x_0,x_1 = init_vals
    while abs(f(x_1)) > ACCURACY:
        count += 1
        m = (f(x_1) - f(x_0))/(x_1-x_0)
        x_0 = x_1
        if m == 0: #ideally something here
            pass
        x_1 = -f(x_0)/m + x_0    
    return x_1, count

def secant2(init_vals,f):
    """secant method with small change - 
    one point stays fixed so the secant tends towards becoming a tangent"""
    count = 0
    x_0,x_1 = init_vals
    while abs(f(x_0)) > ACCURACY:
        count += 1
        m = (f(x_1) - f(x_0))/(x_1-x_0)
        if m == 0:
            pass
        x_0 = -f(x_1)/m + x_1
    return x_0, count

def bisect(init_vals,f):
    """original bisection method for finding roots"""
    count = 0
    x_0,x_1 = init_vals
    while abs(f(x_1)) > ACCURACY:
        count += 1
        new = (x_0 + x_1) /2
        if f(new) >= 0:
            x_1 = new
        else:
            x_0 = new    
    return x_1, count

def get_function():
    """accepts and sanitises user defined function"""
    s = input('f(x) = ').replace('^','**')
    for i in range(len(s)-2,-1,-1):
        if s[i].isdigit() and s[i+1] == 'x':
            s = s[:i+1] + '*' + s[i+1:]
    try:
        f = eval('lambda x : ' + s) 
        #f(0)
    except:
        print('Invalid function: Please try again.')   
    return f

def main():
    cont = 'Y'
    while cont == 'Y':
        print('***\nInput a function whose range (co-domain) contains both negative and positive values.')
        f = get_function()
        initial = get_init_values(f)
        if initial[0] == None:
            print('Invalid function')
        else:
            print('Initial values: {:.2f}, {:.2f}'.format(initial[0],initial[1]))
            root, count_sec = secant1(initial,f)
            print('Secant method 1\nRoot: x ~', round(root,5), '\nNumber of iterations:', count_sec, end = '\n\n')
            #root, count = secant2(initial,f)
            #print('Secant method 2\nRoot: x ~', round(root,10), '\nNumber of iterations:', count, end = '\n\n')
            root, count_bis = bisect(initial,f)
            print('Bisection method\nRoot: x ~', round(root,5), '\nNumber of iterations:', count_bis,end = '\n\n')
            ratio = count_bis / count_sec
            if ratio > 1:
                print('The secant method was', round(ratio,2),'times faster than the bisection method.')
            else:
                print('The bisection method was', round(1/ratio,2),'times faster than the secant method.')
        cont = input('Continue? (Y/N): ').upper()[0]
    print('***')
        
if __name__ == '__main__':
    main()