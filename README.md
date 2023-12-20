# Enrichment Analysis for Cancer Drug Sensitivity

## The Problem

Cancers can appear in a range of tissues, and exhibit different behaviors and interactions with important systems in the human body. This poses a challenge for drug discovery and testing, since the same compound may have different levels of toxicity against different varieties of cancer cells. Additionally, while in vitro measurements such as IC50 may describe how a drug inhibits cancer cells in a culture dish, biomarkers of cancer cell activity and decline are needed to verify that the drug has similar effects in the human body.

## What This Program Does

The data for this program is from the Broad Institute's [Cancer Therapeutics Response Portal v2](https://portals.broadinstitute.org/ctrp.v2.1/?cluster=true?page=#ctd2Cluster). This data describes the sensitivity of 664 cancer cell lines against 481 therapeutic compounds, as measured in the area (AUC) under the function of drug dose (the concentration of the administered compound) and cell response. For a given cell line and drug, a lower AUC indicates a faster drop in cell growth, division, and viability-- meaning that the cell line is particularly sensitive to this drug.

In this dataset, cell lines are characterized by the tissue they originate from, and the primary histology of the cancer. This program examines which categories of cell lines are overrepresented or enriched among those cells most sensitive to a particular drug.

## Ready to Begin?

Necessary packages: Install the packages in the provided Pip file. Then run the Flask application in the "app" folder with "flask run". By default it runs on port 5000.
