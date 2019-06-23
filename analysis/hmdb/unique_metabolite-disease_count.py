import pandas as pd

disease_keyword = "cancer"

path = "/Users/ijmiller2/Desktop/UW_2019/UrineMetabolomics/" + \
    "RealTimeUrineMetabolomics/data/disease_metabolite_full_data.csv"
df = pd.read_csv(path)
df.dropna(inplace=True)

len(df['metabolite'].unique())
