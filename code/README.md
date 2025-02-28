## Assessing GEO vs FungiExp 
The aim of this is to check if the TPM values in FungiExp align closely with the RPKM of the GEO dataset or a TPM value from your RNA-seq pipeline. This is achieved through looking at the correlation

#### Why log transform?
When working with gene expression data (such as RPKM, TPM, or FPKM), the distribution of expression levels is typically highly skewed, with many genes having very low expression counts and a few genes having very high counts.

**Taking a log transform helps in several ways:**

- Normalizes the Scale: By applying a log transform, extreme high values are compressed, and smaller values are spread out a bit more. This makes it easier to see variations across the entire range of expression levels.
- Reduces Skewness: Gene expression data often spans multiple orders of magnitude. The log transform can produce a distribution that is closer to normal (Gaussian), allowing for more robust statistical analyses and clearer visual patterns.

#### Interpreation 
- A high correlation (close to 1.0) means RPKM and TPM track closely.
- Because of differences in how RPKM and TPM are calculated, it’s normal  for their magnitudes to differ, but they should still be highly correlated.
