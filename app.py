import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import io

st.title('Video Game Sales Data Analysis')

# Load dataset
sales = pd.read_csv('vgsales.csv')
sales.dropna(how="any", inplace=True)
sales['Year'] = sales['Year'].astype(int)

option = st.sidebar.selectbox("Contents", ["Introduction", "Dataset", "Visualization", "Conclusion"])
if option == "Introduction":
    st.header("Introduction")

    st.image("Game.gif", use_column_width=True)

    st.write("""
    This analysis delves into video game sales data of 1980 to 2023, focusing on various sales metrics across different regions, including North America (NA Sales), Japan (JP Sales), Europe (EU Sales), and other territories. Additionally, we will consider the influence of the game publisher and its release year on sales performance.

By examining these variables, we aim to identify patterns and trends that reveal how regional markets respond to different titles and genres. Analyzing sales data in relation to the publisher can provide insights into successful marketing strategies, while exploring the impact of the release year will help us understand how market dynamics evolve over time.

Utilizing statistical methods and data visualization techniques, this analysis seeks to uncover actionable insights that can inform stakeholders and guide strategic decisions in game development and marketing. As we navigate through this data, we aim to contribute to a deeper understanding of the video game market landscape and its ever-changing nature.
    """)

elif option == "Dataset":
    st.header("Dataset Overview")
    
    st.subheader("Preview of the Dataset")
    st.write(sales.head())
    
    st.subheader("Missing Data Overview")
    st.markdown("""
        The following matrix visualizes any missing data within the dataset. It's crucial to identify missing values early in the analysis process as they can significantly impact the quality of our insights.
        """)
    st.image("outputgamematrix.png", caption="Missing Data Matrix", use_column_width=True)

    st.subheader("Dataset Statistics")
    st.write(sales.describe())
    
    st.markdown("""
    The dataset consists of several columns with sales figures from different regions, including North America (NA), Europe (EU), Japan (JP), and global sales. Here's a quick review:
    
    - *Mean and Median*: Indicate the average and middle sales figures respectively. 
    - *Standard Deviation*: Reflects the variability of the sales data.
    - *Minimum and Maximum*: Show the range of sales, from the lowest to the highest observed in the dataset.
    
    These statistics give us an initial overview of the spread and concentration of sales figures across different regions.
    """)

    

    # Display statistics for each sales column with interpretation
    st.header("Sales Statistics by Region")
    st.markdown("""
    Below, statistical insights are provided for video game sales in different regions, including North America (NA), Europe (EU), Japan (JP), and Global sales:
    """)
    
    def print_statistics(column_name, column_data):
        stats = {
            "Mean": column_data.mean(),
            "Standard Deviation": column_data.std(),
            "Minimum": column_data.min(),
            "Maximum": column_data.max(),
            "Median": column_data.median()
        }
        return stats

    # Loop through sales columns and display statistics for each region
    for column_name in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales']:
        column_data = sales[column_name]
        st.subheader(f"Statistics for {column_name.replace('_', ' ')}")
        stats = print_statistics(column_name, column_data)
        st.write(stats)
        
        # Add interpretations for each region's sales
        if column_name == 'NA_Sales':
            st.markdown("""
            *North American Sales (NA_Sales)*:
            - The highest sales concentration is observed in this region.
            - The spread (as seen by the standard deviation) suggests that some games have exceptionally high sales compared to others.
            """)
        elif column_name == 'EU_Sales':
            st.markdown("""
            *European Sales (EU_Sales)*:
            - The average sales are lower compared to North America.
            - However, there are several games that performed well in Europe, indicated by the maximum sales value.
            """)
        elif column_name == 'JP_Sales':
            st.markdown("""
            *Japanese Sales (JP_Sales)*:
            - Sales in Japan are significantly lower in comparison to NA and EU, indicating a smaller market size or different preferences.
            """)
        elif column_name == 'Global_Sales':
            st.markdown("""
            *Global Sales (Global_Sales)*:
            - These are the total sales figures across all regions.
            - The large standard deviation suggests that global hits significantly outperform others in the market.
            """)

    # Source information
    st.subheader("Source:")
    st.write("""
    This dataset is sourced from Kaggle. You can explore it further here:  
    [Game Sales Data Analysis](https://www.kaggle.com/code/berkkarabilliolu/game-sales-data-analysis-vizualizations-ml-90/notebook)
    """)


elif option == "Visualization":
    st.header("Visualization")
    # Convert sales columns to integers
    sales[['NA Sales', 'EU Sales', 'Japan Sales', 'Other Sales', 'Global Sales']] = sales[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].astype(int)

    
    def plot_sales_distribution(sales_column, column_name):
    # Sort the data by the sales column and select the top 10 games
        top_games = sales[['Name', sales_column]].sort_values(by=sales_column, ascending=False).head(10)
    
    # Create the bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_games['Name'], y=top_games[sales_column])
    
        plt.xlabel('Video Games')
        plt.ylabel(f'{column_name}')
        plt.title(f'Sales {column_name}')
        plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
    
        img = io.BytesIO()  # Save the figure to a buffer
        plt.savefig(img, format='png')
        img.seek(0)
    
        return img



    
    sales_options = ['NA Sales', 'EU Sales', 'Japan Sales', 'Other Sales', 'Global Sales']
    selected_sales_column = st.selectbox("Select a sales category to visualize:", sales_options)

    
    st.subheader(f'{selected_sales_column} Distribution')
    img = plot_sales_distribution(selected_sales_column, selected_sales_column)
    st.image(img, caption=f'{selected_sales_column} Distribution Bar Plot', use_column_width=True)
    plt.close()

   
    if selected_sales_column == 'NA Sales':
        st.write("This bar plot displays the frequency of sales in North America. Higher bars indicate a greater number of games sold in that sales bracket.")
    elif selected_sales_column == 'EU Sales':
        st.write("This bar plot shows the frequency of sales in Europe. The height of the bars reflects the volume of sales per category.")
    elif selected_sales_column == 'Japan Sales':
        st.write("This graph presents the frequency of sales in Japan, illustrating how well games performed in this market.")
    elif selected_sales_column == 'Other Sales':
        st.write("This plot indicates the frequency of sales in regions other than North America, Europe, and Japan, providing insight into global sales dynamics.")
    elif selected_sales_column == 'Global Sales':
        st.write("This bar plot summarizes the global sales frequencies, showing the overall popularity of games across all markets.")


    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    numeric_sales = sales.select_dtypes(include=[np.number])
    plt.figure(figsize=(10, 6))
    sns.heatmap(numeric_sales.corr(), annot=True, linewidths=0.5)
    plt.title('Correlation Heatmap for Sales Data', fontsize=16)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    st.image(img, caption='Correlation Heatmap', use_column_width=True)
    plt.close()


    st.markdown("""
    The heatmap visualizes the relationship between sales in different regions.
    """)


    #PIECHART
    st.subheader("Piecharts: Top 10 Game Sales by Region")
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
        st.markdown("These are the top 10 video games based on total global sales. The chart shows the distribution of sales among the best-selling games worldwide with Wii Sports being the highest percentage. It's popularity comes from the majority of NA and EU regions.")

    elif region == "North America":
        sales = pd.read_csv('vgsales.csv')
        st.subheader("Top 10 Sales in North America by Game")
        top10_na_sales = sales[['Name', 'NA_Sales']].sort_values(by='NA_Sales', ascending=False).head(10)
        labels = top10_na_sales['Name']
        sizes = top10_na_sales['NA_Sales']
        plot_pie_chart(sizes, labels, 'Top 10 Sales in North America')
        st.markdown("These are the top 10 video games based on sales in North America. The chart highlights how each game performed in this region with Wii sports being most popular of 19.9 percent of the chart. It's easy nature encourages families and social gatherings to enjoy casual sports game or friendly competition compared to the other top games.")

    elif region == "Europe":
        sales = pd.read_csv('vgsales.csv')
        st.subheader("Top 10 Sales in Europe by Game")
        top10_eu_sales = sales[['Name', 'EU_Sales']].sort_values(by='EU_Sales', ascending=False).head(10)
        labels = top10_eu_sales['Name']
        sizes = top10_eu_sales['EU_Sales']
        plot_pie_chart(sizes, labels, 'Top 10 Sales in Europe')
        st.markdown("These are the top 10 video games based on sales in Europe. The pie chart shows the market share of each game in this region. Similar to the NA region, Wii sports has the highest sale percentage of 24.5 percent.")

    elif region == "Japan":
        sales = pd.read_csv('vgsales.csv')
        st.subheader("Top 10 Sales in Japan by Game")
        top10_jp_sales = sales[['Name', 'JP_Sales']].sort_values(by='JP_Sales', ascending=False).head(10)
        labels = top10_jp_sales['Name']
        sizes = top10_jp_sales['JP_Sales']
        plot_pie_chart(sizes, labels, 'Top 10 Sales in Japan')
        st.markdown("These are the top 10 video games based on sales in Japan. The chart represents the dominance of various titles in the Japanese market with Pokemon Red/Pokemon Blue being the highest sale percentage of 16.1 percent. Japan prefers role playing action games, as seen in the graphs majority in the chart consist of role playing games.")

elif option == "Conclusion":
    st.header("Conclusion")
    st.write("From the analysis of the dataset, we derived several meaningful insights into Nintendo's enduring influence on the gaming market from 1980 to 2020. One of the most striking trends was Nintendo's consistent presence in the top 10 best-selling games across various regions, demonstrating the company's significant impact on the global gaming landscape. Iconic titles from franchises such as Super Mario have maintained high sales figures over decades, highlighting the brand's ability to captivate audiences across generations.This era brought gaming into households that traditionally may not have been interested, appealing to a broader demographic and solidifying Nintendo's reputation for family-friendly entertainment.The success of Nintendo titles is not just a reflection of the games themselves but also of the brand's ability to adapt and resonate with evolving consumer preferences. This ongoing relationship between Nintendo and its audience underscores the company's enduring relevance in the gaming world and its role to shaping the industry's future.")
