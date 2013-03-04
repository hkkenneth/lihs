args <- commandArgs(TRUE)
min_v = as.integer(args[1])
max_v = as.integer(args[2])
X11()
x = 0

table = read.delim(args[3], header=FALSE)
x = table[,1]
y = table[,2]
index = which(( x <= max_v ) & ( x >= min_v ))
steps <- seq(1, length(index), by=(length(index)/50))
plot(y[index[steps]], type="o", axes=FALSE, main="Trinity Length Distribution", xlab="length", ylab="counts")
axis(1, at=1:length(index[steps]), lab=x[index[steps]])
axis(2, las=1)
box()

message("Press Return To Continue")
invisible(readLines("stdin", n=1))
