# Quantitative-Mathematics-Portfolio

A collection of advanced, computational and predictive modelling projects undertaken during my second year at the University of Nottingham, studying for a BSc in Financial Mathematics.

This portfolio displays the practical applications of abstract mathematical theories, statistical evaluations, and data analytics using R to solve complex, real-world, data-driven problems. The portfolio also demonstrates my skills in using numerical methods in Python to help construct high-precision computational solvers and approximate solutions where exact analytical solutions are intractable.

---

## Statistical Modelling (R)

### Predictive Modelling of Washington D.C. Daily Bike Rentals | Grade: 86%

* **Objective**: Constructed a parsimonious multiple linear regression model using a dataset of 550 observations to identify the temporal and environmental factors that affect the demand for bike rentals in Washington D.C.
* **Methodology**:
  * **Exploratory Data Analysis (EDA)**: Utilised scatter plots and box plots to gain an idea of the data and identify the strongest predictors for potential non-linear relationships. Ultimately helping to find the covariates to use in the proposed multiple linear regression model.
  * **Model Selection**: Proposed a baseline model including all temporal and environmental factors. Then, using a bidirectional stepwise regression procedure (`step` in R), found the model that minimises the Akaike Information Criterion (AIC). The algorithm dropped `atemp` and `workingday` to prevent multicollinearity, as these factors are highly correlated.
  * **Hypothesis Test**: Rigorously confirmed the stepwise selection to use the new model confidently. This was done by running an ANOVA F-test to compare the nested model against the full model. With the data received, we failed to reject the null hypothesis (The new nested model is adequate; the dropped variables have no explanatory effect), while the final parsimonious model achieved an Adjusted R-squared of 0.841, explaining 84.1% of the variance in daily bike rentals.
  * **Diagnostics**: Verified the core assumptions of ordinary least squares (OLS) regression by plotting and analysing Residuals vs Fitted and Normal Q-Q plots to confirm homoscedasticity and normally distributed errors. Then used Cook's distance to check that no high-leverage outliers were disproportionately skewing the regression coefficients.
   * **Unseen Data Check**: Finally, using unseen test data, tested the model. The parsimonious model achieved a Test Deviance of 115,705,948. This vastly outperformed the simple baseline average model, which had a deviance of 494,819,527.

### Predicting Ames House Prices with a Bayesian Linear Model | Grade: 100%

* **Objective**: Engineered a Bayesian linear regression model to predict property valuations in Ames. This was done by comparing the predictive accuracy and regularisation parameters of Bayesian estimators vs standard frequentist Ordinary Least Squares (OLS).
* **Methodology**:
  * **Exploratory Data Analysis (EDA)**: Applied logarithmic scaling to the response variable (`Sale_Price`) to correct a severe positive right-skew after investigating the dataset. Then transformed ordinal variables (such as overall material quality and overall condition) into ordered factor levels to preserve their numerical hierarchy.
  * **Model Selection**: Chose three models to evaluate, in increasing order of complexity. Used the Bayesian Information Criterion (BIC) and calculated Bayes Factors to identify the optimal parsimonious model. Ultimately, the model incorporating living area and overall quality was selected, as it achieved the lowest BIC and a decisive Bayes Factor against the baseline model.
  * **Diagnostics**: Validated the core assumptions to be confident in the choice of the parsimonious model. Evaluated Residuals vs Fitted and Q-Q Residuals plots, confirming homoscedasticity and normality for the log-transformed data. Analysed Cook's distance to ensure no high-leverage outliers exceeded the 1.0 threshold.
  * **Posterior Sampling**: Computed the updated posterior parameters based on a conjugate Normal-Inverse-Gamma prior. Using the `MASS` package in R, 10,000 samples from the joint posterior distribution were drawn to visualise the marginal posterior distributions via histograms and analyse the variance ($\sigma^2$) and regression coefficients ($\beta$).
  * **OLS Comparison**: Compared the Bayesian point estimates against standard Ordinary Least Squares (OLS) estimates. From this, a strong "shrinkage" effect that pulled the categorical factor levels closer to zero was discovered. This then demonstrated the regularising effect of the prior on the 200-observation dataset.
  * **Unseen Data Check**: Evaluated the model's predictive performance against an unseen independent dataset. The Bayesian model achieved a Test Set Root Mean Squared Error (RMSE) of 0.2861. Then, the predicted log sale prices were plotted against the actual log sale prices, which confirmed that the model successfully generalised to new data without overfitting.
 
---
## Numerical Methods and Scientific Computation (Python)

### Algorithmic Root Solvers & Linear System Solver | Grade: 100%

* **Objective**: Developed a mathematical library using `numpy` and `matplotlib.pyplot` with key numerical algorithms for solving non-linear algebraic equations and high-dimensional linear systems.
* **Methodology**:
  * **Root-Finding algorithms**: Programmed and compared the Bisection, Fixed-Point Iteration, Newton’s and Secant methods. Implemented early-stopping criteria based on tolerances and generated logarithmic error plots to visually verify theoretical linear and quadratic convergence rates.
  * **Brief Analysis on Failure**: Examined cases in which standard methods fail, looking at why Newton's method oscillates endlessly or when an initial guess is too far from the root to guarantee convergence.
  * **Linear Algebra Solver**: Built an $Ax = b$ solver using Gaussian elimination with scaled partial pivoting and backward substitution. Used a permutation vector to track row ordering. Additionally, utilised vectorised row operations using `numpy` and structural checks to identify singular matrices under machine precision limits.

### Numerical Calculus | Grade: 85%

* **Objective**: Created a computational toolkit in Python for numerical differentiation and integration, applying these techniques to simulate and solve practical questions.
* **Methodology**:
  * **Derivative Approximation & Extrapolation**: Implemented a centered three-point finite difference formula to approximate the second derivative of a function at a point. Created an algorithm using the Richardson method to progressively eliminate leading error terms, proving it achieves rapid convergence for smooth functions ($$\sin(\pi x)$$) but fails on non-smooth functions with singularities.
  *  **Composite Integration Rules**: Programmed and evaluated composite Trapezoidal and 2-point Gauss integration rules. Verified that the Gauss rule achieves $$O(h^4)$$ convergence in comparison to the $$O(h^2)$$ of the Trapezoidal rule, and analysed how singularities break theoretical tolerance bounds.
  *   **Real-World Applications**: Modelled and computed a falling object's landing time by solving a non-linear physics equation. Selected a composite 2-point Gauss integration rule to evaluate the terminal velocity profile while coupling it with the Secant method for root solving. Achieving 3 decimal places of accuracy using just 10 panels to minimize computational cost.

