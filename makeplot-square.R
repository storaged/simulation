

pdf('square-plot.pdf')

T = as.matrix(read.table('square.Rdata'))

boxplot.matrix(T[,2:101], use.cols=FALSE, xlab='Environmental stress level (phenotypic units/generation)', ylab='Number of autonomous transposons', names=format(T[,1]*0.002, scientific=FALSE), cex.lab=1.3)

dev.off()

pdf('perc-plot.pdf')

v = T[,1]

for(i in 1:50) { v[i] = 0; for(j in 2:101) { if(T[i, j] == 0) v[i] = v[i] + 1 } }
options(scipen=5)
plot(y=v, xlab='Environmental stress level (phenotypic units/generation)', ylab='Numer of runs in which TEs have been excised (out of a total of 100)', x=T[,1]*0.002, cex.lab=1.3)
lines(y=v, x=T[,1]*0.002)
abline(h=100, lty=2)


dev.off()


