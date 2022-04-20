#============================MODULES===================================
import sqlite3
from datetime import datetime
import getpass


#===========================METHODS==========================

#welcome
def welcome():
    print("\n #######################################################################################################################")
    print("\t\t\t\t\t\t\tWELOCOME")
    print(" #######################################################################################################################")

# DATABASE AND TABLE CREATION
def database():
    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS 'client'
                    (Id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT,
                     Client_name TEXT,
                     Email TEXT,
                     Admin_name TEXT,
                     Contact TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS 'services'
                    (Id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT,
                     Client_id INTEGER,
                     Service_name TEXT,
                     Time_based BOOLEAN,
                     Date_of_registration DATE,
                     Time_period_in_days INTEGER,
                     Payment INTEGER,
                     Status TEXT,
                     FOREIGN KEY(Client_id) REFERENCES Client(Id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS 'admin'
                    (Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Admin_id TEXT,
                    Password TEXT)''')
    #SELECT DATE_FORMAT("2017-06-15", "%Y %M %D");

    cursor.close()
    conn.close()

# INSERT DATA INTO THE TABLE client
def insert_data_in_client(client_tup):
    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()

    # inserting data into client table
    cursor.execute('''INSERT INTO 'client'
                      (Client_name, Email, Admin_name, Contact )
                      VALUES(?, ?, ?, ?)''', (client_tup))
    conn.commit()
    cursor.close()
    conn.close()

# INSERT DATA INTO THE TABLE services
def insert_data_in_services(service_tup):
    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()

    # inserting data into services table
    cursor.execute('''INSERT INTO 'services'
                      (Client_id, Service_name, Time_based, Date_of_registration, Time_period_in_days, Payment, Status)
                      VALUES(?, ?, ?, ?, ?, ?, ?)''', (service_tup))
    conn.commit()
    cursor.close()
    conn.close()

# INSERT DATA INTO THE TABLE ADMIN
def insert_data_in_admin(id,pw):
    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()

    # inserting data into services table
    cursor.execute('''INSERT INTO 'admin'
                      (Admin_id, Password)
                      VALUES(?, ?)''', (id, pw))
    conn.commit()
    cursor.close()
    conn.close()


# DISPLAY DATA FROM THE TABLES
def display_data(res_rows):
    print("Id  Client_name    Email\tContact    Service  Date_of_registration  Time_period  Payment\tStatus")
    for row in res_rows:
        print("{}   {}\t{}\t{}   {}\t{}\t\t{}\t{}\t{}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))

# DISPLAY DATA FOR THE ALERT NOTIFICATIONS
def display_data_alert(res_rows, daysleft ):
    i=0
    print("Id  Client_name    Email\tContact    Service  Date_of_registration  Time_period  Payment\tStatus\tDays_left")
    for row in res_rows:
        print("{}   {}\t{}\t{}   {}\t{}\t\t{}\t{}\t{}\t\t{}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],daysleft[i]))
        i=i+1

# ADMIN REGISTER
def register():
    admins=[]

    sql="SELECT Admin_id FROM 'admin'"
    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    fetch=cursor.fetchall()
    admins=[row[0] for row in fetch]
    cursor.close()
    conn.close()

    flagr=True
    while(flagr):
        print("\n\n #######################################################################################################################")
        print("\t\t\t\t\tREGISTRATION")
        print("#######################################################################################################################")
        #print("\n Fill the following details")
        id=input("     Enter ID ->")
        pw=getpass.getpass("     Enter PASSWORD ->")
        cpw=getpass.getpass("  Re-enter PASSWORD ->")
        if id not in admins:
            if(pw==cpw):
                insert_data_in_admin(id,pw)
                print("\n  SUCCESSFULLY REGISTERED ...")
            else:
                print("\n  PASSWORD MISMATCHED ...")
        else:
            print("\n  ADMIN ALREADY REGISTERED ...")
            print("\n _______________________________________________________________________________________________________________________\n")
            flag=input("  MOVE TO LOGIN ?? (Y / N) ").lower()
            if(flag=='y' or flag=="yes"):
                login()
        print(" _______________________________________________________________________________________________________________________\n")
        flag=input("  DO YOU WANT TO EXIT FROM REGISTRATION WINDOW ?? (Y / N) ").lower()
        if(flag=="y" or flag=="yes"):
            flagr=False
        else:
            continue



# ADMIN LOGIN
def login():
    print("\n #######################################################################################################################")
    print("\t\t\t\t\tLOGIN ")
    print(" #######################################################################################################################")
    #print("\n Fill the following details")
    id=input("   Enter ID ->")
    pw=getpass.getpass("   Enter PASSWORD ->")
    #check_pw=admins.get(id,0)

    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT Password
            FROM 'admin'
            WHERE Admin_id = ?''',(id,))

    try:
        check_pw = cursor.fetchone()
        cpw=check_pw[0]
    except:
        cpw=0
    cursor.close()
    conn.close()

    if(cpw==pw):
        print("\n  SUCCESSFULLY LOGGED IN ...")
        admin_dashboard(id)
    elif(cpw==0):
        print("\n  ADMIN NOT REGISTERED ...")
        print(" _______________________________________________________________________________________________________________________\n")
        flag=input("  MOVE TO REGISTER WINDOW ?? (Y / N) ").lower()
        if(flag=='y' or flag=="yes"):
            register()
    else:
        print("\n  INCORRECT PASSWORD ...")
        print(" _______________________________________________________________________________________________________________________\n")
        flag=input(" WANT TO TRY LOGGING AGAIN ?? (Y / N) ").lower()
        if(flag=='y' or flag=="yes"):
            login()


# ADMIN DASHBOARD
def admin_dashboard(admin_id):
    flag=True
    while(flag):
        welcome()
        print(" _______________________________________________________________________________________________________________________")
        print("\t\t\t\t  CURRENTLY  --->", admin_id, "<---  LOGGED IN ...")
        print(" _______________________________________________________________________________________________________________________")
        print(" #######################################################################################################################")
        print("\t\t\t\t\tMENU")
        print(" #######################################################################################################################\n")
        print(" 1. ADD CLIENT \ DETAILS")
        print(" 2. UPDATE CLIENT \ DETAILS")
        print(" 3. SHOW CLIENTS \ DETAILS")
        print(" 4. SHOW NOTIFICATIONS")
        print(" 5. LOGOUT")
        print(" _______________________________________________________________________________________________________________________")
        c=input("\n  Enter your choice (1-5) --> ")
        try:
            c=int(c)
            if(c==1):
                add_cldet(admin_id)
            elif(c==2):
                edit_cldet()
            elif(c==3):
                show_cldet(admin_id)
            elif(c==4):
                show_notifications(admin_id)
            elif(c==5):
                flag=False
            else:
                #print("try")
                print("\n  ENTER VALID CHOICE ...")
        except:
            #print("except")
            print("\n  ENTER VALID CHOICE ...")

        if(flag):
            print(" _______________________________________________________________________________________________________________________")
            f=input("\n  DO YOU WANT TO LOGOUT  ?? (Y / N) ").lower()
            if(f=="y" or f=="yes"):
                flag=False
        else:
            continue


# ADMIN - 1. ADD CLIENT / DETAILS
def add_cldet(admin_id):
    flag=True
    while(flag):
        print("\n #######################################################################################################################")
        print("\t\t\t\t\t MENU")
        print(" #######################################################################################################################")
        print(" 1.  ADD CLIENT DETAILS ")
        print(" 2.  ADD SERVICE DETAILS ")
        print(" _______________________________________________________________________________________________________________________\n")
        c=input("\n  Enter your choice (1-2) --> ")
        try:
            c=int(c)
            if(c==1):
                add_client_details(admin_id)
            elif(c==2):
                print(" _______________________________________________________________________________________________________________________")
                cid=input("\n  Enter the Client Id --> ")
                print(" _______________________________________________________________________________________________________________________")
                try:
                    cid=int(cid)
                    cids=[]
                    conn = sqlite3.connect("clients.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM 'client' WHERE Admin_name = ? ",(admin_id,))
                    fetch=cursor.fetchall()
                    for row in fetch:
                        cids.append(row[0])
                    cursor.close()
                    conn.close()
                    if(cid in cids):
                        add_services_details(cid)
                    else:
                        print(" _______________________________________________________________________________________________________________________\n")
                        print("\n  CLIENT ID {} DOESN'T EXIST ...".format(cid))
                except:
                    print("\n  ENTER VALID CLIENT ID ...")
            else:
                print("\n  ENTER VALID CHOICE ...")
        except:
            print("\n  ENTER VALID CHOICE ...")
        print(" _______________________________________________________________________________________________________________________")
        f=input("\n  WANT TO ADD MORE ENTRIES TO THE DATABASE ?? (Y / N) ").lower()
        if(f=='y' or f=="yes"):
            continue
        else:
            flag=False


def add_client_details(admin_id):
    flag=True
    while(flag):
        cdict={}
        print("\n #######################################################################################################################")
        print("\t\t\t PLEASE ENTER THE ASKED DETAILS...")
        print(" #######################################################################################################################")

        print("\n _______________________________________________________________________________________________________________________")
        print("  ADD CLIENT DETAILS ...\n")
        for i in range(4):
            att="  Enter {} -->".format(c_att[i])
            if c_att[i]=="Admin_name":
                det=admin_id
            else:
                det=input(att).lower()
            cdict[c_att[i]]=det
        print("\n _______________________________________________________________________________________________________________________")

        try:
            ct=list(cdict.values())
            insert_data_in_client(ct)

            print("\n #######################################################################################################################")
            print("\t\t\t\tCLIENT ADDED SUCCESSFULLY...")
            print(" #######################################################################################################################\n")
            conn = sqlite3.connect("clients.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM 'client' WHERE Client_name = ? AND Admin_name = ?", (ct[0],admin_id))
            cid=cursor.fetchone()[0]
            cursor.close()
            conn.close()
            print("\n _______________________________________________________________________________________________________________________")
            fld=input("\n  WANT TO ADD SERVICES FOR THIS CLIENT ?? (Y / N) ").lower()
            if(fld=='y' or fld=="yes"):
                add_services_details(cid)

        except:
            print("\n #######################################################################################################################")
            print("\t\t\t\tERROR OCCURRED... CLIENT NOT ADDED...")
            print(" #######################################################################################################################")

        f=input("\n  WANT TO ADD MORE CLIENTS  ?? (Y / N) ").lower()
        if(f=='y' or f=="yes"):
            continue
        else:
            flag=False


def add_services_details(cid):

    flagser=True
    while(flagser):
        sdict={}
        print("\n #######################################################################################################################")
        print(" _______________________________________________________________________________________________________________________")
        print("  ADD SERVICE DETAILS FOR THE CLIENT ID ENTERED ...\n")
        for i in range(7):
            att="  Enter {} -->".format(s_att[i])
            if s_att[i]=="Client_id":
                det=cid
            else:
                det=input(att).lower()
            if(i==4 or i==5):
                det=int(det)
            sdict[s_att[i]]=det
        try:

            st=list(sdict.values())
            insert_data_in_services(st)

            print("\n #######################################################################################################################")
            print("\t\t\t\tSERVICE ADDED SUCCESSFULLY...")
            print(" #######################################################################################################################\n")
        except:
            print("\n #######################################################################################################################")
            print("\t\t\t\tERROR OCCURRED...  SERVICE ISN'T ADDED...")
            print(" #######################################################################################################################\n")
        print("\n _______________________________________________________________________________________________________________________")
        f=input("\n  WANT TO ADD MORE SERVICES FOR THIS CLIENT  ?? (Y / N) ").lower()
        if(f=='y' or f=="yes"):
            continue
        else:
            flagser=False




# ADMIN - 2. EDIT CLIENT / DETAILS
def edit_cldet():
    #print("edit client called")
    fl=True
    while(fl):
        details={}
        print("\n #######################################################################################################################")
        print("\t\t\t UPDATING THE ENTRIES ...\n")
        print(" #######################################################################################################################\n")
        flag=True
        id=int(input("  Enter the client Id that is to be updated -->"))
        print("\n _______________________________________________________________________________________________________________________")
        print("\n  Enter the column name/details to be edited ...")
        while(flag):
            d=input("\n  COLUMN NAME / DETAIL  -->")
            val=input("  VALUE -->").lower()
            if (d=="Client_id" or d==" Time_period_in_days" or d=="Payment"):
                val=int(val)
            if d not in details:
                details[d]=val
            print("\n _______________________________________________________________________________________________________________________")
            f=input("\n  WANT TO EDIT MORE DETAILS ?? (Y / N) ").lower()
            if(f=='y' or f=="yes"):
                continue
            else:
                flag=False

        colname=list(details.keys())
        conn = sqlite3.connect("clients.db")
        cursor = conn.cursor()
        for i in range(len(colname)):

            if colname[i] in c_att:
                sql="UPDATE 'client' SET {} = ? WHERE id = ? ".format(colname[i])
                val=tuple((details[colname[i]], id))
            elif colname[i] in s_att:
                sql="UPDATE 'services' SET {} = ? WHERE Client_id = ? ".format(details[i])
                val=tuple((details[colname[i]], id))
            else:
                print(" ",details[i]," doesnt exist in database...")
                sql=""
                val=()

            try:
                if (sql!="" and val!=()):
                    cursor.execute(sql,val)
                    conn.commit()
                print("\n #######################################################################################################################")
                print("\t\t\t CLIENT DETAILS EDITED SUCCESSFULLY...")
                print(" #######################################################################################################################\n")
            except:
                print("\n #######################################################################################################################")
                print("\t\t\t ERROR OCCURRED...  CLIENT DETAILS AREN'T UPDATED...")
                print(" #######################################################################################################################\n")
        #for loop ends(222)
        cursor.close()
        conn.close()
        print("\n _______________________________________________________________________________________________________________________")
        f=input("\n  WANT TO EDIT MORE CLIENTS  ?? (Y / N ) ").lower()
        if(f=='y' or f=="yes"):
            continue
        else:
            fl=False





# ADMIN - 3. SHOW CLIENT /DETAILS
def show_cldet(admin_id):
    flag=True
    while(flag):
        print("\n #######################################################################################################################")
        print("\t\t\t\t\tMENU")
        print("\n #######################################################################################################################")
        print("  1. DISPLAY ALL DETAILS OF CLIENTS ")
        print("  2. DISPLAY DETAILS OF SPECIFIC CLIENTS ")
        print("\n _______________________________________________________________________________________________________________________")
        c=input("\n  Enter your choice (1-2) --> ")
        try:
            c=int(c)
            if(c==1):
                show_all(admin_id)
            elif(c==2):
                show_clients(admin_id)
            else:
                print("\n  ENTER VALID CHOICE ...")
        except:
            print("\n  ENTER VALID CHOICE ...")
        print("\n _______________________________________________________________________________________________________________________")
        f=input("\n  WANT TO GO BACK TO THE MAIN MENU ?? (Y / N) ").lower()
        if(f=='y' or f=="yes"):
            flag=False
        else:
            continue



# ADMIN - 3. 1. SHOW ALL CLIENTS / DETAILS
# ct--> (Id, Client_name, Email, Admin_name, Contact)
# st--> (Client_id, Service_name, Time_based, Date_of_registration, Time_period_in_days, Payment, Status)

def show_all(admin_id):
    res_rows=[]
    print("\n #######################################################################################################################")
    print(" \t\t\t CLIENTS AND THEIR DETAILS ")
    print("\n #######################################################################################################################")
    sql='''SELECT client.Id, client.Client_name, client.Email, client.Contact,
            services.Service_name, services.Date_of_registration, services.Time_period_in_days, services.Payment, services.Status
            FROM 'client' JOIN 'services'
            ON client.Id=services.Client_id
            WHERE  client.Admin_name = ?'''
    conn=sqlite3.connect("clients.db")
    cursor=conn.cursor()
    cursor.execute(sql,(admin_id,))
    fetch = cursor.fetchall()
    for row in fetch:
        res_rows.append(row)
    cursor.close()
    conn.close()
    #calling the display_data function to diplay the resultant rows
    display_data(res_rows)


# ADMIN - 3. 2. SHOW CLIENTS USING SPECIFIC COLUMN NAME / DETAILS
def show_clients(admin_id):
    print("\n #######################################################################################################################")
    print("\t\t\t\t\tMENU")
    print("\n #######################################################################################################################")
    print("  1. DISPLAY DETAILS BY CLIENT'S NAME")
    print("  2. DISPLAY DETAILS BY CLIENT'S ID")
    print("  3. DISPLAY DETAILS BY DATE OF REGISTRATION ")
    print("\n _______________________________________________________________________________________________________________________")
    c=input("\n  Enter your choice (1-3) --> ")
    try:
        c=int(c)
        if(c==1):
            show_by_name(admin_id)
        elif(c==2):
            show_by_id(admin_id)
        elif(c==3):
            show_by_date_of_reg(admin_id)
        else:
            print("\n  ENTER VALID CHOICE ...")
    except:
        print("\n  ENTER VALID CHOICE ...")

# ADMIN - 3. 2. 1. SHOW DETAILS BY NAME
def show_by_name(admin_id):
    res_rows=[]
    print("\n _______________________________________________________________________________________________________________________")
    cname=input(" Enter the Client's Name -->").lower()
    print("\n #######################################################################################################################")
    print("\t\t\t CLIENTS AND THEIR DETAILS ")
    print(" #######################################################################################################################\n")

    sql='''SELECT client.Id, client.Client_name, client.Email, client.Contact,
            services.Service_name, services.Date_of_registration, services.Time_period_in_days, services.Payment, services.Status
            FROM 'client' JOIN 'services'
            ON client.Id=services.Client_id
            WHERE  client.Admin_name = ? AND client.Client_name = ?'''
    conn=sqlite3.connect("clients.db")
    cursor=conn.cursor()
    cursor.execute(sql,(admin_id,cname))
    fetch = cursor.fetchall()
    for row in fetch:
        res_rows.append(row)
    cursor.close()
    conn.close()
    #calling the display_data function to diplay the resultant rows
    display_data(res_rows)

# ADMIN - 3. 2. 2. SHOW DETAILS BY ID
def show_by_id(admin_id):
    res_rows=[]
    print("\n _______________________________________________________________________________________________________________________")
    cid=input(" Enter the Client's Id -->")
    try:
        cid=int(cid)
        print("\n #######################################################################################################################")
        print(" \t\t\t CLIENTS AND THEIR DETAILS ")
        print("\n #######################################################################################################################")

        sql='''SELECT client.Id, client.Client_name, client.Email, client.Contact,
                services.Service_name, services.Date_of_registration, services.Time_period_in_days, services.Payment, services.Status
                FROM 'client' JOIN 'services'
                ON client.Id=services.Client_id
                WHERE  client.Admin_name = ? AND client.Id = ?'''
        conn=sqlite3.connect("clients.db")
        cursor=conn.cursor()
        cursor.execute(sql,(admin_id,cid))
        fetch = cursor.fetchall()
        for row in fetch:
            res_rows.append(row)
        cursor.close()
        conn.close()
        #calling the display_data function to diplay the resultant rows
        display_data(res_rows)
    except:
        print("\n  ENTER VALID CLIENT ID ...")


# ADMIN - 3. 2. 3. SHOW DETAILS BY DATE OF REGISTRATION
def show_by_date_of_reg(admin_id):
    res_rows=[]
    print("\n _______________________________________________________________________________________________________________________")
    cdate=input(" Enter the Client's Date of Registration(YYYY-MM-DD)  -->")
    print("\n #######################################################################################################################")
    print(" \t\t\t CLIENTS AND THEIR DETAILS ")
    print("\n #######################################################################################################################")

    sql='''SELECT client.Id, client.Client_name, client.Email, client.Contact,
            services.Service_name, services.Date_of_registration, services.Time_period_in_days, services.Payment, services.Status
            FROM 'client' JOIN 'services'
            ON client.Id=services.Client_id
            WHERE  client.Admin_name = ? AND services.Date_of_registration = ?'''
    conn=sqlite3.connect("clients.db")
    cursor=conn.cursor()
    cursor.execute(sql,(admin_id,cdate))
    fetch = cursor.fetchall()
    for row in fetch:
        res_rows.append(row)
    cursor.close()
    conn.close()
    #calling the display_data function to diplay the resultant rows
    display_data(res_rows)


#ADMIN - 4. SHOW NOTIFICATIONS
def show_notifications(admin_id):
    #sql_rows is a list that stores the details
    #which have less than or equal to a week time before their service time period ends
    sql_rows=[]
    rows=[]    #(Client_id,service.id,days_left)
    daysleft=[]
    sql='''SELECT services.Id, services.Client_id, services.Date_of_registration, services.Time_period_in_days
            FROM 'client' JOIN 'services'
            ON client.Id = services.Client_id
            WHERE services.Status="process" AND Admin_name = ? '''
    curr_date = datetime.now()
    conn=sqlite3.connect("clients.db")
    cursor=conn.cursor()
    cursor.execute(sql,(admin_id,))
    fetch = cursor.fetchall()
    flag=False
    for row in fetch:
        cdate=row[2].split("-")         #this gives a list of string values of reg_date
        cdate=[int(i) for i in cdate]   #changes to int values
        client_date=datetime(cdate[0],cdate[1],cdate[2])     #changes to datetime values
        days=int(str(curr_date-client_date).split()[0].split()[0])   #gives the no. of days between the current date and reg_date
        days_left=(int(row[3])) - days                   #gives the no. of days left for the completion of the service time period
        if(days_left<=7):
            flag=True
            rows.append((int(row[0]),int(row[1]),days_left))
    cursor.close()
    conn.close()
    print(" sql_rows -",sql_rows)
    print("daysleft - ",daysleft)
    conn=sqlite3.connect("clients.db")
    cursor=conn.cursor()
    sql='''SELECT client.Id, client.Client_name, client.Email, client.Contact,
            services.Service_name, services.Date_of_registration, services.Time_period_in_days, services.Payment, services.Status
            FROM 'client' JOIN 'services'
            ON client.Id=services.Client_id
            WHERE  client.Admin_name = ? AND services.Id = ? AND client.Id = ?  '''
    for r in rows:
        cursor.execute(sql,(admin_id,r[0],r[1]))
        res = cursor.fetchone()
        sql_rows.append(res)
        daysleft.append(r[2])
    print(" sql_rows -",sql_rows)
    print("daysleft - ",daysleft)
    print("\n #######################################################################################################################")
    print("\t\t\t\t NOTIFICATIONS ...")
    print("\n #######################################################################################################################")
    print("\n  \tTHESE CLIENTS HAVE LESS THAN OR EXACTLY A WEEK FOR THEIR SERVICE TIME PERIOD TO END ...")
    print(" _______________________________________________________________________________________________________________________")
    #calling the display_data function to diplay the resultant rows
    if(sql_rows!=[]):
        display_data_alert(sql_rows,daysleft)
    else:
        print("\n  NO NOTIFICATIONS ...")

    cursor.close()
    conn.close()


# HOMEPAGE OR COMMON DASHBOARD

# CALLING DATABASE METHOD TO CREATE THE DATABASE AND TABLES IF IT DOESN'T EXIST
database()

c_att=["Client_name", "Email", "Admin_name", "Contact"]
s_att=["Client_id", "Service_name", "Time_based", "Date_of_registration", "Time_period_in_days", "Payment", "Status" ]

flag=True
while(flag):
    welcome()
    print("\n ************************************ CLIENT ********* MANAGEMENT ********* SYSTEM ************************************")
    print(" #######################################################################################################################\n")
    print("\n  1. REGISTER")
    print("  2. LOGIN")
    print(" _______________________________________________________________________________________________________________________")
    c = input("\n  Enter your choice (1-2) -->")
    try:
        c=int(c)
        if(c==1):
            register()
        elif(c==2):
            login()
        else:
            print("\n  Please enter valid choice...")
            print("\n _______________________________________________________________________________________________________________________")
            f=input("\n  DO YOU WANT TO TRY LOGGING IN OR REGISTERING AGAIN ?? (Y / N) ").lower()
            if (f=='y' or f=="yes"):
                continue
            else:
                flag=False
    except:
        print("\n  Please enter valid choice...")

    if(flag):
        print(" _______________________________________________________________________________________________________________________")
        f=input("\n  DO YOU WANT TO TRY LOGGING IN OR REGISTERING AGAIN ?? (Y / N) ").lower()
        if (f=='y' or f=="yes"):
            continue
        else:
            flag=False
