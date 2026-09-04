# Title: Bayesian Predictive Property Valuation
# Author: Alexander Friedrich
# Description: Bayesian linear regression model predicting property valuations
#              using conjugate Normal-Inverse-Gamma priors and OLS comparisons.

library(ggplot2)
library(gridExtra)
ames_train <- read.csv("AmesTrain.csv")
ames_test <- read.csv("AmesTest.csv")
category_variables <- c("Overall_Qual", "Overall_Cond")
quality_levels <- c("Very_Poor", "Poor", "Fair", "Below_Average", "Average",
                    "Above_Average", "Good", "Very_Good", "Excellent", "Very_Excellent")
ames_train[category_variables] <- lapply(ames_train[category_variables], factor,
                                         levels = quality_levels, ordered =TRUE)
ames_test[category_variables] <- lapply(ames_test[category_variables], factor,
                                        levels = quality_levels, ordered =TRUE)
ames_train$log_Sale_Price <- log(ames_train$Sale_Price)
par(mfrow=c(1,2))
hist(ames_train$Sale_Price, main="Raw Sale Price", xlab="Sale Price", col="purple")
hist(ames_train$log_Sale_Price, main="Log Sale Price", xlab="Log Sale Price", col="red")
par(mfrow=c(1,1))
plot(ames_train$Gr_Liv_Area, ames_train$log_Sale_Price,
     main = "Log Sale Price Against Living Area", xlab="Above-Ground Living Area (sq ft)",
     ylab="Log Sale Price", pch=16, col="darkgray")
abline(lm(log_Sale_Price~ Gr_Liv_Area, data =ames_train), col="darkred", lwd=2)
library(BayesFactor)
m1_lm <- lm(log_Sale_Price~ Gr_Liv_Area, data = ames_train)
m2_lm <- lm(log_Sale_Price~ Gr_Liv_Area + Overall_Qual, data = ames_train)
m3_lm <- lm(log_Sale_Price~ Gr_Liv_Area + Overall_Qual + Overall_Cond, data = ames_train)
m1_bf <- lmBF(log_Sale_Price~ Gr_Liv_Area, data = ames_train)
m2_bf <- lmBF(log_Sale_Price~ Gr_Liv_Area + Overall_Qual, data= ames_train)
m3_bf <- lmBF(log_Sale_Price~ Gr_Liv_Area + Overall_Qual+ Overall_Cond, data= ames_train)
print("BIC Values:")
BIC(m1_lm, m2_lm, m3_lm)
print("Bayes Factor (Model 2 vs Model 1)")
m2_bf/m1_bf
print("Bayes Factor (Model 3 vs Model 2)")
m3_bf/m2_bf
par(mfrow = c(1, 3))
plot(m2_lm, which = 1)
plot(m2_lm, which = 2)
plot(m2_lm, which = 4)
library(MASS)
y<-ames_train$log_Sale_Price
Z<-model.matrix(~Gr_Liv_Area + Overall_Qual, data = ames_train)
n<-nrow(Z)
p<-ncol(Z)
B0 <- rep(0,p)
Sigma0 <- diag(10,p)
a0<- 1
b0<-1
Sigma0inv <-solve(Sigma0)
Sigman <- solve(Sigma0inv + t(Z) %*% Z)
Bn <- Sigman %*%(t(Z) %*% y +Sigma0inv %*% B0)
an <- a0+n/2
B0S0invB0 <- t(B0) %*% Sigma0inv %*% B0
BnSninvBn <- t(Bn) %*% solve(Sigman) %*% Bn
bn <- as.numeric(b0 +0.5*(t(y) %*% y + B0S0invB0- BnSninvBn))
set.seed(42)
nsamples<-10000
sigma2samples <- 1/ rgamma(nsamples, shape=an, rate=bn)
betasamples <- matrix(0, nrow=nsamples, ncol=p)
for (i in 1:nsamples) { betasamples[i, ] <- mvrnorm(1, mu=Bn, Sigma = Sigman * sigma2samples[i])}
par(mfrow = c(3,4), mar = c(4,4,2,1))
for (j in 1:p) {
  hist(betasamples[, j],
       main = paste("Beta: ", colnames(Z)[j]),
       xlab = "Sample Value",
       col = "purple",
       breaks = 30)
}
hist(sigma2samples,
     main= expression(paste("Posterior: ", sigmaˆ2)),
     xlab= "Sample Value",
     col="darkgreen",
     breaks=30)
bayescoef <- colMeans(betasamples)
bayessigma2 <- mean(sigma2samples)
olsmodel <- lm(y~Z-1)
olscoef <- coef(olsmodel)
olssigma2 <- summary(olsmodel)$sigmaˆ2
comparisondf <- data.frame(
  OLSest = round(as.numeric(olscoef), 4),
  Bayesest = round(as.numeric(bayescoef), 4),
  Diff = round(abs(as.numeric(olscoef)- as.numeric(bayescoef)), 4)
)
rownames(comparisondf) <- names(olscoef)
print("Comparion of Regression Coefficents:")
print(comparisondf)
print(paste("OLS Residual Variance:", round(olssigma2, 4)))
print(paste("Bayesian Posterior Varience:", round(bayessigma2, 4)))
ames_test$Overall_Qual <- factor(ames_test$Overall_Qual, levels=quality_levels, ordered=TRUE)
ytest <- log(ames_test$Sale_Price)
Ztest <- model.matrix(~Gr_Liv_Area + Overall_Qual, data = ames_test)
predictions <- Ztest %*% bayescoef
rmse <- sqrt(mean((ytest-predictions)ˆ2))
plot(ytest, predictions,
     main = "Baysian Model Predictions Against Actual Prices (log)",
     xlab = "Actual Log Sale Price",
     ylab = "Predicted Log Sale Price",
     col = "darkblue", pch=16)
abline(0, 1, col = "red", lwd=2, lty = 2)
print(paste("Test Set RMSE: ", round(rmse, 4)))
