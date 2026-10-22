"""Traslado a Django de las reglas de main.py y los catálogos de guiosad.py.
Mantiene la escala 1–4, importancia relativa con división entera,
ponderación media, FODA y prioridades A/B/C originales.
"""
import csv
from pathlib import Path
from django.conf import settings

LEVELS = ["Irrelevante", "Opcional", "Importante", "Fundamental"]
SUB_LEVELS = ["No cumple el requisito", "Desconozco si cumple requisito", "Cumple parcialmente el requisito", "Cumple el requisito"]

def catalogue():
    data = {}
    with (settings.BASE_DIR / "data" / "guiosad_data.csv").open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            entry = data.setdefault(row["Factor"], {"name": row["Factor"], "dimension": row["Dimensión"], "subfactors": []})
            entry["subfactors"].append(row["Subfactor"])
    with (settings.BASE_DIR / "data" / "factors.csv").open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            data[row["Factor"]]["suggested"] = int(row["Sugerida"])
            data[row["Factor"]]["scope"] = row["Alcance"]
    return list(data.values())

def init_state(catalog):
    return {str(i): {"decisor": 1, "scope": "Interno" if f["scope"] == "Ambos" else f["scope"], "weights": [1]*len(f["subfactors"]), "saved": False} for i, f in enumerate(catalog)}

def relative(suggested, decisor):
    # Código original: índices base cero y división entera.
    return (suggested - 1 + decisor - 1) // 2

def derive(catalog, state):
    rows = []
    for i, f in enumerate(catalog):
        s = state[str(i)]
        rel = relative(f["suggested"], s["decisor"])
        relevant = rel > 0
        score = sum(s["weights"])/len(s["weights"]) if s["weights"] and s["saved"] and relevant else None
        foda = None
        if score is not None:
            if s["scope"] == "Interno":
                foda = "Fortaleza" if score >= 3 else "Debilidad"
            else:
                foda = "Oportunidad" if score >= 3 else "Amenaza"
        rows.append({**f, "id":i, "decisor":s["decisor"], "decisor_label":LEVELS[s["decisor"]-1], "relative":LEVELS[rel], "relevant":relevant, "scope_selected":s["scope"], "weights":s["weights"], "saved":s["saved"], "score":score, "foda":foda})
    return rows

RA = "Recomendación C: La organización debe de proporcionar los recursos necesarios que garanticen una adopción satisfactoria. Si se trata de factores internos deben de ser aspectos a mejorar dentro de la organización y si son factores externos, dedicar recursos de ingeniería para mejorar el software."
RB = "Recomendación B: Es posible adoptar. A pesar que se han detectado amenazas y/o debilidades en factores cuya importancia relativa es opcional, por lo tanto, se sugiere revisar los criterios que no cumplen con lo mínimo requerido para adoptar."
RC = "Recomendación A: Adoptar. Todos los factores han sido identifcados como Oportunidades y/o Fortalezas. Esto quiere decir que la organización cumple satisfactoriamente con la mayoria de requisitos para adoptar la solución FLOSS."

def recommendation(rows):
    evaluated = [r for r in rows if r["foda"]]
    if not evaluated:
        return ""  # Evita el IndexError original cuando no hay factores evaluados.
    a = any(r["foda"] in ("Amenaza", "Debilidad") and r["relative"] in ("Importante", "Fundamental") for r in evaluated)
    b = any(r["foda"] in ("Amenaza", "Debilidad") and r["relative"] == "Opcional" for r in evaluated)
    return RA if a else RB if b else RC
