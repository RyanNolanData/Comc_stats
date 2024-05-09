import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime, timedelta
import seaborn as sns

st.set_page_config(layout="wide")

def extract_year(set_name):
    match = re.search(r'\b\d{4}\b', set_name)
    if match:
        return int(match.group())
    else:
        return None

def main():
    st.title("COMC Seller Stats Expanded")

    st.write('Welcome to the COMC Seller Stats Breakdown app. This was created by Ryan Nolan (Breakout Cards / Ryan Nolan Data on YouTube)')
    st.write("This App is Free. If you want to help support it, please consider buying a card from my [COMC store](https://www.comc.com/Users/breakoutsports,sr,i100)")
    st.write('Upload your Spreadsheets down below to get started. I do not store any of this data. The code behind this app is on my Github page')
    st.write('Looking to have some data analyzed for your business? Or Need help with a Data Project? I take on Freelance work. Email me at ryannolandata@gmail.com (Also open to full time job opportunities)')

    # Upload file
    file = st.file_uploader("Upload a spreadsheet (CSV or Excel file)", type=["csv", "xlsx"])

    if file is not None:
        # Read file
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
   #     elif file.name.endswith('.xlsx'):
   #         df = pd.read_excel(file, engine='openpyxl')

            # Show date range selector
            st.title("Sold Date Range Selector")
            date_range_option = st.selectbox("Select Date Range", ["Custom", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Last 180 Days"])
            
            if date_range_option == "Custom":
                min_date = pd.to_datetime(df['Date Sold']).min().date()
                max_date = pd.to_datetime(df['Date Sold']).max().date()
                start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
                end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
            elif date_range_option == "Last 7 Days":
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=6)
            elif date_range_option == "Last 30 Days":
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=29)
            elif date_range_option == "Last 90 Days":
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=89)
            elif date_range_option == "Last 180 Days":
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=179)

            # Filter dataframe by selected date range
            filtered_df = df[(pd.to_datetime(df['Date Sold']).dt.date >= start_date) & 
                            (pd.to_datetime(df['Date Sold']).dt.date <= end_date)]
            

            st.title("Aquired Date Range Selector")
            date_range_option = st.selectbox("Select Acquired Date Range", ["Custom", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Last 180 Days"], key='Sales_Date')
            
            if date_range_option == "Custom":
                min_date_acq = pd.to_datetime(df['Acquisition Date']).min().date()
                max_date_acq = pd.to_datetime(df['Acquisition Date']).max().date()
                start_date_acq = st.date_input("Start Date", min_value=min_date_acq, max_value=max_date_acq, value=min_date_acq)
                end_date_acq = st.date_input("End Date", min_value=min_date_acq, max_value=max_date_acq, value=max_date_acq)
            elif date_range_option == "Last 7 Days":
                end_date_acq = datetime.now().date()
                start_date_acq = end_date_acq - timedelta(days=6)
            elif date_range_option == "Last 30 Days":
                end_date_acq = datetime.now().date()
                start_date_acq = end_date_acq - timedelta(days=29)
            elif date_range_option == "Last 90 Days":
                end_date_acq = datetime.now().date()
                start_date_acq = end_date_acq - timedelta(days=89)
            elif date_range_option == "Last 180 Days":
                end_date_acq = datetime.now().date()
                start_date_acq = end_date_acq - timedelta(days=179)

            # Filter dataframe by selected date range
            filtered_df = df[(pd.to_datetime(df['Acquisition Date']).dt.date >= start_date_acq) & 
                            (pd.to_datetime(df['Acquisition Date']).dt.date <= end_date_acq)]
            


            st.title("Sales Price Selector")
            sales_price_option = st.selectbox("Select Sales Price Range", ["Custom", "Under 39 Cents", "Under 75 Cents", "Under $2.51", "Over $2.50"], key='Acquired_Date')

            if sales_price_option == "Custom":
                min_price = 0.01
                max_price = 100000
                start_price = st.number_input("Start Price", min_value=float(min_price), max_value=float(max_price), value=float(min_price))
                end_price = st.number_input("End Price", min_value=float(min_price), max_value=float(max_price), value=float(max_price))
            elif date_range_option == "Under 39 Cents":
                start_price = min_price
                end_price = 0.39
            elif date_range_option == "Under 75 Cents":
                start_price = min_price
                end_price = 0.75
            elif date_range_option == "Under $2.51":
                start_price = min_price
                end_price = 2.50
            elif date_range_option == "Over $2.50":
                start_price = 2.51
                end_price = max_price

            #look at 10, 25, 50

            filtered_df = filtered_df[(filtered_df['Sale Price'] >= start_price) & (filtered_df['Sale Price'] <= end_price)]
            
            st.title("Added vs Flipped Selector")
            Added_Select = st.checkbox("Added", value=True)
            Flipped_Select = st.checkbox("Flipped", value=True)

            # Apply filters based on checkbox selections
            if Added_Select and not Flipped_Select:
                # Show only added cards
                filtered_df = filtered_df[filtered_df['Purchase Price'].isnull()]
            elif Flipped_Select and not Added_Select:
                # Show only flipped cards
                filtered_df = filtered_df[filtered_df['Purchase Price'].notnull()]
            elif Flipped_Select and Added_Select:
                filtered_df = filtered_df
            else:
                # No checkbox selected, show message
                st.write("Please select at least one checkbox")
            

            st.title("Category Selector")

            # Create three columns
            col1, col2, col3 = st.columns(3)

            # Create checkboxes with default value set to True
            with col1:
                Baseball_Select = st.checkbox("Baseball", value=True)
                Football_Select = st.checkbox("Football", value=True)
                Basketball_Select = st.checkbox("Basketball", value=True)
                Hockey_Select = st.checkbox("Hockey", value=True)
                Soccer_Select = st.checkbox("Soccer", value=True)

            with col2:
                Golf_Select = st.checkbox("Golf", value=True)
                Racing_Select = st.checkbox("Racing", value=True)
                MultiSport_Select = st.checkbox("MultiSport", value=True)
                MMA_Select = st.checkbox("MMA", value=True)
                Boxing_Select = st.checkbox("Boxing", value=True)
                Olympic_Select = st.checkbox("Olympic", value=True)

            with col3:
                Wrestling_Select = st.checkbox("Wrestling", value=True)
                Non_Sports_Select = st.checkbox("Non-Sports", value=True)
                Star_Wars_Select = st.checkbox("Star Wars", value=True)
                Marvel_Select = st.checkbox("Marvel", value=True)
                Pokemon_Select = st.checkbox("Pokemon", value=True)

            # "Select All" button logic
            st.write("Select All Button in the future")

            selected_categories = []

            if Baseball_Select:
                selected_categories.append("Baseball")
            if Football_Select:
                selected_categories.append("Football")
            if Basketball_Select:
                selected_categories.append("Basketball")
            if Hockey_Select:
                selected_categories.append("Hockey")
            if Soccer_Select:
                selected_categories.append("Soccer")
            if Golf_Select:
                selected_categories.append("Golf")
            if Racing_Select:
                selected_categories.append("Racing")
            if MultiSport_Select:
                selected_categories.append("MultiSport")
            if MMA_Select:
                selected_categories.append("MMA")
            if Boxing_Select:
                selected_categories.append("Boxing")
            if Olympic_Select:
                selected_categories.append("Olympic")
            if Wrestling_Select:
                selected_categories.append("Wrestling")
            if Non_Sports_Select:
                selected_categories.append("Non-Sports")
            if Star_Wars_Select:
                selected_categories.append("Star Wars")
            if Marvel_Select:
                selected_categories.append("Marvel")
            if Pokemon_Select:
                selected_categories.append("Pokemon")

            # Filter the DataFrame based on selected categories
            if selected_categories:
                filtered_df = filtered_df[filtered_df['Sport'].isin(selected_categories)]
            else:
                st.write("Please select at least one category")

            #additional Calcs and filtering
            filtered_df['Year'] = filtered_df['Set Name'].apply(extract_year)


            col4, col5, col6 = st.columns(3)

            with col4:
                st.title("Sport Breakdown")
                sport_counts = filtered_df['Sport'].value_counts()
                fig, ax = plt.subplots()
                ax.bar(sport_counts.index, sport_counts.values)
                ax.set_xlabel('Sport')
                ax.set_ylabel('Count')
                ax.tick_params(axis='x', rotation=90)
                st.pyplot(fig)


            with col5:
                if 'Year' in filtered_df.columns:
                    min_year = int(filtered_df['Year'].min())
                    max_year = int(filtered_df['Year'].max())
                    decade_start = min_year - min_year % 10
                    decade_end = max_year + (10 - max_year % 10)
                    filtered_df['Decade'] = pd.cut(filtered_df['Year'], bins=range(decade_start, decade_end + 1, 10), right=False)

                    # Plot decade distribution
                    st.title("Decade Distribution")
                    decade_counts = filtered_df['Decade'].value_counts().sort_index()
                    if not decade_counts.empty:
                        fig, ax = plt.subplots()
                        ax.bar(decade_counts.index.astype(str), decade_counts.values)
                        ax.set_xlabel('Decade')
                        ax.set_ylabel('Count')
                        ax.tick_params(axis='x', rotation=90)
                        st.pyplot(fig)
                    else:
                        st.write("No years found in the dataset.")
                else:
                    st.write("No 'Set Name' column found in the dataset.")

            with col6:
                st.title("Quick Stats")
                cards_added = filtered_df['Purchase Price'].isnull().sum()
                cards_flipped = filtered_df['Purchase Price'].notnull().sum()   
                serial_numbered = filtered_df['Qty Manufactured'].notnull().sum()

                avg_purchase_price = filtered_df['Purchase Price'].mean()


                st.write("Cards Manually Added Sold:", cards_added)
                st.write("Flipped Cards Sold:", cards_flipped)

                st.write("Serial Number Cards Sold:", serial_numbered)

                #ebay vs cart vs sellers
                # Grouping by 'Purchased By' column and summing based on conditions
                ebay_count = (filtered_df['Purchased By'] == 'eBay').sum()
                cart_count = (filtered_df['Purchased By'] == '*Cart*').sum()
                comc_count = (filtered_df['Purchased By'] != 'eBay')[filtered_df['Purchased By'] != 'Cart'].sum()  # Assuming anything other than eBay or Cart is Comc


                # Displaying the sums using Streamlit
                st.write("Count of Cards Sold on eBay:", ebay_count)
                st.write("Count of Cards Sold by Cart:", cart_count)
                st.write("Count of Cards Sold to COMC Sellers:", comc_count)




                st.write("Average purchase price of Flip Cards:", round(avg_purchase_price, 2))

                #show data or a tbale for each sport

        #New Dataframe Created
        st.header("Stats Breakdown")
        st.write("The assumption on purchase price is 0.5 per card listed to the site for cards not flipped, 2 for any over 99")
        st.write("This also does not factor in storeage fees at the moment")

        new_data_df = filtered_df


        new_data_df['Purchase Price'].fillna(new_data_df['Sale Price'].apply(lambda x: 2 if x > 99 else 0.5), inplace=True)

        #Profit (comc credit-cost)
        new_data_df['Profit'] = new_data_df['COMC Credit'] - new_data_df['Purchase Price'] 

        #Markup (sale price-purchase)/purchase
        new_data_df['Markup'] = 100 * (new_data_df['Sale Price'] - new_data_df['Purchase Price']) / new_data_df['Purchase Price'] 

        #Days to sale
        new_data_df['Date Sold'] = pd.to_datetime(new_data_df['Date Sold'], format='%m/%d/%Y %I:%M:%S %p')
        new_data_df['Acquisition Date'] = pd.to_datetime(new_data_df['Acquisition Date'], format='%m/%d/%Y %I:%M:%S %p')


        # Calculating the difference and converting it to days
        new_data_df['Days to sale'] = (new_data_df['Date Sold'] - new_data_df['Acquisition Date']).dt.days

        new_data_df['Annualized Return'] = ((new_data_df['Sale Price'] - new_data_df['Purchase Price']) / new_data_df['Purchase Price']) * (365 / new_data_df['Days to sale']) * 100


        #grouped_df = new_data_df.groupby('Sport').agg({'Profit': 'sum', 'Markup': 'median', 'Days to sale': 'median'})
        grouped_df = new_data_df.groupby('Sport').agg({'Profit': 'sum',
                                        'Markup': 'median',
                                        'Days to sale': 'median',
                                        'Annualized Return': 'median',
                                        'Sale Price': ['sum', 'count']})
        
        grouped_df.columns = ['Profit_sum', 'Markup_median', 'Days_to_sale_median', 'Annualized_Return_median', 'Total_sales_amount', 'Sales_count']
        grouped_df = grouped_df[['Profit_sum', 'Total_sales_amount', 'Sales_count', 'Markup_median', 'Days_to_sale_median', 'Annualized_Return_median']]

        grouped_df = grouped_df.round(2)
        grouped_df_sorted = grouped_df.sort_values(by='Profit_sum', ascending=False)

        st.dataframe(grouped_df_sorted, width=1000, height=700)

        st.header("Advanced Profit by Quantile")
        # Group by 'Sport' and calculate deciles
        profit_deciles = new_data_df.groupby('Sport')['Profit'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]).unstack()
        # Reset index for better presentation
        profit_deciles.reset_index(inplace=True)
        # Rename columns for clarity
        profit_deciles.columns = ['Sport', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%']
        profit_deciles = profit_deciles.round(2)
        # Display the deciles
        st.dataframe(profit_deciles, width=1000, height=700)

        st.header("Days to Sale by Quantile")
        # Group by 'Sport' and calculate deciles
        dts_deciles = new_data_df.groupby('Sport')['Days to sale'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]).unstack()
        # Reset index for better presentation
        dts_deciles.reset_index(inplace=True)
        # Rename columns for clarity
        dts_deciles.columns = ['Sport', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%']
        dts_deciles = dts_deciles.round(2)
        # Display the deciles
        st.dataframe(dts_deciles, width=1000, height=700)

        st.header("Markup by Quantile")
        # Group by 'Sport' and calculate deciles
        markup_deciles = new_data_df.groupby('Sport')['Markup'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]).unstack()
        # Reset index for better presentation
        markup_deciles.reset_index(inplace=True)
        # Rename columns for clarity
        markup_deciles.columns = ['Sport', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%']
        markup_deciles = markup_deciles.round(2)
        # Display the deciles
        st.dataframe(markup_deciles, width=1000, height=700)

        st.header("Annualized Return by Quantile")
        # Group by 'Sport' and calculate deciles
        ar_deciles = new_data_df.groupby('Sport')['Annualized Return'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]).unstack()
        # Reset index for better presentation
        ar_deciles.reset_index(inplace=True)
        # Rename columns for clarity
        ar_deciles.columns = ['Sport', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%']
        ar_deciles = ar_deciles.round(2)
        # Display the deciles
        st.dataframe(ar_deciles, width=1000, height=700)

if __name__ == "__main__":
    main()




#I’d like to see correlation between buy and sell and purchase price and time to sell
#I’d like to see sales / profit / time to sell expressed as deciles.  Example 80% of profit came from what purchase price?  Which sale price?  How many days to sell? Etc
#So a table with deciles 10%, 20%, 30% etc 
#No.  I was going to mention that I’d like a separate tabe for submitted cards, using the processing fee as cost basis.
