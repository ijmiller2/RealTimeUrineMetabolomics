import pandas as pd

disease_keyword = "cancer"

path = "/Users/ijmiller2/Desktop/UW_2019/UrineMetabolomics/" + \
    "RealTimeUrineMetabolomics/data/hmdb_info.xlsx"
df = pd.read_excel(path)
df.dropna(inplace=True)

disease_count = 0
for index,row in df.iterrows():
    associated_diseases = row['AssocitedDiseases']
    if disease_keyword.lower() in associated_diseases.lower():
        disease_count += 1

print("Found {} keyword {} times...".format(disease_keyword,disease_count))
