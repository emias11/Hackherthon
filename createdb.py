from flask import render_template, Flask, jsonify, redirect, request, url_for, send_file
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config["MYSQL_USER"] = 'sql4397169'
app.config["MYSQL_PASSWORD"] = 'wHMPPqiMDy'
app.config["MYSQL_HOST"] = 'sql4.freemysqlhosting.net'
app.config["MYSQL_DB"] = 'sql4397169'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'

mysql = MySQL(app)

item = ["Fresh fruit", "citrus", "apples","apricots","avocados","bananas","blueberries","cantaloupe","cherries","cranberries",
		"grapes","honeydew","kiwi","mangoes","papaya","peaches","pears","pineapples","plums","raspberries","strawberries",
		"watermelon","Processed fruit","canned fruit","frozen fruit","dried fruit","fruit juices","Fresh vegetables",
		"artichokes","asparagus","bell peppers","broccoli","brussel sprouts","cabbage","carrots","cauliflower","celery",
		"collards","sweet corn","cucumbers","eggplant", "escarole & endive","garlic","kale", "head lettuce",
		"romaine & leaf lettuce","lima beans","mushrooms","mustard greens","okra","onions", "potatoes","pumpkin","radishes",
		"snap beans","spinach","squash","sweet potatoes","tomatoes","turnip greens"]

energy = [0.045, 0.011, 0.0061, 0.0016, 0.00065, 0.013, 0.016, 0.071, 0.013, 0.021, 0.013, 0.067, 0.19, 0.18, 0.3, 0.0059,
		  0.0055, 0.0062, 0.015, 0.016, 0.036, 0.08, 0, 0.041, 0.011, 0.018, 0.081, 0.033, 0.062, 0.013, 0.089, 0.1, 0.068,
		  0.019, 0.0068, 0.12, 0.019, 0.096, 0.011, 0.2, 0.21, 0.18, 0.0022, 0.058, 0.23, 0.17, 0.08, 0.022, 0.11,
		  0.093, 0.0079, 0.0094, 0.11, 0.18, 0.29, 0.12, 0.18, 0.0056, 0.29, 0.09]

water = [0.32, 0.3, 0.36, 0.12, 0.26, 0.23, 0.56, 0.097, 1.1, 0.24, 0.22, 0.092, 0.54, 0.95, 0.13, 0.62, 0.24, 0.014, 0.74,0.27,
		 0.25, 0.2, 0, 0.77, 0.084, 0.39, 0.3, 0.18, 0.76, 3.6, 0.34, 0.15,0.12,0.31,0.059, 0.21, 0.17,0.2, 0.18, 0.78, 0.26,
		 0.22, 0.09, 0.14, 0.28, 0.21, 0.083, 1.0, 0.27, 0.42, 0.11, 0.087, 0.1, 0.093, 0.31, 0.11, 0.17, 0.027, 0.39,
		 0.074]


@app.route("/")
def index():
	cur = mysql.connection.cursor()
	# cur.execute('''CREATE TABLE table1 (item VARCHAR(100), energy FLOAT, water FLOAT)''')
	for i in range(0, len(item)):
		cur.execute(f'''INSERT INTO table1 VALUES ("{item[i]}", {energy[i]}, {water[i]})''')
	mysql.connection.commit()
	return " "


def main():
	app.run(debug=True)


if __name__ == "__main__":
	main()