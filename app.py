from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculadora():
    visor = ""
    if request.method == "POST":
        visor = request.form["visor"]
        botao = request.form["botao"]

        if botao == "C":
            visor = ""
        elif botao == "=":
            try:
                visor = str(eval(visor))
            except:
                visor = "Erro"
        else:
            visor += botao

    botoes = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "C", "0", "=", "+"]
    return render_template("index.html", visor=visor, buttons=botoes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

