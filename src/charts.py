import plotly.express as px


def expenses_by_time(time_frame, data_frame):
    """Plot the spent amount over a fixed time_frame on a daily frequency, using a line chart."""

    # Make the x axis the date column of the df and y axis the amount column of the df.
    fig = px.line(data_frame, x="Date", y="Amount", title=f"Daily spending in the last {time_frame}")
    fig.show()
