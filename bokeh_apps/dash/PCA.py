from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import CDSView
from bokeh.layouts import row
from data import return_sample_data_source, return_metabolite_data_source

# bokeh tools
tools = "pan,wheel_zoom,box_zoom,reset,save"

# PCA scores plot
def PCA_scores_plot(sample_source_list):

    TOOLTIPS = [
        ("index", "$index"),
        ("(x,y)", "(@PC1, @PC2)"),
        ("Subject", "@Subject"),
    ]

    p = figure(title = "PCA Scores", tooltips=TOOLTIPS, tools=tools,
        plot_width=600, plot_height=400)

    p.xaxis.axis_label = 'PC1 (0.11)'
    p.yaxis.axis_label = 'PC2 (0.20)'
    p.toolbar.logo = None

    # add data from Subject1 and Subject2
    for sample_data_source in sample_source_list:
        p.circle('PC1','PC2', color='color', fill_alpha=0.2, size=10,
            source=sample_data_source, hover_color="black")

    return p

# PCA loadings plot
def PCA_loadings_plot(metabolite_data_source, metabolite_of_interest_source, selection_dict):

    TOOLTIPS = [
        ("(x,y)", "(@LoadingsOnPC1, @LoadingsOnPC2)"),
        ("desc", "@MetaboliteID"),
    ]

    metabolite_of_interest = selection_dict['metabolite']
    highlight_color = 'black'
    title = "PCA Loadings, {} highlighted in {}".format(metabolite_of_interest,
        highlight_color)
    p = figure(title = title, tooltips=TOOLTIPS, tools=tools,
        plot_width=600, plot_height=400, name="loadings")
    p.xaxis.axis_label = 'Loadings on PC1'
    p.yaxis.axis_label = 'Loadings on PC2'

    p.circle('LoadingsOnPC1','LoadingsOnPC2', fill_alpha=0.2, size=10,
        source=metabolite_data_source)

    # add another point for the metabolite of interest
    p.circle('LoadingsOnPC1','LoadingsOnPC2',
        color=highlight_color, fill_alpha=0.8, size=15,
        source=metabolite_of_interest_source)
    p.toolbar.logo = None

    return p

if __name__ == "__main__":
    output_file("PCA.html")

    selection_dict = {
        "metabolite": "Furoylglycine TMS",
        "user": "Both",
        "scale": "Intensity",
        "biometric": "Calories",
        "distribution": "Metabolite"
    }

    Subject1_sample_data_source = return_sample_data_source("Subject1", selection_dict)
    Subject2_sample_data_source = return_sample_data_source("Subject2", selection_dict)
    Subject1_view = CDSView(source=Subject1_sample_data_source)
    Subject2_view = CDSView(source=Subject2_sample_data_source)

    sample_source_list = [Subject1_sample_data_source, Subject2_sample_data_source]
    metabolite_data_source, metabolite_of_interest_source = return_metabolite_data_source("Furoylglycine TMS")

    p1 = PCA_scores_plot(sample_source_list)
    p2 = PCA_loadings_plot(metabolite_data_source,
        metabolite_of_interest_source, selection_dict)
    g = row([p1, p2])
    show(g)
