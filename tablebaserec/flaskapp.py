import pandas as pd
import yaml
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

path_yaml = "config.yaml"
with open(path_yaml) as file:
    config = yaml.safe_load(file)

col_ct = config["columns"]["categories"][0]
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
    category = str(request.args.get("category"))

    # train (or test) への絞り込み
    tmp = df.copy()
    if contentsToShow == "":
        tmp = tmp[(tmp[col_lk] != 1) & (tmp[col_lk] != 0)].copy()
    elif contentsToShow == "train":
        tmp = tmp[(tmp[col_lk] == 1) | (tmp[col_lk] == 0)].copy()
    # 属性による絞り込み
    if category != "":
        tmp = tmp[tmp[col_ct] == category]
    # page の絞り込み
    tmp = tmp.sort_values(col_lk, ascending=False)
    tmp = tmp.reset_index(drop=True)
    tmp = tmp[(page - 1) * contentsIn1Page : page * contentsIn1Page]
    # return
    return tmp.T.to_json()


@app.route("/image", methods=["GET"])
def image():
    index = int(request.args.get("id"))
    image = send_file(f"./images/{index}.png")
    return image


@app.route("/categories", methods=["GET"])
def categories():
    cts = (
        df[[col_ct, col_lk]].groupby(col_ct).mean().sort_values(col_lk, ascending=False)
    )
    return cts[col_lk].to_json()


if __name__ == "__main__":
    app.run(debug=True)
