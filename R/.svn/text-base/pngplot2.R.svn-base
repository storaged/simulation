library("fields")
clamp <- function(X, cval)
{
   return(X);
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
   return(X)
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

options(scipen=10)
png(file = "plot.png", width = 1500, height = 1500, pointsize = 30);
#x11()
ticks <- 2^(1:20/10);

xpl <- c("None", "High");
imp(1:(dim(T)[1]), 1:(dim(T)[2]), T, xlab="Environmental stress level", ylab="Generation", axes=FALSE);
box()
axis(2)
axis(1, at=c(1,100), labels=c("None", "High"))
c <- 0
#Sys.sleep(10)
