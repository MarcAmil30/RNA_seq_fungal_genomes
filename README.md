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

Change the <code>taxon_id</code> based on the taxon id at the end of the link


3. Run <code>gene_expression_extraction_fungiexp.py</code>

4. This will create a new directory named the same as the <code>taxon_id</code> -->  This will automatically download all the Gene expression .tsv file and will be placed into the new created directory.

