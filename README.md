# phyloBARCODER
A web tool for species identification of metabarcoding DNA sequences through phylogenetic tree estimation. The analysis pages provide the following marker and reference database options: **Mitochondrial genes** uses MIDORI2 references from metazoans (animals); **SSU rRNA / PR2** uses PR2 references, mainly eukaryotic 18S rRNA. PR2 focuses on protists and also includes animals, fungi and plants. **rbcL** uses the Bell plant chloroplast reference library; **Fungi** supports ITS1 and ITS2 with UNITE references, and LSU rRNA with SILVA references covering eukaryotes, bacteria and archaea. The PR2, rbcL and Fungi tools are available as public beta tools; validation results and bug reports are welcome.


---

> **🆕 New (5 October 2026): Tree Identification and Sequence Extraction for SSU rRNA (PR2), plant rbcL, and fungal ITS1/ITS2 (UNITE) and LSU rRNA (SILVA) are now available as public beta tools. Validation results and bug reports are welcome.**
[SSU rRNA Tree](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_protists.html) · [SSU rRNA Extraction](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_protists.html) · [rbcL Tree and example](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_rbcl.html) · [rbcL Extraction](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_rbcl.html) · [Fungi Tree](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_unite.html) · [Fungi Extraction](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_unite.html) · [BLAST Identification](https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_blast.html) · [Instructions](https://fish-evol.org/phylobarcoder_instruction/index.html)


## Analysis tools

yurai-CGI and viento-Flask provide mirror access to mitochondrial Tree Identification. Additional tools currently available on each site are shown below.

<table>
  <thead>
    <tr>
      <th rowspan="2">Marker / reference database</th>
      <th colspan="2">yurai-CGI</th>
      <th>viento-Flask</th>
    </tr>
    <tr>
      <th>Tree Identification</th>
      <th>Sequence Extraction</th>
      <th>Tree Identification</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Mitochondrial genes</strong></td>
      <td><a href="https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index.html">Tree</a><br>Since 11 May 2025</td>
      <td><a href="https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction.html">Extraction</a></td>
      <td><a href="https://orthoscope.jp/phylobarcoder/">Tree</a><br>Since 3 September 2025</td>
    </tr>
    <tr>
      <td><strong>SSU rRNA / PR2</strong><br>Public beta · 4 October 2026</td>
      <td><a href="https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_protists.html">Tree</a></td>
      <td><a href="https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_protists.html">Extraction</a></td>
      <td>—</td>
    </tr>
    <tr>
      <td><strong>rbcL / Plants</strong><br>Public beta · 4 October 2026</td>
      <td><a href="https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_rbcl.html">Tree</a></td>
      <td><a href="https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_rbcl.html">Extraction</a></td>
      <td>—</td>
    </tr>
    <tr>
      <td><strong>Fungi: ITS1 / ITS2 / LSU</strong><br>UNITE / SILVA<br>Public beta · 5 October 2026</td>
      <td><a href="https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_tree_unite.html">Tree</a></td>
      <td><a href="https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_seqExtraction_unite.html">Extraction</a></td>
      <td>—</td>
    </tr>
    <tr>
      <td></td>
      <td colspan="2"><strong>Similarity search:</strong> <a href="https://yurai.aori.u-tokyo.ac.jp/phylobarcoder/index_blast.html">BLAST Identification (yurai-CGI)</a></td>
      <td>—</td>
    </tr>
  </tbody>
</table>



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
