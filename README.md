# PNGaseA Analysis Scripts

This repository contains R scripts and processed datasets used to generate Figures 4 and 5 of:

Wei et al., "A bifidobacterial PNGase A structure suggests a role in parasite glycoprotein degradation"

## Data availability

Raw RNA-seq data: GEO GSE315009  
Crystal structure: PDB 9VLA  

## Requirements

R >= 4.2.0  
Packages:
- DESeq2
- ggplot2
- pheatmap
- ape
- ggtree
- tidyverse

Python 3.13.11 
Packages:
- Biopython ≥ 1.85

## Scripts

1. Fig4_DE_analysis.R
2. Fig4_volcano_plot.R
3. Fig5_heatmap.py


## Sequence datasets (FASTA)

The following multifasta (.faa) files were used for phylogenetic analysis of PNGase A–type enzymes:

1. all_199_PNGase_sequences.faa  
   → Core dataset of 199 representative PNGase A–type sequences used for primary phylogenetic inference.
2. all_199_PNGase_sequences_plus_single_outgroup.faa  
   → Core dataset supplemented with one structurally defined outgroup for rooting analysis.
3. all_199_PNGase_sequences_plus_two_outgroups.faa  
   → Core dataset supplemented with two independent outgroups to assess root robustness.

All sequences were retrieved from the NCBI non-redundant database, filtered for length and redundancy, and trimmed to the conserved catalytic core prior to phylogenetic analysis, as described in the Methods section.