import pandas as pd
import yaml
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

path_yaml = "config.yaml"
with open(path_yaml) as file:
    config = yaml.safe_load(file)

col_itm = config["columns"]["item"]
col_url = config["columns"]["url"]
col_lk = config["columns"]["like"]

df = pd.read_parquet(config["datas"]["prediction"])
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app)


@app.route("/datas", methods=["GET"])
def images():
    contentsToShow = str(request.args.get("contentsToShow"))
    contentsIn1Page = int(request.args.get("contentsIn1Page"))
    page = int(request.args.get("page"))

    # train (or test) への絞り込み
    if contentsToShow == "":
        tmp = df[(df[col_lk] != 1) & (df[col_lk] != 0)].copy()
    elif contentsToShow == "train":
        tmp = df[(df[col_lk] == 1) | (df[col_lk] == 0)].copy()
    tmp = tmp.sort_values(col_lk, ascending=False)
    tmp = tmp.reset_index(drop=True)
    # 属性による絞り込み

    # page の絞り込み
    tmp = tmp[(page - 1) * contentsIn1Page + 1 : page * contentsIn1Page]
    # return
    return tmp.T.to_json()


if __name__ == "__main__":
    app.run(debug=True)
