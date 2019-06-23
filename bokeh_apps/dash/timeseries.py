
import pandas as pd
import numpy as np
from math import pi
from bokeh.plotting import figure, show, output_file, ColumnDataSource, curdoc
from bokeh.models.tickers import DaysTicker
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models import CDSView
from bokeh.models import Span


# bokeh tools -> to hide the help message and docs
tools = "pan,wheel_zoom,box_zoom,reset,save"
# Enable tooltips for only some glyphs
#https://stackoverflow.com/questions/29435200/bokeh-plotting-enable-tooltips-for-only-some-glyphs

# function to create time series plot
def time_series_plot(source_data_1, source_data_2, view_1, view_2, selection_dict):

    metabolite_of_interest = selection_dict['metabolite']
    user_of_interest = selection_dict['user']
    intensity_scale = selection_dict['scale']
    start_time = pd.to_datetime('8/22/2018')
    end_time = pd.to_datetime('9/1/2018')

    TOOLTIPS = [("sample", "@SampleID")]

    title = "Abundance of {} over time in user(s): {}".format(
        metabolite_of_interest,user_of_interest)
    p = figure(title = title, tooltips=TOOLTIPS, tools=tools,
        plot_width=800, plot_height=400, x_axis_type="datetime",
        x_range=[start_time, end_time])

    #Format ticks based on Subject2 data (since he has more time points)
    p.xaxis.ticker = DaysTicker(days=np.arange(
        1,59))
    p.xaxis.formatter=DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
    p.xaxis.major_label_orientation = pi/4
    p.xaxis.axis_label = 'Datetime'
    p.yaxis.axis_label = intensity_scale

    p.output_backend = "svg"
    p.toolbar.logo = None
    p.outline_line_color = None
    p.xgrid.visible = False
    p.ygrid.visible = False

    ###

    if user_of_interest == "Subject1":
        p.line('Datetime',metabolite_of_interest, source = source_data_1,
            color='red')
        p.circle('Datetime',metabolite_of_interest, source=source_data_1,
            color="red", size=5, alpha=0.5, view=view_1, hover_color="black")

    elif user_of_interest == "Subject2":
        p.line('Datetime',metabolite_of_interest, source=source_data_2,
            color='blue')
        p.circle('Datetime',metabolite_of_interest, source=source_data_2,
            color="blue", size=5, alpha=0.5, view=view_2, hover_color="black")

    elif user_of_interest == "Both":
        p.line('Datetime',metabolite_of_interest,
            source=source_data_1, color='red')
        p.circle('Datetime',metabolite_of_interest, source=source_data_1,
            color="red", size=5, alpha=0.5, view=view_1, hover_color="black")

        p.line('Datetime',metabolite_of_interest,
            source=source_data_2, color='blue')
        p.circle('Datetime',metabolite_of_interest, source=source_data_2,
            color="blue", size=5, alpha=0.5, view=view_2, hover_color="black")

    else:
        pass

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
    output_file("timeseries.html")

    from data import return_sample_data_source

    selection_dict = {
        "metabolite": "Acetominophen 2 TMS",
        "user": "Both",
        "scale": "Intensity",
        "biometric": "Calories",
        "distribution": "Metabolite"
    }

    Subject1_sample_data_source = return_sample_data_source("Subject1", selection_dict)
    Subject2_sample_data_source = return_sample_data_source("Subject2", selection_dict)
    Subject1_view = CDSView(source=Subject1_sample_data_source)
    Subject2_view = CDSView(source=Subject2_sample_data_source)

    p = time_series_plot(
        Subject1_sample_data_source, Subject2_sample_data_source,
        Subject1_view, Subject2_view, selection_dict
    )

    show(p)
