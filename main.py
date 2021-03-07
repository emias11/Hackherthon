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
		print(request.args)
		return render_template("homehtml.html", isithiddenvar='None')
	if request.method == "POST":
		weight = request.form["weight"]
		food = request.form["food"]
		kilocalories, fuel_used = originscraper.main(weight, food)

		cur = mysql.connection.cursor()
		#fix this
		cur.execute(f'''SELECT water, energy FROM table1 WHERE item="{food}"''')
		listvals = cur.fetchall()[0]
		waterperunit = listvals['water']
		energyperunit = listvals['energy']
		water_used = waterperunit * kilocalories
		energy_used = energyperunit * kilocalories
		return render_template("homehtml.html", water_used=water_used, energy_used=energy_used, fuel_used=fuel_used, isithiddenvar='Block', weight=weight, food=food)

def main():
	app.run(debug=True)


if __name__ == "__main__":
	main()

