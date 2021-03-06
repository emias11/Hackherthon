from flask import render_template, Flask, jsonify, redirect, request, url_for, send_file

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def load_app():
	return render_template("homehtml.html")


def main():
	app.run(debug=True)


if __name__ == "__main__":
	main()