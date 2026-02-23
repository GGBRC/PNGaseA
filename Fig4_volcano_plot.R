# ==========================================================
# Nature-quality Volcano Plot
# PNGaseDJ vs DJ101A
# True edgeR FDR
# Arial | SVG | RGB | Publication-ready
# ==========================================================

library(ggplot2)
library(dplyr)
library(ggrepel)

# -------------------------------
# Load DE results with gene symbols
# -------------------------------
df <- read.csv("DE_PNGaseDJ_vs_DJ101A.csv", stringsAsFactors = FALSE)

# If you saved res_DJ2 with gene symbols, load that instead:
# df <- read.csv("DE_PNGaseDJ_vs_DJ101A_annotated.csv")

# If symbols already merged:
if ("external_gene_name" %in% colnames(df)) {
    df$gene_symbol <- df$external_gene_name
} else {
    df$gene_symbol <- df$GeneID
}

df <- df %>%
    mutate(
        negLogFDR = -log10(FDR)
    )

# -------------------------------
# Thresholds
# -------------------------------
lfc_cut <- 1
fdr_cut <- 0.05

df <- df %>%
    mutate(
        category = case_when(
            FDR < fdr_cut & logFC >  lfc_cut ~ "Up",
            FDR < fdr_cut & logFC < -lfc_cut ~ "Down",
            TRUE ~ "NS"
        )
    )

# -------------------------------
# Translation machinery genes
# -------------------------------
translation_patterns <- c("^rpl-", "^rps-", "^eif-", "^eef-", "^mrpl-", "^mrps-")

df$translation_gene <- grepl(
    paste(translation_patterns, collapse="|"),
    df$gene_symbol,
    ignore.case = TRUE
)

# -------------------------------
# Color palette (Nature-safe)
# -------------------------------
neutral_grey <- "grey85"
up_color     <- "#3B7EA1"   # muted blue
down_color   <- "#C23B22"   # muted red (color-blind safe)

# -------------------------------
# Plot
# -------------------------------
p <- ggplot(df, aes(x = logFC, y = negLogFDR)) +

    # Non-significant
    geom_point(
        data = subset(df, category=="NS"),
        color = neutral_grey,
        size = 1.2
    ) +

    # Upregulated
    geom_point(
        data = subset(df, category=="Up"),
        color = up_color,
        size = 1.6,
        alpha = 0.85
    ) +

    # Downregulated
    geom_point(
        data = subset(df, category=="Down"),
        color = down_color,
        size = 1.6,
        alpha = 0.85
    ) +

    # Highlight significant translation genes
    geom_point(
        data = subset(df, translation_gene & FDR < fdr_cut),
        shape = 21,
        fill = "black",
        color = "white",
        size = 2.5,
        stroke = 0.4
    ) +

    # Threshold lines
    geom_vline(
        xintercept = c(-lfc_cut, lfc_cut),
        linetype = "dashed",
        color = "grey50",
        linewidth = 0.4
    ) +

    geom_hline(
        yintercept = -log10(fdr_cut),
        linetype = "dashed",
        color = "grey50",
        linewidth = 0.4
    ) +

    labs(
        x = "log2 Fold Change (PNGaseDJ vs DJ101A)",
        y = expression(-log[10]("FDR"))
    ) +

    theme_classic(base_family = "Arial") +

    theme(
        text = element_text(size = 10),
        axis.title = element_text(size = 12),
        axis.text  = element_text(size = 10),
        legend.position = "none"
    )

# -------------------------------
# Label top translation hits
# -------------------------------
top_translation <- df %>%
    filter(translation_gene & FDR < fdr_cut) %>%
    arrange(FDR) %>%
    head(6)

p <- p +
    geom_text_repel(
        data = top_translation,
        aes(label = gene_symbol),
        size = 3,
        family = "Arial",
        box.padding = 0.3,
        segment.size = 0.3,
        max.overlaps = 20
    )

# -------------------------------
# Export as SVG (Nature compliant)
# -------------------------------
ggsave(
    "Figure4b_Volcano_PNGaseDJ_FINAL.svg",
    plot = p,
    width = 6,
    height = 5
)

cat("Nature-ready volcano SVG generated.\n")
