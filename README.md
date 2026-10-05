# phyloBARCODER
A web tool for species identification of metabarcoding DNA sequences through phylogenetic tree estimation. The analysis pages provide the following marker and reference database options: **Mitochondrial genes** uses MIDORI2 references from metazoans (animals); **SSU rRNA / PR2** uses PR2 references, mainly eukaryotic 18S rRNA. PR2 focuses on protists and also includes animals, fungi and plants. **rbcL** uses the Bell plant chloroplast reference library; **Fungi** supports ITS1 and ITS2 with UNITE references, and LSU rRNA with SILVA references covering eukaryotes, bacteria and archaea. The PR2, rbcL and Fungi tools are available as public beta tools; validation results and bug reports are welcome.


---

> **🆕 New (5 October 2026): Tree Identification and Sequence Extraction for SSU rRNA (PR2), plant rbcL, and fungal ITS1/ITS2 (UNITE) and LSU rRNA (SILVA) are now available as public beta tools. Validation results and bug reports are welcome.**
[SSU rRNA Tree](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_protists.html) · [SSU rRNA Extraction](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_protists.html) · [rbcL Tree and example](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_rbcl.html) · [rbcL Extraction](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_rbcl.html) · [Fungi Tree](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_unite.html) · [Fungi Extraction](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_unite.html) · [BLAST Identification](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_blast.html) · [Instructions](https://fish-evol.org/phylobarcoder_instruction/index.html)


## Analysis tools

| Marker / reference database | yurai-CGI<br>Tree Identification | yurai-CGI<br>Sequence Extraction | viento-Flask<br>Tree Identification |
| --- | --- | --- | --- |
| **Mitochondrial genes** | [Tree](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index.html)<br>Since 11 May 2025 | [Extraction](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction.html) | [Tree](https://orthoscope.jp/phylobarcoder/)<br>Since 3 September 2025 |
| **SSU rRNA / PR2**<br>Public beta · 4 October 2026 | [Tree](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_protists.html) | [Extraction](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_protists.html) | — |
| **rbcL / Plants**<br>Public beta · 4 October 2026 | [Tree](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_rbcl.html) | [Extraction](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_rbcl.html) | — |
| **Fungi: ITS1 / ITS2 / LSU**<br>UNITE / SILVA<br>Public beta · 5 October 2026 | [Tree](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_unite.html) | [Extraction](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_unite.html) | — |

On both Fungi pages, select **ITS1**, **ITS2** or **LSU rRNA**. LSU uses **SILVA 138.2 Parc** or **Ref NR99**, with **LSU / Parc as the default**. Both databases retain all biological domains. A published 27-OTU decaying-wood eDNA example is included ([Shirouzu et al. 2020](https://doi.org/10.1038/s41598-020-59620-0), Figs. 2 and 3; Matsuoka 2022, p. 221, Fig. 3). [Compare the Parc and Ref NR99 trees and sequence matches](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/silva_LSU_comparison.html).

**Similarity search:** [BLAST Identification (yurai-CGI)](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_blast.html)


---
## Instruction　　　
English   
[https://fish-evol.org/phylobarcoder_instruction](https://fish-evol.org/phylobarcoder_instruction)   
Japanese   
[https://fish-evol.org/phylobarcoder_instruction/indexJPN.html](https://fish-evol.org/phylobarcoder_instruction/indexJPN.html)   

---
## Source code availability
 
The source code is not publicly available.
 
Source code may be provided upon reasonable request to the author.


---
## Citation
Inoue J. et al. 
phyloBARCODER: An web tool for phylogenetic classification of eukaryote metabarcodes using custom reference databases. Molecular Biology and Evolution, in press. [Link](https://academic.oup.com/mbe/advance-article/doi/10.1093/molbev/msae111/7689935?utm_source=advanceaccess&utm_campaign=mbe&utm_medium=email).   

---
## Contact 
Email: [_jinoueATg.ecc.u-tokyo.ac.jp_](http://www.fish-evol.org/index_eng.html)
<br />  
