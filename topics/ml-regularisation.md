---
id: ml-regularisation
title: "ML & Regularisation"
type: topic
domain: prob-stats
sources: [src-squarepoint-dqa-workbook]
---
# ML & Regularisation

OLS is unbiased but can have large variance when regressors are many or correlated. This chapter explains the bias–variance trade-off and the standard tools that trade a little bias for a lot less variance — ridge, lasso and elastic net — plus logistic regression for probabilities and PCA for dimension reduction.

**Prerequisites:** [[ols-regression]], [[multicollinearity]], [[estimator-properties]], [[maximum-likelihood]], [[eigen-svd-psd]].

**Leads to:** [[cross-validation-leakage]] (measuring test error), [[mean-variance-optimization]] (shrinkage in portfolios).

**Sections:** [[bias-variance-tradeoff]] · [[ridge-regression]] · [[lasso-elastic-net]] · [[logistic-regression]] · [[pca]]

<a id="bias-variance-tradeoff"></a>

## Bias–Variance Trade-off
<!-- section: bias-variance-tradeoff | prerequisites: [estimator-properties] | related: [ridge-regression, lasso-elastic-net, cross-validation-leakage, r-squared, conditional-expectation-best-predictor] | sources: [src-squarepoint-dqa-workbook] | tags: [generalisation, overfitting] -->

The expected test error of a fitted model splits into irreducible noise, squared bias and variance — the prediction version of MSE = variance + bias².

### Formula
$$E\big[(Y-\hat f(x))^2\big]=\sigma^2+\mathrm{Bias}\big(\hat f(x)\big)^2+\mathrm{Var}\big(\hat f(x)\big)$$

**Variables:**

- $Y=f(x)+\varepsilon$ new observation at input $x$
- $f$ true regression function
- $\varepsilon$ noise with variance $\sigma^2$
- $\hat f$ model fitted on a random training set

### Key points
- More flexibility → less bias, more variance.
- The trade-off is about **test** error, not training fit.

### Connections
- **Builds on:** [[estimator-properties]] (MSE = Var + Bias²).
- **Levers:** [[ridge-regression]], [[lasso-elastic-net]]. **Measured by:** [[cross-validation-leakage]].

<a id="ridge-regression"></a>

## Ridge Regression (L2)
<!-- section: ridge-regression | prerequisites: [ols-regression, multicollinearity, bias-variance-tradeoff] | related: [lasso-elastic-net, beta-bernoulli-conjugacy, mean-variance-optimization, eigen-svd-psd] | sources: [src-squarepoint-dqa-workbook] | tags: [regularisation, shrinkage] -->

Ridge adds a penalty on the squared size of the coefficients. This shrinks them toward zero and stabilises the directions in which $X^\top X$ is nearly singular.

### Formula
$$\hat\beta_R=\arg\min_\beta\ \|y-X\beta\|^2+\lambda\|\beta\|_2^2=(X^\top X+\lambda I)^{-1}X^\top y$$

**Variables:**

- $\hat\beta_R$ ridge coefficients
- $y$ response vector
- $X$ centred/standardised features (the intercept is not penalised)
- $\lambda>0$ penalty strength
- $\|\beta\|_2^2=\sum_j\beta_j^2$ squared L2 norm
- $I$ identity matrix

### Key points
- In each eigen-direction of $X^\top X$ (eigenvalue $d_j^2$, where $d_j$ is a singular value of $X$, [[eigen-svd-psd]]) the inverse changes from $1/d_j^2$ to $1/(d_j^2+\lambda)$ — this tames near-singular directions.
- Biased but can lower prediction MSE; never sets coefficients exactly to 0.
- Individual coefficients need not shrink monotonically with correlated predictors.
- **Bayesian view:** the posterior mode under the prior $\beta\sim N(0,\tau^2I)$ with $\lambda=\sigma^2/\tau^2$ ($\sigma^2$ noise variance, $\tau^2$ prior variance).
- Fit the standardisation on training data only.

### Connections
- **Fixes:** [[multicollinearity]]. **Contrast:** [[lasso-elastic-net]] (sparsity).
- **Same idea as:** [[beta-bernoulli-conjugacy]] (prior shrinkage); covariance shrinkage in [[mean-variance-optimization]].

<a id="lasso-elastic-net"></a>

## Lasso (L1) & Elastic Net
<!-- section: lasso-elastic-net | prerequisites: [ridge-regression] | related: [bias-variance-tradeoff] | sources: [src-squarepoint-dqa-workbook] | tags: [sparsity, soft-thresholding] -->

Lasso penalises the absolute size of the coefficients. The corner of the L1 penalty at zero sets some coefficients exactly to zero, so lasso also selects features.

### Formulas
$$\hat\beta_L=\arg\min_\beta\ \|y-X\beta\|^2+\lambda\|\beta\|_1;\qquad X^\top X=I\ \Rightarrow\ \hat\beta_{L,j}=\mathrm{sign}(z_j)\,\big(|z_j|-\lambda/2\big)^+,\quad z=X^\top y$$
$$\text{Elastic net: }\ \|y-X\beta\|^2+\lambda_1\|\beta\|_1+\lambda_2\|\beta\|_2^2$$

**Variables:**

- $\hat\beta_L$ lasso coefficients
- $\|\beta\|_1=\sum_j|\beta_j|$ L1 norm
- $\lambda,\lambda_1,\lambda_2$ penalty strengths
- $z_j$ OLS coefficient under an orthonormal design ($X^\top X=I$)
- $(\cdot)^+$ positive part (soft-thresholding)

### Key points
- The L1 corner at 0 gives exact zeros (feature selection). The threshold depends on the loss scaling (½, 1/n) — state the convention.
- A Laplace prior gives L1 as the posterior mode. Elastic net helps with correlated predictors.

### Connections
- **Builds on:** [[ridge-regression]]. **Lever for:** [[bias-variance-tradeoff]].

<a id="logistic-regression"></a>

## Logistic Regression
<!-- section: logistic-regression | prerequisites: [maximum-likelihood, ols-regression] | related: [] | sources: [src-squarepoint-dqa-workbook] | tags: [classification, cross-entropy] -->

For a binary outcome, logistic regression models the log-odds as linear in the features and is fitted by maximum likelihood (minimising cross-entropy).

### Formulas
$$P(Y=1\mid x)=\frac{1}{1+e^{-x^\top\beta}},\qquad \ln\frac{p}{1-p}=x^\top\beta,\qquad \mathcal L=-\sum_i\big[y_i\ln p_i+(1-y_i)\ln(1-p_i)\big]$$

**Variables:**

- $Y\in\{0,1\}$ binary outcome
- $x$ feature vector
- $\beta$ coefficients
- $p=P(Y=1\mid x)$; $p_i$ predicted probability for observation $i$
- $y_i$ observed outcome of observation $i$
- $\mathcal L$ cross-entropy loss (negative Bernoulli log-likelihood)

### Key points
- It models a probability (unlike OLS on 0/1 outcomes).
- Under class imbalance, accuracy misleads — calibration and decision costs matter.

### Connections
- **Builds on:** [[maximum-likelihood]] (Bernoulli MLE), [[ols-regression]].

<a id="pca"></a>

## Principal Component Analysis (PCA)
<!-- section: pca | prerequisites: [eigen-svd-psd, variance-covariance-correlation] | related: [multicollinearity, portfolio-variance-diversification, cross-validation-leakage] | sources: [src-squarepoint-dqa-workbook] | tags: [dimension-reduction, eigenvectors] -->

PCA finds the orthogonal directions along which the data vary most. They are the eigenvectors of the covariance matrix, ordered by eigenvalue.

### Formula
$$\max_v\ v^\top\Sigma v\ \ \text{s.t. } v^\top v=1\ \Rightarrow\ \Sigma v=\lambda v,\qquad \text{explained share}_j=\frac{\lambda_j}{\sum_i\lambda_i}$$

**Variables:**

- $\Sigma$ covariance matrix of the centred features
- $v$ unit direction (a principal component when it solves the problem)
- $\lambda,\lambda_j$ eigenvalues, ordered $\lambda_1\ge\lambda_2\ge\dots$

### Worked example
$\Sigma=\begin{pmatrix}1&0.8\\0.8&1\end{pmatrix}$ → eigenvectors $(1,1)/\sqrt2$ ($\lambda=1.8$, 90% of variance) and $(1,-1)/\sqrt2$ ($\lambda=0.2$).

### Pitfalls
- **Unsupervised** — ignores $y$; the low-variance direction may hold the signal.
- Components are uncorrelated, not necessarily independent; the sign of an eigenvector is arbitrary.
- Covariance-PCA vs correlation-PCA (standardised): with covariance-PCA the units can dominate.
- Fit centring, scaling and PCA on training data only.

### Connections
- **Builds on:** [[eigen-svd-psd]], [[variance-covariance-correlation]].
- **Remedy for:** [[multicollinearity]]. **Leakage risk:** [[cross-validation-leakage]].
