#Load data
setwd("C:\\Users\\Miguel\\Dropbox\\Caltech_2015-2016\\Spring\\EE_145\\discovr_code\\pair_data")
act = read.csv("output_pairs20160503-224536.txt",header=FALSE)
names(act)<-c("primary","secondary","matches")

#normalize
act=act[order(act$primary,act$secondary),]
num_pair=numeric()
for(activity in unique(act$primary))
{
  num_pair=append(num_pair,length(which(act$primary==activity)))
}
act.counts=act[which(act$primary==act$secondary),]$matches

act.counts=rep(act.counts,num_pair)

act.matrix=as.matrix(as.numeric(act$matches))

act.norm=sweep(act.matrix,1,act.counts,"/")

act$normalized<-act.norm

#only take top 20 activities (in order)
act.unique=act[which(act$primary==act$secondary & is.finite(act$normalized)),]
act.unique.sort=act.unique[order(-act.unique$matches),]
act.short.names=factor(head(act.unique.sort,20)$primary)
act.short=act[which(is.element(act$primary,act.short.names) & is.element(act$secondary,act.short.names)),]
act.short$primary<-factor(act.short$primary)
act.short$secondary<-factor(act.short$secondary)

#get desired form
act.corr=xtabs(act.short$normalized ~ act.short$primary + act.short$secondary, act.short)

#plot
library(corrplot)

#M <- cor(act.corr)
custom_col=colorRampPalette(c("white","white","red"))
corrplot(act.corr,method="color",order="FPC",tl.srt=90,cl.lim=c(0,1),tl.cex=1)
  
