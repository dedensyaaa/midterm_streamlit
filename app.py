import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import io

# Set Streamlit app title
st.title('Video Game Sales Data Analysis')

# Load dataset
sales = pd.read_csv('vgsales.csv')
sales.dropna(how="any", inplace=True)
sales['Year'] = sales['Year'].astype(int)

# Show basic info and data
st.header("Dataset Overview")
st.write(sales.head())  # Display the first few rows of the dataset
st.write(sales.describe())  # Show dataset statistics

# Visualize missing data
st.header("Missing Data Visualization")
msno_plt = msno.matrix(sales)
plt.figure(figsize=(10, 6))
img = io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)
st.image(img, caption="Missing Data Matrix", use_column_width=True)
plt.close()

# Helper function for statistics
def print_statistics(column_name, column_data):
    stats = {
        "Mean": column_data.mean(),
        "Standard Deviation": column_data.std(),
        "Minimum": column_data.min(),
        "Maximum": column_data.max(),
        "Median": column_data.median()
    }
    return stats

# Display column statistics in Streamlit
st.header("Statistics for Sales Columns")
for column_name in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales']:
    column_data = sales[column_name]
    st.subheader(f"Statistics for {column_name}")
    stats = print_statistics(column_name, column_data)
    st.write(stats)

# Convert sales columns to integers
sales[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']] = sales[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].astype(int)

# Helper function for bar plot
def plot_sales_distribution(sales_column, column_name):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=sales[sales_column].value_counts().index, y=sales[sales_column].value_counts().values)
    plt.xlabel(f'{column_name}')
    plt.ylabel('Frequency')
    plt.title(f'{column_name} Bar Plot')
    plt.xticks(rotation=45)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img

# Plot bar plots for sales distribution in Streamlit
st.header("Sales Distribution Bar Plots")
for col in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']:
    st.subheader(f'{col} Distribution')
    img = plot_sales_distribution(col, col)
    st.image(img, caption=f'{col} Distribution Bar Plot', use_column_width=True)
    plt.close()

# Correlation heatmap
st.header("Correlation Heatmap")
numeric_sales = sales.select_dtypes(include=[np.number])
plt.figure(figsize=(10, 6))
sns.heatmap(numeric_sales.corr(), annot=True, linewidths=0.5)
plt.title('Correlation Heatmap for Sales Data', fontsize=16)
img = io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)
st.image(img, caption='Correlation Heatmap', use_column_width=True)
plt.close()

#PIECHART
st.header("Piecharts: Top 10 Game Sales by Region")
st.write("""
This dashboard displays pie charts of the top 10 best-selling video games, segmented by Global Sales, North America (NA) Sales, Europe (EU) Sales, and Japan (JP) Sales. 
""")
region = st.selectbox(
    "Select the region to display top 10 sales",
    ("Global", "North America", "Europe", "Japan")
)

def plot_pie_chart(sizes, labels, title):
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    explode = [0.1] + [0] * (len(labels) - 1)
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=90)
    ax.set_title(title, fontsize=16)
    ax.axis('equal')  
    st.pyplot(fig)

if region == "Global":
    sales = pd.read_csv('vgsales.csv')
    st.subheader("Top 10 Global Sales by Game")
    labels = sales['Name'].head(10)
    sizes = sales['Global_Sales'].head(10)
    plot_pie_chart(sizes, labels, 'Top 10 Total Global Sales by Game')
    st.markdown("These are the top 10 video games based on total global sales. The chart shows the distribution of sales among the best-selling games worldwide.")

elif region == "North America":
    sales = pd.read_csv('vgsales.csv')
    st.subheader("Top 10 Sales in North America by Game")
    top10_na_sales = sales[['Name', 'NA_Sales']].sort_values(by='NA_Sales', ascending=False).head(10)
    labels = top10_na_sales['Name']
    sizes = top10_na_sales['NA_Sales']
    plot_pie_chart(sizes, labels, 'Top 10 Sales in North America')
    st.markdown("These are the top 10 video games based on sales in North America. The chart highlights how each game performed in this region.")

elif region == "Europe":
    sales = pd.read_csv('vgsales.csv')
    st.subheader("Top 10 Sales in Europe by Game")
    top10_eu_sales = sales[['Name', 'EU_Sales']].sort_values(by='EU_Sales', ascending=False).head(10)
    labels = top10_eu_sales['Name']
    sizes = top10_eu_sales['EU_Sales']
    plot_pie_chart(sizes, labels, 'Top 10 Sales in Europe')
    st.markdown("These are the top 10 video games based on sales in Europe. The pie chart shows the market share of each game in this region.")

elif region == "Japan":
    sales = pd.read_csv('vgsales.csv')
    st.subheader("Top 10 Sales in Japan by Game")
    top10_jp_sales = sales[['Name', 'JP_Sales']].sort_values(by='JP_Sales', ascending=False).head(10)
    labels = top10_jp_sales['Name']
    sizes = top10_jp_sales['JP_Sales']
    plot_pie_chart(sizes, labels, 'Top 10 Sales in Japan')
    st.markdown("These are the top 10 video games based on sales in Japan. The chart represents the dominance of various titles in the Japanese market.")

