# Additional Bioconductor Packages
source("http://bioconductor.org/biocLite.R") 
biocLite(c("AnnotationDbi", "impute", "GO.db", 
	"preprocessCore", "org.Hs.eg.db")) 
install.packages("WGCNA")

# Graph related packages
install.packages("igraph")

# 0MQ for message passing
install.packages("rzmq")