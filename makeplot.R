



suppressPackageStartupMessages(library('fields'))

makeplot <- function(in_filename, out_filename, correction = -1)
{
base_file_name = strsplit(in_filename, '\\.')[[1]][1]
desc_file_name = paste(base_file_name, 'bin', 'desc', 'Rdata', sep = '.')
#dev = png(file = out_filename, width = 1000, height = 700, pointsize = 30)
#dev = pdf(file = out_filename)
desc = read.table(desc_file_name)
desc.length = desc$V1

#colors = rev(rainbow(10000, start=0.0, end=0.8))

#colors[1] = '#FFFFFF'
colors = gray(5000:0/10000)
colors[1] = '#FFFFFF'

T = as.matrix(read.table(in_filename))

png(file = paste(out_filename, '.png', sep=''), width = 1000, height = 700, pointsize = 30)
image.plot(1:dim(T)[1], (1:dim(T)[2]/(dim(T)[2])*desc.length)+correction, T, xlab="", ylab="", col = colors)
dev.off()

#dev = pdf(file = paste(out_filename, '.pdf', sep=''))
#image.plot(1:dim(T)[1], (1:dim(T)[2]/(dim(T)[2])*desc.length)+correction, T, xlab="", ylab="", col = colors)
#dev.off()
}



makeplot('output-aut_transposons.bin.Rdata', 'plot-1')
makeplot('output-nonaut_transposons.bin.Rdata', 'plot-2')
makeplot('output-fitness.bin.Rdata', 'plot-3', correction = 0)
makeplot('output-total_mutations.bin.Rdata', 'plot-4')




mut_te = read.table('output-transpositions.bin.Rdata')[[1]]
mut_te_median = read.table('output-transpositions-median.bin.Rdata')[[1]]
mut_rn = read.table('output-random_mutations.bin.Rdata')[[1]]
mut_tot = mut_te + mut_rn
#png(file = 'plot-5.png', width=1000, height=700, pointsize=30)

plot5 <- function()
{
  plot(mut_tot, type='l', col='white', xlab='', ylab='')
  lines(mut_rn, col='black')
  lines(mut_te, col='gray')
  lines(mut_te_median, col='red')
  legend(
    'topleft', 
    legend=c('random mutations', 'TE-induced mutations avg', 'TE-induced mutations median'), 
    fill=c('black', 'gray', 'red'),
    pch=1,
    cex=0.5
    )
}

#pdf(file = 'plot-5.pdf')
#plot5()
#dev.off()

png(file = 'plot-5.png', width = 1000, height = 700, pointsize = 30)
plot5()
dev.off()


make_sweep_plot <- function(in_filename, out_filename)
{
T = as.matrix(read.table(in_filename))
png(file = paste(out_filename, '.png', sep=''), width = 1000, height = 700, pointsize = 30)
image.plot(T)
dev.off()
#dev = pdf(file = paste(out_filename, '.pdf', sep=''))
#image.plot(T)
#dev.off()
}

make_sweep_plot('imagedata-aut_transposons_i.bin.Rdata', 'plot-6')
make_sweep_plot('imagedata-fitness_i.bin.Rdata', 'plot-7')
make_sweep_plot('imagedata-nonaut_transposons_i.bin.Rdata', 'plot-8')

horiz.color.bar <- function(lut, min, max, nticks=5, digits=3, ticks=NA, title='') {
    if(min==max){
      if(min==0){
        min=0
        max=1
      }
      else{min=0}
    }
    ticks=round(seq(min, max, len=nticks), digits=digits)
    par(mar = c(2,1,0,1))
    scale = (length(lut)-1)/(max-min)

    #dev.new(width=5, height=1.75)
    plot(c(min,max), c(0,1), type='n', bty='n', xaxt='n', xlab='', yaxt='n', ylab='', main=title)
    axis(1, ticks, las=1)
    for (i in 1:(length(lut)-1)) {
      y = (i-1)/scale + min
        rect(y,0,y+1/scale,10, col=lut[i], border=NA)
    }
}


make_map_plot <- function(in_filename, out_filename, out_counter, plotsize=7)
{
  generations = as.matrix(read.table(paste(in_filename, 'generations.bin.Rdata', sep='')))
  for (generation in generations[,1]){
    T = as.matrix(read.table(paste(in_filename, 'gen', generation, '.bin.Rdata', sep='')))
    T = t(T)
    title = sprintf("generation: %d, population size: %d", generation, length(T[1,]))

    png(file = paste(out_filename, out_counter,'.png', sep=''), width = 1000, height = 700, pointsize = 30)
    layout(matrix(c(1,1,rep(c(2,4), plotsize), 3,5), plotsize+2, 2, byrow=TRUE))

    par(mar = c(0,0,0,0))
    plot(c(0, 1), c(0, 1), ann = F, bty = 'n', type = 'n', xaxt = 'n', yaxt = 'n')
    text(x = 0.5, y = 0.5, cex = 1.6, title, col = "black")

    plotEx = function(pos, halo, fill, titleEx, halomax='n', fillmax='n'){
      if(halomax=='n') halomax=max(halo,1)
      if(fillmax=='n') fillmax=max(fill,1)
      halo2 = rainbow(120)[71:1][round(halo*70/halomax+1)]
      fill2 = gray(fill/fillmax)
      par(mar = c(2,0,1,0))
      plot(pos[1,], pos[2,], pch=22, bg=fill2, col=halo2, main=titleEx, xlim=c(-1,1), ylim=c(-1,1), cex=0.4, lwd=2, xlab="x", ylab="y")
      horiz.color.bar(rainbow(120)[71:1], 0, halomax)
    }
    plotEx(T[c(1,2),], T[3,], T[4,], "transposons")
    plotEx(T[c(1,2),], T[5,], T[4,], "fitness", halomax=1)

    dev.off()
    write(paste("done generation ", generation), stderr())
    out_counter <- out_counter +1
  }
}
#make_map_plot('mapdata-phenotype_map_RED-', 'plot-', 9, "map phenotype: RED")
#make_map_plot('mapdata-phenotype_map_GREEN-', 'plot-', 10, "map phenotype: GREEN")
#make_map_plot('mapdata-phenotype_map_BLUE-', 'plot-', 11, "map phenotype: BLUE")
#make_map_plot('mapdata-alive_locations-', 'plot-', 9)
