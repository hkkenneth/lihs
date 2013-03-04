args <- commandArgs(TRUE)

X11()
efile = read.delim(args[1], header=FALSE)
cutoff <- as.real(args[2])
eval = efile[,2] / efile[,1]
eh= hist(eval[which(abs(eval) < cutoff)], breaks=100, main="Size difference Ratio (Ref - Prediction)/(Ref Size) Distribution", xlab="Size difference ratio", ylab="Counts")

message("Press Return To Continue")
invisible(readLines("stdin", n=1))
