from env import secure
import mysql.connector

# Database class
class Database:

    db = mysql.connector.connect(
    host = secure.DATABASE_HOST,
    user = secure.DATABASE_USER,
    password = secure.DATABASE_PASS,
    database = secure.DATABASE_NAME,
    auth_plugin="mysql_native_password"

    )
    cursor = db.cursor(buffered=False)