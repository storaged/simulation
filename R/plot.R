
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

T <- as.matrix(read.table("results.table"))

T <- clamp(T, 1000)

M <- persp(1:dim(T)[1], 1:dim(T)[2], T, phi = 10, theta = 30, col="lightblue", ltheta=-90, lphi=60, xlab="Environmental stress", ylab="Generation", zlab="Inactive transposons")

for (idx in 1:dim(T)[1]) 
{
v <- T[idx,1:dim(T)[2]];
lines(trans3d(idx, 1:dim(T)[2], v, M), col = "black")
}

