import requests
from bs4 import BeautifulSoup
from flask import Flask, request

app = Flask(__name)

@app.route('/processar_pesquisa', methods=['POST'])
def processar_pesquisa():
    string_to_search = request.form['string_to_search']
    url = 'https://dev.tibiadata.com/v4/world/Nefera'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        if string_to_search in soup.get_text():
            return f"A string '{string_to_search}' foi encontrada na página."
        else:
            return f"A string '{string_to_search}' não foi encontrada na página."
    else:
        return "Falha ao acessar a página."

if __name__ == '__main__':
    app.run(debug=True)
