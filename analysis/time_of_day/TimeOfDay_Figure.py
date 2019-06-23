
import pandas as pd
import pingouin as pg
import numpy as np
from scipy.stats import zscore
from math import pi
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column, row
import copy

subject = "Subject1"
filter_by_normal_dist = False

data_path = "../../data/combined_sample_data.xlsx"
combined_df = pd.read_excel(data_path, sheet_name="SampleData", index_col="SampleID")
metabolite_list = combined_df.columns[8:]

# Get list of metabolites for subject
subject_df = combined_df[combined_df['Subject'] == subject]
subject_df = subject_df[subject_df['TimeOfDay'] != 4]

alpha = 0.05
subject_diurnal_list = []
for metabolite in metabolite_list:
    log2_metabolite = np.log2(subject_df[metabolite])
    normal, shapiro_wilk_pval = pg.normality(log2_metabolite)

    lr_info = pg.linear_regression(subject_df['TimeOfDay'], log2_metabolite)
    lr_pval = lr_info.iloc[1]['pval']
    if filter_by_normal_dist:
        if lr_pval < alpha and normal:
            subject_diurnal_list.append(metabolite)
    else:
        if lr_pval < alpha:
            subject_diurnal_list.append(metabolite)
print(len(subject_diurnal_list))


# calcualte z-score

#subject_zscore_df = pd.DataFrame(zscore(np.log2(subject_df[subject_df.columns[9:]])), 
#                                index=subject_df.index, columns=subject_df.columns[9:])
subject_log2_df = pd.DataFrame(np.log2(subject_df[subject_df.columns[8:]]), 
                                 index=subject_df.index, columns=subject_df.columns[8:])
subject_zscore_df = copy.deepcopy(subject_log2_df)
print(subject_zscore_df.head(n=10))
for column in subject_log2_df.columns:
    print(column)
    subject_zscore_df[column] = zscore(subject_log2_df[column])
print(subject_zscore_df.head(n=10))

# these values change based on order of table (maybe due to bad index?)
print(subject_zscore_df.head(n=10))
subject_zscore_df.columns = subject_df.columns[8:]
subject_zscore_df['TimeOfDay'] = subject_df['TimeOfDay']

average_int_dict = {
    1:{},
    2:{},
    3:{}}

for metabolite in subject_diurnal_list:
    print(metabolite)
    for TimeOfDay in [1,2,3]:
        
        average_time_int_zscore = subject_zscore_df[subject_zscore_df['TimeOfDay']==TimeOfDay][metabolite].median()
        #average_time_int_zscore = np.log2(subject_df[subject_df['TimeOfDay']==TimeOfDay][metabolite]).mean()
        print("\t" + str(TimeOfDay) + "\t" + str(average_time_int_zscore))
        average_int_dict[TimeOfDay][metabolite] = average_time_int_zscore
        #print("\t",TimeOfDay,average_time_int_zscore)

# create dataframe and labels

subject_deviation_df = pd.DataFrame(average_int_dict)
effect_time_list = []
color_list = []
hex_dict = {
    1:"#5ba965",
    2:"#777acd",
    3:"#ca5c4b"
}

hex_dict = {
    1:"green",
    2:"red",
    3:"blue"
}

print(subject_deviation_df.head(n=10))
for metabolite,row in abs(subject_deviation_df).iterrows():
    time_effect = row.idxmax(axis=1) # label by highest average deviation
    color = hex_dict[time_effect]
    color_list.append(color)
    if time_effect == 1:
        effect_time_list.append("morning")
    elif time_effect == 2:
        effect_time_list.append("afternoon")
    elif time_effect == 3:
        effect_time_list.append("evening")

subject_deviation_df['effect_time'] = effect_time_list
subject_deviation_df['color'] = color_list
print(subject_deviation_df.head(n=10))
### create line plots

p1 = figure(title = "Morning Effect Metabolites", tools="save",
    plot_width=600, plot_height=200)

for metabolite, row in subject_deviation_df[subject_deviation_df['effect_time']=="morning"].iterrows():
    xs = [1,2,3]
    ys = [i for i in subject_deviation_df.loc[metabolite][:3]]
    color = subject_deviation_df.loc[metabolite]['color']
    p1.line(x=xs,y=ys, color=color, hover_color="black")

# p2
p2 = figure(title = "Afternoon Effect Metabolites", tools="save",
    plot_width=600, plot_height=200)

for metabolite, row in subject_deviation_df[subject_deviation_df['effect_time']=="afternoon"].iterrows():
    xs = [1,2,3]
    ys = [i for i in subject_deviation_df.loc[metabolite][:3]]
    color = subject_deviation_df.loc[metabolite]['color']
    p2.line(x=xs,y=ys, color=color, hover_color="black")

# p3
p3 = figure(title = "Evening Effect Metabolites", tools="save",
    plot_width=600, plot_height=200)

for metabolite, row in subject_deviation_df[subject_deviation_df['effect_time']=="evening"].iterrows():
    xs = [1,2,3]
    ys = [i for i in subject_deviation_df.loc[metabolite][:3]]
    color = subject_deviation_df.loc[metabolite]['color']
    p3.line(x=xs,y=ys, color=color, hover_color="black")

from bokeh.layouts import column

for p in [p1,p2,p3]:
    p.xaxis.axis_label = 'time of day'
    p.yaxis.axis_label = 'Median Z-Score'
    p.toolbar.logo = None
    p.grid.grid_line_color = None
    p.outline_line_color = None
    p.xaxis.ticker = [1, 2, 3]
    p.xaxis.major_label_overrides = {1: 'Morning', 2: 'Afternoon', 3: 'Evening'}
    p.output_backend = "svg"

# get metabolite counts for each effect type

effect_count_dict = {}
for timeOfDay in subject_deviation_df['effect_time'].unique():
    effect_count_dict[timeOfDay] = len(subject_deviation_df[subject_deviation_df['effect_time']==timeOfDay])
effect_count_dict
data = pd.Series(effect_count_dict).reset_index(name='value').rename(columns={'index':'timeOfDay'})

# create pie charts
data['angle'] = data['value']/data['value'].sum() * 2*pi

color_map_dict = {
    "morning":"green",
    "afternoon":"red",
    "evening":"blue"
}

effect_time = "morning"
color_list = [color_map_dict[i] if i==effect_time else "grey" for i in data.timeOfDay]
data['color'] = color_list
title = "{} of {} metabolites".format(effect_count_dict[effect_time], sum(effect_count_dict.values()))
pie1 = figure(plot_height=200, plot_width=300, title=title,
           tools="save", x_range=(-0.5, 1.0))

pie1.wedge(x=0, y=1, radius=0.2,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='timeOfDay', source=data, fill_alpha=0.5)

# pie 2
effect_time = "afternoon"
title = "{} of {} metabolites".format(effect_count_dict[effect_time], sum(effect_count_dict.values()))
color_list = [color_map_dict[i] if i==effect_time else "grey" for i in data.timeOfDay]
data['color'] = color_list

title = "{} of {} metabolites".format(effect_count_dict[effect_time], sum(effect_count_dict.values()))
pie2 = figure(plot_height=200, plot_width=300, title=title,
           tools="save", x_range=(-0.5, 1.0))

pie2.wedge(x=0, y=1, radius=0.2,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='timeOfDay', source=data, fill_alpha=0.5)

# pie 3
effect_time = "evening"
title = "{} of {} metabolites".format(effect_count_dict[effect_time], sum(effect_count_dict.values()))
color_list = [color_map_dict[i] if i==effect_time else "grey" for i in data.timeOfDay]
data['color'] = color_list
pie3 = figure(plot_height=200, plot_width=300, title=title,
           tools="save", x_range=(-0.5, 1.0))

pie3.wedge(x=0, y=1, radius=0.2,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='timeOfDay', source=data, fill_alpha=0.5)


for p in [pie1,pie2,pie3]:
    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    p.outline_line_color = None
    p.toolbar.logo = None
    p.output_backend = "svg"

# show the plots
# redefine row
from bokeh.layouts import column, row
output_file("{}_TimeOfDayFigure.html".format(subject))

show(
    column([row([p1, pie1]), row([p2, pie2]), row([p3, pie3])] )
)

#show(column([p1,p2,p3]))"""

print(data)