### Import modules ###
import numpy as np
import matplotlib.pyplot as plt
### No further imports should be required ###



### Functions provided for the coursework ###

def centred_difference(x,h,f):
    """
    Approximate the second derivative of a function f at a point x using
    the standard centred three-point finite difference approximation.

    Inputs:
    ----------
    x (float): the value at which to approximate the derivative
    h (float): the displacement to use in the derivative approximation
    f (function): the function to be differentiated

    Outputs:
    ----------
    derivative_approximation (float): the approximation to the derivative
    """

    # Construct the standard centred difference approximation of the
    # second derivative.
    derivative_approximation = (f(x+h)-2*f(x)+f(x-h))/(h*h)

    return derivative_approximation


def trapezoidal_integration(a,b,f):
    """
    Approximate the definite integral of a function f over an interval
    [a,b] using the trapezoidal rule.

    Inputs:
    ----------
    a (float): the lower limit of integration
    b (float): the upper limit of integration
    f (function): the function to be integrated

    Outputs:
    ----------
    integral (float): the approximation to the integral
    """

    # Compute the trapezoidal rule approximation
    integral = 0.5*(b-a)*(f(a)+f(b))

    return integral

### End of provided functions



### Functions to be edited for the coursework ###

### QUESTION 1 - derivative approximation
def approximate_derivative(x,h,nvalues,f,d2fdx2,produce_fig):
    
    """
    This function generates approximations of the second derivative of a function (f) at a point (x).
    The function uses a range of step sizes h and computes the absolute errors of these approximations.
    
    Inputs:
        x (float): The point at which we approximate the second derivative
        h (numpy ndarray): An array of step sizes
        nvalues (int): The number of elements in h
        f (function): The function which we differentiate
        d2fdx2 (function): The second derivative of f; we use this to compute the errors
        produce_fig (boolean): If set to true, it generates a loglog  plot of the errors against h
        
    Outputs:
        approx_values (numpy ndarray): The approximated second derivatives
        error_values (numpy ndarray): The absolute errors of the approximations
        fig (matplotlib figure): The generated plot (if it is produced)
    
    """
    
    #This initialises two arrays of the size of nvalues
    approx_values = np.zeros(nvalues)
    error_values = np.zeros(nvalues)
    
    #This computes the exact value of the second derivative at x
    exactval = d2fdx2(x) 
    
    #This for loop begins the approximation of the derivative
    for i in range(nvalues):
        approx_values[i] = centred_difference(x, h[i], f) #The derivative approximation. Then it is put into the array of approx values
        error_values[i] = np.abs(approx_values[i]- exactval) #This computes the absolute error,  then it is put into the array of error values
    
    fig=None
    # If a figure is requested, then the if statement is activated to plot the results
    if produce_fig:
        fig = plt.figure()
        plt.loglog(h, error_values, marker = "x", label='Abs Error') #The scale is set to loglog
        plt.title("Absolute Errors Against h")
        plt.xlabel("h (log)")
        plt.ylabel("Absolute Errors(log)")
        plt.legend()


    return approx_values, error_values, fig


### QUESTION 2 - extrapolation
def extrapolate_derivative(x,h,nvalues,nlevels,r,f,d2fdx2):
    """
    Analysis of extrapolated approximations:
        
        1. f_1(x) = sin(pi * x) at x=0.25:
            This function is very smooth (meaning it is infinitely differentiable).
            We can see that the theoretical error expansion for the centred difference approximation only contains even powers of h (O(h**2n),).
            We can see in the plot that the standard extrapolation formula works perfectly (each level l successfully eliminates the leading error terms, which resulted in progressively steeper lines and much faster convergence rates for higher levels).
        
        2. f_2(x) = max(0, (x-1)**3) at x=1:
            This function is not smooth enough (its third derivative is discontinuous at x=1).
            This leads to the error that the expansion of the centred difference does not consist of purely even powers of h.
            When we evaluate the approximation near the singularity, we see that the leading error term is O(h).
            We can see in the plot that the standard extrapolation formula fails, and the error terms fail to improve across levels, since the formula is trying to eliminate an O(h**2) term that doesn't exist.
        
        Suggested modification for f_2(x):
            To improve the result of this function, the extrapolation formula needs to be modified to eliminate the actual powers of h in the errors.
            Since the first error is O(h), we should adjust the powers used in the formula to p_(l-1)=l, starting at 1 and increasing by 1 at each level, rather than p_(l-1)=2*l
    
    
    """
    #Here we call the approximate_derivative function from Q1 to get the level 0 approximations and their initial errors
    approx_values, initial_errors, _= approximate_derivative(x, h, nvalues, f, d2fdx2, False)
    #Here we compute the exact value of the second derivative so that we can calculate the errors
    exactval= d2fdx2(x)
    #Here we create the arrays which have 0s for now
    N = np.zeros((nvalues, nlevels+1))
    error_values = np.zeros((nvalues, nlevels+1))
    #We set the frist column to the initial approximations and errors 
    N[:, 0] = approx_values
    error_values[:, 0] = initial_errors
    
    #Here we begin the extrapolation loop for each level
    for l in range(1, nlevels+1):
        #Here we set the h power to increase by 2 at each level
        power =2*l
        rpower = r**power
        
        #We use a nested for loop to compute the extrapolated values for the current level
        for k in range(nvalues-l):
            #This is the extrapolation formula to eliminate the leading error term
            N[k,l] = ((rpower * N[k+1, l-1] - N[k, l-1]) / (rpower - 1.0))
            #This computes and stores the absolute error of the extrapolated approximation
            error_values[k,l]= np.abs(N[k, l]- exactval)
    fig=None
    
    #Generate the loglog plot of the errors
    fig=plt.figure()
    #Plots the errors for each extrapolation level, ignoring the trailing zeros
    for l in range(nlevels+1):
        vh = h[:nvalues-l]
        verrors = error_values[:nvalues-l, l]
        plt.loglog(vh, verrors, marker="*", label=f'Level {l}')
        
    plt.title("Errors of Extrapolated Derivative Approximations Against h")
    plt.xlabel("h (log)")
    plt.ylabel("Absolute Error (log)")
    plt.legend()
        
    return error_values, fig


# QUESTION 3 - Gauss integration rule
def gauss_integration(a,b,f):
    
    """
    This function computes an approximation over the general interval [a,b] of the integral of a function (f).
    We do this approximation using the 2-point Gauss integration rule.
    
    Inputs:
        a (float): The lower bound of the general interval
        b (float): The upper bound of the general interval
        f (function): The function of which we want to approximate the integral
    
    Outputs:
        integral (float): The approximated value of the integral
    """
    
    #Defining the nodes and the weights for the interval [-1,1]
    xi1 = -1.0 / np.sqrt(3.0) 
    xi2 = 1.0 / np.sqrt(3.0)
    omega1 = omega2 = 1.0
    
    #Here we transform the nodes into the general interval [a,b]
    x1 = ((b-a) / 2.0)* xi1 + ((b+a) /2.0)
    x2 = ((b-a) / 2.0)* xi2 + ((b+a) /2.0)
    
    #Here we transform the weights into the general interval [a,b]
    w1 = ((b-a) / 2.0) * omega1
    w2 = ((b-a) / 2.0) * omega2
    
    #This computes the 2-point Gauss approximation in the general interval [a,b]
    integral = w1*f(x1) + w2*f(x2)
    
    return integral


# QUESTION 4 - composite numerical integration
def composite_integration(a,b,npanels,f,f_int,integration_rule):
    
    """
    This function computes an approximation over the general interval [a,b] of the integral of a function (f).
    We do this using composite numerical integration
    
    Inputs:
        a (float): The lower bound of the general interval
        b (float): The lower bound of the general interval
        npanels (int): The number of panels used to subdivide the interval
        f (function): The function we want to integrate
        f_int (function): The indefinite integral of f; this is used to compute the exact error
        integration_rule (function): The integration rule to apply to every panel (For example, Trapezoidal or Gauss)

    Outputs:
        integral (float): The approximated value of the integral computed using the said integration rule
        error_value (float): The absolute value of the error of the approximation
        
    """
    h=(b-a)/npanels #The formula for the width of each panel
    integral = 0.0 #Initialising the integral value 
    
    for i in range(npanels): #The for loop that applies each integration rule at each panel
        xstart = a + i * h # Defining both the start and end of each panel
        xend= a + (i+1) * h
        integral += integration_rule(xstart, xend, f) #Apply the specific rule to the current panel and add to the total 
        
    exactintegral = f_int(b) - f_int(a) #Computes the exact integral using the indefinate integral function f_int
    error_value = np.abs(integral- exactintegral) # Computes the error between the exact integral and the approximation

    return integral, error_value


# QUESTION 5 - errors in composite numerical integration
def composite_errors(a,b,npanels,f,d2fdx2,d4fdx4,f_int):    
    """
    Analysis of composite integration errors:
        
        1. f_1(x)= sin(pi*x) with [a,b]=[1,2]:
            This function is very smooth and highly differentiable.
            The absolute errors follow the theoretical error bounds perfectly.
            We can see that, through the trapezoidal rule, the error decreases at the rate O(h**2).
            Through the 2-point Gauss rule error the error decreases at a far faster rate of O(h**4)
            
        2. f_2(x)= x * ln(x) with [a,b]=[0,1]:
            This function has a singularity in its derivatives at x=0 (for example the d2fdx2=1/x and d4fdx4=2/x**3 and when x=0 is zero they are singular).
            This means the theoretical error bounds evaluate to extremely large and inaccurate values.
            In the plot, we can see the actual error and bound relationship break down (in comparison to the example in main, in which they are fairly similar). 
            The convergence rate degenerates a lot, and it is much slower than O(h**2) and O(h**4) bounds observed for the smooth function


    """
    #We create 1000 subintervals so that we can evaluate the maximum derivatives at the midpoints
    xedges = np.linspace(a, b, 1001)
    xmid = (xedges[:-1] + xedges[1:]) / 2.0
    
    #Here we compute the maximum absolute values of both the second and fourth derivatives
    maxd2 = np.max(np.abs(d2fdx2(xmid)))
    maxd4 = np.max(np.abs(d4fdx4(xmid)))
    
    #Here we create arrays so that we can store the calculated errors and the theoretical bounds
    error_values = np.zeros((2, npanels.size))
    error_bounds = np.zeros((2, npanels.size))
    
    #This for loop loops through each panel count in the npanels array
    for k in range(npanels.size):
        n = npanels[k]
        h = (b-a) / n
        
        #Here we calculate the integration error and the theoretical bound for the Trapezoidal rule
        _, errortrap = composite_integration(a, b, n, f, f_int, trapezoidal_integration)
        error_values[0,k] = errortrap
        error_bounds[0,k] = ((b-a) * (h**2)/ 12.0) * maxd2
        
        #Here we calculate the integration error and theoretical bound for the 2-point Gauss rule
        _, errorgauss = composite_integration(a, b, n, f, f_int, gauss_integration) 
        error_values[1,k] = errorgauss
        error_bounds[1,k] = ((b - a) * (h ** 4) / 4320.0) * maxd4
    
    fig = plt.figure()
    
    #This code plots the Trapezoidal errors and bounds
    plt.loglog(npanels, error_values[0,:],label = "Trapeziodial Error (log)", marker = ".")
    plt.loglog(npanels, error_bounds[0,:],label = "Trapeziodial Bound (log)", linestyle = "--")
    
    #This code plots the 2-point Gauss errors and bounds
    plt.loglog(npanels, error_values[1,:],label = "Gauss Erorr (log)", marker = "*")
    plt.loglog(npanels, error_bounds[1,:], label = "Gauss Bound (log)", linestyle = "--")
    
    plt.title("Error and Bounds Against N of Panels")
    plt.xlabel("N of Panels (log)")
    plt.ylabel("Abs Error / Bound (log)")
    plt.legend()
               
    return error_values, error_bounds, fig


# QUESTION 6 - landing time computation
def compute_time(a,b,Nmax,TOL,hinitial,vterm):
    """
    Method Justification:
        1. Nonlinear Solver: 
            I chose the Secant method since it provides superlinear convergence; this makes it significantly faster than the Bisection method. We also do not need to compute the derivative of the integral, which gives the Secant method the edge over the Newton method
        2. Integration rule:
            I chose the 2-point Gauss integration rule. This is because it has a more accurate convergence rate than the Trapezoidal rule (O(h**4) in comparison to the O(h**2) of the trapezoidal rule). This allows us to use fewer panels while still achieving the required 3 dp of accuracy, reducing the computational cost
        3. Additional parameters:
            Due to us not needing a large number of panels in the Gauss rule, I set 'npanels=10'. This is more than suffficient ot caclulate the landing time to the required 3dp without unnecessary calculations.
        4.Evalutation of v(t):
            The secant method evaluated the integral for p0 and p1 and then once for each iteration (excluding the final iteration where it breaks early). Therefore, for 'niters' iterations, the integral is evaluated 'niters+1' times.
            For each time F(t) is evaluated, the composite 2-point Gauss rule evaluates v(t) exactly two times per panel. Therefore, the formula for the total number of v(t) evaluations is (niters+1)*(2*npanels)
    """
    
    
    #Here we are defining the gravity constant and the npanels
    g = 9.81
    npanels = 10
    
    #Here we are defining the velocity formula and the dummy zero function for fint0
    v = lambda t: vterm * np.tanh((g*t) / vterm)
    fint0 = lambda t : 0.0
    
    
    #We are defining a root-finding function, and we are going to use the Gauss integration function
    def F(T):
        integral, _ = composite_integration(0.0, T, npanels, v, fint0, gauss_integration)
        return hinitial - integral
    
    #Here we are defining the bounds we will use for the Secant method
    p0, p1 = a, b
    q0, q1 = F(p0), F(p1)
    
    
    #Setting the niters for the upcoming loop
    niters = 0
    
    #This for loop is iterating over the secant method
    for n in range(Nmax):
        niters += 1
        
        #We are using this if statement to prevent division by 0
        if (q1-q0) == 0:
            break
        
        #Here we are calculating the next approx
        pnext = p1 -q1 * (p1-p0) / (q1 - q0)
        
        #Here we are checking for convergence against TOL
        if np.abs(pnext - p1) < TOL:
            p1=pnext
            break
        
        #Here we are updating the values for the next iteration of the secant method
        p0, p1 = p1, pnext
        q0, q1 = q1, F(p1)
        
    #This is the final approximation    
    landing_time = p1
    


    return landing_time, niters

