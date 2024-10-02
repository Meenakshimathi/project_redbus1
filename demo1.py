import streamlit as st
import pymysql
import pandas as pd

# Connect to MySQL database
def get_connection():
    return pymysql.connect(host='127.0.0.1', user='root', passwd='Ajay2017', database='project')

# Function to fetch route names starting with a specific letter, arranged alphabetically
def fetch_Route_name(connection, starting_letter):
    query = f"SELECT DISTINCT Route_name FROM redbus WHERE Route_name LIKE '{starting_letter}%' ORDER BY Route_name"
    Route_name = pd.read_sql(query, connection)['Route_name'].tolist()
    return Route_name

# Function to fetch data from MySQL based on selected ROUTE_NAME and price sort order
def fetch_data(connection, Route_name, price_sort_order):
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    query = f"SELECT * FROM redbus WHERE Route_name = %s ORDER BY Ratings DESC, PRICE {price_sort_order_sql}"
    df = pd.read_sql(query, connection, params=(Route_name,))
    return df

# Function to filter data based on RATING and BUS_TYPE
def filter_data(df, ratings, Bus_type):
    filtered_df = df[df['Ratings'].isin(ratings) & df['Bus_type'].isin(Bus_type)]
    return filtered_df

# Main Streamlit app
def main():
    st.header('Easy and Secure Online Bus Tickets Booking')

    connection = get_connection()

    try:
        # Sidebar - Input for starting letter
        starting_letter = st.sidebar.text_input('Enter Starting Letter of Route Name', 'A')

        # Fetch route names starting with the specified letter
        if starting_letter:
            Route_name = fetch_Route_name(connection, starting_letter.upper())

            if Route_name:
                # Sidebar - Selectbox for ROUTE_NAME
                selected_route = st.sidebar.radio('Select Route Name', Route_name)

                if selected_route:
                    # Sidebar - Selectbox for sorting preference
                    price_sort_order = st.sidebar.selectbox('Sort by Price', ['Low to High', 'High to Low'])

                    # Fetch data based on selected ROUTE_NAME and price sort order
                    data = fetch_data(connection, selected_route, price_sort_order)

                    if not data.empty:
                        # Display data table with a subheader
                        st.write(f"### Data for Route: {selected_route}")
                        st.write(data)

                        # Filter by RATING and BUS_TYPE
                        Ratings = data['Ratings'].unique().tolist()
                        selected_ratings = st.multiselect('Filter by Ratings', Ratings)

                        Bus_type = data['Bus_type'].unique().tolist()
                        selected_Bus_type = st.multiselect('Filter by Bus_type', Bus_type)

                        if selected_ratings and selected_Bus_type:
                            filtered_data = filter_data(data, selected_ratings, selected_Bus_type)
                            # Display filtered data table with a subheader
                            st.write(f"### Filtered Data for Rating: {selected_ratings} and Bus_type: {selected_Bus_type}")
                            st.write(filtered_data)
                    else:
                        st.write(f"No data found for Route: {selected_route} with the specified price sort order.")
            else:
                st.write("No routes found starting with the specified letter.")
    finally:
        connection.close()

if __name__ == '__main__':
    main()
