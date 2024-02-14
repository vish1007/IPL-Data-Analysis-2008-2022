import streamlit as st
import psycopg2
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##initization of database for login/registration queries
dbname = "IPLdata"
user = "postgres"
db_password = "postgres"
host = "localhost"

# Set page title
st.set_page_config(page_title="IPL Dashboard", page_icon="🏏",layout="centered")

# Set background image using CSS
background_image_url = "https://wallpapercave.com/wp/wp1809746.jpg"
background_style = f"""
    <style>
        .stApp {{
            background-image: url("{background_image_url}");
            background-size: 100% 100%;
            background-repeat: no-repeat;
            background-attachment: fixed;
            
        }}
    </style>
"""

##Apply the background style
##unsafe_allow_html=True: This parameter in st.markdown() allows the rendering of HTML content. By default, Streamlit blocks the rendering of HTML for security reasons.
##Setting unsafe_allow_html=True permits the rendering of HTML content.
st.markdown(background_style, unsafe_allow_html=True)

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource(max_entries=1, ttl=600)
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# Function to fetch and display data
def display_data(query, column_titles, subheading, limit=None):
    rows = run_query(query)
    data = pd.DataFrame(rows, columns=column_titles)
    
    if limit:
        st.subheader(subheading)
        st.dataframe(data.head(limit).style.set_properties(**{'font-size': '16px', 'font-weight': 'bold'}), use_container_width=True)
    else:
        st.subheader(subheading)
        st.dataframe(data.style.set_properties(**{'font-size': '16px', 'font-weight': 'bold'}), use_container_width=True)

# Function to get years for dropdown
def get_years():
    years_query = "SELECT DISTINCT EXTRACT(YEAR FROM match_date) as year FROM matches ORDER BY year;"
    years = run_query(years_query)
    years = [str(year[0]) for year in years]
    years.insert(0, "All Years")
    return years

# Define user_login and admin_login functions
def user_login(username, password):
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=db_password, host=host)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        valid = cursor.fetchone() is not None
        cursor.close()
        connection.close()
        return valid
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def admin_login(username, password):
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=db_password, host=host)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        valid = cursor.fetchone() is not None
        cursor.close()
        connection.close()
        return valid
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# Define the registration function
def register_user(username, password):
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=db_password, host=host)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def User_dashboard():
    st.title("User Dashboard")
    st.write("Welcome to the user dashboard!")

def login_page():
    st.title("IPL-Data Insights(2008-2022)!!")
    
        # User Registration
    new_username = st.text_input("Enter New Username:")
    new_password = st.text_input("Enter New Password:", type="password")
    confirm_password = st.text_input("Confirm Password:", type="password")

    # Handling empty fields during registration
    if st.button("Register Now"):
        if not new_username or not new_password or not confirm_password:
            st.error("Please enter username, password, and confirm password.")
        elif new_password != confirm_password:
            st.error("Passwords do not match. Please re-enter.")
        else:
            if register_user(new_username, new_password):
                st.success("User registration successful! You can now log in.")
                st.session_state.logged_in = False
                st.session_state.user_role = None
            else:
                st.error("Failed to register user. Please try again.")


    # Login Section
    st.write("Already have an account? Login Here:")
    username = st.text_input("Enter Username:")
    password = st.text_input("Enter Password:", type="password")
    role = st.selectbox("Role", ["User", "Admin"])

 
    if st.button("Login Now"):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            if role == "Admin":
                if admin_login(username, password):
                    #st.session_state.logged_in = True
                    #st.session_state.user_role = "Admin"
                    #st.write("Successfully logged In!!")
                    st.session_state.user_role = "Admin"
                    #admin_dashboard()
                    st.session_state.logged_in = True
                    st.rerun()

                else:
                    st.error("Failed to admin-login!!")
            elif role == "User":
                if user_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.user_role = "User"
                    #st.write("Successfully logged In!!")
                    st.rerun()
                else:
                    st.error("Failed to user-login!!")



# Main App
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

if not st.session_state.logged_in:
    if st.session_state.user_role == "Admin":
        st.write("admin dashboard")
    elif st.session_state.user_role == "User":
        st.write("user dashboard")
    else:
        login_page()
else:
    if st.button("Logout", key="logout_button", help="Click to log out"):
        st.session_state.logged_in = False
        st.session_state.user_role = None         ##need for logout completely
        st.session_state.expire_on_browser_close = True
        st.rerun()
    if st.session_state.user_role == "Admin":
        st.write("Welcome to the admin dashboard!")
        if st.button("All User Data"):
            query_users = "SELECT user_id,username,password FROM users;"
            column_titles = ["ID", "Username", "Password"]
            subheading = "Users Data"
            display_data(query_users, column_titles, subheading)
            # Display database credentials for admin
        st.subheader("Database Credentials:")
        st.write(f"Database Name: {dbname}")
        st.write(f"User: {user}")
        st.write(f"Host: {host}")
    
    st.write("<h4>Welcome to exciting journey of unraveling the mysteries of cricket through data!</h4>", unsafe_allow_html=True)
    st.sidebar.title('IPL Dashboard(2008-22)')
    st.write('''Explore the thrilling world of cricket as we delve into the intricacies of 
                the sport through insightful data analysis. Welcome to the IPL Dashboard (2008-22),
              your gateway to uncovering the secrets behind every match, player, and venue. 
             Embark on an exciting journey through the statistics that define the essence of cricket's premier league''', 
             unsafe_allow_html=True)
    a="1.Team's Winning Venues"
    b="2.Batsmen's Performance in a Match"
    c="3.Bowlers' Performance in a Match"
    d="4.Top 10 Batsmen in a Year."
    e="5.Top 10 Bowlers in a Year"
    f="6.Toss Impact on Match Results"
    g="7.Batsman vs. Bowler: Key Dismissals"
    h="8.Best Batsman per Match in a Year"
    i="9.Top 5 Bowlers as Batsmen in a Year"


    x="Batting Records"
    y="Bowling Records"
    selected_page1 = st.sidebar.selectbox("Select Option", ["Select any Question",x,y])
    selected_question = st.sidebar.selectbox("Select Question", ["Select any Question", a, b, c, d, e, f, g, h, i])

    if selected_question=="Select any Question":

        # Select year
        
        if selected_page1.startswith(x):
            selected_year = st.selectbox("Select Year", get_years())
        # Select number of entries to display
            selected_limit = st.select_slider("Select Number of Entries", options=[20,40,60,80,100])
            query_batting_records = f"SELECT player_name, SUM(runs_scored) FROM batting, matches, players WHERE batting.match_id=matches.match_id AND players.player_id=batting.player_id AND EXTRACT(YEAR FROM matches.match_date) = {selected_year if selected_year != 'All Years' else 'EXTRACT(YEAR FROM matches.match_date)'} GROUP BY player_name ORDER BY SUM(runs_scored) DESC;"
            display_data(query_batting_records, ["Player Name", "Total Runs"], f"All Batting Records ({selected_year if selected_year != 'All Years' else 'All Years'})", selected_limit)
        elif selected_page1.startswith(y):
            selected_year = st.selectbox("Select Year", get_years())
        # Select number of entries to display
            selected_limit = st.select_slider("Select Number of Entries", options=[20,40,60,80,100])
            query_bowling_records = f"SELECT player_name, SUM(wicket_delivery) FROM bowling, matches, players WHERE bowling.match_id=matches.match_id AND players.player_id=bowling.player_id AND bowling.dismissal_kind NOT IN ('retired hurt', 'retired out', 'run out', 'obstructing the field') AND EXTRACT(YEAR FROM matches.match_date) = {selected_year if selected_year != 'All Years' else 'EXTRACT(YEAR FROM matches.match_date)'} GROUP BY player_name ORDER BY SUM(wicket_delivery) DESC;"
            display_data(query_bowling_records, ["Player Name", "Total Wickets"], f"All Bowling Records ({selected_year if selected_year != 'All Years' else 'All Years'})", selected_limit)

    if selected_page1=="Select any Question":

                #Defining a function to get year
        def get_years1():
            years_query = "SELECT DISTINCT EXTRACT(YEAR FROM match_date) as year FROM matches ORDER BY year;"
            years1 = run_query(years_query)
            years1 = [str(year[0]) for year in years1]
            return years1
        def draw_plot(data):
        # Create a bar plot using Plotly Express
            fig = px.bar(data, x='Stadium Name', y='Matches Won', color='Team Name',
                        labels={'Stadium Name': 'Stadium Name', 'Matches Won': 'Matches Won'},
                        title='Stadiums Where Each Team Has Won the Maximum Matches')

            # Customize layout
            fig.update_layout(xaxis_title='Stadium Name', yaxis_title='Matches Won')
            fig.update_xaxes(tickangle=90)  # Rotate x-axis labels

            # Display the bar plot in Streamlit
            st.plotly_chart(fig)

    ##for question 1
        if selected_question.startswith(a):
            query = """
            WITH TeamVenueWins AS (
                SELECT
                    team_name,
                    venue_name,
                    COUNT(*) AS match_count
                FROM (
                    SELECT
                        team1_name AS team_name,
                        venue_name
                    FROM
                        matches
                    WHERE
                        winning_team = team1_name

                    UNION ALL

                    SELECT
                        team2_name AS team_name,
                        venue_name
                    FROM
                        matches
                    WHERE
                        winning_team = team2_name
                ) AS subquery
                GROUP BY
                    team_name, venue_name
            )

            SELECT
                DISTINCT ON (team_name)
                team_name AS "Team Name",
                venue_name AS "Stadium Name",
                match_count AS "Matches Won"
            FROM TeamVenueWins
            ORDER BY team_name, match_count DESC;
            """
            result = run_query(query)
            if result:
                st.write(f"### Team Winning Venues")
                st.write("---")
                df = pd.DataFrame(result, columns=["Team Name", "Stadium Name", "Matches Won"])
                draw_plot(df)
                
                
            else:
                st.write("No data found")
    ##for question 4
        elif selected_question.startswith(d):
            st.title("Top 10 Scoring Batsman in a Year")
            yea = st.selectbox("Select Year :", get_years1())   
            query = f"""
        select player_name,sum(runs_scored),count(distinct batting.match_id) AS total_matches_played
    from batting,matches,players 
    where batting.match_id=matches.match_id and players.player_id=batting.player_id and EXTRACT(YEAR FROM matches.match_date) = {yea}
    group by player_name
    order by sum(runs_scored) desc limit 10; 
            """ 
            result = run_query(query)
            if result:
                st.write(f"### IN {yea}")
                st.write("---")
                df = pd.DataFrame(result, columns=["player_name", "totalruns","total_matches_played"])
                fig = px.bar(df, x='player_name', y='totalruns',
                labels={'player_name': 'Player Name', 'totalruns': 'Total Runs'},
                title='Total Runs by Player')

                # Customize layout (optional)
                fig.update_layout(xaxis_title='Player Name', yaxis_title='Total Runs')

                # Display the bar plot in Streamlit
                st.plotly_chart(fig)
            
            else:
                st.write("No data found")

                ##question 5


        elif selected_question.startswith(e):
            st.title("Top 10 Most Wicket Taker(Bowler) in a Year")
            year_input = st.selectbox("Select Year :", get_years1())      
            query = f"""
            select player_name,sum(wicket_delivery) as total_wickets
    from bowling,matches,players 
    where bowling.match_id=matches.match_id and players.player_id=bowling.player_id and bowling.dismissal_kind NOT IN ('retired hurt', 'retired out', 'run out', 'obstructing the field') and EXTRACT(YEAR FROM matches.match_date) = {year_input}
    group by player_name 
    order by sum(wicket_delivery) desc limit 10; 
            """ 
            result = run_query(query)
            if result:
                st.write(f"### IN {year_input}")
                st.write("---")
                df = pd.DataFrame(result, columns=["player_name", "total_wickets"])
                #col1, col2 = st.columns([1, 2])
                # Display table in the first column
                #with col1:
                #st.write(df)

                # Display bar plot in the second column
                #with col2:
                bubble_sizes = df['total_wickets']  # You can change this to another column if needed

    # Create a bubble plot using Plotly Express
                fig = px.scatter(df, x='player_name', y='total_wickets', size=bubble_sizes, color='player_name',
                                labels={'player_name': 'Player Name', 'total_wickets': 'Total Wickets'},
                                title='Bubble Plot: Total Wickets Taken by Players',
                                hover_data={'total_wickets': True})

                # Customize layout
                fig.update_layout(xaxis_title='Player Name', yaxis_title='Total Wickets')

                # Display the bubble plot in Streamlit
                st.plotly_chart(fig)

                # Show total wickets on each bar
            
            else:
                st.write("No data found")

    ##Question 2


        elif selected_question.startswith(b):
            # Function to fetch data based on selected match ID
            def get_runs_by_batsmen(match_id):
                query = f"""
                    WITH RunsScored AS (
                SELECT
                    player_id,
                    SUM(runs_scored) AS total_runs
                FROM
                    batting
                WHERE
                    match_id = {match_id} 
                GROUP BY
                    player_id
            ),
            DismissalTypes AS (
                SELECT
                    player_id,
                    dismissal_kind
                FROM
                    batting
                WHERE
                    match_id = {match_id}
                    AND dismissal_kind IS NOT NULL
            )
            SELECT
                p.player_name AS "Batsman",
                COALESCE(rs.total_runs, 0) AS "Total Runs",
                COALESCE(dt.dismissal_kind, 'Not Dismissed') AS "Dismissal Type"
            FROM
                players AS p
            right JOIN RunsScored AS rs ON p.player_id = rs.player_id
            right JOIN DismissalTypes AS dt ON p.player_id = dt.player_id;

                """
                with conn.cursor() as cur:
                    cur.execute(query)
                    data = cur.fetchall()
                    columns = ['Player Name', 'Total Runs', 'Dismissal']
                    return pd.DataFrame(data, columns=columns)

            # Function to get distinct match IDs from the database
        
            def get_match_ids():
                query = "SELECT DISTINCT match_id FROM batting order by match_id ;"
                with conn.cursor() as cur:
                    cur.execute(query)
                    match_ids = [row[0] for row in cur.fetchall()]
                    return match_ids

            # Main Streamlit app
            st.title("Batsmen Performance in a Match")

            # Get the available match IDs
            match_ids = get_match_ids()

            # Display dropdown to select match ID
            selected_match_id = st.selectbox("### Select Match ID:", match_ids)

            if selected_match_id:
                st.write(f"### In Match: {selected_match_id}")
                st.write("---")
                batsmen_data = get_runs_by_batsmen(selected_match_id)

                if not batsmen_data.empty:
                    plt.figure(figsize=(11, 7))
                    ax = sns.barplot(data=batsmen_data, x='Player Name', y='Total Runs',hue='Dismissal')
                    plt.xlabel('Player Name', fontsize=15)
                    plt.ylabel('Total Runs', fontsize=15)
                    plt.title('Batsmen Performance in a Match"', fontsize=14)
                    plt.xticks(rotation=90,fontsize=15)
                    plt.legend(title='Dismissal', fontsize='large', title_fontsize='15')
                    # Show total wickets on each bar
                    for index, row in batsmen_data.iterrows():
                        ax.text(index, row['Total Runs'], str(row['Total Runs']), color='black', ha="center",fontsize=15)
                    st.pyplot(plt)
                    #st.write(batsmen_data)
                else:
                    st.write("No data available for the selected match ID.")


        ## question 3


        elif selected_question.startswith(c):
            # Function to fetch data based on selected match ID
            def get_wickets_by_bowler(match_id):
                query = f"""
                    select players.player_name,sum(bowling.wicket_delivery)
    from bowling,players
    where bowling.match_id={match_id} and bowling.dismissal_kind NOT IN ('retired hurt', 'retired out', 'run out', 'obstructing the field')
    and bowling.player_id=players.player_id
    group by players.player_name

                """
                with conn.cursor() as cur:
                    cur.execute(query)
                    data = cur.fetchall()
                    columns = ['Player Name', 'Total Wickets']
                    return pd.DataFrame(data, columns=columns)

            # Function to get distinct match IDs from the database
        
            def get_match_ids():
                query = "SELECT DISTINCT match_id FROM bowling order by match_id;"
                with conn.cursor() as cur:
                    cur.execute(query)
                    match_ids = [row[0] for row in cur.fetchall()]
                    return match_ids

            # Main Streamlit app
            st.title("Bowler Performance in a Match")

            # Get the available match IDs
            match_ids = get_match_ids()

            # Display dropdown to select match ID
            selected_match_id = st.selectbox("## Select Match ID:", match_ids)

            if selected_match_id:
                st.write(f"### Showing data for Match ID: {selected_match_id}")
                bowler_data = get_wickets_by_bowler(selected_match_id)

                if not bowler_data.empty:
                # Choose the type of plot using a selectbox
                    plot_type = st.selectbox('Select Plot Type:', ['Select one','Bar Chart', 'Pie Chart'])

        
                    if plot_type == 'Bar Chart':
                        st.write(f"### In Match {selected_match_id}")
                        st.write("Bar Chart:")
                        fig_bar = px.bar(bowler_data, x='Player Name', y='Total Wickets', title='Total Wickets Taken by Players')
                        fig_bar.update_xaxes(title='Player Name')
                        fig_bar.update_yaxes(title='Total Wickets')
                        st.plotly_chart(fig_bar)

                    # Plotting pie chart in the second column
                    elif plot_type == 'Pie Chart':
                        st.write(f"### In Match {selected_match_id}")
                        st.write("Pie Chart:")
                        fig_pie = px.pie(bowler_data, values='Total Wickets', names='Player Name', title='Wickets Distribution by Players')
                        fig_pie.update_traces(textinfo='percent+label')
                        st.plotly_chart(fig_pie)
                        
                else:
                    st.write("No data available for the selected match ID.")


    ##Question 6

        elif selected_question.startswith(f):
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM toss WHERE winning_team = toss_winner;")
                matches_won = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM toss WHERE winning_team <> toss_winner;")
                matches_lost = cur.fetchone()[0]

        
            # Create a DataFrame with the counts
            data = {'Result': ['Matches Won by Winning Toss', 'Matches Lost by Winning Toss'],
                    'Count': [matches_won, matches_lost]}

            # Create a Streamlit app
            st.title('Relationship between Winning Toss and Winning Match')
            st.write("---")
            # Create a pie chart using Plotly
            fig = px.pie(data, values='Count', names='Result', title='Winning Toss vs. Winning Match')
            fig.update_traces(hovertemplate='<b>%{label}</b><br>%{percent}<br><br><i>Count</i>: %{value}', 
                    textfont=dict(size=20))
            st.plotly_chart(fig)

    ##Question 7

        elif selected_question.startswith(g):
            st.title("Top Bowler vs. Batsman Dismissals")
            def get_distinct_player_names():
                conn = psycopg2.connect(**st.secrets["postgres"])
                query = "SELECT DISTINCT player_name FROM players JOIN batting ON players.player_id = batting.player_id"
                
                with conn.cursor() as cur:
                    cur.execute(query)
                    player_names = [row[0] for row in cur.fetchall()]
                return player_names

            player_names = get_distinct_player_names()
            selected_player = st.selectbox("Select Player", player_names)
            st.write(f"### Against which bowler did {selected_player} get out most often?")
            if selected_player:
                # Execute query for specific player
                conn = psycopg2.connect(**st.secrets["postgres"])
                query = """
                    SELECT bowler_name, COUNT(dismissal_id) AS num_dismissals
                    FROM dismissals
                    WHERE batsman_name = %s
                    GROUP BY bowler_name
                    ORDER BY COUNT(dismissal_id) DESC
                    LIMIT 3;
                """
                with conn.cursor() as cur:
                    cur.execute(query, (selected_player,))
                    data = cur.fetchall()

                if data:
                    columns = ['Bowler Name', 'Number of times wicket taken']
                    df = pd.DataFrame(data, columns=columns)
                    fig = px.bar(df, x='Bowler Name', y='Number of times wicket taken', color='Bowler Name',
                    title=f"Most Frequent Dismissals of {selected_player} by {', '.join(df['Bowler Name'].tolist()) if not df.empty else 'Bowler'}")
                    st.plotly_chart(fig)
                else:
                    st.write(f"No data found for '{selected_player}'.")
        
        ##Question 8
        elif selected_question.startswith(h):
            
            # Function to fetch data based on selected match ID
            def get_best_batsman(year):
                query = f"""
    WITH TotalRunsByBatsman AS (
        SELECT
            b.match_id,
            b.player_id,
            p.player_name,
            SUM(b.runs_scored) AS total_runs_scored
        FROM
            Batting b
        JOIN Players p ON b.player_id = p.player_id
        JOIN Matches m ON b.match_id = m.match_id
        WHERE
            EXTRACT(YEAR FROM m.match_date) = {year} 
        GROUP BY
            b.match_id, b.player_id, p.player_name
    )
    SELECT
        trb.match_id,
        trb.player_name,
        trb.total_runs_scored
    FROM
        TotalRunsByBatsman trb
    WHERE
        trb.total_runs_scored = (
            SELECT MAX(total_runs_scored)
            FROM TotalRunsByBatsman trb2
            WHERE trb.match_id = trb2.match_id
        )
    ORDER BY trb.match_id;

                """
                with conn.cursor() as cur:
                    cur.execute(query)
                    data= cur.fetchall()
                    columns = ['Match ID', 'Player Name','Total Runs Scored']
                    return pd.DataFrame(data, columns=columns)

            st.title("Best Batsman per Match in a Year")
            sele_year = st.selectbox("Select Year :", get_years1())
            if sele_year:
                st.write(f"### IN Year: {sele_year}")
                bat_data = get_best_batsman(sele_year)
                st.write(bat_data)
            else:
                st.write("No data available for the selected match ID.")

    ##Question 9

        elif selected_question.startswith(i): 
            st.title("Top 5 Bowlers as Batsmen in a Year")
            years = ["Select"] + get_years1()  # Assuming get_years1() retrieves a list of available years
            selected_year = st.selectbox("Select Year:", years)

            def bow_as_bat(selected_year):
                if selected_year != "Select":
                    query = """
                    
                SELECT
                    p.player_name,
                    SUM(b.runs_scored) AS total_runs,
                    COUNT(b.player_id) AS balls_faced
                FROM
                    batting b
                    JOIN players p ON b.player_id = p.player_id
                    JOIN (
                        SELECT
                            player_id
                        FROM
                            bowling
                        JOIN matches ON bowling.match_id = matches.match_id
                        WHERE
                            EXTRACT(YEAR FROM matches.match_date) = %s
                        GROUP BY
                            player_id
                        HAVING
                            COUNT(*) > 100
                    ) AS bowlers ON b.player_id = bowlers.player_id
                    JOIN matches m ON b.match_id = m.match_id
                WHERE
                    EXTRACT(YEAR FROM m.match_date) = %s
                GROUP BY
                    b.player_id, p.player_name
                HAVING
                    COUNT(b.player_id) < 100
                ORDER BY
                    total_runs DESC
                LIMIT 5;
                    """
                    # Execute the query
                    if selected_year != "Select":
                        selected_year_int = int(selected_year)  # Convert selected_year to integer
                        # Execute the query
                        with conn.cursor() as cur:
                            cur.execute(query, (selected_year_int, selected_year_int))
                            results = cur.fetchall()
                            columns = ["Bowler Names", "Total runs", "Balls faced"]
                            return pd.DataFrame(results, columns=columns)

            if selected_year:
                bowlers_data = bow_as_bat(selected_year)
                if bowlers_data is not None:        
                    st.write(bowlers_data)
                else:
                    st.write("No data available for the selected year.")

        

    
 


            
                


    
    


     
       