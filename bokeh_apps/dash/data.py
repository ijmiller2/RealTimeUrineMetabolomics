
import pandas as pd
from scipy.stats import zscore
# turn off warnings for adding column with sample_data_df['Subject'] syntax
pd.options.mode.chained_assignment = None
import numpy as np
from bokeh.plotting import ColumnDataSource

sample_data_df = pd.read_excel("../data/combined_sample_data.xlsx",
    sheet_name="SampleData")
sample_data_df['Datetime'] = pd.to_datetime(sample_data_df['Datetime'])
#sample_data_df['SizeByVol'] = sample_data_df['Volume'] / 30

metabolite_data_df = pd.read_excel("../data/combined_sample_data.xlsx",
    sheet_name="MetaboliteData")

biometric_data_df = pd.read_excel("../data/combined_sample_data.xlsx",
    sheet_name="BiometricsAveragedMSData")

def return_sample_data_source(subject, selection_dict):
    # load dataframe from spreadsheet

    scale = selection_dict['scale']
    metabolite = selection_dict['metabolite']

    Subject1_sample_data_df = sample_data_df[sample_data_df['Subject'] == 'Subject1']
    Subject1_sample_data_df_subset = Subject1_sample_data_df[Subject1_sample_data_df.columns[:9]]
    Subject1_sample_data_df_subset['color'] = 'red'

    Subject2_sample_data_df = sample_data_df[sample_data_df['Subject'] == 'Subject2']
    Subject2_sample_data_df_subset = Subject2_sample_data_df[Subject2_sample_data_df.columns[:9]]
    Subject2_sample_data_df_subset['color'] = 'blue'

    if scale == "log2(Intensity)":
        Subject1_sample_data_df_subset[metabolite] = np.log2(
            Subject1_sample_data_df[metabolite])
        Subject2_sample_data_df_subset[metabolite] = np.log2(
            Subject2_sample_data_df[metabolite])
    elif scale == "z-score":
        Subject1_sample_data_df_subset[metabolite] = zscore(
            Subject1_sample_data_df[metabolite])
        Subject2_sample_data_df_subset[metabolite] = zscore(
            Subject2_sample_data_df[metabolite])
    else:
        Subject1_sample_data_df_subset[metabolite] = Subject1_sample_data_df[metabolite]
        Subject2_sample_data_df_subset[metabolite] = Subject2_sample_data_df[metabolite]

    Subject1_sample_data_source = ColumnDataSource(Subject1_sample_data_df_subset)
    Subject2_sample_data_source = ColumnDataSource(Subject2_sample_data_df_subset)

    if subject == "Subject1":
        return Subject1_sample_data_source
    elif subject == "Subject2":
        return Subject2_sample_data_source

def return_metabolite_data_source(metabolite_of_interest):
    # load dataframe from spreadsheet

    metabolite_data_source = ColumnDataSource(metabolite_data_df)
    metabolite_options = metabolite_data_df['MetaboliteID'].tolist()

    # parse out data for metabolite of interest
    # BUG: don't think this will acount for mutliple redundant values..
    metabolite_index = metabolite_options.index(metabolite_of_interest)
    metabolite_of_interest_x = metabolite_data_df.iloc[metabolite_index]['LoadingsOnPC1']
    metabolite_of_interest_y = metabolite_data_df.iloc[metabolite_index]['LoadingsOnPC2']

    # convert to ColumnDataSource object
    metabolite_of_interest_source = ColumnDataSource(data=dict(
        LoadingsOnPC1=[metabolite_of_interest_x],
        LoadingsOnPC2=[metabolite_of_interest_y],
        MetaboliteID=[metabolite_of_interest]
    ))

    return metabolite_data_source, metabolite_of_interest_source

def return_biometric_data_source(subject):

    Subject1_biometric_data_df = biometric_data_df[biometric_data_df['Subject'] == 'Subject1']
    Subject2_biometric_data_df = biometric_data_df[biometric_data_df['Subject'] == 'Subject2']
    Subject1_biometric_data_source = ColumnDataSource(Subject1_biometric_data_df)
    Subject2_biometric_data_source = ColumnDataSource(Subject2_biometric_data_df)

    if subject == "Subject1":
        return Subject1_biometric_data_source
    elif subject == "Subject2":
        return Subject2_biometric_data_source

def return_default_options(field):

    if field == "biometric":
        options = biometric_data_df.columns[2:15].tolist()
        default = 'Calories from Alcohol'
        return default, options

    if field == "show_biometric":
        options = ["True", "False"]
        default = "False"
        return default, options

    if field == "metabolite":
        options = metabolite_data_df['MetaboliteID'].tolist()
        default = "Carbohydrate 6"
        return default, options

    if field == "user":
        options = ['Subject2','Subject1','Both']
        default = 'Both'
        return default, options

    if field == "scale":
        default = "Intensity"
        options = ['Intensity','log2(Intensity)', 'z-score']
        return default, options

    if field == "distribution":
        default = "Metabolite"
        options = ["Metabolite", "Biometric", "Daily Average Metabolite"]
        return default, options
