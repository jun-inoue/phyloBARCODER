# phyloBARCODER
A web tool for species identification of metabarcoding DNA sequences through phylogenetic tree estimation. Version 1 stores a database comprising all eukaryotic mitochondrial gene sequences. 


---

## New: Online BLAST species identification
phyloBARCODER now supports online BLAST searches against
MIDORI2 GB265 LONGEST, covering 15 metazoan mitochondrial genes.
Paste eDNA or metabarcoding sequences in FASTA format to obtain
up to three matches per query and download the results as CSV.
No installation or sign-in is required for BLAST searches.

[Run BLAST](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_blast.html)
· [Instructions](https://fish-evol.org/phylobarcoder_instruction/index.html)


## Analysis site   
yurai (CGI) - fast   
[https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/)   
(from 11 May 2025)   

viento (FLASK)  
[viento (FLASK)](https://orthoscope.jp/phylobarcoder/)　　　     
(from 3 Sep. 2025)   


---
## Instruction　　　
English   
[https://fish-evol.org/phylobarcoder_instruction](https://fish-evol.org/phylobarcoder_instruction)   
Japanese   
[https://fish-evol.org/phylobarcoder_instruction/indexJPN.html](https://fish-evol.org/phylobarcoder_instruction/indexJPN.html)   

---
## Programming code　　　
The programming code is accessible from [Releases](https://github.com/jun-inoue/phyloBARCODER/releases). Users install phyloBARCODER set up servers as follows:
- save downloaded html and cgi-bin directories in /var/www/.
- install R and a package, [ape](https://github.com/emmanuelparadis/ape?tab=readme-ov-file).
- save dowlonaded dependencies (Rscript, BLASTN, BLASTDBCMD, MAKEBLASTDB, MAFFT, and TRIMAL) in the /cgi-bin/PHYLOBARCODERscripts directory.   

Those scripts were confirmed to run on the Linux operating system with an Apache HTTP Server Server.   


---
## Citation
Inoue J. et al. 
phyloBARCODER: An web tool for phylogenetic classification of eukaryote metabarcodes using custom reference databases. Molecular Biology and Evolution, in press. [Link](https://academic.oup.com/mbe/advance-article/doi/10.1093/molbev/msae111/7689935?utm_source=advanceaccess&utm_campaign=mbe&utm_medium=email).   

---
## Contact 
Email: [_jinoueATg.ecc.u-tokyo.ac.jp_](http://www.fish-evol.org/index_eng.html)
<br />  
