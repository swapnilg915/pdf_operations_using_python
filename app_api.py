import os
import pathlib
import re
import json
import time
import traceback
import numpy as np

from scripts import detect_scanned_pdf
from scripts import extract_text
import config as cf
# for reproducible results
np.random.seed(777)

from flasgger import Swagger, swag_from
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.debug = True
app.url_map.strict_slashes = False
Swagger(app)


@swag_from(os.path.join(cf.BASE_PATH, "swagger_files", "pdf_operations.yml"))
@app.route("/api/v1/pdf_operations", methods=['POST', 'OPTIONS'])
def pdf_operations():
	res = ""
	res_json = {"result": "", "status":"", "message":"", "filename":"", "operation":""}
	try:
		start_time = time.time()
		""" validate and save uploaded file """
		file = request.files['file']
		operation = request.form['operation'] # extract text / detect scanned
		filename = pathlib.Path(file.filename).name
		print("\n filename : ",filename)
		extension = pathlib.Path(file.filename).suffix

		if extension.lower() not in cf.extensions_list:
			res_json["status"] = 400
			res_json["message"] = ""
			return jsonify(res_json)

		upload_folder = os.path.join(cf.data_path, "uploaded_files")
		if not os.path.exists(upload_folder):
			os.makedirs(upload_folder)
		save_file_path = os.path.join(upload_folder, filename)
		file.save(save_file_path)

		if operation == "extract text": res = extract_text.extract_text(save_file_path)
		elif operation == "detect scanned": res = detect_scanned_pdf.detect_scanned(save_file_path)
		print("\n total time --- ",time.time() - start_time)

		res_json["result"] = res
		res_json["operation"] = operation
		res_json["filename"] = filename
		res_json["message"] = "Successfull"
		print("\n result: ", json.dumps(res_json, indent=4))
	except Exception as e:
		print("\n Error in pdf_operations :",traceback.format_exc())
		res_json["status"] = "400"

	return jsonify(res_json)

@app.route("/clustering_results", methods=['GET', 'OPTIONS'])
def clustering_results():
	return render_template("index.html")



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001)

	""" INPUT DATA FORMAT

	data_json = {
		"BotId":"bot_3",
		"Language":"nb",
		"number_of_clusters":292,
		"TrainingData":[
			
		]
	}

	"""