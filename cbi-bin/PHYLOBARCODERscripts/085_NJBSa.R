library(ape)

args            <- commandArgs()
infile          <- args[6]
outGroup        <- args[7]
selectedModel   <- args[8]
num_bootstrap   <- args[9]
outfile.nwk     <- args[10]
#outfile.leaves.txt <- paste(outfile.nwk, '.leaves.txt', sep = '')

#print ('  ## 085_NJBSa.R starts.')
#print('infile')
#print(infile)
#print("")
#print('outGroup')
#print(outGroup)
#print("")
#print('selectedModel')
#print(selectedModel)
#print("")
#print("num_bootstrap")
#print(num_bootstrap)
#print("")
#q()


#print(outfile.nwk)
#print("")

#  print (paste('  infile', infile))


## Open the 'infile' file
if(file.access(infile) != 0){
  print (paste(infile,' does not exist.'))
} else {
  infile.phy  <- read.dna(infile, format = "fasta")
}

## Estimate distance
dist.selectedModel <- dist.dna(infile.phy, model = selectedModel, pairwise.deletion=TRUE, gamma=5)

## #Estimate NJ tree
nj.selectedModel <- njs(dist.selectedModel)

## Reroot by outGroup
nj.selectedModel <- root(nj.selectedModel,outGroup,r=T)

## ladderize from bottom
#nj.selectedModel <- ladderize(nj.selectedModel,TRUE)
nj.selectedModel <- ladderize(nj.selectedModel,FALSE)
if (num_bootstrap < 1){
    write.tree(nj.selectedModel, file = outfile.nwk)
    q()
}

## BS analysis with partitioning data (1st+2nd)
###nj.boot.nj.selectedModel <- boot.phylo(nj.selectedModel, infile.phy,     function(xx) root(nj(dist.dna(xx, model = "selectedModel", pairwise.deletion = TRUE, gamma = 5)),outGroup,r=T), 100, 2)
###nj.boot.nj.selectedModel <- boot.phylo(nj.selectedModel, infile.phy,     function(xx) root(njs(dist.dna(xx, model = "selectedModel", pairwise.deletion = TRUE)), outGroup,r=T), 100, 2)
nj.boot.nj.selectedModel <- boot.phylo(nj.selectedModel, infile.phy,     function(xx) root(njs(dist.dna(xx, model = selectedModel, pairwise.deletion = TRUE)), outGroup,r=T), 100)
nj.selectedModel$node.label <- nj.boot.nj.selectedModel

## Change bs calues: NA -> 0
print("## before Change bs values: NA -> 0")
for(p in 1:length(nj.selectedModel$node.label)){
  print(p)
  print(nj.selectedModel$node.label[p])
  print("")
}
#cat('\n\n')

nj.selectedModel$node.label[is.na(nj.selectedModel$node.label)]<-0

print("## after Change bs values: NA -> 0")
for(p in 1:length(nj.selectedModel$node.label)){
  print(p)
  print(nj.selectedModel$node.label[p])
  print("")
}

#cat('\n')

## Write tree
write.tree(nj.selectedModel, file = outfile.nwk)

