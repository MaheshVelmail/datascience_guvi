import streamlit as st
import mysql.connector  #SQL COnnector package import 
import pandas as pd
from datetime import   datetime

mydb = mysql.connector.connect( #This method sets up a connection, establishing a session with the MySQL server
    host = "localhost",
    user = "root",
    password=""
)

mycursor = mydb.cursor(buffered=True) #fter executing a query, a MySQLCursorBuffered cursor fetches the entire result set from the server and buffers the rows.
mycursor.execute("USE mahe") 
querry="SELECT * FROM `secure_traffic` where vehicle_number like 'TN'"
mycursor.execute(querry)
outt=mycursor.fetchall()
print("outside ",outt)

def insert(query,slbox_text,value):
     #print("Queryyyyyyyyyyyyyyy  ", query)
     mycursor.execute(query, value)     
     mydb.commit()
     #print("row counttttyyyyyyyyyyyyy",mycursor.rowcount)
     st.write("New Data Inserted Sucesfully in to DataBase secure_traffic")
     #mycursor.close()
     #mydb.close()

    #Data passed without fetch all option into selection box 
def meidum_query_d(query,slbox_text,fetch):
       vn = get_data(query)      
       
       
       if fetch == "select":
            selected_vn = st.selectbox(slbox_text, vn)
            st.write(slbox_text,"      :     ",selected_vn)
       elif fetch == "fetch":
            st.write("Failurein SQl Query ")
            st.title(" SQL Query Results")
            mycursor.execute(query)
            out=mycursor.fetchall()
            print("outside ")
            selected_vn = st.selectbox(slbox_text, out)

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

#Get the SQL Query Data using Panda 
def get_data(query, params=None):
    if params=="None":
        df = pd.read_sql_query(query, mydb, params=params)
    else:
        df = pd.read_sql_query(query, mydb)
        print(df)
    return df
# mycursor.execute("create database anyname") - to create DB

#Title for page
st.title(' Police Security Traffic Check ')
st.header("Vehice test") 
page = st.sidebar.selectbox(f"**Pages**",["Home","New Complaint adding", "View the existing complaint record details",  "Medium_Complex_Queries"])

if page == "Home":
    print("Welcome to home page ")
    st.write("""Police check posts require a centralized system for 
             logging, tracking, and analyzing vehicle movements. Currently, 
             manual logging and inefficient databases slow down security processes. 
             This project aims to build an SQL-based check post database with a Python-powered dashboard 
             for real-time insights and alerts.
    """)
    
elif page == "View the existing complaint record details":
    st.title("SQL Query Execution Box")

# Text area for user input
    query = st.text_area("Enter your SQL query:")

# Button to execute query
    if st.button("Run Query"):
       try:
        result = pd.read_sql_query(query, mydb)
        st.write("Query Result:")
        st.dataframe(result)
       except Exception as e:
        st.error(f"Error: {e}")
    st.write("                                             ")
    st.write("                                             ")
    st.write("                                             ")
    st.subheader("   All Data Table View from secure_traffic Table  ")
    mycursor.execute("SELECT * FROM `secure_traffic`")
    se=mycursor.fetchall()
    print(type(se))
    print(se)
    columns = [desc[0] for desc in mycursor.description]
    df = pd.DataFrame(se,columns=columns)
    st.dataframe(df)
elif page == "New Complaint adding":
    print("New Complaint ")   
    st.write(" Please add your New complaint registration here  ")
    #if st.button('Click'):
    st.write("we are inside ..")
    #name=st.text_input('Enter the Name of Driver',"Type Here ...")
    stop_date_st=st.date_input('Enter the stop_date ')
    #date_obj = datetime.strptime(stop_date_st," %y/%m/%d")
    
    #Converting into yyyy-mm-dd
    stop_date = stop_date_st.strftime("%y-%m-%d") #s 
    #stop_date=date_obj.strftime("%y-%m-%d")
    print("Stop date " , stop_date)
    stop_time_t=st.time_input('Enter the stop_time') 
    stop_time = stop_time_t.strftime("%H:%M") #s 
    print(stop_time,"timeeeee")
    #country_name = st.text_input('Country', max_chars=6)
    country_name=st.selectbox("Country",("Select from drop down...","India","USA","Canada")) #s
    driver_gender = st.radio("driver_gender ", ('M', 'F')) #s
    driver_age=st.number_input('Driver Age',min_value=18,max_value=100) #
    driver_age_raw=st.number_input('Driver Raw Age',min_value=18,max_value=100) #3
    
    driver_race = st.selectbox("Driver race",("Select from drop down...","Asian","Black","White","Hispanic","Other")) #s

    violation_raw = st.selectbox("Driver violation raw",("Select from drop down...","Speeding","Other","Drunk Driving","Signal Violation","Seatbelt"))
    violation = st.selectbox("Driver violation",("Select from drop down...","Speeding","DUI","Signal","Other","Seatbelt"))
    # violation=""
    # if violation_raw == "Speeding":
    #    print()
    #    violation = "Speeding"
    # elif violation_raw == "Drunk Driving":
    #    violation = "DUI"
    # elif violation_raw == "Signal Violation":
    #    violation = "Signal"
    # elif violation_raw == "Seatbelt":
    #    violation = "Seatbelt"
    # else:
    #    violation = "Other"
    
    search_conducted = st.radio("Was Search Conducted? ", ('True', 'False')) #s
    print("Search Status ",search_conducted)
    
    search_type = st.selectbox("search_type",("Select from drop down...","Vehicle Search","Frisk","None","Others"))#s
    
    stop_outcome = st.selectbox("stop outcome",("Select from drop down...","Ticket","Arrest","Warning"))
    is_arrested =""
    if stop_outcome == "Arrest":
       print("Arrested == ",True)
       is_arrested = "True"
    else:
       print("Arrested == ",False)
       is_arrested = "False"
    print("Arrested or not ",is_arrested )
    
    drugs_related_stop = st.radio("Was is Drug Related? ", ('True', 'False'))
    
    stop_duration = st.selectbox("stop_duration",("Select from drop down...","16-30 Min","0-15 Min","30+ Min")) #s
    vehicle_number = st.text_input('Vehicle Number','Type here...',max_chars=10) #s

    #mylist= [name,stop_date,stop_time,country_name,driver_gender,driver_age,driver_age_raw,driver_race,violation_raw,violation,search_conducted,search_type,stop_outcome,is_arrested,drugs_related_stop,stop_duration,vehicle_number ]
    mylist= [stop_date,stop_time,country_name,driver_gender,driver_age,driver_age_raw,driver_race,violation_raw,violation,search_conducted,search_type,stop_outcome,is_arrested,drugs_related_stop,stop_duration,vehicle_number ]
    mylist1= [stop_date,stop_time,country_name,driver_gender,driver_age,driver_age_raw,driver_race,violation_raw,violation,search_conducted,search_type,stop_outcome,is_arrested,drugs_related_stop,stop_duration,vehicle_number ]
    key = ["stop_date", "stop_time", "country_name", "driver_gender", "driver_age", "driver_age_raw", "driver_race", "violation_raw", "violation", "search_conducted", "search_type", "stop_outcome", "is_arrested", "drugs_related_stop", "stop_duration", "vehicle_number"]
    value = [stop_date, stop_time, country_name, driver_gender, driver_age, driver_age_raw, driver_race, violation_raw, violation, search_conducted, search_type, stop_outcome, is_arrested, drugs_related_stop, stop_duration, vehicle_number]

    merged_dict = dict(zip(key, value))
    
    
    if(st.button("Predict Stop Outcome and Violation")):
      #st.write("Name of the Driver",mylist[name])
      mylist1= [stop_date,stop_time,country_name,driver_gender,driver_age,driver_age_raw,driver_race,violation_raw,violation,search_conducted,search_type,stop_outcome,is_arrested,drugs_related_stop,stop_duration,vehicle_number ]
      lis = pd.DataFrame(mylist1)
      s=st.dataframe(lis)
      s=len(mylist1)
      print(type(mylist1))
      print("Length   ",s)

      print("Dictionoryyy",merged_dict)
      null_or_empty_items = [item for item in mylist1 if item is None or item == "" or item== 'Select from drop down...' or item == [] or item == {}]
      list_key={}
      k=0
      u=0
      db=0
      
      for key, value in merged_dict.items():
        if value is None or value == "" or  value == 'Select from drop down...' or value == [] or value == {}:
         print(f"{key}: {value}")
         print("Keyyyyyy",key)
         k=1
         list_key[key] = value
         dic= pd.DataFrame([list_key])
         dic1 = pd.DataFrame(list_key, index=[0])   
         print ("list_ke  y",list_key)    
      
      if k==1:
       st.write(k==1)
       keyss = list(dic.keys())
       #st.dataframe(dic)
       ks=pd.DataFrame(keyss,columns=["Input is not provided "])
       st.dataframe(ks)
      else:
        db=1        
        #if(st.button("Update the Prediction into DB")):             
        print("       updateddddddddddddddd--------------     ")

      query = """
    INSERT INTO `secure_traffic` 
    (`stop_date`, `stop_time`, `country_name`, `driver_gender`, `driver_age_raw`, `driver_age`, `driver_race`, `violation_raw`, `violation`, `search_conducted`, `search_type`, `stop_outcome`, `is_arrested`, `stop_duration`, `drugs_related_stop`, `vehicle_number`) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

      values = (
    merged_dict['stop_date'],
    merged_dict['stop_time'],
    merged_dict['country_name'],
    merged_dict['driver_gender'],
    merged_dict['driver_age_raw'],
    merged_dict['driver_age'],
    merged_dict['driver_race'],
    merged_dict['violation_raw'],
    merged_dict['violation'],
    merged_dict['search_conducted'],
    merged_dict['search_type'],
    merged_dict['stop_outcome'],
    merged_dict['is_arrested'],
    merged_dict['stop_duration'],
    merged_dict['drugs_related_stop'],
    merged_dict['vehicle_number']
)
      if(db==1):                       
         insert(query, "Update", values)


elif page == "Medium_Complex_Queries":
    #st.subheader("**List of Medium Quries -- **")
    AVW="""SELECT 
        COUNT(CASE WHEN stop_outcome = 'Arrest' THEN 1 END) AS stop_outcome_Arrest,
        COUNT(CASE WHEN stop_outcome = 'Warning' THEN 1 END) AS stop_outcome_Warnings
    FROM secure_traffic"""

    CSG="""SELECT 
        COUNT(CASE WHEN driver_gender = 'M' THEN 1 END) AS driver_gender_Male,
        COUNT(CASE WHEN driver_gender = 'F' THEN 1 END) AS driver_gender_Female
    FROM secure_traffic"""

    MCVA=""" SELECT 
    violation, 
    COUNT(*) AS violation_Arrest
FROM secure_traffic
WHERE stop_outcome = 'Arrest'
GROUP BY violation
ORDER BY violation_Arrest DESC
LIMIT 1 """

    ARBDG="""SELECT 
        AVG(CASE WHEN driver_gender = 'M' AND is_arrested = True THEN 1 ELSE 0 END) AS avg_arrested_m,
        AVG(CASE WHEN driver_gender = 'F' AND is_arrested = True THEN 1 ELSE 0 END) AS avg_arrested_f
    FROM secure_traffic"""

    NOSCN="""SELECT 
    stop_outcome AS Police_Stops,
    COUNT(stop_outcome) AS Police_Stops_Count,
    stop_time AS Time_of_Stop
FROM 
    secure_traffic
WHERE 
    CAST(stop_time AS TIME) >= '22:00:00' 
    OR CAST(stop_time AS TIME) <= '05:00:00'
GROUP BY 
    stop_outcome, stop_time
"""
     
    medium_queries = {
        "1. Count of Stops by Violation Type": "select violation as violation_Types ,count(stop_outcome) as Stop_Count from secure_traffic group by violation",
        "2. Number of Arrests vs Warnings": AVW,
        "3. Average Age of Drivers Stopped ": "select AVG(driver_age) from secure_traffic",
        "4. Top 5 Most Frequent Search Types": "SELECT search_type FROM secure_traffic GROUP BY search_type ORDER BY search_type limit 5",
        "5. Count of Stops by Gender": CSG,
        "6. Most Common Violation for Arrests": MCVA,
        "7. Average Stop Duration for Each Violation": "SELECT violation, AVG(stop_duration) AS violation_stop_duration FROM secure_traffic GROUP BY violation",
        "8. Number of Drug-Related Stops by Year": "select year(stop_date) as year_of_stop, count(drugs_related_stop) from secure_traffic GROUP BY year(stop_date)",
        "9. Number of Searches Conducted by Violation Type": "select DISTINCT violation as violation_Type , Count(*) as violation_count from secure_traffic group BY violation",
        "10. Violation Trends Over Time": "SELECT DISTINCT DATE_FORMAT(`stop_date`, '%Y-%m') AS `year_month` FROM `secure_traffic`",
        "11. Most Common Stop Outcomes for Drug-Related Stops": "select MAX(stop_outcome) as Max_outcome , COUNT(stop_outcome) as Stop_Count from secure_traffic where drugs_related_stop='TRUE'",
        "12. Total Number of Police Stops": "SELECT stop_outcome as Police_Stop , count(*) as Total_Count FROM `secure_traffic` GROUP by stop_outcome",
        "13. Drivers with the Highest Number of Stops": "select driver_race,count(stop_outcome) as Highest_Number_Of_Stops from secure_traffic group by driver_race",
        "14. Number of Stops Conducted at Night (Between 10 PM - 5 AM)": NOSCN,
        "15. Arrest Rate by Driver Gender": "select AVG(driver_gender = 'M') as Avg_Male_Arrested ,AVG(driver_gender = 'F') as Avg_Female_Arrested from secure_traffic where stop_outcome='Arrest'",
            }
    sel=st.selectbox("**Medium Queries**",medium_queries)
    meidum_query_d(medium_queries[sel],"Query Result ....","df")  
    
    DVTBR=""" SELECT *
FROM (
    SELECT driver_age AS Age, driver_race AS Race, violation,
           CASE  
             WHEN driver_age > 60 THEN '60 And Up'
             WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
             WHEN driver_age BETWEEN 21 AND 40 THEN '21-40'
             WHEN driver_age <= 20 THEN '20 And Below' 
           END AS agerange
    FROM secure_traffic 
) AS subquery
GROUP BY Age, Race, violation, agerange
"""

    TVHRS=""" SELECT violation, COUNT(*) AS arrest_count
FROM secure_traffic
WHERE stop_outcome = 'Arrest'
GROUP BY violation
ORDER BY arrest_count DESC
LIMIT 5"""

    CBAVS= """ SELECT stop_duration, Age , Violations FROM (
    SELECT 
        violation as Violations,
        driver_age as Age,
        stop_duration,
        COUNT(driver_age) as Age_count
    FROM secure_traffic 
    GROUP BY driver_age, violation, stop_duration
) as sub 
GROUP BY Age, stop_duration"""
    complex_queries = {
        "1. Yearly Breakdown of Stops and Arrests by Country": "SELECT Years, country , COUNT(Years) as Yearly_Count FROM (SELECT  YEAR(stop_date) AS Years, country_name AS country FROM secure_traffic WHERE stop_outcome = 'Arrest') AS sub GROUP by Years",
        "2. Driver Violation Trends Based on Age and Race": DVTBR,
        "3. Time Period Analysis of Stops ": "select stop_duration as Time_Period ,stop_outcome as Polcie_Stops from secure_traffic group by stop_duration",
        "4. Correlation Between Age, Violation, and Stop Duration": CBAVS,
        "5. Violations with High Search and Arrest Rates": "select violation , max(violation) as max_violation, count(violation) as count_violation , stop_outcome from secure_traffic WHERE  stop_outcome='Arrest'",
        "6. Driver Demographics by Country": "SELECT driver_age as Age , driver_gender as Gender , driver_race Race , country_name as Country from secure_traffic GROUP by country_name",
        "7. Top 5 Violations with Highest Arrest Rates": TVHRS
            }
    cel=st.selectbox("**Complex Queries**",complex_queries)
    meidum_query_d(complex_queries[cel],"Number of Searches Conducted by Violation Type","df")