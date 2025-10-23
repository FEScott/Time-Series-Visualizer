from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True, index_col='date')

# Set the index to the date column



# Clean data: exclude top and bottom 2.5%
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # Draw line plot
    fig = plt.figure()
    plt.plot(df.index, df['value'], color='r', linewidth=1)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.ylabel('Page Views')
    plt.xlabel('Date')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar 
    df_bar = df.copy()
    df_bar['month'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year

    # Group data by year then by month and calculate the average monthly value 
    # adding column to data
    df_bar = df_bar.groupby(['year', 'month']).agg(average_value=('value', 'mean'))
    # re-order data so that we have the correct format for the bar chart
    df_bar = df_bar.unstack(level='month')

    # Draw bar plot
    ax = df_bar.plot(kind='bar', figsize=(12,6))
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Page Views per Month')
    ax.legend(title='Month', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    
    fig = ax.get_figure()  # Get the figure from the axes

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    print(df_box.head())
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=ax2)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax1.set_xlabel('Year')
    ax2.set_xlabel('Month')
    ax1.set_ylabel('Page Views')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
