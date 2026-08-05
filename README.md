# CS 131 Final Project

## Project Goals:
1. Answer a real data-science question with big data analysis
2. Profile the difference between tools that load everything into memory (Excel, pandas) and tools that stream or distribute the work (command-line pipelines, Spark)

### Topic
We are focused on uncovering how similar the genetic effect sizes for triglyceride-associated variants and type II diabetes-associated variants are for people of European or Central/South Asian ancestry. Using the Pan-UK Biobank database, which has multi-ancestry analysis of 7,228 phenotypes, effect size and standard error of each variant is utilized to answer our data science question. We expect to uncover genetic variant differences due to the over prevalence of European (EUR) ancestry data in GWAS studies and higher numbers of missing data values for Central/South Asian (CSA) ancestry.

Database Source: PAN UK-BioBank GWAS studies 
https://pan.ukbb.broadinstitute.org/downloads/index.html
https://docs.google.com/spreadsheets/d/1AeeADtT0U1AukliiNyiVzVRdLYPkTbruQSk38DeutU8/edit#gid=903887429

## Project Findings
### Phase 1 and 2
- There are more NA values for CSA (~13,000,000) than EUR (~5,000,000) meaning CSA has a smaller sample size in the Biobank.
### Phase 3 and 4
- Europeans exhibit stronger statistical significance overall but have the same chromosomes effected as Central/South Asian ancestry  -> Manhattan plots
- The Manhattan plot shows the statistical significance of different variants across the entire genome.
  - ex: Chromosome 11 contains variants significantly associated with levels of triglycerides.
- <img width="933" height="576" alt="triglycerides_EUR_neglog" src="https://github.com/user-attachments/assets/08ed163e-8a26-4b65-aaa2-0756f0a02f2a" />
<img width="933" height="576" alt="triglycerides_CSA_neglog" src="https://github.com/user-attachments/assets/23f2e9a9-9c72-4b10-9a5e-390f75722094" />

- EUR have much stronger association signals and CSA has fewer genome-wide significant hits -> Q-Q plots
<img width="929" height="574" alt="diabetes_EUR_neglog" src="https://github.com/user-attachments/assets/ee32ab61-4b5a-4927-bd86-ac5e46bd613a" />
<img width="929" height="574" alt="diabetes_CSA_neglog" src="https://github.com/user-attachments/assets/0a006333-a41b-4c60-b836-4b49b6dde137" />

- There are chromosomes where there is large differences in ancestry between CSA and EUR in effect size divergence -> barplot
  - The largest difference in ancestry in triglycerides is on chromosome 14 and in diabetes is on chromosome 21
<img width="2800" height="1200" alt="chr_barplot" src="https://github.com/user-attachments/assets/a63232a9-6343-4f81-94cb-47731d8b1eca" />

-  The effect size does not diverge between ancestry in many of the chromosomes for triglyceride and diabetes -> heatmap
  - Triglyceride diverges most on chromosome 6, 11, and 14. Diabetes diverges most on chromosome 18, and 21.
  - In the heatmap, a lighter color indicates more divergence in the variant effects between the populations.
    - ex: Chromosome 14 has the highest variant effect size divergence between the two populations in triglycerides.
<img width="2800" height="700" alt="chr_heatmap" src="https://github.com/user-attachments/assets/cb0a023b-1e6b-413e-8735-f0e7dd03b62a" />

- Our calculated z-scores show the same analysis made by the Pan-UKBB using heterogeneity test neglog(p) -> heterogeneity_crosscheck
<img width="1400" height="1200" alt="heterogeneity_crosscheck" src="https://github.com/user-attachments/assets/34ee7e75-6a18-4ace-95eb-8952cdfea4a6" />

More plots are located in the *4_findings* folder

### Conclusion
- The differences in chromosomes highlighted by the two plots (effect size and Manhattan) may not necessarily be due variants with the the strongest GWAS association and instead could be due to ancestry alone.
- Significant discrepancies in the data between European and Central/South Asian samples (8,413 CSA v.s. 40,0639 EUR in triglycerides and 1,662 CSA v.s. 22,634 EUR in diabetes) suggest that CSA's results are systematically less reliable/precise, which limits how much we can trust both the Manhattan plot comparison and the heterogeneity z-scores.
