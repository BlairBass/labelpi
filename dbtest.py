from script.sqlbrowser import get_instance_info
import pymssql



sql = get_instance_info("192.168.10.5", "KS21DB")
port = sql[0]['tcp']
server = "192.168.10.5," + port
print(server)

#con = pymssql.connect(server=r"192.168.10.5\\KS21DB", database="KS21DB", user=r"pgl\\gala365", tds_version="8.0")

con = pymssql.connect(host=r"192.168.10.5\KS21DB", database="KS21GO360", user=r"labelpi", password="labelpi", tds_version="8.0")
cursor = con.cursor()
cursor.execute("SELECT * FROM tbLVKopf WHERE LVNr = '136' AND ArbeitsbereichNum = 1")
row = cursor.fetchone()

print(row)