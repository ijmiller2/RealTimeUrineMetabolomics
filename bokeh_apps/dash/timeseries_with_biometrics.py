import pandas as pd
import numpy as np
from math import pi
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models.tickers import DaysTicker
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.transform import dodge
from bokeh.models import LinearAxis, Range1d
from bokeh.models import Span

import pingouin as pg

# bokeh tools
tools = "pan,wheel_zoom,box_zoom,reset,save"

# biometric bar plot
def time_series_with_biometric_bar_plot(biometric_source_data_1,
    biometric_source_data_2, sample_source_data_1,
    sample_source_data_2, view_1, view_2, selection_dict):

    # parse selections
    biometric = selection_dict['biometric']
    metabolite = selection_dict['metabolite']
    user = selection_dict['user']
    scale = selection_dict['scale']
    start_time = pd.to_datetime('8/22/2018')
    end_time = pd.to_datetime('9/1/2018')

    # set up data and relevant stats
    if user == "Both":

        # run rm_corr
        title = 'Daily total/average: {}'.format(biometric)
        # .tolist() causing refresh error
        x = list(biometric_source_data_1.data[biometric]) + list(biometric_source_data_2.data[biometric])
        y = list(np.log2(biometric_source_data_1.data[metabolite])) \
            + list(np.log2(biometric_source_data_2.data[metabolite]))
        subject = ["Subject1"] * len(biometric_source_data_1.data[metabolite]) \
            + ["Subject2"] * len(biometric_source_data_2.data[metabolite])
        df = pd.DataFrame({
            'x': x,
            'y': y,
            'subject': subject,
        })
        r, p, dof = pg.rm_corr(data=df, x='x', y='y', subject='subject')
        title = "Daily total/average: {} vs. log2 (Avg. Int.) {}; RM Corr : r = {}, p = {}".format(
            biometric, metabolite, round(r, 3), round(p, 3))

        #  get biometric max
        biometric_max = max(x)
        # get metabolite intensity min
        metabolite_intensities = list(sample_source_data_1.data[metabolite]) \
            + list(sample_source_data_2.data[metabolite])
        intensity_min, intensity_max = min(metabolite_intensities), \
            max(metabolite_intensities)

    elif user == "Subject1":
        # calculate Spearman's Rho for Subject1
        x = biometric_source_data_1.data[biometric]
        y = np.log2(biometric_source_data_1.data[metabolite])
        corr_df = pg.corr(x, y, method='skipped')
        coef = corr_df.iloc[0]['r']
        p = corr_df.iloc[0]['p-val']
        #print(corr_df)
        title = "Daily average {} vs. log2(Avg. Int.) {}; Spearman's Rho: {}, p = {}".format(
            biometric, metabolite, round(coef, 3), round(p, 5))

        #  get biometric max
        biometric_max = max(x)
        # get metabolite intensity min
        metabolite_intensities = list(sample_source_data_1.data[metabolite])
        intensity_min, intensity_max = min(metabolite_intensities), \
            max(metabolite_intensities)

    elif user == "Subject2":
        # calculate Spearman's Rho
        x = biometric_source_data_2.data[biometric]
        y = np.log2(biometric_source_data_2.data[metabolite])
        corr_df = pg.corr(x, y, method='skipped')
        coef = corr_df.iloc[0]['r']
        p = corr_df.iloc[0]['p-val']
        #print(corr_df)
        title = "Daily average {} vs. log2(Avg. Int.) {}; Spearman's Rho: {}, p = {}".format(
            biometric, metabolite, round(coef, 3), round(p, 5))

        #  get biometric max
        biometric_max = max(x)
        # get metabolite intensity range
        metabolite_intensities = sample_source_data_2.data[metabolite]
        intensity_min, intensity_max = min(metabolite_intensities), \
            max(metabolite_intensities)

    # Set up figure and formatting
    p = figure(title = title, tools=tools, x_axis_type="datetime",
        plot_width=800, plot_height=400, x_range=[start_time, end_time],
        y_range = [intensity_min, intensity_max],)
        #tooltips = [("sample", "@SampleID")])

    # Setting the second y axis range name and range
    biometric_max_start = biometric_max * 0.10
    biometric_range_end = biometric_max * 1.10
    p.extra_y_ranges = {"biometric_axis":
        Range1d(start=biometric_max_start, end=biometric_range_end)}

    # Adding the second axis to the plot.
    p.add_layout(LinearAxis(y_range_name="biometric_axis"), 'right')

    p.xaxis.ticker = DaysTicker(days=np.arange(
        1,59))
    p.xaxis.formatter=DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )

    p.output_backend = "svg"
    p.xaxis.axis_label = None
    p.toolbar.logo = None
    p.xaxis.major_label_orientation = pi/4
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.outline_line_color = None

    p.yaxis.axis_label = metabolite + "  {}".format(scale)
    p.yaxis[1].axis_label = biometric

    ### Now for actual data ###

    # Have to make width huge, since Datetime has millisecond resolution:
    # https://stackoverflow.com/questions/45711567/categorical-y-axis-and-datetime-x-axis-with-bokeh-vbar-plot
    # 1 hr * 4
    millisecond_width = 3600000 * 24
    if user == "Both" or user == "Subject1":

        # time series data
        legend_title = "Subject 1 [{}]".format(metabolite)
        p.line('Datetime',metabolite, source = sample_source_data_1,
            color='red')
        p.circle('Datetime',metabolite, source=sample_source_data_1,
            color="red", size=5, alpha=0.5, view=view_1, hover_color="black")

        # biometric data
        legend_title = "Subject 1 Daily Total {}".format(biometric)
        p.step('Datetime', y=biometric, color="red", mode="center",
            line_dash="dashed", source=biometric_source_data_1,
            legend=legend_title, y_range_name="biometric_axis")

        p.vbar('Datetime', top=biometric, fill_color="red",
            width=millisecond_width, line_color=None, alpha=0.3,
            source=biometric_source_data_1, y_range_name="biometric_axis")

    # overwrite
    if user == "Both" or user == "Subject2":

        # time series data
        legend_title = "Subject 2 [{}]".format(metabolite)
        p.line('Datetime',metabolite, source=sample_source_data_2,
            color='blue')
        p.circle('Datetime',metabolite, source=sample_source_data_2,
            color="blue", size=5, alpha=0.5, view=view_2, hover_color="black")

        # biometric data
        legend_title = "Subject 2 Daily Total {}".format(biometric)
        p.step('Datetime', y=biometric, color="blue", mode="center",
            line_dash="dashed", source=biometric_source_data_2,
            legend=legend_title, y_range_name="biometric_axis")

        p.vbar(x='Datetime', top=biometric, fill_color="blue",
            width=millisecond_width, line_color=None, alpha=0.3,
            source=biometric_source_data_2, y_range_name="biometric_axis")

    # Light cycle formatting, this needs to come second for tool tips to render
    vline_list = []
    for datetime in pd.date_range(start='8/22/2018', end='9/1/2018'):
        vline = Span(
            location=datetime,
            dimension='height',
            line_color='grey',
            #this should creat a ~6 hr window around midnight, to simulate
            # the dark cycle during this time period
            line_width=24,
            line_dash='solid',
            line_alpha=0.3
            )
        vline_list.append(vline)
    p.renderers.extend(vline_list)

    return p

if __name__ == "__main__":
    output_file("biometrics.html")

    from data import return_biometric_data_source, return_sample_data_source

    selection_dict = {
        "metabolite": "Hydrocaffeic acid 3 TMS",
        "user": "Subject1",
        "scale": "Intensity",
        "biometric": "Sleep (hrs)",
        "distribution": "Metabolite"
    }

    Subject1_biometric_data_source = return_biometric_data_source("Subject1")
    Subject2_biometric_data_source = return_biometric_data_source("Subject2")
    Subject1_sample_data_source = return_sample_data_source("Subject1", selection_dict)
    Subject2_sample_data_source = return_sample_data_source("Subject2", selection_dict)
    Subject1_view = CDSView(source=Subject1_sample_data_source)
    Subject2_view = CDSView(source=Subject2_sample_data_source)


    p = time_series_with_biometric_bar_plot(Subject1_biometric_data_source,
        Subject2_biometric_data_source, Subject1_sample_data_source,
        Subject2_sample_data_source, Subject1_view, Subject2_view,
        selection_dict)

    show(p)
