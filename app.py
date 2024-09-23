from flask import Flask, render_template, request, flash, redirect, url_for, session
import time
from modules.carro import Auto

app = Flask(__name__)
app.secret_key = "super_secret_key"

autos = []


@app.route("/")
def Sesion():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    usuario = request.form.get("usuario")
    contrasena = request.form.get("contraseña")
    if usuario == "empleado" and contrasena == "$uper4utos#":
        return redirect(url_for("inicio"))
    else:
        flash("Usuario o contraseña incorrectos", "error")
        session["flash_time"] = time.time() + 3
        return redirect(url_for("Sesion"))


@app.route("/inicio")
def inicio():
    return render_template("Inicio.html")


@app.route("/creaAuto", methods=["GET", "POST"])
def crea_auto():
    if request.method == "POST":
        placa = request.form.get("placa")
        if any(auto.placa == placa for auto in autos):
            flash(
                "Error: Ya existe un auto con esta placa. Por favor, use una placa diferente o elimine el auto existente.",
                "error",
            )
            session["flash_time"] = time.time() + 3
            return redirect(url_for("crea_auto"))
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        descripcion = request.form.get("descripcion")
        precio_unitario = float(request.form.get("precio"))
        cantidad = int(request.form.get("cantidad"))
        imagen_url = request.form.get("url_imagen")

        nuevo_auto = Auto(
            placa, marca, modelo, descripcion, precio_unitario, cantidad, imagen_url
        )
        autos.append(nuevo_auto)
        return redirect(url_for("show_car"))
    else:
        return render_template("creaAuto.html")


@app.route("/showCar")
def show_car():
    return render_template("showCar.html", autos=autos)


@app.route("/eliminar_auto/<placa>", methods=["POST"])
def eliminar_auto(placa):
    global autos
    autos = [auto for auto in autos if auto.placa != placa]
    return redirect(url_for("show_car"))


@app.before_request
def before_request():
    if "flash_time" in session and time.time() > session["flash_time"]:
        session.pop("_flashes", None)
        session.pop("flash_time", None)


if __name__ == "__main__":
    app.run(debug=True)
