from flask import Flask, render_template, request, jsonify
from database import db, Locomotiva
from locomotive_classifier import classificar_resultado_com_modelo 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locomotivas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/avaliar', methods=['POST'])
def avaliar_locomotiva():
    try:
        dados = request.get_json()

        temperatura_motor = dados['temperaturaMotor']
        consumo_combustivel_km = dados['consumoCombustivel']
        ja_sofreu_manutencao = dados['jaSofreuManutencao']
        pressao_oleo_motor = dados['pressaoOleo']
        temperatura_combustivel = dados['temperaturaCombustivel']
        temperatura_oleo_refrigeracao = dados['temperaturaOleo']

        locomotiva = Locomotiva(
            temperatura_motor=temperatura_motor,
            consumo_combustivel_km=consumo_combustivel_km,
            ja_sofreu_manutencao=ja_sofreu_manutencao,
            pressao_oleo_motor=pressao_oleo_motor,
            temperatura_combustivel=temperatura_combustivel,
            temperatura_oleo_refrigeracao=temperatura_oleo_refrigeracao
        )
        db.session.add(locomotiva)
        db.session.commit()

        valores = [temperatura_motor, consumo_combustivel_km, pressao_oleo_motor, temperatura_combustivel, temperatura_oleo_refrigeracao]
        campos_fora_do_ideal = classificar_resultado_com_modelo(valores, ja_sofreu_manutencao)

        return jsonify({'camposForaDoIdeal': campos_fora_do_ideal})
    
    except Exception as e:
        print(f"Erro ao processar a solicitação: {e}")
        return jsonify({'error': 'Ocorreu um erro ao processar os dados.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
