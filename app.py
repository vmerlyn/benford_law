from flask import Flask, render_template, request, redirect, url_for
from census_data import CensusData
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        if not os.path.exists('temp_data'):
            os.makedirs('temp_data')
        destination_file = os.path.join("temp_data", uploaded_file.filename)
        uploaded_file.save(destination_file)
        data = CensusData(destination_file)
        data.generate_plot()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
