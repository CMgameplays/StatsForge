import os
import sys
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Blueprint, request, jsonify, render_template

try:
    from shared.limiter import limiter
except ImportError:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter = Limiter(get_remote_address, storage_uri="memory://")

bp = Blueprint("statsforge", __name__, template_folder="templates")


@bp.route("/")
def index():
    return render_template("statsforge/index.html")


@bp.route("/api/calculate", methods=["POST"])
@limiter.limit("60 per minute")
def calculate():
    data = request.get_json(force=True)

    try:
        attack = float(data.get("attack", 100))
        defense = float(data.get("defense", 20))
        crit_chance = float(data.get("crit_chance", 15))
        crit_mult = float(data.get("crit_mult", 2.0))
        fire_rate = float(data.get("fire_rate", 2))
        n_hits = int(data.get("n_hits", 20))
    except (TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid input: {e}"}), 400

    n_hits = max(1, min(n_hits, 500))
    crit_chance = max(0.0, min(crit_chance, 100.0))
    fire_rate = max(0.01, fire_rate)

    effective_hit = max(1.0, attack - defense)
    crit_probability = crit_chance / 100.0
    expected_per_hit = effective_hit * (1 - crit_probability) + effective_hit * crit_mult * crit_probability
    dps = expected_per_hit * fire_rate
    min_damage = effective_hit
    max_damage = effective_hit * crit_mult

    rng = random.Random(42)
    simulated_hits = []
    for _ in range(n_hits):
        if rng.random() < crit_probability:
            simulated_hits.append(round(effective_hit * crit_mult, 2))
        else:
            simulated_hits.append(round(effective_hit, 2))

    formula_steps = [
        f"effective_hit  = max(1, attack - defense)",
        f"             = max(1, {attack} - {defense}) = {effective_hit}",
        f"crit_prob      = crit_chance / 100 = {crit_chance} / 100 = {crit_probability}",
        f"expected/hit   = eff × (1 - p) + eff × crit_mult × p",
        f"             = {effective_hit} × {round(1 - crit_probability, 4)} + {effective_hit} × {crit_mult} × {crit_probability}",
        f"             = {round(expected_per_hit, 4)}",
        f"DPS            = expected/hit × fire_rate",
        f"             = {round(expected_per_hit, 4)} × {fire_rate} = {round(dps, 4)}",
        f"min_damage     = effective_hit = {min_damage}",
        f"max_damage     = effective_hit × crit_mult = {effective_hit} × {crit_mult} = {max_damage}",
    ]

    return jsonify({
        "dps": round(dps, 4),
        "expected_per_hit": round(expected_per_hit, 4),
        "min_damage": round(min_damage, 4),
        "max_damage": round(max_damage, 4),
        "simulated_hits": simulated_hits,
        "formula_steps": formula_steps,
    })


if __name__ == "__main__":
    from flask import Flask
    standalone = Flask(__name__)
    standalone.register_blueprint(bp, url_prefix="/")
    limiter.init_app(standalone)
    standalone.run(debug=True, port=5000)
