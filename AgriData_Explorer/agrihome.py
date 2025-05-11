import streamlit as st
import mysql.connector  #SQL COnnector package import 
import pandas as pd
from datetime import   datetime

mydb = mysql.connector.connect( #This method sets up a connection, establishing a session with the MySQL server
    host = "localhost",
    user = "root",
    password=""
)

mycursor = mydb.cursor(buffered=True) #after executing a query, a MySQLCursorBuffered cursor fetches the entire result set from the server and buffers the rows.
mycursor.execute("USE mahe") 
querry="SELECT * FROM `indian_agri_data`"
mycursor.execute(querry)
outt=mycursor.fetchall()
#print("outside ",outt)

#Title for page
st.title('Indian Agri Culture and Development')
#st.header("IAGY") 
page = st.sidebar.selectbox(f"**Pages**",["Home","AgriDetails"])

def query_execution(query,slbox_text,fetch):
       vn = get_data(query)      
       print("VNNNNNNNNNNNNNNNNNNN",vn,"typeeeeeee",type(vn))
       
       print("Fectchhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh",fetch)
       if fetch == "select":
            selected_vn = st.selectbox(slbox_text, vn)
            print(slbox_text,"llllllllllllllllllllllllllllllll")
            st.write(slbox_text,"      :     ",selected_vn)
       elif fetch == "fetch":
            st.write("Failurein SQl Query ")
            st.title(" SQL Query Results")
            mycursor.execute(query)
            out=mycursor.fetchall()
            print("outside ")
            selected_vn = st.selectbox(slbox_text, out)
            print(slbox_text,"sssssssssssssssssssssss")

       else:            
  
           mycursor.execute(query)
           se=mycursor.fetchall()
           print(type(se))
           print("SSEE",se)
           print(type(mycursor.description))
           print("mucursor desc",mycursor.description)
           columns = [desc[0] for desc in mycursor.description]   
           df = pd.DataFrame(se,columns=columns)
           st.write(slbox_text)
           st.dataframe(df)
           print(slbox_text,"MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")

#Get the SQL Query Data using Panda 
def get_data(query, params=None):
    if params=="None":
        df = pd.read_sql_query(query, mydb, params=params)
    else:
        df = pd.read_sql_query(query, mydb)
        print(df)
    return df

if page == "Home":
    #print("Inside Home")
    
    #print("Welcome to home page ")
    st.write("""India's agricultural sector is a global leader, producing the most rice, wheat, pulses, and spices worldwide.
              It also has the largest cattle herd and the largest area under wheat, rice, and cotton cultivation.
              India is a major producer of rice, wheat, cotton, sugarcane, and other crops, with a significant portion of its land dedicated to agriculture. """)
                 
    st.write("""India is one of the major players in the agriculture sector worldwide and it is the primary source of livelihood for 55percentage of India’s population.
              India has the world's largest cattle herd (buffaloes), 
              the largest area planted for wheat, rice, and cotton, and is the largest producer of milk, pulses, and spices in the world.
              It is the second-largest producer of fruit, vegetables, tea, farmed fish, cotton, sugarcane, wheat, rice, cotton, and sugar. """)
             
    st.write(""" The agriculture sector in India holds the record for second-largest agricultural land in the world generating employment for about half of the country’s population.
              Thus, farmers become an integral part of the sector to provide us with a means of sustenance.
              The Indian food industry is poised for huge growth, increasing its contribution to world food trade every year due to its immense potential for value addition, particularly within the food processing industry. The Indian food processing industry accounts for 32 percentage of the country’s total food market, one of the largest industries in India and is ranked fifth in terms of production, consumption, export and expected growth.
    """)
# SELECT        `RICE PRODUCTION (1000 tons)` as Rice_Production , `State Name` as State , `Year` as Years FROM indian_agri_data;
#SELECT        `RICE PRODUCTION (1000 tons)` as Rice_Production , `State Name` as State , `Year` as Years FROM indian_agri_data ORDER BY `RICE PRODUCTION (1000 tons)` DESC limit 5;
    st.image("D:/DataScinece/Project/AgriData_Explorer/env/A1.jpg")
elif page == "AgriDetails":
    print("Inside Agric")
    sql_queries = {
        "1. Year-wise Trend of Rice Production Across States (Top 3)": "SELECT `RICE PRODUCTION (1000 tons)` as Rice_Production , `State Name` as State , `Year` as Years FROM indian_agri_data ORDER BY `RICE PRODUCTION (1000 tons)` DESC limit 5;",
        "2. Top 5 Districts by Wheat Yield Increase Over the Last 5 Years": "select `WHEAT YIELD (Kg per ha)` as Wheat_Yield , `Dist Name` as District , `Year` as Years from indian_agri_data order by `WHEAT YIELD (Kg per ha)` DESC limit 5;",
        "3. States with the Highest Growth in Oilseed Production (5-Year Growth Rate)": "SELECT   sum(`OILSEEDS PRODUCTION (1000 tons)`) AS maxs,   `State Name` FROM   indian_agri_data GROUP BY    `State Name` ORDER BY  maxs DESC LIMIT 5;",
        "4. District-wise Correlation Between Area and Production for Rice Crops ": "SELECT   `Dist Name` AS District,    `RICE AREA (1000 ha)` AS Rice_Area,     `RICE PRODUCTION (1000 tons)` As Rice_Production  FROM indian_agri_data  GROUP BY `Dist Name`",
        "5. District-wise Correlation Between Area and Production for Wheat Crops ": "SELECT   `Dist Name` AS District,    `WHEAT AREA (1000 ha)` as Wheat_Area , `WHEAT PRODUCTION (1000 tons)`as Wheat_Production  FROM indian_agri_data  GROUP BY `Dist Name`",
        "6. District-wise Correlation Between Area and Production for Maize Crops ": "SELECT   `Dist Name` AS District,    `MAIZE AREA (1000 ha)` as Maize_Area , `MAIZE PRODUCTION (1000 tons)` as Maize_Production   FROM indian_agri_data  GROUP BY `Dist Name`",
        "7. Yearly Production Growth of Cotton in Top 5 Cotton Producing States": "select `COTTON PRODUCTION (1000 tons)` ,`State Name` ,`Year` as Years  from indian_agri_data order by `COTTON PRODUCTION (1000 tons)` DESC LIMIT 5;",
        "8. Districts with the Highest Groundnut Production in 2020": "select COUNT(`GROUNDNUT PRODUCTION (1000 tons)`) from indian_agri_data where `Year`=2020;",
        "9. Districts with the Highest Groundnut Production in 2010": "select COUNT(`GROUNDNUT PRODUCTION (1000 tons)`) ,  `State Name` from indian_agri_data where `Year`=2010 GROUP BY `State Name`;;",
        "10. Annual Average Maize Yield Across All States": "SELECT `Year`,`State Name`, AVG(`MAIZE YIELD (Kg per ha)`) FROM indian_agri_data GROUP BY `Year`, `State Name`;",
        "11. Total Area Cultivated for Oilseeds in Each State": "select sum(`OILSEEDS AREA (1000 ha)`) , `State Name` FROM indian_agri_data GROUP by `State Name`",
        "12. Districts with the Highest Rice Yield": "select MAX(`RICE YIELD (Kg per ha)`), `Dist Name` from indian_agri_data GROUP by `Dist Name`;",
        "13. Compare the Production of Wheat and Rice for the Top 5 States Over 10 Years": "SELECT `RICE PRODUCTION (1000 tons)` as Rice_Production , `WHEAT PRODUCTION (1000 tons)` as Wheat_Production , `State Name` from indian_agri_data GROUP by `State Name`, `RICE PRODUCTION (1000 tons)`,`WHEAT PRODUCTION (1000 tons)`;",
            }
    print("typeeeee",type(sql_queries))
    sel=st.selectbox("**SQl ALL Queries**",sql_queries)
    print("...........selected the query..........",sel,".................",sql_queries[sel])
    query_execution(sql_queries[sel],"Query Result ....","df")

