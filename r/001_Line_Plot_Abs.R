args <- commandArgs(TRUE)
min_v = as.integer(args[1])
max_v = as.integer(args[2])
X11()
x = 0

count = 0

#hs = list(rep(0, length(args)-2))
#yvals = list(rep(0, length(args)-2))

#colors = c("red","blue","green","darkred","black", "purple", "orange", "pink") 
#i = args[3]
#count = count + 1
len = read.delim(args[3], header=FALSE)
len_sub <- len[which((len[,2] >= min_v) & (len[,2] <= max_v)), ]

table(unlist(len_sub[, 2]))
sum(unlist(len_sub[, 2]))

h <- hist(len_sub[,2], plot = FALSE)
yval <- h$counts

#hs[[count]]  = h$mids
#yvals[[count]] = yval

y_range = range(0, yval)

plot(h, yval, type="l", main="Length Distribution", ylim=y_range, col=1, xlab="Length", ylab="Count", pch=i, lwd=3)
#if (length(args) > 3) {
#	for (i in 2:(length(args)-2)) {
#	   lines(hs[[i]], yvals[[i]], col=i, pch=i, lwd=3)
#	}
#}

#length(hs)
#range(2, length(args)-2)

#legend(x = "topright", args[3:length(args)], cex=0.5, col=1:count, lty = 1)

message("Press Return To Continue")
invisible(readLines("stdin", n=1))
