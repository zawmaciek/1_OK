library('neuralnet')
fun = function(x){
  return( x^3+2*x)
}
trainingoutput<-1:100
traininginput<-fun(trainingoutput)
scaled.traininginput<-(traininginput-min(traininginput))/(max(traininginput)-min(traininginput))
trainingdata<-cbind(scaled.traininginput,trainingoutput)
colnames(trainingdata)<-c("feature","regression")
net.val <-neuralnet(regression~feature,data=trainingdata,hidden=c(9,9,9,9),threshold=0.003, stepmax = 1e+06)
net.results<-compute(net.val,trainingdata)
plot(net.val)
ls(net.results)