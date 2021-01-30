import mysql.connector

class UserHistory:

    ## check user History Table for Expensive and Premium
    def userHist(self, acountNumber, methodName):

        ## creating connection on MYSQL server
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="flask"
        )

        cursor = mydb.cursor()

   #     if methodName == "expensive":
   #         tableName  = "userHistory"
   #     if methodName == "premium":
   #         tableName = "premium"

        sql = "SELECT * FROM "+methodName+" WHERE card_number = %s"
        cardNum = (acountNumber,)

        cursor.execute(sql, cardNum)

        data = cursor.fetchall()

        userHist = []
        for x in data:
            # uId = x[0]
            # emailId = x[3]
            userHist.append(x)

        length = len(userHist)

        return length

    ## save entry for a user in userHistory table for Expensive method
    def UpdateUserHistoryTable(self, accHolderName, cardNumber):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="flask"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO userHistory (acc_holder_name, card_number) VALUES (%s, %s)"
        val = (accHolderName, cardNumber)
        mycursor.execute(sql, val)
        mydb.commit()
        value = mycursor.rowcount
        print(mycursor.rowcount, "record inserted.")
        return value

    ## save user data in premium table for Premium payment Method
    def PremiumHistory(self, accHolderName, cardNumber):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="flask"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO premium (acc_holder_name, card_number) VALUES (%s, %s)"
        val = (accHolderName, cardNumber)
        mycursor.execute(sql, val)
        mydb.commit()
        value = mycursor.rowcount
        print(mycursor.rowcount, "record inserted.")
        return value

    def createTable(self):

        ## creating connection on MYSQL server
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="flask"
        )
        cursor = mydb.cursor()
        cursor.execute("CREATE TABLE premium (id INT AUTO_INCREMENT PRIMARY KEY, acc_holder_name VARCHAR(255), card_number VARCHAR(255))")
        cursor = mydb.cursor()
        cursor.execute("CREATE TABLE expensive (id INT AUTO_INCREMENT PRIMARY KEY, acc_holder_name VARCHAR(255), card_number VARCHAR(255))")
        return "Table Created"
