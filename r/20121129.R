args <- commandArgs(TRUE)
X11()

table = read.delim(args[1], header=FALSE)
transcripts_length = table[,2]
hist(transcripts_length, breaks=100, main="Length Distribution of Unique Ferret Transcripts", xlab="Transcript Length", ylab="Number of Unique Ferret Transcripts")

message("Press Return To Continue")
invisible(readLines("stdin", n=1))
