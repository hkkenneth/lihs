args <- commandArgs(TRUE)
X11()

broad = read.delim("broad.len", header=FALSE)
broad_len = broad[,2]
our = read.delim("our.len", header=FALSE)
our_len = our[,2]

bh = hist(broad_len, breaks=100, freq=FALSE, plot=FALSE)
oh = hist(our_len, breaks=100, freq=FALSE, plot=FALSE)

plot(bh$mids, bh$counts/20061, type="l", col="red",  main="Length Distribution of Unique Ferret Transcripts", xlab="Transcript Length", ylab="Frequency of Unique Ferret Transcripts")
lines(oh$mids, oh$counts/17646, col="blue")

legend(x = "topright", c("Broad Institute", "Our Data"), cex=1.5, col=c("red", "blue"), lty = 1)

message("Press Return To Continue")
invisible(readLines("stdin", n=1))

