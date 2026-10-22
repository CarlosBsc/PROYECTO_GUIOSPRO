from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .logic import catalogue, init_state, derive, recommendation, LEVELS, SUB_LEVELS
from django.contrib.auth.decorators import login_required
from .forms import EvaluacionForm

@login_required
@require_http_methods(["GET", "POST"])
def inicio(request):
    cat = catalogue()
    state = request.session.get("guiospro_state")
    if not isinstance(state, dict) or set(state) != {str(i) for i in range(len(cat))}:
        state = init_state(cat)
    tab = "factores"
    error = ""
    show_recommendation = False
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "reset":
            state = init_state(cat)
        elif action == "factors":
            try:
                for i, f in enumerate(cat):
                    state[str(i)]["decisor"] = parse_rating(request.POST.get(f"decisor_{i}"))
                    scope = request.POST.get(f"scope_{i}") if f["scope"] == "Ambos" else f["scope"]
                    if scope not in ("Interno", "Externo"):
                        raise ValueError("El alcance es inválido")
                    state[str(i)]["scope"] = scope
                tab = "subfactores"
            except ValueError:
                error = "Revise las valoraciones de los factores."
        elif action == "subfactors":
            try:
                i = int(request.POST.get("factor_id", "-1"))
                if i < 0 or i >= len(cat):
                    raise ValueError("Factor desconocido")
                values = [parse_rating(request.POST.get(f"weight_{i}_{j}")) for j in range(len(cat[i]["subfactors"]))]
                state[str(i)]["weights"] = values
                state[str(i)]["saved"] = True
                tab = "subfactores"
            except ValueError:
                error = "Revise las valoraciones de los subfactores."
                tab = "subfactores"
        elif action == "recommendation":
            tab = "resultados"
            show_recommendation = True
        request.session["guiospro_state"] = state
    rows = derive(cat, state)
    relevant = [r for r in rows if r["relevant"]]
    selected_id = request.POST.get("factor_id") if request.method == "POST" else request.GET.get("factor_id")
    try:
        selected_id = int(selected_id)
    except (ValueError, TypeError):
        selected_id = relevant[0]["id"] if relevant else None
    if selected_id not in [r["id"] for r in relevant]:
        selected_id = relevant[0]["id"] if relevant else None
    selected = rows[selected_id] if selected_id is not None else None
    return render(request, "evaluacion/inicio.html", {"rows":rows,"relevant":relevant,"selected":selected,"levels":list(enumerate(LEVELS,1)),"sublevels":list(enumerate(SUB_LEVELS,1)),"tab":tab,"error":error,"recommendation":recommendation(rows) if show_recommendation else None})

def parse_rating(value):
    value = int(value)
    if value not in (1,2,3,4):
        raise ValueError("Fuera de rango")
    return value


@login_required
def nueva_evaluacion(request):

    if request.method == "POST":

        form = EvaluacionForm(request.POST)

        if form.is_valid():

            evaluacion = form.save(commit=False)

            # Asociar la evaluación al usuario autenticado
            evaluacion.usuario = request.user

            # Guardar los datos en PostgreSQL
            evaluacion.save()

            # Guardar el identificador de la evaluación actual
            request.session["evaluacion_actual_id"] = evaluacion.id

            # Inicializar las valoraciones para la nueva evaluación
            request.session["guiospro_state"] = init_state(catalogue())

            # Abrir la evaluación original de GUIOSPRO
            return redirect("evaluacion:inicio")

    else:
        form = EvaluacionForm()

    return render(
        request,
        "evaluacion/nueva_evaluacion.html",
        {"form": form}
    )


@login_required
def panel(request):
    return render(request, "evaluacion/panel.html")