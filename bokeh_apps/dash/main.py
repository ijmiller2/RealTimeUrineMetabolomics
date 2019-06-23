
# bokeh depencies for main
from bokeh.plotting import curdoc
from bokeh.models import Select, CDSView
from bokeh.layouts import row, widgetbox, column, gridplot, layout
from bokeh.models.widgets import Paragraph

# load functions from other files
from PCA import PCA_scores_plot, PCA_loadings_plot
from timeseries import time_series_plot
from timeseries_with_biometrics import time_series_with_biometric_bar_plot

# main function to update plot on new selection
def update(attr, old, new):

    # update selection_dict
    selection_dict = dict(
        metabolite = metabolite.value,
        user = user.value,
        scale = scale.value,
        biometric = biometric.value,
        show_biometric = show_biometric.value,
        #distribution = distribution.value
    )

    # update sample data
    Subject1_sample_data_source = return_sample_data_source("Subject1",
        selection_dict)
    Subject2_sample_data_source = return_sample_data_source("Subject2",
        selection_dict)
    Subject1_view = CDSView(source=Subject1_sample_data_source)
    Subject2_view = CDSView(source=Subject2_sample_data_source)

    # update metabolite data
    metabolite_data_source, metabolite_of_interest_source = return_metabolite_data_source(metabolite.value)

    # update second item of second row (time series plot)
    if show_biometric.value == "True":
        try:
            layout.children[0].children[1].children[1] = \
            time_series_with_biometric_bar_plot(Subject1_biometric_data_source,
            Subject2_biometric_data_source, Subject1_sample_data_source,
            Subject2_sample_data_source, Subject1_view, Subject2_view,
            selection_dict)
        except KeyError as e:

            #if e == 'r':
            message = Paragraph(
            text="""
            Correlation analysis failed.
            This subject's biometric data type may be too sparse.
            Please try another biometric or subject combination.
            """,
            style={'font-size': '20px', 'text-align': 'center'},
            width=500, height=100)
            """else:

                message = Paragraph(
                text="Key Error: {}".format(e),
                style={'font-size': '20px', 'text-align': 'center'},
                width=500, height=100)"""

            layout.children[0].children[1].children[1] = message
    else:
        layout.children[0].children[1].children[1] = time_series_plot(
            Subject1_sample_data_source, Subject2_sample_data_source,
            Subject1_view, Subject2_view, selection_dict
        )
    # update second item of first row (PCA loadings plot)
    metabolite_data_source, metabolite_of_interest_source = return_metabolite_data_source(metabolite.value)
    layout.children[0].children[0].children[1] = PCA_loadings_plot(
        metabolite_data_source, metabolite_of_interest_source, selection_dict)

    # update second item of first row (PCA scores plot) - to keep view link
    sample_source_list = [Subject1_sample_data_source, Subject2_sample_data_source]
    layout.children[0].children[0].children[0] = PCA_scores_plot(
        sample_source_list)

    #row_test.children[0] = PCA_scores_plot(
    #    sample_source_list)
    p6 = PCA_scores_plot(
        sample_source_list)

    # update first item of third row - [metabolite|biometric] histogram
    """if distribution.value == "Metabolite":
        layout.children[0].children[2].children[0] = metabolite_histogram_plot(
            Subject1_sample_data_source, Subject2_sample_data_source, selection_dict)
    elif distribution.value == "Biometric":
        layout.children[0].children[2].children[0] = biometric_histogram_plot(
            Subject1_biometric_data_source, Subject2_biometric_data_source, selection_dict)
    elif distribution.value == "Daily Average Metabolite":
        layout.children[0].children[2].children[0] = avg_metabolite_histogram_plot(
            Subject1_biometric_data_source, Subject2_biometric_data_source, selection_dict)

    # update second item of third row biometric barplot
    layout.children[0].children[2].children[1] = biometric_bar_plot(
        Subject1_biometric_data_source, Subject2_biometric_data_source, selection_dict)"""

### setup the interactive controls ###
from data import *

metabolite_default, metabolite_options = return_default_options("metabolite")
metabolite = Select(title='Metabolite', value=metabolite_default,
    options=metabolite_options)
metabolite.on_change('value', update)

user_default, user_options = return_default_options("user")
user = Select(title='User', value=user_default, options=user_options)
user.on_change('value', update)

scale_default, scale_options = return_default_options("scale")
scale = Select(title='Metabolite Scale', value=scale_default,
    options=scale_options)
scale.on_change('value', update)

show_biometric_default, biometric_options = return_default_options("show_biometric")
show_biometric = Select(title='Correlate with Biometric Data',
    value=show_biometric_default, options=biometric_options)
show_biometric.on_change('value', update)

biometric_default, biometric_options = return_default_options("biometric")
biometric = Select(title='Biometric', value=biometric_default,
    options=biometric_options)
biometric.on_change('value', update)

"""distribution_default, distribution_options = return_default_options("distribution")
distribution = Select(title='Distribution', value=distribution_default,
    options=distribution_options)
distribution.on_change('value', update)"""

selection_dict = dict(
    metabolite = metabolite.value,
    user = user.value,
    scale = scale.value,
    biometric = biometric.value,
    show_biometric = show_biometric.value,
    #distribution = distribution.value
)

controls = widgetbox([
    metabolite,
    user,
    scale,
    show_biometric,
    biometric], width=400)
    #distribution], width=400)

### outsource data processing to functions in data.py ###
metabolite_data_source, metabolite_of_interest_source = return_metabolite_data_source(metabolite.value)
Subject1_biometric_data_source = return_biometric_data_source("Subject1")
Subject2_biometric_data_source = return_biometric_data_source("Subject2")

Subject1_sample_data_source = return_sample_data_source("Subject1", selection_dict)
Subject2_sample_data_source = return_sample_data_source("Subject2", selection_dict)
Subject1_view = CDSView(source=Subject1_sample_data_source)
Subject2_view = CDSView(source=Subject2_sample_data_source)
sample_source_list = [Subject1_sample_data_source, Subject2_sample_data_source]

### initial figure setup ###
p1 = PCA_scores_plot(sample_source_list)
p2 = PCA_loadings_plot(metabolite_data_source,
    metabolite_of_interest_source, selection_dict)
p3 = time_series_plot(
    Subject1_sample_data_source, Subject2_sample_data_source,
    Subject1_view, Subject2_view, selection_dict
)

p6 = PCA_loadings_plot(metabolite_data_source,
    metabolite_of_interest_source, selection_dict)

row_test = row([p6])

### setup document layout ###
layout = layout(sizing_mode='scale_width')
layout.children.append(column(
    row(p1,p2),
    row(controls, p3)))

# Save curdoc() to make sure all threads
# see the same document.
doc = curdoc()
doc.add_root(layout)
#doc.add_root(row_test)
#doc.add_root(p6)
doc.title = "Metabolite Viewer"
