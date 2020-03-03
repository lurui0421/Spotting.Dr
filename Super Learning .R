### Import the data set
###  More complex super learning algorithms
data<-read.csv(file=file.choose())
data<-data[c(-1)]
install.packages("SuperLearner")
library(SuperLearner)
remotes::install_github("ecpolley/SuperLearner")
##Set a seed for reproducibility in this random sampling.
set.seed(1)
train_obs = sample(nrow(data),6859*0.75)
# X is our training sample.
x_train = data[train_obs,c(1:34)]
# Create a holdout set for evaluating model performance.
# Note: cross-validation is even better than a single holdout sample.
x_holdout = data[-train_obs,c(1:34)]
y_train = data$y[train_obs]
y_holdout = data$y[-train_obs]
# Review the outcome variable distribution.
install.packages("xgboost")
library(xgboost)
sl_lib = c("SL.xgboost", "SL.randomForest",
           "SL.glmnet", "SL.nnet",
           "SL.ksvm","SL.bartMachine")
sl = SuperLearner(Y = y_train, X = x_train, family = binomial(),SL.library =sl_lib)
pred = predict(sl, x_holdout, onlySL = TRUE)
pred_all = predict(sl, data[,c(1:34)], onlySL = TRUE)
### Display the predicted quality index via histogram
hist(pred_all$pred, main="Histogram for Quality Index",
     xlab="Quality Index",
     border="black",
     col="royal blue",
     xlim=c(0,1),
     breaks=50)
### Create predicted index based on probability
pred_index=ifelse(round(pred$pred,2)>0.50,1,0)
### Estimate F1 score
install.packages("MLmetrics")
library(MLmetrics)
F1_Score(y_holdout,pred_index, positive = NULL)
### Get confusion matrix
install.packages("caret")
library(caret)
pred_index<-as.vector(pred_index)
pred_index<-factor(pred_index)
y_holdout<-factor(y_holdout)
confusionMatrix(
  pred_index,
  y_holdout,
  positive = NULL,
  dnn = c("Prediction", "Reference"))

hist(pred, main="Histogram for Quality Index",
     xlab="Quality Index",
     border="black",
     col="royal blue",
     xlim=c(0,1),
     breaks=50)
pred_index=ifelse(round(pred,2)>0.50,1,0)
install.packages("MLmetrics")
library(MLmetrics)
F1_Score(y_holdout,pred, positive = NULL)
install.packages("caret")
library(caret)
pred_index<-as.vector(pred_index)
pred_index<-factor(pred_index)
y_holdout<-factor(y_holdout)
confusionMatrix(
  pred_index,
  y_holdout,
  positive = NULL,
  dnn = c("Prediction", "Reference"))
### create the list to hold the results
sample_data<-list()
for (i in 1:100){
  sample_labels<-sample(nrow(data),6859*0.75 )
  # X is our training sample.
  x_train=data[sample_labels,c(1:34)]
  # Create a holdout set for evaluating model performance.
  # Note: cross-validation is even better than a single holdout sample.
  x_holdout=data[-sample_labels,c(1:34)]
  y_train=data$y[sample_labels]
  y_holdout=data$y[-sample_labels]
  sl_lib = c("SL.xgboost", "SL.randomForest",
             "SL.glmnet", "SL.nnet",
             "SL.ksvm","SL.bartMachine")
  sl=SuperLearner(Y = y_train, X = x_train, family = binomial(),
                    SL.library =sl_lib)
  pred_all=predict(sl, data[,c(1:34)], onlySL = TRUE)
  sample_data[[i]]= pred_all$pred
}
pred=apply(sample_data,2,median)


