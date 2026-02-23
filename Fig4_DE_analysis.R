# ==========================================================
# edgeR Differential Expression
# PNGaseDJ vs DJ101A
# PNGaseF  vs DJ101A
# Single-replicate design (fixed BCV)
# ==========================================================

library(edgeR)

# -------------------------------
# Read featureCounts output
# -------------------------------
counts <- read.delim("gene_counts_3cond.txt",
                     comment.char = "#",
                     stringsAsFactors = FALSE)

count_matrix <- counts[, 7:9]
rownames(count_matrix) <- counts$Geneid
colnames(count_matrix) <- c("DJ101A", "PNGaseDJ", "PNGaseF")

# -------------------------------
# Build DGE object
# -------------------------------
group <- factor(c("DJ101A", "PNGaseDJ", "PNGaseF"))

dge <- DGEList(counts = count_matrix, group = group)

# Filter low-expression genes
keep <- filterByExpr(dge)
dge <- dge[keep, , keep.lib.sizes = FALSE]

# Normalize
dge <- calcNormFactors(dge)

# -------------------------------
# Assign fixed dispersion
# BCV = 0.3 (typical whole-animal RNA-seq)
# -------------------------------
dge$common.dispersion <- 0.3^2

# -------------------------------
# Differential tests
# -------------------------------

# PNGaseDJ vs DJ101A
et_DJ <- exactTest(dge, pair = c("DJ101A", "PNGaseDJ"))
res_DJ <- topTags(et_DJ, n = Inf)$table
res_DJ$GeneID <- rownames(res_DJ)

# PNGaseF vs DJ101A
et_F <- exactTest(dge, pair = c("DJ101A", "PNGaseF"))
res_F <- topTags(et_F, n = Inf)$table
res_F$GeneID <- rownames(res_F)

# -------------------------------
# Export results
# -------------------------------
write.csv(res_DJ,
          "DE_PNGaseDJ_vs_DJ101A.csv",
          row.names = FALSE)

write.csv(res_F,
          "DE_PNGaseF_vs_DJ101A.csv",
          row.names = FALSE)

cat("DE analysis complete.\n")
cat("Files generated:\n")
cat(" - DE_PNGaseDJ_vs_DJ101A.csv\n")
cat(" - DE_PNGaseF_vs_DJ101A.csv\n")
