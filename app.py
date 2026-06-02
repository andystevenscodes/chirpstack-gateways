from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from chirpstack_client import list_all_gateways, save_config, get_api_token

app = Flask(__name__)
app.secret_key = "change-me-in-production"


@app.route("/")
def index():
    # Redirect to config if no token set yet
    if not get_api_token():
        return redirect(url_for("config"))
    return render_template("index.html")


@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        token = request.form.get("api_token", "").strip()
        if not token:
            flash("API token mag niet leeg zijn.", "error")
        else:
            save_config({"api_token": token})
            flash("Token opgeslagen.", "success")
            return redirect(url_for("index"))
    return render_template("config.html", has_token=bool(get_api_token()))


@app.route("/api/gateways")
def gateways():
    filter_token = request.args.get("filter", "").strip().upper()

    try:
        all_gateways = list_all_gateways()
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 502

    if filter_token:
        def matches(gw: dict) -> bool:
            name = gw["name"].upper()
            suffix = name.rsplit("-", 1)[-1]
            return filter_token in suffix or filter_token in name
        all_gateways = [gw for gw in all_gateways if matches(gw)]

    return jsonify(all_gateways)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)