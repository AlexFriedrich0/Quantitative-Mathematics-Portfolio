# Title: Predictive Modelling of Washington D.C. Daily Bike Rentals
# Author: Alexander Friedrich
#

library(ggplot2)
library(gridExtra)

# Load datasets
train_data <- read.csv("BikeTrain.csv")
test_data <- read.csv("BikeTest.csv")

# Convert categorical features to factors
category_variables <- c("season", "yr", "mnth", "holiday", "weekday",
                        "workingday", "weathersit")
train_data[category_variables] <- lapply(train_data[category_variables], as.factor)
test_data[category_variables] <- lapply(test_data[category_variables], as.factor)

# EDA Plots
plot1 <- ggplot(train_data, aes(x = temp, y = cnt)) +
  geom_point(alpha = 0.5) + 
  geom_smooth(method = "lm", col = "blue", se = FALSE) + 
  theme_bw() + 
  labs(title = "Bike Rentals vs Temperature",
       x = "Normalised Temperature",
       y = "Total Rentals")

plot2 <- ggplot(train_data, aes(x = season, y = cnt, fill = season)) +
  geom_boxplot() +
  theme_bw() +
  labs(title = "Bike Rentals by Season", 
       x = "Season (1 = Spring, 2 = Summer, 3 = Fall, 4 = Winter)", 
       y = "Total Rentals") +
  theme(legend.position = "none")

grid.arrange(plot1, plot2, ncol = 2)

# Fit Baseline Model with all variables
model <- lm(cnt ~ season + yr + mnth + holiday + weekday + workingday + weathersit +
              temp + atemp + hum + windspeed, data = train_data)

# Bidirectional Stepwise Regression (AIC selection)
bestmodel <- step(model, direction = "both", trace = 0)
summary(bestmodel)

# Compare Nested Stepwise Model vs Full Model
anova(bestmodel, model)

# Diagnostic Plots
plot(bestmodel)

# Evaluate predictions on unseen test data
bestpred <- predict(bestmodel, newdata = test_data)
baselinemodel <- lm(cnt ~ season, data = train_data)
predbaseline <- predict(baselinemodel, newdata = test_data)

devbest <- sum((test_data$cnt - bestpred)^2)
devbaseline <- sum((test_data$cnt - predbaseline)^2)

cat("Test Deviance of Parsimonious Model: ", devbest, "\n")
cat("Test Deviance of Baseline Model: ", devbaseline, "\n")

# Visualise prediction accuracy on test data
par(mfrow = c(1, 2)) 
plot(test_data$cnt, bestpred,
     main = "Parsimonious Model",
     xlab = "Actual Bike Rentals (cnt)",
     ylab = "Predicted Bike Rentals",
     col = "purple")
abline(0, 1, col = "red") 

plot(test_data$cnt, predbaseline,
     main = "Baseline Model",
     xlab = "Actual Bike Rentals (cnt)",
     ylab = "Predicted Bike Rentals",
     col = "green")
abline(0, 1, col = "red")
