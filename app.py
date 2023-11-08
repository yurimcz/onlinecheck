from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verificar_online', methods=['POST'])
def verificar_online():
    nome_boneco = request.json.get('nome_boneco', '')
    resultado = "Erro ao verificar online"  # Mensagem padrão
    if request.method == 'POST':
        nomes = ["Ambra", "Antica", "Astera", "Axera", "Belobra", "Bombra", "Bona", 
             "Calmera", "Castela", "Celebra", "Celesta", "Collabra", "Damora", "Descubra", 
             "Dia", "Epoca", "Esmera", "Etebra", "Ferobra", "Firmera", "Flamera", 
             "Gentebra", "Gladera", "Gravitera", "Guerribra", "Harmonia", "Havera", "Honbra", 
             "Impulsa", "Inabra", "Issobra", "Jacabra", "Jadebra", "Jaguna", "Kalibra", 
             "Kardera", "Kendria", "Lobera", "Luminera", "Lutabra", "Menera", "Monza", 
             "Mykera", "Nadora", "Nefera", "Nevia", "Obscubra", "Ombra", "Ousabra", 
             "Pacera", "Peloria", "Premia", "Pulsera", "Quelibra", "Quintera", "Rasteibra", "Refugia", "Retalia", "Runera", 
             "Secura", "Serdebra", "Solidera", "Syrena", "Talera", "Thyria", "Tornabra", "Ustebra", 
             "Utobra", "Venebra", "Vitera", "Vunira", "Wadira", "Wildera", "Wintera", "Yonabra", "Yovera", "Zuna", "Zunera"
             ]

        
        url = "https://www.tibia.com/community/?name=" + nome_boneco

        requisicao = requests.get(url)

        if requisicao.status_code == 200:
            soup = BeautifulSoup(requisicao.text, "html.parser")
            elementos_de_texto = soup.find_all(string=True)
            primeiro_nome_encontrado = None

            for elemento in elementos_de_texto:
                for nome in nomes:
                    if nome in elemento:
                        primeiro_nome_encontrado = nome
                        break

                if primeiro_nome_encontrado:
                    break

            if primeiro_nome_encontrado:
                world = primeiro_nome_encontrado
                online_world = "https://www.tibia.com/community/?subtopic=worlds&world=" + world

                requisicao2 = requests.get(online_world)

                if requisicao2.status_code == 200:
                    soup = BeautifulSoup(requisicao2.text, 'html.parser')
                    tags_a = soup.find_all("a", href=True)
                    encontrado = False

                    for tag in tags_a:
                        if nome_boneco in tag["href"]:
                            encontrado = True
                            break

                    if not encontrado and " " in nome_boneco:
                        nome_com_espaco_substituido = nome_boneco.replace(" ", "+")

                        for tag in tags_a:
                            if nome_com_espaco_substituido in tag["href"]:
                                encontrado = True
                                break

                    if encontrado:
                        resultado = f"Player '{nome_boneco}' de '{world}' está online."
                    else:
                        resultado = f"Player '{nome_boneco}' de '{world}' está offline."
                else:
                    resultado = "Erro ao verificar online."

                    return jsonify({'resultado': resultado})

    #return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
