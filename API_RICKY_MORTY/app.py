from flask import Flask, render_template
import urllib.request, json
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

@app.route("/")
def hello_world():
    
    return render_template("index.html")

@app.route("/location/<id>")
def get_location(id):
    # Validação do id fornecido pelo usuário
    if 0 < int(id) < 127:
        # Acessar a api do Ricky and Morty e carregar os dados da localização
        url = "https://rickandmortyapi.com/api/location/" + id
        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)

    # Levantar erro se o id fornecido não consta na base de dados da api
    else:
        raise BadRequest(f"Localização com o id {id} não encontrada")
    
    residents = {}
   

    # Acessar os dados de cada um dos residentes da localização fornecida e extrair o nome do personagem
    for url_character in dict["residents"]:
        url2 = url_character
        response2 = urllib.request.urlopen(url2)
        data_character = response2.read()
        dict_character = json.loads(data_character)
        residents[dict_character["id"]] = dict_character["name"]


    return render_template("location.html", location=dict, characters=residents)

if __name__ == '__main__':
    app.run(debug=True)