
library('fields')

tbl = t(as.matrix(read.table('heatmap.Rdata')))

png('plot.png')
image.plot(tbl)
dev.off()

