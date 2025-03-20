import numpy as np
from scipy import stats
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

# Function to calculate relative standard deviation (RSD)
def rsd(x): 
    return x.std() / x.mean()

# Function to filter dataset based on TPM and RSD thresholds
def filter_tpm_rsd_dataset(dataset, tpm_threshold, rsd_threshold):
    gene_stats = dataset.query('TPM > 0').groupby('geneId').agg({'TPM': ['sum', 'mean', 'median', 'std', rsd]})
    ge_data_tpm_median = dataset.query('TPM > {}'.format(tpm_threshold)).groupby("geneId").agg({'TPM': 'median'}).reset_index() # Filter genes with TPM > tpm_threshold and get the median TPM per gene
    valid_gene_ids = gene_stats["TPM"].query('rsd < {}'.format(rsd_threshold)).index  # Keep only genes whose RSD (from gene_stats) is below the rsd_threshold
    ge_data_tpm_median_rsd = ge_data_tpm_median[ge_data_tpm_median["geneId"].isin(valid_gene_ids)]
    return ge_data_tpm_median_rsd

# Function to filter dataset based on TPM and RSD thresholds and maintain order
def filter_tpm_rsd_dataset_geneId(dataset, tpm_threshold, rsd_threshold):
    gene_stats = dataset.query('TPM > 0').groupby(['geneId']).agg({'TPM' :['sum', 'mean', 'median', 'std', rsd]})
    ge_data_tpm_median = dataset.query('TPM > {}'.format(tpm_threshold)).groupby("geneId").agg({'TPM': 'median'}).reset_index()
    ge_data_tpm_median_rsd = ge_data_tpm_median[ge_data_tpm_median["geneId"].isin(gene_stats["TPM"].query('rsd < {}'.format(rsd_threshold)).index)]
    ge_data_tpm_median_rsd = ge_data_tpm_median_rsd.sort_values(by="TPM", ascending=True)
    sorted_kept_geneIds = ge_data_tpm_median_rsd["geneId"].tolist()
    filtered_dataset = dataset[dataset["geneId"].isin(sorted_kept_geneIds)].copy()
    filtered_dataset["geneId"] = pd.Categorical(filtered_dataset["geneId"], categories=sorted_kept_geneIds, ordered=True)
    filtered_dataset = filtered_dataset.sort_values(by="geneId")

    return filtered_dataset

# Function to transform TPM values using Box-Cox and Yeo-Johnson transformations
def transform_tpm(dataset):
    # Box-Cox transformation (requires positive values; our filtering ensures TPM>0)
    try:
        boxcox_tpm, bc_lmbda = stats.boxcox(dataset["TPM"])
        dataset["boxcox_tpm"] = boxcox_tpm
        dataset["bc_lmbda"] = bc_lmbda
    except Exception as e:
        dataset["boxcox_tpm"] = np.nan
        dataset["bc_lmbda"] = np.nan

    # Yeo-Johnson transformation
    try:
        yj_tpm, yj_lmbda = stats.yeojohnson(dataset["TPM"])
        dataset["yj_tpm"] = yj_tpm
        dataset["yj_lmbda"] = yj_lmbda
    except Exception as e:
        dataset["yj_tpm"] = np.nan
        dataset["yj_lmbda"] = np.nan
        
    return dataset

# Function to plot transformed TPM values and save the plot
def plot_transformed(dataset, title, save_path=None):
    # Save the transformed dataset as a TSV if a save path is provided.
    if save_path is not None:
        dataset.to_csv(save_path, sep="\t", index=False)
    fig, axes = plt.subplots(1, 4, figsize=(15, 6), sharex=False, sharey=False)
    sns.set_theme()
    sns.histplot(ax=axes[0], x="TPM", data=dataset).set(xlabel="TPM")
    sns.histplot(ax=axes[1], x="TPM", data=dataset, log_scale=True).set(xlabel="TPM log scale")
    sns.histplot(ax=axes[2], x="boxcox_tpm", data=dataset).set(xlabel="Boxcox transformed TPM")
    sns.histplot(ax=axes[3], x="yj_tpm", data=dataset).set(xlabel="Yeo Johnson transformed TPM")
    fig.suptitle('Dataset size: {}, {}'.format(dataset.shape[0], title))
    
    if save_path is not None:
        fig.savefig(save_path.replace(".tsv", ".png"), dpi=300)

# -------------------------