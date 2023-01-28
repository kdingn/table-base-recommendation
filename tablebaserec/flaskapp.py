import pandas as pd
import yaml
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

path_yaml = "config.yaml"
with open(path_yaml) as file:
    config = yaml.safe_load(file)

col_lk = config["columns"]["like"]
df = pd.read_parquet(config["datas"]["prediction"])
df = df.rename(
    columns={
        config["columns"]["id"]: "id",
        config["columns"]["item"]: "item",
        config["columns"]["url"]: "url",
    }
)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app)


@app.route("/datas", methods=["GET"])
def datas():
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


@app.route("/image", methods=["GET"])
def images():
    index = int(request.args.get("id"))
    image = send_file(f"./images/{index}.jpg")
    return image


if __name__ == "__main__":
    app.run(debug=True)
