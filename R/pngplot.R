library("fields")
clamp <- function(X, cval)
{
   for (i in 1:(dim(X)[1]))
   {
       for (j in 1:(dim(X)[2]))
       {
	   if ((!is.nan(X[i, j])) && X[i, j] > cval)
	   {
	   	X[i, j] = NaN
	   }
	}
    }
    print(max(X, na.rm=TRUE));
    return(X);
}

clamp2 <- function(X)
{
   for (i in 1:(dim(X)[1]))
   {
       for (j in 1:(dim(X)[2]))
       {
       		if((!is.nan(X[i, j])) && X[i, j] > 0)
	   	{
			X[i, j] = log2(X[i, j])
		}
	}
    }
    print(max(X, na.rm=TRUE));
    return(X);
}

T <- as.matrix(read.table("results.table"))

T <- clamp2(T)


imp <- `body<-`(image.plot,value=`[[<-`(body(image.plot),28,

    quote({par(big.par)

          par(plt = big.par$plt, xpd = TRUE)
          par(mfg = mfg.save, new = FALSE)
          invisible()})))


png(file = "plot.png", width = 1000, height = 1000, pointsize = 30);
#x11()
ticks <- 2^(1:20);

xpl <- c("None", "High");
imp(1:(dim(T)[1]), 1:(dim(T)[2])*100, T, xlab="Environmental stress level", ylab="Generation", axis.args=list(labels = ticks, at=log2(ticks)), axes=FALSE);
box()
axis(2)
axis(1, at=c(1,100), labels=c("None", "High"))
c <- 0
#Sys.sleep(10)
