import psycopg2

separator = (45*"*")
overscore = (45*"-")
underscore = (45*"_")

def connect_database():
    """Funktionen som ansluter till databasen"""
    return psycopg2.connect(dbname="Dbprojekt", user="ai7596", password="70fab1nu", host="pgserver.mah.se")

def disconnect_database():
    """Funktionen som kopplar ifrån databasen"""
    con = connect_database()
    con.close()   

def main():
    """Funktionen som kör programmet och printar menyn"""
    print_menu()
    while True:
        user_input = input("{}".format("Select option: "))
        if user_input == "0":
            show_bookings()
            break
        elif user_input == "1":
            travelers()
            break
        elif user_input == "2":
            bus_info()
            break
        elif user_input == "3":
            print("{}".format("Thank you for your time!"))
            print("")
            break
        else:
            continue

def print_menu():
    """Funktionen för menyn"""
    print(separator)
    print("{:<10}|{:<10}|{:<10}".format("","Welcome To Mörtfors", ""))
    print("{}".format("|You need to be registered to book a trip|"))
    print(separator)
    print("")
    print("{}".format("0. Show my bookings"))
    print("{}".format("1. Register"))
    print("{}".format("2. Already Registered"))
    print("{}".format("3. Quit"))
    print("")

def bus_info(email = ''):
    """Funktionen visar informatiionen till bussarna som finns, frågar användaren 2vilken buss de vill välja!"""
    con = connect_database()
    cur = con.cursor()
    print(separator)
    print("{}".format("Booking"))
    print(separator)
    print("")
    #GLÖM INTE FIXA FELMEDDELANDE SÅ ATT ANVÄNDAREN INTE KAN VÄLJA FEL STAD
    cur.execute("SELECT bus_info.departure_des from bus_info GROUP BY departure_des")
    all_results2 = cur.fetchall()
    print("")
    print("|{:<10}|".format("Cities to travel From: "))
    for result in all_results2:
        print("|{:<10}|".format(result[0]))
    print("")
    
    fr_om = input("Choose from the choises above: ")
    #GLÖM INTE FIXA FELMEDDELANDE SÅ ATT ANVÄNDAREN INTE KAN VÄLJA FEL STAD
    cur.execute("SELECT bus_info.arrival_des from bus_info WHERE bus_info.departure_des iLike %s GROUP BY arrival_des", (fr_om,))
    all_results3 = cur.fetchall()
    print("")
    print("|{:<10}|".format("Cities to travel to: "))
    for result in all_results3:
        print("|{:<10}|".format(result[0]))
    print("")
    
    to = input("Choose to  the city from the choises above: ")
    cur.execute("SELECT trip_info.trip_id, bus_info.departure_des, bus_info.arrival_des, trip_info.da_te, trip_info.departure_time, trip_info.arrival_time, trip_info.price FROM bus_info, trip_info WHERE bus_info.departure_des iLIKE %s AND bus_info.arrival_des iLIKE %s AND bus_info.id = trip_info.bus_id" ,(fr_om, to,))
    all_results = cur.fetchall()
    print("|{:<10}|{:<15}|{:<15}|{:<15}|{:<15}|{:<15}|{:<15}".format("Bus", "From", "To", "Date", "Departure time", "Arrival time", "Price"))
    for result in all_results:
        print("|{:<10}|{:<15}|{:<15}|{}{:<5}|{}{:<7}|{}{:<7}|{:<15}".format(result[0], result[1], result[2], result[3], "", result[4], "", result[5], "", result[6]))

    while True:
        print(separator)
        bus_number = input("Select bus: ")
        
        if locate_bus(bus_number) == False:
            print("{}".format("The buss coudn´t be found! Please try again! "))
            print(separator)
            print("")
            continue    
        else:
            True
            trip_info(bus_number, email)
        break

def locate_bus(id):
    """Denna funktionen tar input som användaren skrev in i funktionen(bus_info) för att se om buss numret finns med i databasen"""
    con = connect_database()
    cur = con.cursor()
    if id.isdigit() == False:
        return False
    else:
        #GLÖM INTE FIXA FELMEDDELANDET SÅ ATT ANVÄNDAREN INTE VÄLJER EN BUSS SOM INTE FINNS I LISTAN
        cur.execute("SELECT EXISTS (SELECT * FROM trip_info WHERE trip_id=%s)", (id,))
        return cur.fetchone()[0]


def bus_stop(id, email, seat_confirm):
    """Visar användaren infon till resan som valdes, frågar användaren om mail adress om han inte redan är registrerad"""
    con = connect_database()
    cur = con.cursor()
    cur.execute("SELECT country, city, street_name FROM bus_stop WHERE bus_id=%s", (id,))
    all_results = cur.fetchall()
    for result in all_results:
        print("{}".format("Bus you selected start/end position info"))
        print(overscore)
        print("{:<40}|{:<40}".format("Departure/Arrival countries: ", result[0]))
        print("")
        print("{:<40}|{:<40}".format("Departure/Arrival cities: ", result[1]))
        print("")
        print("{:<40}|{:<40}".format("Arrival destination address: ", result[2]))
        print(overscore)
    while True:
        if email != '':
            booking_confirm(id, seat_confirm, email)
        else:
            registered = input("To continue, please enter your email: ")
            if user_exist(registered):
                booking_confirm(id, registered, seat_confirm)
                print("")
            else:
                print("{}{}{}".format("The email that you entered (", registered ,") does not exsist"))
                continue
        break

def show_bookings():
    pass


def travelers():
    """Funktionen som registrerar användaren i databasen"""
    con = connect_database()
    cur = con.cursor()
    print(overscore)
    print("{:<8}|{:<10}|{:<8}".format("","MÖRTFORS REGISTRATION FORM",""))
    print(overscore)
    print("")
    while True:
        name = input("{}".format("First name: "))
        if name.isalpha():
            True
        else:
            print("{}".format("Try again.. "))
            continue
        address = input("{}".format("Address: "))
        email = input("{}".format("Email: "))
        while True:
            phone_nr = input("{}".format("Phone number?: "))
            if phone_nr.isdigit():
                break
            else:
                print("{}".format("Try again.. "))
                continue
        break 
    query = "INSERT INTO travelers (prn_name, street_name, email, phone_nr) VALUES (%s, %s, %s, %s)"
    traveler_input = (name, address, email, phone_nr)
    cur.execute(query, traveler_input)
    con.commit()
    print("{}".format("Thank you for registering"))
    print(separator)
    bus_info(email)
    disconnect_database()

def user_exist(email):
    """Kontrollerar så att användaren finns i databasen"""
    con = connect_database()
    cur = con.cursor()
    cur.execute("SELECT exists (SELECT * FROM travelers WHERE email=%s)", (email,))
    return cur.fetchone()[0]

def trip_info(id, email):
    """Skiver ut tillgängliga resor som finns den bussen som valdes, """
    con = connect_database()
    cur = con.cursor()
    print("|{:<10}|{:<15}".format("Bus", "Seating left"))
    print(underscore*2)
    print("")
    cur.execute("SELECT trip_id, seating FROM trip_info WHERE trip_id=%s", (id,))
    all_results = cur.fetchall()
    for result in all_results:
        seating = result[1]
        print("|{:<10}|{:<5}".format(result[0], result[1], sep=''))
    print(separator*2)
    print("")
    print("{}".format("We have found these choices above!"))
    print("{}".format("Continue with the booking?"))
    print("")
    while True:
        print("{}".format("1. Continue"))
        print("{}".format("2. Cancel"))
        confirmation = input("Select option: ")
        print("")
        if confirmation == "1":
            while True:
                seat_confirm = input("How many passengers are traveling? ")
                if seat_confirm.isdigit() == False:
                    print("{}".format("Please enter a number.."))
                    print("")
                    continue
                elif int(seat_confirm) > int(seating):
                    print("{}".format("Not enough seats! Please try again.."))
                    print("")
                    continue
                else:
                    print("")
                    bus_stop(id, email, seat_confirm)
                    True    
                break
            print(separator)        
        elif confirmation == "2":
            print("{}".format("Your booking has been canceled"))
            break
        else:
            print("{}".format("Please enter a vaild choice.."))
            continue
        break

def booking_confirm(id, email, seat_confirm):
    """Skriver ut boknings information för användaren"""
    con = connect_database()
    cur = con.cursor()
    print("")
    print("{}".format("BOOKING CONFIIRMATION"))
    print(underscore)
    cur.execute("SELECT da_te, departure_time, arrival_time, price FROM trip_info WHERE trip_id=%s", (id,))
    all_results = cur.fetchall()
    for result in all_results:
        print("|{:<25}|{}".format("Date: ", result[0]))
        print("|{:<25}|{}".format("Departure time: ", result[1]))
        print("|{:<25}|{}".format("Arrival time: ", result[2]))
        print("|{:<25}|{}{}".format("Price: ", result[3],"Kr"))
    
    cur.execute("SELECT travelers.id FROM travelers, trip_info WHERE trip_id=%s AND email=%s", (id, email,))
    all_results2 = cur.fetchall()
    query = "INSERT INTO bookings (trip_id, prn_id) VALUES (%s, %s)"
    traveler_input = (id, all_results2[0])
    cur.execute(query, traveler_input)
    con.commit()
    print("|{:<25}|{:<25}".format("Bus number: ", id))
    print("|{:<25}|{:<25}".format("Email: ", email))
    print("|{:<25}|{:<25}".format("Booked seating: ", seat_confirm))
    print("")
    print(separator)
    print("{}".format("Thank you for choosing Mörtfors buss!"))
    print("{}".format("Have a good day!"))


main()
