#rotate this between the different drug sensitivities... a bunch of them have R^2 close to 0, which means
#that trying to discriminate by site is about as effective as just guessing the overall mean of AUCs for that
#drug regardless of site
#e.g. site isn't a good predictor for AUC... means that even in the sites where there's low AUC for a certain
#drug & cell line, high AUC cell lines get in the way

#maybe there's something else we can do: namely, we could try and find the lowest 30 AUCs in each set and then 
#verify two things 1) verify that the mean of this sample is substantially different from the mean of the 
#overall (or the mean of the rest)... and 2) verify that certain sites or histologies are "enriched" relative
#to the majority

#a t - test, then a chi sq test? why not.

import pandas as pd
from scipy.stats import chi2_contingency

def chisq(crosstab):
    results = {}
    
    ct_filtered = crosstab[crosstab[True] >= 5]
    results["cells_over_0"] = crosstab[crosstab[True] > 0].shape[0]
    results["cells_5_and_over"] = ct_filtered.shape[0]
    #chi2_results = chi2_contingency(ct_filtered)
    
    chi2_results = chi2_contingency(crosstab)

    results["chi2"] = chi2_results[0]
    results["p"] = chi2_results[1].__round__(5)
    results["df"] = chi2_results[2]
    expected_counts = pd.DataFrame(chi2_results[3], columns=["no", "o"])

    #make an table of observed and expected counts
    table = {}
    table['header'] = [x.replace("_", " ") for x in crosstab.index]
    table['observed_no'] = [x.__round__(3) for x in crosstab[False]]
    table['observed_o'] = [x.__round__(3) for x in crosstab[True]]
    table['expected_no'] = [x.__round__(3) for x in expected_counts["no"]]
    table['expected_o'] = [x.__round__(3) for x in expected_counts["o"]]

    #print(table)

    return results, table

def sensitivity_tests(drug_id):
    """Applies tests to cell lines and outputs a dictionary of results required to fill out the
    HTML template for this page."""

    results = {}
    table_site = []
    table_hist = []
    
    results['drug_id'] = drug_id
    AUC_id = drug_id+"_AUC"

    #this filepath only works because the python interpreter is being called from within app/...
    data = pd.read_csv("../data/regression_data.tsv", sep="\t")[['site', 'histology', AUC_id]].dropna()

    results['num_cell_lines'] = data.shape[0]

    upper_quartile = data[AUC_id].quantile(.75)
    lower_quartile = data[AUC_id].quantile(.25)
    iqr = upper_quartile - lower_quartile

    results['maximum'] = data[AUC_id].max().__round__(2)
    results['minimum'] = data[AUC_id].min().__round__(2)
    results['median'] = data[AUC_id].median().__round__(2)
    results['Q1'] = upper_quartile.__round__(2)
    results['Q3'] = lower_quartile.__round__(2)
    results['iqr'] = iqr.__round__(2)

    #find outlier AUCs
    is_outlier = data[AUC_id] < lower_quartile - (1.5 * iqr)
    data["is_outlier"] = is_outlier
    
    results["num_outliers"] = len(data[data["is_outlier"]])

    #test 1: are the proportions of categories in site significantly different from in outliers compared to 
    #rest of data
    site_crosstabs = pd.crosstab(index=data["site"], columns=data["is_outlier"], margins=False)
    site_results, site_table = chisq(site_crosstabs)

    #test 2: are the proportions of categories in histology significantly different from data or rest of data
    histology_crosstabs = pd.crosstab(index=data["histology"], columns=data["is_outlier"], margins=False)
    hist_results, hist_table = chisq(histology_crosstabs)

    return results, site_results, hist_results, site_table, hist_table

#drug = "nelarabine"
#sensitivity_tests(drug)