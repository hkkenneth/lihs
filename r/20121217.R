args <- commandArgs(TRUE)
X11()

efile = read.delim(args[1], header=FALSE)
#eval = log10(efile[,2])
eval = efile[,2]

eh= hist(eval, breaks=100, main="E-value Distribution", xlab="E-values", ylab="Counts")

message("Press Return To Continue")
invisible(readLines("stdin", n=1))

