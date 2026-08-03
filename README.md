# CS 131 Final Project

## Project Goals:
1. Answer a real data-science question with big data analysis
2. Profile the difference between tools that load everything into memory (Excel, pandas) and tools that stream or distribute the work (command-line pipelines, Spark)

### Topic
Our goal for this study is to understand how similar the genetic effect sizes for triglyceride-associated variants are across different ancestry groups. We expect to uncover genetic variant differences due to the over prevalence of European ancestry data in GWAS studies.

Looking at the PAN UK-BioBank GWAS studies 
https://pan.ukbb.broadinstitute.org/downloads/index.html
https://docs.google.com/spreadsheets/d/1AeeADtT0U1AukliiNyiVzVRdLYPkTbruQSk38DeutU8/edit#gid=903887429

## Project Findings
### Phase 1 and 2
- There are more NA values for CSA (~13,000,000) than EUR (~5,000,000) meaning CSA has a smaller sample size in the Biobank.
### Phase 3 and 4
- Europeans exhibit stronger statistical significance overall but have the same chromosomes effected as Central/South Asian ancestry  -> Manhattan plots
- EUR have much stronger association signals and CSA has fewer genome-wide significant hits -> Q-Q plots
- There are chromosomes where there is large differences in ancestry between CSA and EUR in effect size divergence -> barplot
  - The largest difference in ancestry in triglycerides is on chromosome 14 and in diabetes is on chromosome 21
-  The effect size does not diverge between ancestry in many of the chromosomes for triglyceride and diabetes -> heatmap
  - Triglyceride diverges most on chromosome 6, 11, and 14. Diabetes diverges most on chromosome 18, and 21.
- Our calculated z-scores show the same analysis made by the Pan-UKBB using heterogeneity test neglog(p) -> heterogeneity_crosscheck
    - The differences in chromosomes highlighted by the two plots (effect size and Manhattan) may not necessarily be due to the strongest GWAS association and instead could be due to ancestry alone.
