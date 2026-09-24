---
id: ml-regularisation
title: "ML & Regularisation"
type: topic
domain: signal-research
sources: [src-squarepoint-dqa-workbook]
---
# ML & Regularisation

**Sections:** [[bias-variance-tradeoff]] · [[ridge-regression]] · [[lasso-elastic-net]] · [[logistic-regression]] · [[pca]]

<a id="bias-variance-tradeoff"></a>

## Bias–Variance Trade-off
<!-- section: bias-variance-tradeoff | prerequisites: [estimator-properties] | related: [ridge-regression, lasso-elastic-net, cross-validation-leakage, r-squared] | sources: [src-squarepoint-dqa-workbook] | tags: [generalisation, overfitting] -->

$$E[(Y-\hat f(x))^2]=\sigma^2+\mathrm{Bias}(\hat f(x))^2+\mathrm{Var}(\hat f(x))$$

**Variables:**

- $Y=f(x)+\varepsilon$
- $\sigma^2$ noise variance
- $\hat f$ model fitted on a random training set

- More flexibility → less bias, more variance.
- It's about **test** error, not training fit.

### Connections
- **Levers:** [[ridge-regression]], [[lasso-elastic-net]]; **measured by:** [[cross-validation-leakage]]. Mirrors [[estimator-properties]] (MSE = Var + Bias²).

<a id="ridge-regression"></a>

## Ridge Regression (L2)
<!-- section: ridge-regression | prerequisites: [ols-regression, multicollinearity] | related: [lasso-elastic-net, bias-variance-tradeoff, beta-bernoulli-conjugacy, mean-variance-optimization] | sources: [src-squarepoint-dqa-workbook] | tags: [regularisation, shrinkage] -->

$$\hat\beta_R=\arg\min_\beta\|y-X\beta\|^2+\lambda\|\beta\|_2^2=(X^\top X+\lambda I)^{-1}X^\top y$$

**Variables:**

- $\lambda>0$ penalty
- $X$ centred/standardised features (intercept unpenalised)

### Key points
- In each eigen-direction of $X^\top X$ (eigenvalue $d$): $1/d\to1/(d+\lambda)$ — tames near-singular directions.
- Biased but can lower prediction MSE; never sets coefficients exactly to 0.
- Individual coefficients need not shrink monotonically with correlated predictors.
- **Bayesian view:** posterior mode with prior $\beta\sim N(0,\tau^2I)$, $\lambda=\sigma^2/\tau^2$.
- Fit standardisation on training data only.

### Connections
- **Fixes:** [[multicollinearity]]. **Contrast:** [[lasso-elastic-net]] (sparsity). **Same idea in portfolios:** covariance shrinkage in [[mean-variance-optimization]].

<a id="lasso-elastic-net"></a>

## Lasso (L1) & Elastic Net
<!-- section: lasso-elastic-net | prerequisites: [ridge-regression] | related: [bias-variance-tradeoff] | sources: [src-squarepoint-dqa-workbook] | tags: [sparsity, soft-thresholding] -->

$$\hat\beta_L=\arg\min\|y-X\beta\|^2+\lambda\|\beta\|_1;\qquad X^\top X=I\Rightarrow \hat\beta_{L,j}=\mathrm{sign}(z_j)(|z_j|-\lambda/2)_+,\ z=X^\top y$$
Elastic net: $\|y-X\beta\|^2+\lambda_1\|\beta\|_1+\lambda_2\|\beta\|_2^2$.

**Variables:**

- $\lambda,\lambda_1,\lambda_2$ penalties
- $z_j$ OLS coefficient under orthonormal design

- L1 corner at 0 ⇒ exact zeros (feature selection). Threshold depends on loss scaling (½, 1/n) — state convention.
- Laplace prior ⇒ L1 posterior mode. Elastic net helps with correlated predictors.

<a id="logistic-regression"></a>

## Logistic Regression
<!-- section: logistic-regression | prerequisites: [maximum-likelihood, ols-regression] | related: [] | sources: [src-squarepoint-dqa-workbook] | tags: [classification, cross-entropy] -->

$$P(Y=1\mid x)=\frac{1}{1+e^{-x^\top\beta}},\qquad \log\frac{p}{1-p}=x^\top\beta,\qquad \mathcal L=-\sum_i[y_i\log p_i+(1-y_i)\log(1-p_i)]$$

**Variables:**

- $x$ features
- $\beta$ coefficients
- $p_i$ predicted probability

- Models a probability (unlike OLS on 0/1).
- Under class imbalance, accuracy misleads — calibration & decision costs matter.

<a id="pca"></a>

## Principal Component Analysis (PCA)
<!-- section: pca | prerequisites: [eigen-svd-psd, variance-covariance-correlation] | related: [multicollinearity, portfolio-variance-diversification, cross-validation-leakage] | sources: [src-squarepoint-dqa-workbook] | tags: [dimension-reduction, eigenvectors] -->

$$\max_v v^\top\Sigma v\ \ \text{s.t. } v^\top v=1\ \Rightarrow\ \Sigma v=\lambda v,\qquad \text{explained share}_j=\frac{\lambda_j}{\sum_i\lambda_i}$$

**Variables:**

- $\Sigma$ covariance of centred features
- $v$ unit direction
- $\lambda_j$ ordered eigenvalues

**Example:** $\Sigma=\begin{pmatrix}1&0.8\\0.8&1\end{pmatrix}$ → eigenvectors $(1,1)/\sqrt2$ (λ=1.8, 90%) and $(1,-1)/\sqrt2$ (λ=0.2).

### Pitfalls
- **Unsupervised** — ignores $y$; the 1% low-variance direction may hold the signal.
- Components uncorrelated, not necessarily independent; eigenvector sign arbitrary.
- Covariance-PCA vs correlation-PCA (standardised) — units can dominate.
- Fit centring/scaling/PCA on training data only.

### Connections
- **Builds on:** [[eigen-svd-psd]]. **Remedy for:** [[multicollinearity]]. **Leakage risk:** [[cross-validation-leakage]].
