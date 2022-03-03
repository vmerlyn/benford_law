import os
import time

from flask import Flask, redirect, render_template, request, url_for

from census_data import CensusData

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    try:
        if uploaded_file.filename != "":
            PLOT_GENERATION_DELAY = 2  # seconds
            if not os.path.exists('temp_data'):
                os.makedirs('temp_data')
            destination_file = os.path.join(
                "temp_data", uploaded_file.filename)
            uploaded_file.save(destination_file)
            column_name = request.form['col_name']
            data = CensusData(destination_file, column_name)
            data.generate_plot()
            # FIXME
            # Adding this artificial delay to allow for the plot to finish generating
            # before we redirect to the base page and display the generated HTML.
            # NOT ideal. But only way to fix the occasional issue where the plots
            # were not being displayed.
            time.sleep(PLOT_GENERATION_DELAY)

        else:
            CensusData.generate_html()
    except Exception as exception_instance:
        CensusData.generate_html()
        print(type(exception_instance))
        print(exception_instance.args)
        print(exception_instance)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
