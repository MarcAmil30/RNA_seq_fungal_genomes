import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.metrics import r2_score


# ------------------------------------------------------------------------------
# 1) Importing the data and matching common geneIds
# ------------------------------------------------------------------------------

directory_geo_fungiexp = "./22_2_25_GEO_fungiexp_test"
txt_file_path = f"{directory_geo_fungiexp}/YL1_GSM3914229_WT-RNA.txt"
tsv_file_path = f"{directory_geo_fungiexp}/YL1_WT_SRX6386859.gene.expr.tsv"

df_txt = pd.read_csv(txt_file_path, sep="\t")
df_txt = df_txt.rename(columns={"GeneName": "geneId"}) #rename column to match the TSV file
df_tsv = pd.read_csv(tsv_file_path, sep="\t")

df_tsv["geneId"] = df_tsv["geneId"].str.replace("_", "", regex=False) # Remove underscores from 'geneId' column in the TSV file
merged_df = pd.merge(df_txt, df_tsv, on="geneId", how="inner") # Merge the DataFrames on the 'geneId' column, keeping only matching rows

# Remove any rows where RPKM or TPM is missing or zero (to avoid log issues)
merged_df = merged_df.dropna(subset=["RPKM", "TPM"])
merged_df = merged_df[(merged_df["RPKM"] > 0) & (merged_df["TPM"] > 0)]
print(merged_df.shape)


# ------------------------------------------------------------------------------
# 2) Compute R2 for the TPM values 
# ------------------------------------------------------------------------------

r2 = r2_score(merged_df["RPKM"], merged_df["TPM"])
# Compute Pearson correlation
corr_pearson = merged_df[["RPKM", "TPM"]].corr(method='pearson').iloc[0,1]
# Compute Spearman correlation
corr_spearman = merged_df[["RPKM", "TPM"]].corr(method='spearman').iloc[0,1]
print(f"\nPearson correlation between RPKM and TPM: {corr_pearson:.4f}")
print(f"Spearman correlation between RPKM and TPM: {corr_spearman:.4f}")
print(f"R² score between RPKM and TPM: {r2:.4f}")



# ------------------------------------------------------------------------------
# 3) VISUALIZE THE RELATIONSHIP (Scatter Plots)
# ------------------------------------------------------------------------------
sns.set_style("whitegrid")

# (A) RAW VALUES
plt.figure(figsize=(6, 4))
sns.scatterplot(data=merged_df, x="RPKM", y="TPM", alpha=0.6)
sns.regplot(data=merged_df, x="RPKM", y="TPM", scatter=False, line_kws={"color": "red", "linestyle": "dashed"})
r2_raw = r2_score(merged_df["RPKM"], merged_df["TPM"])
plt.title(f"Raw RPKM vs. TPM Scatter Plot\nR² = {r2_raw:.4f}", fontsize=14)
plt.xlabel("RPKM", fontsize=12)
plt.ylabel("TPM", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.gca().spines['bottom'].set_linewidth(2)
plt.gca().spines['left'].set_linewidth(2)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()
plt.grid(False)
plt.show()

# (B) LOG-SCALED VALUES
# Adding 1 to avoid log(0) if any values are extremely small or zero.
merged_df["log_RPKM"] = np.log2(merged_df["RPKM"] + 1)
merged_df["log_TPM"] = np.log2(merged_df["TPM"] + 1)

plt.figure(figsize=(6, 4))
sns.scatterplot(data=merged_df, x="log_RPKM", y="log_TPM", alpha=0.6)
sns.regplot(data=merged_df, x="log_RPKM", y="log_TPM", scatter=False, line_kws={"color": "red", "linestyle": "dashed"})
r2_log = r2_score(merged_df["log_RPKM"], merged_df["log_TPM"])
plt.title(f"Log2(RPKM + 1) vs. Log2(TPM + 1) with Regression Line\nR² = {r2_log:.4f}", fontsize=14)
plt.xlabel("log2(RPKM + 1)", fontsize=12)
plt.ylabel("log2(TPM + 1)", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.gca().spines['bottom'].set_linewidth(2)
plt.gca().spines['left'].set_linewidth(2)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()
plt.grid(False)
plt.show()



