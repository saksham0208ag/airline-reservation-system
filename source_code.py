import pymysql
import pymysql.cursors


db_config = {
    "host": "localhost",
    "user": "root",
    "db": "Airlines",
}

connection = pymysql.connect(**db_config)
cursor = connection.cursor()


def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PASSENGER (
            Passenger_ID INT PRIMARY KEY AUTO_INCREMENT,
            Name VARCHAR(255) NOT NULL,
            Date_of_Birth DATE NOT NULL,
            Nationality VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AIRPORT (
            Airport_id VARCHAR(255) PRIMARY KEY,
            City VARCHAR(255) NOT NULL,
            Number_of_runways INT NOT NULL,
            Airport_Type VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AEROPLANE (
            Aeroplane_id INT PRIMARY KEY AUTO_INCREMENT,
            Airline_Name VARCHAR(255) NOT NULL,
            Capacity INT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS FLIGHT (
            Flight_id INT PRIMARY KEY AUTO_INCREMENT,
            departure_date DATE NOT NULL,
            departure_time TIME NOT NULL,
            Arrival_city VARCHAR(255) NOT NULL,
            Departure_city VARCHAR(255) NOT NULL,
            Aeroplane_id INT NOT NULL,
            Duration TIME NOT NULL,
            FOREIGN KEY (Aeroplane_id) REFERENCES AEROPLANE(Aeroplane_id)
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TICKET (
            PNR INT PRIMARY KEY AUTO_INCREMENT,
            Passenger_ID INT NOT NULL,
            Flight_id INT NOT NULL,
            Seat_Number INT NOT NULL,
            Ticket_price INT NOT NULL,
            Booking_Date DATE NOT NULL,
            Booking_time TIME NOT NULL,
            FOREIGN KEY (Passenger_ID) REFERENCES PASSENGER(Passenger_ID),
            FOREIGN KEY (Flight_id) REFERENCES FLIGHT(Flight_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SHOPS (
            Shop_Name VARCHAR(255) NOT NULL,
            Airport_id VARCHAR(255) NOT NULL,
            FOREIGN KEY (Airport_id) REFERENCES AIRPORT(Airport_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BAGGAGE (
            Baggage_ID INT PRIMARY KEY AUTO_INCREMENT,
            Ticket_ID INT NOT NULL,
            Weight INT NOT NULL,
            FOREIGN KEY (Ticket_ID) REFERENCES TICKET(PNR)
        )
    """)

    connection.commit()

create_tables()

def func():
    print("Enter c to continue or q to quit")
    ch = input()
    if(ch == 'c'):
        return
    else:
        exit()

def schedule_flight():
    print("Enter flight details: ")
    row = {}
    while True:
        row["Aeroplane_id"] = int(input("Aeroplane ID: "))
        query = "SELECT * FROM AEROPLANE WHERE Aeroplane_id = %d" % (row["Aeroplane_id"])
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            print("Aeroplane does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()
        else:
            break
    row["Departure_city"] = input("Departure City: ")
    row["Arrival_city"] = input("Arrival City: ")
    row["Departure_date"] = input("Departure Date (YYYY-MM-DD): ")
    row["Departure_time"] = input("Departure Time (HH:MM:SS): ")
    row["Duration"] = input("Duration (HH:MM:SS): ")
    query="INSERT INTO FLIGHT(departure_date, departure_time, Arrival_city, Departure_city, Aeroplane_id, Duration) VALUES('%s', '%s', '%s', '%s', %d, '%s')" % (
        row["Departure_date"], row["Departure_time"], row["Arrival_city"], row["Departure_city"], row["Aeroplane_id"], row["Duration"])
    cursor.execute(query)
    connection.commit()
    print("Inserted Into Database")
    func()
    
def book_ticket():
    print("Enter ticket details: ")
    row = {}
    while True:
        row["Passenger_ID"] = int(input("Passenger ID: "))
        query = "SELECT * FROM PASSENGER WHERE Passenger_ID = %d" % (row["Passenger_ID"])
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Passenger does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()

    while True:
        row["Flight_id"] = int(input("Flight ID: "))
        query = "SELECT * FROM FLIGHT WHERE Flight_id = %d" % (row["Flight_id"])
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Flight does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()
    row["Seat_Number"] = int(input("Seat Number: "))
    row["Ticket_Price"] = int(input("Ticket Price: "))  
    row["Booking_Date"] = input("Booking Date (YYYY-MM-DD): ")
    row["Booking_time"] = input("Booking Time (HH:MM:SS): ")
    query = "INSERT INTO TICKET(Passenger_ID, Flight_id, Seat_Number, Ticket_Price, Booking_Date, Booking_time) VALUES(%d, %d, %d, %d, '%s', '%s')" % (
        row["Passenger_ID"], row["Flight_id"], row["Seat_Number"], row["Ticket_Price"], row["Booking_Date"], row["Booking_time"])
    cursor.execute(query)
    connection.commit()
    print("Inserted Into Database")
    print("Enter c to continue or q to quit")
    ch = input()
    if(ch == 'c'):
        return
    else:
        exit()

def insert_passenger():
    print("Enter Passenger details: ")
    row = {}
    row["Name"] = input("Name: ")
    row["Date_of_Birth"] = input("Date of Birth (YYYY-MM-DD): ")
    row["Nationality"] = input("Nationality: ")
    query = "INSERT INTO PASSENGER(Name, Date_of_Birth, Nationality) VALUES('%s', '%s', '%s')" % (
        row["Name"], row["Date_of_Birth"], row["Nationality"])
    cursor.execute(query)
    connection.commit()
    print("Inserted Into Database")
    func()

def insert_airport():
    print("Enter Airport details: ")
    row = {}
    row["Airport_id"] = input("Airport ID: ")
    row["City"] = input("City: ")
    row["Number_of_runways"] = int(input("Number of Runways: "))
    row["Airport_Type"] = input("Airport Type: ")
    query = "INSERT INTO AIRPORT(Airport_id, City, Number_of_runways, Airport_Type) VALUES('%s', '%s', %d, '%s')" % (
        row["Airport_id"], row["City"], row["Number_of_runways"], row["Airport_Type"])
    cursor.execute(query)
    connection.commit()
    print("Inserted Into Database")
    func()

def insert_aeroplane():
    print("Enter Aeroplane details: ")
    row = {}
    row["Airline_Name"] = input("Airline Name: ")
    row["Capacity"] = int(input("Capacity: "))
    query = "INSERT INTO AEROPLANE(Airline_Name, Capacity) VALUES('%s', %d)" % (
        row["Airline_Name"], row["Capacity"])
    cursor.execute(query)
    connection.commit()
    print("Inserted Into Database")
    func()

def insert_baggage():
    print("Enter Baggage details: ")
    row = {}
    while True:
        row["Ticket_ID"] = int(input("Ticket ID: "))
        query = "SELECT * FROM TICKET WHERE PNR = %d" % (row["Ticket_ID"])
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Ticket does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()
    
    row["Weight"] = int(input("Weight: "))
    query = "INSERT INTO BAGGAGE(Ticket_ID, Weight) VALUES(%d, %d)" % (
        row["Ticket_ID"], row["Weight"])
    cursor.execute(query)
    connection.commit()
    print("Inserted Into Database")
    func()

def insert_shop():
    print("Enter Shop details: ")
    row = {}
    row["Shop_Name"] = input("Shop Name: ")
    while True:
        row["Airport_id"] = input("Airport ID: ")
        query = "SELECT * FROM AIRPORT WHERE Airport_id = '%s'" % (row["Airport_id"])
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Airport does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()
    query = "INSERT INTO SHOPS(Shop_Name, Airport_id) VALUES('%s', '%s')" % (
        row["Shop_Name"], row["Airport_id"])
    cursor.execute(query)
    connection.commit()

def insertquery():
    print("Choose the type of insert query you want to perform")
    print("1. Schedule a flight")
    print("2. Book a ticket")
    print("3. Insert a new passenger")
    print("4. Insert a new airport")
    print("5. Insert a new aeroplane")
    print("6. Insert a Baggage")    
    print("7. Insert a new shop")
    ch = int(input("Enter choice> "))
    if(ch==1):
        schedule_flight()
    elif(ch==2):
        book_ticket()
    elif(ch==3):
        insert_passenger()
    elif(ch==4):
        insert_airport()
    elif(ch==5):
        insert_aeroplane()
    elif(ch==6):
        insert_baggage()
    elif(ch==7):
        insert_shop()

def cancel_ticket():
    while True:
        print("Enter ticket number: ")
        id = int(input())
        query = "SELECT * FROM TICKET WHERE PNR = %d" % (id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Ticket does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()
        
    query="DELETE FROM Baggage where Ticket_ID= %d " % (id)
    cursor.execute(query)
    connection.commit()
    query = "DELETE FROM TICKET WHERE PNR = %d" % (id)
    cursor.execute(query)
    connection.commit()
    print("Ticket Cancelled")
    func()

def cancel_flight():
    while True:
        print("Enter flight number: ")
        id = int(input())
        query = "SELECT * FROM FLIGHT WHERE Flight_id = %d" % (id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Flight does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()
    query="DELETE FROM TICKET where Flight_id= %d " % (id)
    cursor.execute(query)
    connection.commit()
    query = "DELETE FROM FLIGHT WHERE Flight_id = %d" % (id)
    cursor.execute(query)
    connection.commit()
    print("Flight Cancelled")
    func()

def deletequery():
    print("Choose the type of delete query you want to perform")
    print("1. Cancel a flight")
    print("2. Cancel a ticket")
    ch = int(input("Enter choice> "))
    if(ch==1):
        cancel_flight()
    elif(ch==2):
        cancel_ticket()

def update_passenger():
    while True:
        print("Enter passenger id: ")
        id = int(input())
        query = "SELECT * FROM PASSENGER WHERE Passenger_ID = %d" % (id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Passenger does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()
    print("Do you want to update name? (y/n)")
    str = input()
    if (str == 'y'):
        print("Enter new name: ")
        name = input()
        query = "UPDATE PASSENGER SET Name = '%s' WHERE Passenger_ID = %d" % (name, id)
        cursor.execute(query)
        connection.commit()
    print("Do you want to update Date of Birth? (y/n)")
    str = input()
    if (str == 'y'):
        print("Enter new Date of Birth: ")
        dob = input()
        query = "UPDATE PASSENGER SET Date_of_Birth = '%s' WHERE Passenger_ID = %d" % (dob, id)
        cursor.execute(query)
        connection.commit()
    print("Do you want to update Nationality? (y/n)")
    str = input()
    if (str == 'y'):
        print("Enter new Nationality: ")
        nationality = input()
        query="UPDATE PASSENGER SET Nationality = '%s' WHERE Passenger_ID = %d" % (nationality, id)
        cursor.execute(query)
        connection.commit()
    print("Updated Passenger Details")
    func()

def reschedule_flight():
    while True:
        print("Enter flight number: ")
        id = int(input())
        query = "SELECT * FROM FLIGHT WHERE Flight_id = %d" % (id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Flight does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()

    print("Enter new departure date: ")
    date = input()
    print("Enter new departure time: ")
    time = input()
    query = "UPDATE FLIGHT SET departure_date = '%s', departure_time = '%s' WHERE Flight_id = %d" % (date, time, id)
    cursor.execute(query)
    connection.commit()
    print("Flight Rescheduled")
    func()

def updatequery():
    print("Choose the type of update query you want to perform")
    print("1. Update details of a passenger")
    print("2. Reschedule a flight")
    ch = int(input("Enter choice> "))
    if(ch==1):
        update_passenger()
    elif(ch==2):
        reschedule_flight()
    else:
        print("Error: Invalid Option")


def printpassdet():
    while True:
        print("Enter passenger id: ")
        id = int(input())
        query = "SELECT * FROM PASSENGER WHERE Passenger_ID = %d" % (id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Passenger does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()
    
    query = "SELECT * FROM PASSENGER WHERE Passenger_ID = %d" % (id)
    cursor.execute(query)
    result = cursor.fetchall()
    # for row in result:
    print(result)

def printtickdet():
    while True:
        print("Enter ticket number: ")
        id = int(input())
        query = "SELECT * FROM TICKET WHERE PNR = %d" % (id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Ticket does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()

    query = "SELECT * FROM TICKET WHERE PNR = %d" % (id)
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)

def domairports():
    query = "SELECT * FROM AIRPORT WHERE Airport_Type = 'Domestic'"
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print(row)

def totalrevenue():
    while True:
        print("Enter flight id: ")
        id = int(input())
        query = "SELECT * FROM FLIGHT WHERE Flight_id = %d" % (id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("Flight does not exist")
            print("Enter c to continue or q to quit")
            ch = input()
            if(ch == 'q'):
                exit()


    query = "SELECT SUM(Ticket_price) FROM TICKET WHERE Flight_id = %d" % (id)
    cursor.execute(query)
    result = cursor.fetchall()
    print("Total Revenue: ", result)

def avgfare():
    print("Enter departure city: ")
    dep = input()
    print("Enter arrival city: ")
    arr = input()
    query = "SELECT AVG(Ticket_price) FROM TICKET JOIN FLIGHT ON TICKET.Flight_id=FLIGHT.Flight_id WHERE Departure_city = '%s' AND Arrival_city = '%s'" % (
    dep, arr)
    cursor.execute(query)
    result = cursor.fetchall()
    print("The average fare is: ", result)

def mostusedairline():
    query = "SELECT A.Airline_Name FROM FLIGHT AS F JOIN AEROPLANE AS A ON A.Aeroplane_id = F.Aeroplane_ID GROUP BY A.Airline_Name ORDER BY COUNT(F.Flight_id) DESC LIMIT 1;"
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print(result)

def option7():
    print("Enter the Departure_date: ")
    date = input()
    query = "SELECT F.Flight_id, F.Arrival_city, F.Departure_city FROM FLIGHT AS F JOIN ticket AS T ON T.Flight_id = F.Flight_id WHERE F.departure_date = '%s' ORDER BY F.departure_time ASC, T.Ticket_price ASC;" % (date)
    cursor.execute(query)
    result = cursor.fetchall()
    # for row in result:
    print(result)

def viewquery():
    print("Choose the type of view query you want to perform")
    print("1. Print passenger details")
    print("2. Print ticket details")
    print("3. List of domestic airports")
    print("4. Total revenue collected by a flight")
    print("5. Determine the average fare for flights between two specific airports")
    print("6. Select the most used airline")
    print("7. Print All flights from one city to another having same date and time")
    ch = int(input("Enter choice> "))
    if(ch==1):
        printpassdet()
    elif(ch==2):
        printtickdet()
    elif(ch==3):
        domairports()
    elif(ch==4):
        totalrevenue()
    elif(ch==5):
        avgfare()
    elif(ch==6):
        mostusedairline()
    elif(ch==7):
        option7()


def callqueries(ch):
    if(ch == 1):
        insertquery()
    elif(ch == 2):
        deletequery()
    elif(ch == 3):
        updatequery()
    elif(ch == 4):
        viewquery()
    else:
        print("Invalid Option")
    

while (1):
    print("Select the type of query you want to perform")
    print("1. Insert")
    print("2. Delete")
    print("3. Update")
    print("4. View")
    print("5. Exit")
    ch = int(input("Enter choice> "))
    if(ch==5):
        break
    else:
        callqueries(ch)


cursor.close()
connection.close()


