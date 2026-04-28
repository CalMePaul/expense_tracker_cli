import plotly.express as px


def expenses_by_time(data_frame, time_window):
    """Plot the spent amount over a fixed time_window on a daily frequency, using a bar chart."""

    # Make the x axis the date column of the df and y axis the amount column of the df.
    # I chose the bar chart here for testing (i created expenses the same day so one point wouldn't make the chart)
    # The bar chart also allows, in my opinion, better readability of expenses on independent dats.
    fig = px.bar(
        data_frame,
        x="Date",
        y="Amount",
        title=f"Daily spending in the last {time_window} days",
    )
    fig.show()


def expenses_by_category(data_frame, time_window):
    """Plot the spent amount over the last month by category, using a bar chart."""

    # Make the x axis the date column of the df and y axis the amount column of the df.
    fig = px.bar(
        data_frame,
        x="Category",
        y="Amount",
        title=f"Spending by category during the last {time_window} days",
    )
    fig.show()
