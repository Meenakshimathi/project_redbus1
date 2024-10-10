import streamlit as st
import pymysql
import pandas as pd

# Connect to MySQL database
def g_connect():
    return pymysql.connect(host='127.0.0.1', user='root', passwd='Ajay2017', database='bus')

# Function to fetch route names starting with a specific letter, arranged alphabetically
def fetch_routenames(connection, table_name):
    query = f"SELECT DISTINCT Route_name FROM {table_name} ORDER BY Route_name"
    route_names = pd.read_sql(query, connection)['Route_name'].tolist()
    return route_names

# Function to fetch data from MySQL based on selected ROUTE_NAME and price range
def fetch_data(connection, table_name, route_name, min_price, max_price):
    query = f"SELECT * FROM {table_name} WHERE Route_name = %s AND Price BETWEEN %s AND %s ORDER BY Ratings DESC, Price"
    df = pd.read_sql(query, connection, params=(route_name, min_price, max_price))
    return df

# Function to filter data based on RATING and BUS_TYPE
def filter_data(df, ratings, bus_type):
    filtered_df = df[df['Ratings'].isin(ratings) & df['Bus_type'].isin(bus_type)]
    return filtered_df

def main():
    # Set overall page layout
    st.set_page_config(page_title="Ajay Transport App", layout="wide")

    # CSS styles for different sections
    st.markdown(
        """
        <style>
        .section1 {
            background-color: #FFDDC1;  /* Light peach */
            padding: 20px;
            border-radius: 10px;
        }
        .section2 {
            background-color: #D1FAE5;  /* Light green */
            padding: 20px;
            border-radius: 10px;
        }
        .section3 {
            background-color: #D1E7FF;  /* Light blue */
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Section 1: Introduction
    st.markdown('<div class="section1">', unsafe_allow_html=True)
    st.header("Ajay Transport")
    st.write("Transportation between states like Kerala, Andhra Pradesh, Telangana, Chandigarh, Rajasthan, West Bengal, Himachal Pradesh, Assam, Uttar Pradesh, West Bengal WBTC.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 2: Features
    st.markdown('<div class="section2">', unsafe_allow_html=True)
    st.header("Features")
    st.write(""" 
- Safe transportation
- More than 100,000 customers
- Point-to-point services
- Affordable prices
""")
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 3: Contact Us
    st.markdown('<div class="section3">', unsafe_allow_html=True)
    st.header("Contact Us")
    st.write("Email: Ajay@gmail.com | Phone: 0808080808")
    st.markdown('</div>', unsafe_allow_html=True)

    # Transport Booking Section
    st.markdown(
        '<marquee style="color:green; font-family:sans-serif; font-size:30px; text-align:center;">Ajay Transport::Online Bus Tickets Booking</marquee>', 
        unsafe_allow_html=True
    )

    # List of state transport corporations and their corresponding table names
    transport_options = {
        "Kerala KSRTC": "kerala2",
        "Andhra Pradesh APSRTC": "ap1",
        "Telangana TSRTC": "tsrtc2",
        "Chandigarh CHA": "cha2",
        "Rajasthan RSRTC": "rsrtc2",
        "West Bengal SBSTC": "bengal2",
        "Himachal Pradesh HRTC": "hrtc2",
        "Assam ASTC": "astc1",
        "Uttar Pradesh UPSRTC": "up2",
        "West Bengal WBTC CTC": "wbtc2"
    }

    connection = g_connect()

    try:
        # Sidebar for transport corporation selection
        selected_transport = st.sidebar.radio("Select Transport Corporation", list(transport_options.keys()))

        if selected_transport:
            table_name = transport_options[selected_transport]

            # Fetch all route names from the selected table
            route_names = fetch_routenames(connection, table_name)

            if route_names:
                # Sidebar - Selectbox for ROUTE_NAME
                selected_route = st.sidebar.selectbox('Select Route Name', route_names)

                if selected_route:
                    # Sidebar - Slider for selecting price range
                    min_price, max_price = st.sidebar.slider(
                        'Select Price Range',
                        min_value=0,  # Assuming 0 is the minimum price
                        max_value=6000,  # Assuming 6000 is the maximum price
                        value=(50, 2500)  # Default selected range
                    )

                    # Fetch data based on selected ROUTE_NAME and price range
                    data = fetch_data(connection, table_name, selected_route, min_price, max_price)

                    if not data.empty:
                        # Display data table with a subheader
                        st.write(f"### Route: {selected_route} & Price Range: {min_price} - {max_price}")
                        st.write(data)

                        # Filter by RATING and BUS_TYPE
                        ratings = data['Ratings'].unique().tolist()
                        selected_ratings = st.sidebar.multiselect('Filter by Ratings', ratings)

                        bus_types = data['Bus_type'].unique().tolist()
                        selected_bus_types = st.sidebar.multiselect('Filter by Bus Type', bus_types)

                        if selected_ratings and selected_bus_types:
                            filtered_data = filter_data(data, selected_ratings, selected_bus_types)
                            # Display filtered data table with a subheader
                            st.write(f"### selected Rating: {selected_ratings} and Bus Type: {selected_bus_types}")
                            st.write(filtered_data)

                        # Booking Box
                        st.subheader("Book Your Tickets")
                        with st.form(key='booking_form'):
                            name = st.text_input("Your Name")
                            email = st.text_input("Your Email")
                            phone = st.text_input("Your Phone Number")
                            tickets = st.number_input("Number of Tickets", min_value=1, value=1)
                            bus_details = st.selectbox("Select Bus", data['Bus_type'].unique())
                            
                            # Submit button
                            submit_button = st.form_submit_button("Book Now")

                            if submit_button:
                                st.success(f"Thank you, {name}! Your booking for {tickets} ticket(s) on route '{selected_route}' with bus '{bus_details}' has been received.")
                                st.write(f"Details: Name: {name}, Email: {email}, Phone: {phone}, Tickets: {tickets}, Route: {selected_route}, Bus: {bus_details}")

                    else:
                        st.write(f"No data found for Route: {selected_route} within Price Range: {min_price} - {max_price}")
            else:
                st.write("No routes found.")
        else:
            st.write("Please select a transport corporation to proceed.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    main()
