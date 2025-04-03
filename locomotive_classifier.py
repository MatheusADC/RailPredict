import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

LIMITES = {
    "Temperatura do Motor": "90.0",
    "Consumo de Combustível/km": "3.0",
    "Pressão de Óleo do Motor": "4.0",
    "Temperatura do Combustível": "30.0",
    "Temperatura do Óleo de Refrigeração": "85.0",
    "Já sofreu manutenção": "N"
}

def gerar_dados_treinamento(num_amostras=2000):
    X_train = []
    y_train = []
    
    for _ in range(num_amostras):
        temperatura_motor = np.random.uniform(70, 110)
        consumo_combustivel_km = np.random.uniform(2.0, 4.5)
        pressao_oleo_motor = np.random.uniform(3.0, 6.0)
        temperatura_combustivel = np.random.uniform(10.0, 50.0)
        temperatura_oleo_refrig = np.random.uniform(70.0, 100.0)
        ja_sofreu_manutencao = np.random.choice(["N", "S"])  
        
        valores = [temperatura_motor, consumo_combustivel_km, pressao_oleo_motor, 
                   temperatura_combustivel, temperatura_oleo_refrig, ja_sofreu_manutencao]
        
        recomendacoes = [
            1 if temperatura_motor > float(LIMITES["Temperatura do Motor"]) else 0,
            1 if consumo_combustivel_km > float(LIMITES["Consumo de Combustível/km"]) else 0,
            1 if pressao_oleo_motor > float(LIMITES["Pressão de Óleo do Motor"]) else 0,
            1 if temperatura_combustivel > float(LIMITES["Temperatura do Combustível"]) else 0,
            1 if temperatura_oleo_refrig > float(LIMITES["Temperatura do Óleo de Refrigeração"]) else 0,
            1 if ja_sofreu_manutencao == "S" else 0  
        ]
        
        X_train.append(valores[:-1] + [1 if valores[-1] == "S" else 0])  
        y_train.append(recomendacoes)
    
    return np.array(X_train), np.array(y_train)

def criar_modelo():
    model = keras.Sequential([
        keras.layers.Input(shape=(6,)),  
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.4),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(6, activation="sigmoid")  
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model

def carregar_ou_treinar_modelo():
    modelo_path = 'modelo_locomotiva.keras'
    
    if os.path.exists(modelo_path):
        print("Carregando modelo existente...")
        modelo = keras.models.load_model(modelo_path)
    else:
        print("Modelo não encontrado, treinando modelo...")
        X_train, y_train = gerar_dados_treinamento()
        modelo = criar_modelo()
        modelo.fit(X_train, y_train, epochs=2000, batch_size=32, validation_split=0.2)
        modelo.save(modelo_path) 
        print(f"Modelo treinado e salvo em {modelo_path}")
    
    return modelo

def classificar_resultado_com_modelo(valores, ja_sofreu_manutencao):
    valores.append(1 if ja_sofreu_manutencao == "S" else 0)  
    previsao = modelo.predict(np.array([valores]))[0]
    
    campos_fora_do_ideal = []
    parametros = list(LIMITES.keys())
    
    for i, valor in enumerate(previsao):
        if valor >= 0.5:
            campos_fora_do_ideal.append(parametros[i])
    
    return campos_fora_do_ideal

modelo = carregar_ou_treinar_modelo()

# novos_valores = [95.0, 3.0, 4.2, 30.0, 85.0] 
# ja_sofreu_manutencao = "S"
# campos_fora_do_ideal = classificar_resultado_com_modelo(novos_valores, ja_sofreu_manutencao)

# print("Campos fora do limite ideal:", campos_fora_do_ideal)
