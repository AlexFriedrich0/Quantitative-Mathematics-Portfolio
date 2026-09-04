import numpy as np
import matplotlib.pyplot as plt

def show_answer(func, word_limit=40):
    """
    Do not remove or modify this function
    """
    
    text = func.__doc__ or ""
    words = text.split()

    limited = words[:word_limit]
    truncated = len(words) > word_limit

    result = " ".join(limited)
    if truncated:
        result += " ...[truncated]"

    return result


def fixedpoint_with_stopping(g, p0, Nmax, TOL, p=None, C=None, k=None):
    """
    Fixed-Point Iteration Method: Computes the sequence of approximations that the algorithm generates. It uses the TOL as a stopping criterion by checking if the absolute difference between consecutive approximations is less than or equal to the given TOL value. If a p, C and K values are given, then this function plots the absolute error.
        
    Inputs:
        g: function
            Lambda function that corresponds to the function whose fixed point is being located
        p0: float
            The initial guess for the iteration
        Nmax: int
            The maximum number of iterations performed for the function
        TOL: float
            The tolerance used for the stopping criterion (|p_m - p_{m-1}| <= TOL).
        p: float, optional
            If known (the default is that it isn't known), it is the exact fixed point. 
        C: float, optional
            If known (the default is that it isn't known), it is a positive constant for the error bound Ck^n.
        k: float, optional
            If known (the default is that it isn't known), it is a positive constant for the error bound Ck^n.
    Outputs:
        p_array: numpy.ndarray
            The array that contains the iterates p_n. Its shape is (m,) where m is the number of iterations completed before the stopping criterion, calculated by using a for loop.
        fig: matplotlib.figure, optional
            If there is a p value, then this matplotlib function outputs a plot containing the error plot
        ax: matplotlib.axes, optional
            If there is a p value, then this matplotlib function outputs the axes for the plot, making sure we use a log base for the y axis.
    
    """
    p_array = np.zeros(Nmax)
    
    #Write your code for fixed point iteration according to the instructions:
    p_previous = p0
    m=0 #Tracker for the number of iterations done
    #This for loop begins the fixed-point iteration until Nmax
    for n in range(Nmax):
        p_n=g(p_previous)
        p_array[n] = p_n #Stores the values generated in the function into the array
        m = m + 1 # Keeping track of iterations
        if np.abs(p_n - p_previous) <= TOL: #Checks if the iteration can stop
            break
        else: 
            p_previous = p_n #Sets the current approximation as the previous one for the next loop
            
    p_array = p_array[:m] #Makes sure the array only has m values in

    fig = ax = None

    # Write your code to generate plots according to the instructions:
    if p is not None: #Checks if there is an exact fixed point given to generate an error plot
        fig, ax = plt.subplots()
    
        n = np.arange(1, m + 1) #generates an array of iterations for x axis
    
        error = np.abs(p_array - p) #Calculates the absolute error
        ax.plot(n, error, label="Absolute Error", marker='o') #Plots absolute error
        
        if C is not None and k is not None: #checks if C and k are provided to plot error bound
            errorb = C * (k ** n)
            ax.plot(n, errorb, marker='x', label="Error Bound")
        ax.set_yscale("log") #sets the y-axis to logarithmic scale
        ax.set_xlabel("Iteration (n)")
        ax.set_ylabel("Error (log)")
        ax.legend(loc='best') #A legend to label each plotted curve
    

    if fig is not None and ax is not None:
        return p_array, fig, ax
    else:
        return p_array


def q1B_answer():
    """
    For the function g(x)= 1/3 (x**2 -1) with starting guess p0=1
    Q1b(i): State the order of convergence that you observe (max words: 1).
    Answer to Question 1b(i): Linear
    Q1b(i): In the context of 1.6.2 Order of convergence for fixed point iteration, explain why the fixed-point iteration cannot converge with a higher order of convergence (max words: 40).
    Answer to Question 1b(ii): According to Theorem 1.6, the method converges strictly linearly unless the asymptotic error constant is zero (g’(p) =/ 0). In this case, g’(x)= 2x/3, so g’(p) is non-zero, preventing a higher order of convergence.
        
    """
    pass

def q1C_answer():
    """
    Consider the function g:[-0.12,0.2] -> R, g(x)=x**2 (3-2x)
    Use your function fixedpoint_with_stopping with p0=0.15, N_max=20 and TOL=1e-11, and the exact fixed point p.
    Q1c(i): Do you observe linear convergence? (max words: 1)
    Answer to Question 1c(i): No
    Q1c(ii): if the observed order is higher than linear (e.g. quadratic), explain why this does not violate Theorem 1.6 (max words: 50).
    Answer to Question 1c(ii): Theorem 1.6 states the sequence converges strictly linearly if the derivative at the fixed point is non-zero (g’(p) =/ 0). The only fixed point in the interval is p=0 and g′(x)=6x−6x^2. If we put p into the derivative, we get 0. Theorem 1.6 does not apply, allowing for higher-order convergence.
        
    """
    pass

def newton_with_stopping(f,df,p0,Nmax,TOL,p=None):
    """
    Newton's method: Computes the sequence of approximations to the root of a function. It uses Newton's method from lecture notes to locate the roots. It uses TOL to check when to stop the algorithm early. The algorithm uses a nested if statement in a for loop to check whether the absolute value of the function at the current approximation is less than or equal to TOL. If a p value is given, then this function plots the absolute error. 
    Inputs:
        f: function
            Lambda or standard function that corresponds to the function whose roots are being located
        df: function
            Lambda or standard function that corresponds to the derivative of f(x). It is needed for the Newton method to find the next approximations.
        p0: float
            The initial approximation to start Newton's method.
        Nmax: int
            The maximum number of iterations performed for the function
        TOL: float
            The tolerance used for the stopping criterion (|f(p_m)| <= TOL).
        p: float, optional
            If known (the default is that it isn't known), it is the exact root. 
    
    Outputs:
        p_array: numpy.ndarray
            The array that contains the iterates p_n. Its shape is (m,) where m is the number of iterations completed before the stopping criterion, calculated by using a for loop. 
        fig: matplotlib.figure, optional
            If there is a p value, then this mathplotlib function outputs a plot containing the error plot.
        ax: matplotlib.axes, optional
            If there is a p value, then this matplotlib function outputs the axes for the plot, making sure we use a log base for the y-axis.  
              
    """
    
    p_array=np.zeros(Nmax,)
    
    #Write your code for Newton's method according to the instructions:
    p_previous = p0
    m = 0 #Tracker for the amount of iterations done
    for n in range(Nmax): #Begining the Newton method and running Nmax times
        p_n = p_previous - f(p_previous)/df(p_previous) #Computes the next approximation using the formula for Newton's method p_n = p_{n-1} - f(p_{n-1})/f'(p_{n-1})
        p_array[n] = p_n #Stores the values calculated into an array 
        m = m + 1 # Keeping track of iterations
        if np.abs(f(p_n)) <= TOL: #Checks if the iteration can stop
            break
        else:
            p_previous = p_n
    p_array = p_array[:m] #Makes sure the array only has m values in

    
    fig = ax = None

    # Write your code to generate plot according to the instructions:
    if p is not None: #Checks if the exact root is given to generate an error plot
        fig, ax = plt.subplots()
        n = np.arange(1, m+1) # generates an array of iterations for x axis
        error = np.abs(p_array - p) #Calcualtes the abslute error
        ax.set_yscale("log") #sets the y-axis to logarithmic scale
        ax.plot(n, error, marker='o', label="Absolute error") #Plots the absolute error
        ax.set_xlabel("Iteration (n)")
        ax.set_ylabel("Absolute error (log)")
        ax.legend(loc='best')  #A legend to label each plotted curve

    if fig is not None and ax is not None:
        return p_array, fig, ax
    else:
        return p_array

def q2B_answer():
    """
    Consider the function f(x)=(x-1)**2. Using your function Newton_with_stopping with p0=0.1 and N_max=20 and TOL=1e-16, and the exact root p.
    Q2b(i): Do you observe linear convergence (max words: 1)
    Answer to Question 2b(i): Yes
    Q2b(ii): If the observed order is linear, explain why this does not violate Corollary 1.2 (max words: 30).
    Answer to Question 2b(ii): Corollary 1.2 requires f’(p)=/ 0 for quadratic convergence. In this case, p = 1 and f’(x)=2x-2. f’(p)=0; therefore, the corollary condition is not met, explaining the observed linear convergence.
    """
    pass

def secant_with_stopping(f, p0, p1, Nmax, TOL):
    """
    Secant Method: Computes the sequence of approximations of the root using the Secant method. It uses TOL to check when to stop the algorithm early. The algorithm uses a nested if statement in a for loop to check if the absolute difference between p_m and p_{m-1} is less than or equal to TOL(1 + |p_m|). To prevent division by 0, if the denominator is strictly less than 10^-15 it is replaced by 10^-15.
    
    Inputs:
        f: function
            Lambda or standard function that corresponds to the function whose roots are being located
        p0: float
            The initial approximation to start the Secant method.
        p1: float
            The second initial approximation to start the Secant method.
        Nmax: int
            The maximum number of iterations performed for the function
        TOL: float
            The tolerance used for the stopping criterion (|p_m-p_{m-1}| <= TOL(1+|p_m|)).
    Outputs:
        p_array = numpy.ndarray
            The array that contains the iterates p_n generated through the secant method. Its shape is (m,) where m is the number of iterations completed before the stopping criterion, calculated by using a for loop. The array begins at p1

    """

    p_array=np.zeros(Nmax,)
    
    #Write your code for Secant's method according to the instructions:
    p_array[0] = p1
    
    p_previous2 = p0 #Initialises the two previous approximations required for the secant method
    p_previous1 = p1
    m = 1 #The counter for m (number of elements in the sequence)
    
    for n in range(Nmax-1): #Begining the loop for the iteration required for the secant method
        f_previous1 = f(p_previous1) #Evaluates the function at the two approximations
        f_previous2 = f(p_previous2)
        denominator = f_previous1 - f_previous2 #Calculates the denominator for the secant method 
        
        if np.abs(denominator) < 10**-15: #Checks if we are deviding by 0
            denominator = 10**-15
        
        p_n = p_previous1 - f_previous1 * ((p_previous1 - p_previous2) / denominator) #Computing the next approximation using the formula
        p_array[m] = p_n #Stores the values in the array
        m = m + 1 #Increases the counter
        if np.abs(p_n - p_previous1) <= TOL * (1 + np.abs(p_n)):  #Checks if the iteration can stop
            break
        p_previous2 = p_previous1 #Initialises new approximations
        p_previous1 = p_n
    p_array = p_array[:m] #Makes sure the array only has m values in
    
    return p_array

#import numpy library:

def bisection_simple(f,a,b,Nmax):
    """
    Bisection Method: Returns a numpy array of the 
    sequence of approximations obtained by the bisection method.
    
    Inputs:
    ----------
    f: function
        Input function for which the zero is to be found.
    a: float
        Left side of interval.
    b: float
        Right side of interval.
    Nmax: integer
        Number of iterations to be performed.

    Returns
    -------
    p_array: numpy.ndarray, 
            Array containing the sequence of approximations. 
            The shape is (Nmax,)
    """
    
    #Initialise numpy array of size Nmax
    p_array=np.zeros(Nmax,)
    
    #Begin bisection method:
    fa=f(a)
    for n in range(Nmax):
        p=(a+b)/2  # midpoint
        fp=f(p)    # evaluate f at midpoint
        #define new interval
        if fp*fa>0:
            a=p
            fa=fp
        else:
            b=p
        p_array[n]=p
    return p_array

def plot_convergence(p, f, df,  p0_newton, p0_sec, p1_sec,Nmax, TOL):
    """
    Currently, this function plots the error |p-p_n| obtained via Newton's and
    Secant methods encoded in the functions above (once completed). 
    You must modify this function to include the bisection method 
    following the instructions. 
    
    
    Inputs:
    ----------
    p: float
        Exact root    
    f: function
        Input function for which the zero is to be found.
    df: function
        Derivative of the input function for which the zero is to be found.
    p0_newton : float
        Initial approximation for Newton's method'
    p0_sec : float
        Initial approximation for the secant method
    p1_sec : float
        Initial approximation for the secant method
    Nmax: integer
        Number of iterations to be performed.
    TOL: float
        Tolerance for stopping criteria

    Output:
    -------
    fig, ax: matplotlib.pyplot objects of the figure that is produced
    

    """
    
    a = min(p0_sec, p1_sec)
    b = max(p0_sec, p1_sec)
    methods = ["newton", "secant", "bisection"] #Added bisection method

    # map method name -> function that returns the iterate list/array
    runners = {
        "newton": newton_with_stopping(f, df, p0_newton, Nmax, TOL),
        "secant": secant_with_stopping(f, p0_sec, p1_sec, Nmax, TOL),
        "bisection": bisection_simple(f, a, b, Nmax), 
    }
    #define plotting style
    styles = {
        "bisection": dict(marker="D", linestyle=":", color="green", label="Bisection"), #Plotting the bisection method in the graph
        "newton": dict(marker="*", linestyle="--", color="blue",  label="Newton"),
        "secant": dict(marker="o", linestyle="-",  color="black", label="Secant")
    }



    fig, ax = plt.subplots()
    ax.set_yscale("log")
    ax.set_xlabel("iteration ($n$)", fontsize=16)
    ax.set_ylabel(r"$|p - p_{n}|$", fontsize=16)
    ax.grid(True)
    
    #loop over methods and plot errors
    
    for m in methods:
        iters =runners[m]
        n = np.arange(1, len(iters) + 1)
        ax.plot(n, np.abs(iters - p), **styles[m])

    ax.legend(fontsize=16, loc="best")
    
    return fig, ax
    

def q4B_answer():
    """
    Consider the function f:R->R defined by f(x)=x**3 -2x+2. The function has one real root, which you may assume is given by p= -1.7692923542386314. Run your function plot_convergence to obtain approximations for the bisection, secant and Newton methods. Use the following inputs p0_sec=-2 and p1_sec=-1 and p0_newton=0, Nmax = 30, TOL=1e-16 and p as above.
    Q4b(i): Is the bisection method guaranteed to converge? If so, why? (max words: 40)
    Answer to Question 4b(i): Yes, a and b are -2 and -1, respectively. f(-2)= -2 and f(-1)= 3. Since f is continuous and the sign changes along the interval [-2,-1], Theorem 1.1 confirms a root exists, ensuring the bisection method will converge.
    Q4b(ii): Is Newton’s method guaranteed to converge? If so, why? (max words: 40)
    Answer to Question 4b(ii): No, Theorem 1.5 guarantees convergence only if p_0 is sufficiently close to the exact root. We know that p_0=0 and p = -1.7692923542386314. These are too far away from each other; therefore, Newton’s method is not guaranteed to converge.
    Q4b(iii): Based on your output from plot_convergence with the parameters above, do any of the methods fail to converge? If so, explain why. (max words: 40) 
    Answer to Question 4b(iii): Yes, Newton’s method fails. We know p0=0, since f(0)=2 and f’(0)=-2 we get p1=1. Then, evaluating at p1=1, we get p2=0. We can hence tell that the sequence oscillates endlessly between 0 and 1, never reaching the root.
    
    """
    pass


def scaled_pivoting(A, b ,m):
    """
    Scaled Partial Pivoting: Performs Gaussian elimination with scaled partial pivoting on the augmented matrix [A|b]. The algorithm stops once all the entires in the below the main diagonal in the first m columns are set to 0. If the matrix is singular (a row is all 0), then a ValueError is raised.
    Inputs:
        A: numpy.ndarray
            This array is a square matrix of the shape (n,n). This represents the coefficient matrix A for Ax=b
        b: numpy.ndarray
            This is a column vector of shape (n, 1). This represents the b for Ax=b
        m: int
            This is used to stop the Gaussian elimination after processing m columns (1<= m <= n-1)
    Outputs:
        tildeA: numpy.ndarray
            This is the reduced matrix after performing Gaussian elimination for the first m columns
        perm: numpy.ndarray
            This is the permutation vector of shape (n, ). It records the row ordering (for example, row K of tildeA corresponds to row perm[k] of the original argumated matrix)
    """
    
    #Write your code for scaled partial pivoting according to the instructions:
    n = len(A) #Determines the size of A
    tildeA = np.hstack((A,b)) #Form the matrix [A|b]
    perm = np.arange(n) #Initialises the permutation vector to record the row ordering

    s = np.zeros(n) # Initialises array to store scaled factors for each row
    for i in range(n): #Computes the initial scale factors
        s[i] = np.max(np.abs(A[i,:]))
        if s[i] == 0: #Checks if matrix is singualar
            raise ValueError("Matrix is singular (a row is all 0).") #releases a value error if matrix is singualr
        
    for i in range(m): #Begins the Gaussian elimination methos
        max_ratio = 0 #These two variables are used to find the pivot row with the largest scaled ratio
        p = i
        for j in range(i,n): #nested for loop used to check the current row and the rows below it to find the best pivot
            ratio = np.abs(tildeA[j, i] / s[j]) #Calculates the scaled ratio
            if ratio > max_ratio: #If a strictly greater ratio is found, then it updates the max ratio and pivot row index p
                max_ratio = ratio
                p = j
        if p != i: #If the pivot row index p is not the current row i, then it swaps them
            tildeA[[i, p]] = tildeA[[p, i]]
            s[i], s[p] = s[p], s[i]
            perm[i], perm[p] = perm[p], perm[i]
        for j in range(i+1, n): #This for loop eliminates the entries below the pivot element in column i
            mult = tildeA[j, i]/ tildeA[i, i] #Creates a new variable that calculates the multiplier needed for vectorisation
            tildeA[j, i] = 0 #Sets entires under the pivot as 0
            tildeA[j, i+1:] = tildeA[j, i+1:] - (mult * tildeA[i, i+1:]) #Updates row j using vectorisation


    return tildeA, perm


def backward_substitution(tildeA):
    """
    Returns an array representing the solution x of Ax=b computed using
    backward substitution after the augmented matrix tildeA has been successfully computed 
    via Gaussian elimination. 
    
    Parameters
    ----------
    tildeA: numpy.ndarray of shape (n,n+1)
        Array representing the augmented matrix [U v].
    n: int
        Integer that is at least 2.
        
    Returns
    -------
    x: numpy.ndarray of shape (n,1)
        Array representing the solution x.
    """
    n = np.shape(tildeA)[0] 
    x=np.zeros([n,1])
    
    #check for a_{n,n} =0 
    if tildeA[n-1, n-1] == 0:        
      raise ValueError("The system does not have unique solution.")        

    #start back substitution
    x[n-1] = tildeA[n-1,n] / tildeA[n-1,n-1]
    
    for i in np.arange(n-1,0,-1):
        #Computing the sum 
        s = 0
        for j in np.arange(i+1,n+1):
            s = s + tildeA[i-1,j-1]*x[j-1]
        x[i-1] = (tildeA[i-1,n] - s) / tildeA[i-1,i-1]
    
    return x


def sp_solve(A,b):
    """
    System Solvers: This function solves the linear system Ax=b using Gaussian elimination from 5a and the function from Listing 2.2, backward_substitution.
    Inputs:
        A: numpy.ndarray
            This is a square matrix (n,n) that represents the coefficients of matrix A for Ax=b
        b: numpy.ndarray
            This is a column vector (n, 1) that represents the vector b for Ax=b
    Outputs:
        x: numpy.ndarray
            This is a column vector (n, 1) that represents the solution of Ax=b
    """
    
    #Write your code to solve the system according to the instructions:
    n = len(A) #Determines the size of matrix A
    tildeA, perm = scaled_pivoting(A, b, n - 1) # Calls the Gaussian elimination function from the previous question, changing m to n-1 to ensure the algorithm does not end prematurely 
    x = backward_substitution(tildeA) #Calls the function from Listing 2.2 to compute the final solution vector x.

    return x

            


def q5C_answer():
    """
    Consider the linear system Ax=b with
    A= [1, 1, 1/ 1, 1+ε, 1/ 1, 1, 1+ε], b=[1, 1+ε, 1+ε]^T. Compute the exact solution of the linear system. Then run your function sp_solve(A,b) for ε = 10**-16
    Q5c(i): The exact solution (no need to provide the derivation)
    Answer to Question 5ci: x = [-1, 1, 1]^T.
    Q5c(ii): If your numerical solution via sp_solve(A,b) is different from the exact solution (or if your code breaks) explain why (max 50 words).
    Answer to Question 5cii: Since epsilon = 10^-16, it is smaller than machine precision. Floating-point arithmetic then evaluates 1+epsilon as just 1. This makes the matrix singular as it has identical rows, causing the algorithm to break during backward substitution and raise a ValueError.
        
    """
    pass
