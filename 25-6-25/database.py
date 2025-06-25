import mysql.connector

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",      # Replace with your MySQL username
    password="root",  # Replace with your MySQL password
    database="gym"             # Database should already exist
)

cursor = conn.cursor()

# Step 2: Create simple member table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    phone_number VARCHAR(15)
)
""")

# Step 3: Insert one record
insert_query = "INSERT INTO user (name, age, phone_number) VALUES (%s, %s, %s)"
data = ("Alice", 30, "9876543210")
data2 =   ("Abhijeet" ,  25 , "123456789")
cursor.execute(insert_query, data)
cursor.execute(insert_query , )

conn.commit()

# Step 4: Fetch and print all records
cursor.execute("SELECT * FROM user")
rows = cursor.fetchall()

print("All members:")
print("ID | Name | Age | Phone Number")
for row in rows:
    print(row)

# Step 5: Close connection
cursor.close()
conn.close()