from flask import render_template, Flask, jsonify, redirect, request, url_for, send_file
from flask_mysqldb import MySQL
import originscraper

app = Flask(__name__)

app.config["MYSQL_USER"] = 'sql4397169'
app.config["MYSQL_PASSWORD"] = 'wHMPPqiMDy'
app.config["MYSQL_HOST"] = 'sql4.freemysqlhosting.net'
app.config["MYSQL_DB"] = 'sql4397169'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'

mysql = MySQL(app)


@app.route("/", methods=["GET", "POST"])
def load_app():
	if request.method == "GET":
		return render_template("homehtml.html", isithiddenvar='None')
	if request.method == "POST":
		weight = request.form["weight"]
		food = request.form["food"].lower()
		kilocalories, fuel_used = originscraper.main(weight, food)
		fuel_used = fuel_used * int(weight)/112000000
		# this accounts for the fact a plane won't just be carrying one banana, it will be carrying a lot of food
		# cargo weight of a boeing 747
		cur = mysql.connection.cursor()
		# fix thiss
		cur.execute(f'''SELECT item FROM table1''')
		items = cur.fetchall()
		for it in items:
			str_it = it["item"].lower()
			if str_it in food:
				food_query = str_it
			else:
				food_query = "Fresh fruit"  # in case not listed in db, this is our backup value for other fresh food
		cur.execute(f'''SELECT water, energy FROM table1 WHERE item="{food_query}"''')
		listvals = cur.fetchall()[0]
		waterperunit = listvals['water']
		energyperunit = listvals['energy']
		water_used = waterperunit * kilocalories
		energy_used = energyperunit * kilocalories
		waterequivalent = water_used/0.25
		fuelequivalent = fuel_used/1.5
		energyequivalent = energy_used/0.138
		return render_template("homehtml.html", water_used=water_used, energy_used=energy_used, fuel_used=fuel_used,
							   isithiddenvar='Block', weight=weight, food=food, waterequivalent=waterequivalent, fuelequivalent=fuelequivalent, energyequivalent=energyequivalent)


def main():
	app.run(debug=True)


if __name__ == "__main__":
	main()
