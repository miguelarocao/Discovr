#Load data
setwd("C:\\Users\\Miguel\\Dropbox\\Caltech_2015-2016\\Spring\\EE_145\\discovr_code\\pair_data")
act = read.csv("output_pairs20160425-192014.txt",header=FALSE)
names(act)<-c("activity_1","activity_2","matches")

#normalize
act=act[order(act$activity_1,act$activity_2),]
num_pair=numeric()
for(activity in unique(act$activity_1))
{
  num_pair=append(num_pair,length(which(act$activity_1==activity)))
}
act.counts=act[which(act$activity_1==act$activity_2),]$matches
act.counts=rep(act.counts,num_pair)

act.matrix=as.matrix(as.numeric(act$matches))

act.norm=sweep(act.matrix,1,act.counts,"/")

act$normalized<-act.norm

#only take top 20 activities
act.unique=act[which(act$activity_1==act$activity_2 & is.finite(act$normalized)),]
act.unique.sort=act.unique[order(-act.unique$matches),]
act.short.names=factor(head(act.unique.sort,20)$activity_1)
act.short=act[which(is.element(act$activity_1,act.short.names) & is.element(act$activity_2,act.short.names)),]
act.short$activity_1<-factor(act.short$activity_1)
act.short$activity_2<-factor(act.short$activity_2)

#get desired form
act.corr=xtabs(act.short$normalized ~ act.short$activity_1 + act.short$activity_2, act.short)

#plot
library(corrplot)

M <- cor(act.corr)
corrplot(M,method="color",type="upper",tl.srt=45)
  
