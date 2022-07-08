from cgitb import reset
import mysql.connector
mydb = mysql.connector.connect(
 host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'root',
    database='stockbot_data'
)
def check_company(stock):
    mycursor = mydb.cursor()
    for i in stock:
        st=[]
        st.append(i)
        query = """select * from companies where ticker= %s"""
        a=tuple(st)
        mycursor.execute(query,a)
        mycursor.fetchall()
        n = mycursor.rowcount
        if(n==0):
            return False
    return True

def add_company(author,stock,user_id):
    mycursor = mydb.cursor()
    for i in stock:
        st=[]
        st.append(author)
        st.append(i)
        st.append(user_id)
        query = """INSERT into selection values (%s,%s,%s)"""
        a=tuple(st)
        mycursor.execute(query,a)
        mydb.commit()

def see_company(author):
    f =[] #final array
    mycursor = mydb.cursor()
    st=[]
    st.append(author)
    query = """select tickerselect from selection where username= %s"""
    a=tuple(st)
    mycursor.execute(query,a)
    result = mycursor.fetchall()
    for i in result:
        f.append(i[0])
    return f

def auto_check_company():
    f=[]
    mycursor = mydb.cursor()
    st=[]
    query = """select distinct tickerselect from selection"""
    mycursor.execute(query)
    result = mycursor.fetchall()
    for i in result:
        f.append(i[0])
    return f

def see_user(company):
    f =[] #final array
    mycursor = mydb.cursor()
    st=[]
    st.append(company)
    query = """select distinct userid from selection where tickerselect= %s"""
    a=tuple(st)
    mycursor.execute(query,a)
    result = mycursor.fetchall()
    for i in result:
        f.append(i[0])
    return f

def delete_company(author,stock):
    mycursor = mydb.cursor()
    for i in stock:
        st=[]
        st.append(i)
        st.append(author)
        query = """DELETE from selection where tickerselect=%s and username=%s"""
        a=tuple(st)
        print(a)
        mycursor.execute(query,a)
        mydb.commit()
    
