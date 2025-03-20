# RNA_seq_fungal_genomes
Repository of extracting RNA seq data from several fungal genomes 

## Dataset
**FungiExp**:
- https://doi.org/10.1093/bioinformatics/btad042
- https://bioinfo.njau.edu.cn/fungiExp

### How to extract GeneExpression data from FungiExp

1. Open <code>gene_expression_extraction_fungiexp.py</code>
2. Within the file
```
# Define Taxon ID and Base URL
taxon_id = "245562"
base_url = "https://bioinfo.njau.edu.cn/fungiExp/"
```

Change the <code>taxon_id</code> based on the taxon id at the end of the link `https://bioinfo.njau.edu.cn/fungiExp/info.php?taxonId={taxon_id}`


3. Run <code>gene_expression_extraction_fungiexp.py</code>

4. This will create a new directory named the same as the <code>taxon_id</code> -->  This will automatically download all the Gene expression .tsv file and will be placed into the new created directory.


### Filtering FungiExp Data based on TPM and RSD/CV
This part of the code processess FungiExp TPM data, filter based on TPM and RSD values and generates plots for analysis.

#### Files
In the **code** directory:

- <code>Filter_FungiExp_TPM_RSD.py</code>: Main script to process + produce plots for FungiExp data
- <code>tpm_rsd_functions.py</code>: Contains helper functions used in <code>Filter_FungiExp_TPM_RSD.py</code> for filtering, transforming, plotting data.

#### Usage 

1. **Prepare your data**:
    - Place your FungiExp folders in the `fungiexp_data` directory. There are currently some folders there for trial but add or move the directories there. 
    - Ensure you have the mapping file `output_with_species.csv` with `Taxon_ID` and `Species_name` columns.   

2. **Run the main script**:

    - Go to the code directory and run the command below:
    <code>python Filter_FungiExp_TPM_RSD.py</code>

3. **Output**:

    - Filtered and transformed data saved as .tsv files 
    - Plots saved as a PNG files in the `output_files_species_fungiexp` directory.

**tpm_rsd_functions.py**:
- Functions:
    - <code>rsd(x)</code>: Calculate relative standard deviation. 
    - <code>filter_tpm_rsd_dataset(dataset, tpm_threshold, rsd_threshold)</code>: Filter dataset based on TPM and RSD thresholds. 
    - <code>filter_tpm_rsd_dataset_geneId(dataset, tpm_threshold, rsd_threshold)</code>: Filter dataset and maintain order. 
    - <code>transform_tpm(dataset)</code>: Transform TPM values using Box-cox and Yeo-Johnson transformations.
    - <code>plot_transformed(dataset, title, save_path)</code>L Plot transformed TPM values and save the plot 

