from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile

import os
import pandas as pd

from func_parse_statements import convert_pdf_to_text
from func_extract_holdings import load_model, extract_holdings
from func_enrich_data import json_to_dfs

app = Flask(__name__)

# Initialise model
model = load_model()

@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Portfolio Panda</h1>
    <form method=post enctype=multipart/form-data action="/upload">
      <input type=file name=pdf>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        return 'No file part', 400
    file = request.files['pdf']
    if file.filename == '':
        return 'No selected file', 400

    filename = secure_filename(file.filename)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file.save(temp_file.name)
        temp_filepath = temp_file.name

    # Convert PDF to text
    text = convert_pdf_to_text(temp_filepath)

    # Convert text to JSON
    holdings_json = extract_holdings(model, text)

    # Convert JSON to Pandas DataFrame
    dfs = json_to_dfs(holdings_json)

    # Create a temporary file path
    excel_filepath = os.path.join(tempfile.gettempdir(), f"{os.path.splitext(file.filename)[0]}.xlsx")

    # Write DataFrames to separate sheets in the Excel file
    with pd.ExcelWriter(excel_filepath, engine='xlsxwriter') as writer:
        for account_number, df in dfs.items():
            df.to_excel(writer, sheet_name=account_number, index=False)

    return send_file(excel_filepath, as_attachment=True, download_name=f"{os.path.splitext(file.filename)[0]}.xlsx")

if __name__ == '__main__':
    app.run(debug=True)
