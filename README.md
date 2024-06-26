# phyloBARCODER
phyloBARCODER is a web tool for species identification of metabarcoding DNA sequences by estimating phylogenetic trees. Version 1 stores a database comprising all eukaryotic mitochondrial gene sequences. 


---

## Analysis site   
viento - fast   
[https://orthoscope.jp/phylobarcoder/](https://orthoscope.jp/phylobarcoder/)      
(from 19 Oct. 2023)

osaka   
[http://133.167.86.72/phylobarcoder/](http://133.167.86.72/phylobarcoder/)   
(from 21 Jan. 2024) 

---
## Instruction　　　
English [https://fish-evol.org/phylobarcoder_instruction](https://fish-evol.org/phylobarcoder_instruction)   
Japanese [https://fish-evol.org/phylobarcoder_instructionJPN](https://fish-evol.org/phylobarcoder_instructionJPN)   

---
## Installation　　　
If users install phyloBARCODER on your own web server, download Source code from [Releases](https://github.com/jun-inoue/phyloBARCODER/releases) and set up the server as follows:
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
