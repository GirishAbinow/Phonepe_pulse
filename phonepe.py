import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly_express as px
import seaborn as sns
import matplotlib.pyplot as plt

#SQL to Dataframe

mydb = mysql.connector.connect(host="localhost", user="root", passwd="Abinow@28", database="phone_pe")
cursor = mydb.cursor()


cursor.execute("select * from aggreated_transaction")
q=cursor.fetchall()
aggreated_transaction=pd.DataFrame(q,columns=['State', 'Year', 'Quater', 'Transaction_type', 'Transaction_count',
       'Transaction_amount'])


cursor.execute("select * from aggreated_user")
q=cursor.fetchall()
aggreated_user=pd.DataFrame(q,columns=['State', 'Year', 'Quater', 'Brands', 'Transaction_count', 'Percentage'])


cursor.execute("select * from map_transaction")
q=cursor.fetchall()
map_transaction=pd.DataFrame(q,columns=['State', 'Year', 'Quater', 'District', 'Transaction_count',
       'Transaction_amount'])


cursor.execute("select * from map_user")
q=cursor.fetchall()
map_user=pd.DataFrame(q,columns=['State', 'Year', 'Quater', 'District', 'Registered_users', 'App_opens'])


cursor.execute("select * from top_transaction")
q=cursor.fetchall()
top_transaction=pd.DataFrame(q,columns=['State', 'Year', 'Quater', 'Pincode', 'Transaction_count',
       'Transaction_amount'])


cursor.execute("select * from top_user")
q=cursor.fetchall()
top_user=pd.DataFrame(q,columns=['State', 'Year', 'Quater', 'Pincode', 'Registered_users'])

def trans_amt_cnt_year(year,quat):
    tacy=aggreated_transaction[aggreated_transaction['Year']==year]
    tacy.reset_index(drop=True,inplace=True)
    tacy1=tacy[tacy['Quater']==quat]
    tacy1.reset_index(drop=True,inplace=True)

    tacy_grp=tacy1.groupby('State')[['Transaction_count','Transaction_amount']].sum()
    tacy_grp.reset_index(inplace=True)
    count=tacy1['Transaction_count'].sum()
    amount=tacy1['Transaction_amount'].sum()

    radio=st.radio("Select",["Analysis","Bar Plot","Geo Plot"])

    if radio=="Analysis":
        st.success(f"Total payment value - :blue[₹ {amount:,}]")
        st.success(f"All PhonePe transactions (UPI + Cards + Wallets) - :blue[{count:,}]")
        st.success(f"Avg. transaction value - :blue[₹ {amount//count:,}]")
        col1,col2=st.columns(2)
        with col1:
            df_query=f'''SELECT Transaction_type,sum(Transaction_count) FROM phone_pe.aggreated_transaction where year={year} and quater={quat}  group by Transaction_type order by sum(Transaction_count) desc'''
            cursor.execute(df_query)
            #mydb.commit()
            temp=cursor.fetchall()
            df=pd.DataFrame(temp,columns=['Categories','Count'])
            st.dataframe(df)
        with col2:
            fig_pie=px.pie(df,names='Categories',values='Count',width=350,height=240,hole=.4)
            st.plotly_chart(fig_pie)

    elif radio=="Bar Plot":

        fig_amt=px.bar(tacy_grp,x='State',y='Transaction_amount',color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{year} Quater {quat} Transaction_amount")
        st.plotly_chart(fig_amt)

        fig_cnt=px.bar(tacy_grp,x='State',y='Transaction_count',color_discrete_sequence=px.colors.sequential.Aggrnyl_r,title=f"{year} Quater {quat} Transaction_count")
        st.plotly_chart(fig_cnt)

    if radio=="Geo Plot":

        fig = px.choropleth(
        tacy_grp,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Transaction_amount',
        color_continuous_scale='Mint',
        title=f"{year} Quater {quat} Transaction_amount")
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

        fig = px.choropleth(
        tacy_grp,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Transaction_count',
        color_continuous_scale='Reds',
        title=f"{year} Quater {quat} Transaction_count")
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

def agg_user_year(year,quat):
    aguy=aggreated_user[aggreated_user['Year']==year]
    aguy.reset_index(drop=True,inplace=True)
    aguy1=aguy[aguy['Quater']==quat]
    aguy1.reset_index(drop=True,inplace=True)

    aguy_grp=aguy1.groupby('Brands')[['Transaction_count','Percentage']].sum()
    aguy_grp.reset_index(inplace=True)
    scatter=px.scatter(aguy_grp,x='Brands',y='Transaction_count',title="Brands and Transaction Count",color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(scatter)

def map_user_year(year,quat):
    aguy=map_user[map_user['Year']==year]
    aguy.reset_index(drop=True,inplace=True)
    aguy1=aguy[aguy['Quater']==quat]
    aguy1.reset_index(drop=True,inplace=True)

    aguy_grp=aguy1.groupby('State')[['App_opens']].sum()
    aguy_grp.reset_index(inplace=True)
    scatter=px.box(aguy_grp,x='State',y='App_opens',title=f"{year} Quater {quat} Application Opens",color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(scatter)

def top_user_year(year,quat):
    tpuy=top_user[top_user['Year']==year]
    tpuy.reset_index(drop=True,inplace=True)
    tpuy1=tpuy[tpuy['Quater']==quat]
    tpuy1.reset_index(drop=True,inplace=True)
    tpuy_grp=tpuy1.groupby('State')[['Registered_users']].sum()
    tpuy_grp.reset_index(inplace=True)

    fig = px.choropleth(
    tpuy_grp,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Registered_users',
    color_continuous_scale='Reds',
    title=f"{year} Quater {quat} Registered Users")
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)


# Sreamlit

st.set_page_config(layout='wide')
st.title("Phonepe Pulse Data Visualization and Exploration")

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #3f1e6d;
    }
    [data-testid=stAppViewContainer] {
        background-color: #170133;
    }
</style>
""", unsafe_allow_html=True)
st.sidebar.header(":wave: :violet[**Hello! Welcome!!**]")
with st.sidebar:
    st.image(r"C:\Users\RANJITH\Desktop\Data Science\CAPSTONE\phoneimg.jpeg")
    select=option_menu("Main Menu",['Home','Data Analysis','Insights','Top 10'])

if select=='Home':
    col1,col2=st.columns(2)
    with col1:
        st.header("Introduction")
        st.text('''PhonePe is an Indian digital payments and financial
services company headquartered in Bengaluru, Karnataka,
India. PhonePe was founded in December 2015, by Sameer
Nigam, Rahul Chari and Burzin Engineer. The PhonePe app,
based on the Unified Payments Interface (UPI), went live
in August 2016.''')
        st.header("Uses of PhonePe")
        st.subheader("1. Mobile recharge:")
        st.text('''By using this app, you can get your mobile phone 
recharged very easily. You simply need to mention the 
amount, phone number and the appropriate mobile operator
name. You can even browse plans.''')
        st.subheader("2. Travel related:")
        st.text('''Whether it is needed to book a ticket online or a
metro recharge to be done, PhonePe is at our rescue.''')
        st.subheader("3. Pay bills:")
        st.text('''you can pay gas cylinder bills through this app.
Not only gas bills, but even electricity bills can be
paid using this app.''')
        st.subheader("4. Transfer money:")
        st.text('''you can transfer money to your friend or relative
using this app. It provides an online payment system
based on Unified Payments Interface. UPI is a novel
process in electronic funds transfer launched by
National Payments Corporation of India (NPCI).
Through PhonePe UPI app, you can send and receive
money instantly using a Virtual Payment Address.''')
        st.subheader("5. Link bank account:")
        st.text('''it is not possible to carry your bank debit and
credit cards everywhere. So in that case, you can
directly link your bank account to this account.''')
        st.subheader("6. Get discount at leading merchants:")
        st.text('''you can use PhonePe wallet to pay for reliance
trends, big basket, Grofers and other leading
associated partners of PhonePe.''')

    with col2:
        st.video(r"C:\Users\RANJITH\Desktop\Data Science\CAPSTONE\PhonePe.mp4")
        st.link_button("Download",url="https://www.phonepe.com/app-download/",use_container_width=True)
        st.image(r"C:\Users\RANJITH\Desktop\Data Science\CAPSTONE\phonepeui.jpeg",use_column_width=True)

elif select=='Data Analysis':
    col1,col2=st.columns(2)
    with col1:
        year = st.selectbox("Select Year",[2018,2019,2020,2021,2022,2023])
    with col2:
        quater = st.slider("Select quater",1,4)

    tab1,tab2=st.tabs(["Transaction","Users"])
    with tab1:
        trans_amt_cnt_year(year,quater)

    with tab2:
        agg_user_year(year,quater)
        map_user_year(year,quater)
        top_user_year(year,quater)

elif select=='Insights':
    question=st.selectbox("Select the question",("1.The most promminent payment type across years?",
                                                 "2.The year which has most transaction?",
                                                 "3.The quater which has top transaction?",
                                                 "4.The state which has most phone pe users?",
                                                 "5.An effective payment during the lockdown(2019-2020)",
                                                 "6.The state which is least or unaware about phone pe?",
                                                 "7.The quater which has least transaction?",
                                                 "8.The year which has most number of appopens?",
                                                 "9.The mobile brand using phonepe highest?",
                                                 "10.District with least registered users?"))
    
    if question=="1.The most promminent payment type across years?":
        query=f'''SELECT Transaction_type,sum(Transaction_count) FROM phone_pe.aggreated_transaction group by Transaction_type order by sum(Transaction_count) desc'''
        cursor.execute(query)
        t=cursor.fetchall()
        df=pd.DataFrame(t,columns=["Transaction type","Transaction Count"])
        fig_cnt=px.bar(df,x='Transaction type',y='Transaction Count',color_discrete_sequence=px.colors.sequential.Blackbody_r,title="The most promminent payment type across years")
        st.plotly_chart(fig_cnt)
        st.success(f":green[{df.iloc[0][0]}] is the most promminent payment type across years")

    elif question=="2.The year which has most transaction?":
        query=f'''SELECT year,sum(Transaction_count) FROM phone_pe.aggreated_transaction group by year order by sum(Transaction_count) desc'''
        cursor.execute(query)
        t=cursor.fetchall()
        df=pd.DataFrame(t,columns=["Year","Transaction Count"])
        fig_cnt=px.scatter(df,x='Year',y='Transaction Count',color_discrete_sequence=px.colors.sequential.Blackbody_r,title="Most transaction year")
        st.plotly_chart(fig_cnt)
        st.success(f":green[{df.iloc[0][0]}] is the year which has most transaction")

    elif question=="3.The quater which has top transaction?":
        query=f'''SELECT quater,sum(Transaction_count) FROM phone_pe.aggreated_transaction group by quater order by sum(Transaction_count) desc'''
        cursor.execute(query)
        t=cursor.fetchall()
        df=pd.DataFrame(t,columns=["Quater","Transaction Count"])
        fig_cnt=px.pie(df,values="Transaction Count",names="Quater",title="Most transaction quater")
        st.plotly_chart(fig_cnt)
        st.success(f":green[{df.iloc[0][0]}] is the quater which has most transaction")

    elif question=="4.The state which has most phone pe users?":
        query=f'''SELECT state,sum(Registered_users) FROM phone_pe.top_user group by state order by sum(Registered_users) desc limit 5'''
        cursor.execute(query)
        t=cursor.fetchall()
        df=pd.DataFrame(t,columns=["State","Registered users"])
        fig_cnt=px.bar(df,x='State',y='Registered users',color_discrete_sequence=px.colors.sequential.Blackbody_r,title="State having most phone pe users")
        st.plotly_chart(fig_cnt)
        st.success(f":green[{df.iloc[0][0]}] is the state which has most phone pe users")

    elif question=="5.An effective payment during the lockdown(2019-2020)":
        query=f'''SELECT Transaction_type,sum(Transaction_count) FROM phone_pe.aggreated_transaction where year<=2020 and year >=2019 group by Transaction_type order by sum(Transaction_count) desc'''
        cursor.execute(query)
        t=cursor.fetchall()
        df=pd.DataFrame(t,columns=["Transaction type","Transaction Count"])
        fig_cnt=px.bar(df,x='Transaction type',y='Transaction Count',color_discrete_sequence=px.colors.sequential.Tealgrn_r,title="An effective payment during the lockdown(2019-2020)")
        st.plotly_chart(fig_cnt)
        st.success(f":green[{df.iloc[0][0]}] is an effective payment during the lockdown(2019-2020)")

    elif question=="6.The state which is least or unaware about phone pe?":
        query=f'''SELECT state,sum(Registered_users) FROM phone_pe.top_user group by state order by sum(Registered_users) limit 5'''
        cursor.execute(query)
        t=cursor.fetchall()
        df=pd.DataFrame(t,columns=["State","Registered users"])
        fig_cnt=px.scatter(df,x='State',y='Registered users',color_discrete_sequence=px.colors.sequential.YlGn,title="The state which is least or unaware about phone pe")
        st.plotly_chart(fig_cnt)
        st.success(f":green[{df.iloc[0][0]}] is the state which is least or unaware about phone pe")

    elif question=="7.The quater which has least transaction?":
        query=f'''SELECT quater,sum(Transaction_count) FROM phone_pe.aggreated_transaction group by quater order by sum(Transaction_count)'''
        cursor.execute(query)
        t=cursor.fetchall()
        df=pd.DataFrame(t,columns=["Quater","Transaction Count"])
        fig_cnt=px.pie(df,values="Transaction Count",names="Quater",title="Least transaction quater")
        st.plotly_chart(fig_cnt)
        st.success(f":green[{df.iloc[0][0]}] is the quater which has least transaction")

    elif question=="8.The year which has most number of appopens?":
        query=f'''SELECT Year,sum(App_opens) FROM phone_pe.map_user group by year order by sum(App_opens) desc limit 5'''
        cursor.execute(query)
        t=cursor.fetchall()
        df=pd.DataFrame(t,columns=["Year","App opens"])
        fig_cnt=px.scatter(df,x='Year',y='App opens',color_discrete_sequence=px.colors.sequential.Rainbow,title="The year having most number of appopens")
        st.plotly_chart(fig_cnt)
        st.success(f":green[{df.iloc[0][0]}] is the year which has most number of appopens")

    elif question=="9.The mobile brand using phonepe highest?":
        query=f'''SELECT brands,sum(Transaction_count) FROM phone_pe.aggreated_user group by brands order by sum(Transaction_count) desc'''
        cursor.execute(query)
        t=cursor.fetchall()
        df=pd.DataFrame(t,columns=["Brands","Transaction Count"])
        fig_cnt=px.bar(df,x='Brands',y='Transaction Count',color_discrete_sequence=px.colors.sequential.Rainbow,title="The mobile brand using phonepe highest")
        st.plotly_chart(fig_cnt)
        st.success(f":green[{df.iloc[0][0]}] is the mobile brand using phonepe highest")

    elif question=="10.District with least registered users?":
        query=f'''SELECT district,sum(Registered_users) FROM phone_pe.map_user group by District order by sum(Registered_users) limit 5'''
        cursor.execute(query)
        t=cursor.fetchall()
        df=pd.DataFrame(t,columns=["District","Registered Users"])
        fig_cnt=px.bar(df,x='District',y='Registered Users',color_discrete_sequence=px.colors.sequential.Rainbow,title="District with least registered users")
        st.plotly_chart(fig_cnt)
        st.success(f":green[{df.iloc[0][0]}] is the district with least registered users")



elif select=='Top 10':
    col1,col2=st.columns(2)
    with col1:
        year = st.selectbox("Select Year",[2018,2019,2020,2021,2022,2023])
    with col2:
        quater = st.slider("Select quater",1,4)

    col3,col4,col5=st.columns(3)
    with col3:
        button1 = st.button("State",use_container_width=True)
    with col4:
        button2 = st.button("District",use_container_width=True)
    with col5:
        button3 = st.button("Pincode",use_container_width=True)

    tab1,tab2=st.tabs(["Transaction","Users"])
    with tab1:
        if button1:
            query=f'''SELECT State,sum(Transaction_count) FROM phone_pe.aggreated_transaction where quater={quater} and year ={year} group by State order by sum(Transaction_count) desc limit 10'''
            cursor.execute(query)
            t=cursor.fetchall()
            df=pd.DataFrame(t,columns=['State','Transaction Count'])
            st.write(df)
            fig_cnt=px.bar(df,x='State',y='Transaction Count',color_discrete_sequence=px.colors.sequential.Aggrnyl_r,title="State wise Transaction count")
            st.plotly_chart(fig_cnt)

        elif button2:
            query=f'''SELECT district,sum(Transaction_count) FROM phone_pe.map_transaction where quater={quater} and year ={year} group by district order by sum(Transaction_count) desc limit 10'''
            cursor.execute(query)
            t=cursor.fetchall()
            df=pd.DataFrame(t,columns=['District','Transaction Count'])
            st.write(df)
            fig_cnt=px.area(df,x='District',y='Transaction Count',color_discrete_sequence=px.colors.sequential.algae,title="District Wise Transaction_count")
            st.plotly_chart(fig_cnt)

        elif button3:
            query=f'''SELECT pincode,sum(Transaction_count) FROM phone_pe.top_transaction where quater={quater} and year ={year} group by pincode order by sum(Transaction_count) desc limit 10'''
            cursor.execute(query)
            t=cursor.fetchall()
            df=pd.DataFrame(t,columns=['Pincode','Transaction Count'])
            st.write(df)
            df['Pincode']=df['Pincode'].astype(str)
            fig_cnt=px.pie(df,values="Transaction Count",names="Pincode")
            st.plotly_chart(fig_cnt)

    with tab2:
        if button1:
            query=f'''SELECT State,sum(Transaction_count) FROM phone_pe.aggreated_user where quater={quater} and year ={year} group by State order by sum(Transaction_count) desc limit 10'''
            cursor.execute(query)
            t=cursor.fetchall()
            df=pd.DataFrame(t,columns=['State','Registered Users'])
            st.write(df)
            fig_cnt=px.bar(df,x='State',y='Registered Users',color_discrete_sequence=px.colors.sequential.Aggrnyl_r,title="Users State wise Transaction count")
            st.plotly_chart(fig_cnt)

        elif button2:
            query=f'''SELECT district,sum(Registered_users) FROM phone_pe.map_user where quater={quater} and year ={year} group by district order by sum(Registered_users) desc limit 10'''
            cursor.execute(query)
            t=cursor.fetchall()
            df=pd.DataFrame(t,columns=['District','Registered Users'])
            st.write(df)
            fig_cnt=px.area(df,x='District',y='Registered Users',color_discrete_sequence=px.colors.sequential.Electric_r,title="District Wise Registered Users")
            st.plotly_chart(fig_cnt)

        elif button3:
            query=f'''SELECT pincode,sum(Registered_users) FROM phone_pe.top_user where quater={quater} and year ={year} group by pincode order by sum(Registered_users) desc limit 10'''
            cursor.execute(query)
            t=cursor.fetchall()
            df=pd.DataFrame(t,columns=['Pincode','Registered Users'])
            st.write(df)
            df['Pincode']=df['Pincode'].astype(str)
            fig_cnt=px.pie(df,values="Registered Users",names="Pincode")
            st.plotly_chart(fig_cnt)