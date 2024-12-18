#Database connection details
import mysql.connector
import scanner
conn_obj=mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@jdeep123",
    database="aug_python_project_MSM")
cur_obj=conn_obj.cursor()

#Define function data_entry_sql
def data_entry_sql(full_name,address,ph_no):

    # Build the query with user-provided name using LIKE operator
    sql = "INSERT INTO cust_details(cust_full_name,cust_ph_no,cust_address) VALUES (%s, %s, %s)"
    data = (full_name,ph_no,address)

    try:
        cur_obj.execute(sql, data)
        print("Cust successfully enterted into our database.")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()

#Define function data_retrieve
def data_retrieve(ph_no):
    query = f"select * from cust_details WHERE cust_ph_no={ph_no}"
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return result

def find_product_details_from_db(p_id):
    query = f"select * from p_details WHERE p_id={p_id}"
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return result

def invoice_table_data_entry(cust_id, cust_name, bill_amount):

    # Build the query with user-provided name using LIKE operator
    sql = "INSERT INTO invoice_table(cust_id, cust_name, bill_amount) VALUES (%s, %s, %s)"
    data = (cust_id, cust_name, bill_amount)

    try:
        cur_obj.execute(sql, data)
        print("Bill details entry successful")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
#main logic
ph_no=input("Please enter customer phone number- ")
details_from_db=data_retrieve(ph_no)
#print(details_from_db)
if details_from_db:
    cust_id=details_from_db[0]
    cust_name=details_from_db[1]
    total_bill_amount=0
    while True:
        #p_id=int(input("Please enter product id- "))
        p_details_from_qr=scanner.qr_code_scanner()
        product_details_list=p_details_from_qr.split(',')
        p_id=product_details_list[0]
        #print(p_id.split(','))
        product_details_db=find_product_details_from_db(p_id)
        p_price_db=product_details_db[2]
        p_quantity=int(input("Please enter product quantity- "))
        bill_amount=p_price_db*p_quantity
        total_bill_amount=total_bill_amount+bill_amount
        print("Bill amount",total_bill_amount)
        user_selection=input("Enter q to quit- ")
        if user_selection=='q' or user_selection=='Q':
            break
    invoice_table_data_entry(cust_id, cust_name, total_bill_amount)
else:
    full_name=input("Enter customer full name- ")
    address=input("Enter customer full address- ")
    data_entry_sql(full_name,address,ph_no)
conn_obj.close()
