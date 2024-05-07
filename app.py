import mysql.connector
import requests
from flask import Flask, jsonify, request
import flask_swagger_ui import get_swaggerui_blueprint

def conectionDB():
    conection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='cancelareserva')
    return conection

app = Flask(__name__)

PREFIX = "/api"
api = Api(app, prefix=PREFIX)

SWAGGER_URL = f'{PREFIX}/swagger/'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'API-Cancela-Reserva'})
app.register_blueprint(swagger_ui_blueprint)

@app.route('/CancelaReserva/<id_reserva>', methods=['GET'])
def consultarCancelamento(id_reserva):
    conection = conectionDB()
    cursor = conection.cursor(dictionary=True)
    sql = 'SELECT * FROM cancelamento WHERE id_reserva = %s'
    values = [id_reserva]
    try:
        cursor.execute(sql, values)
        data = cursor.fetchall()
        if data:
            return jsonify(data[0])
        else:
            return jsonify({'error': 'Cancelamento não encontrado'}), 404
    except mysql.connector.Error as err:
        print(f"Erro ao consultar o cancelamento: {err}")
        return jsonify({'error': f"Erro ao consultar a cancelamento: {err}"}), 400
    finally:
        cursor.close()
        conection.close()




@app.route('/CancelaReserva/<id_reserva>', methods=['POST'])
def cancela_reserva(id_reserva):

    reserva = requests.delete('/reserva/idReserva', params={'id_reserva': id_reserva})
    data = reserva.json()
    id_reserva = data['id_reserva']
    cancelaReserva = cancela_reserva(id_reserva)
    if cancelaReserva:
        return jsonify(cancelaReserva), 200
    else:
        return jsonify({'error': 'Nao foi possivel fazer a reserva'}), 404

    if response.status_code == 200:
        Cancelamento = {
            Id: int,
            Id_reserva: int,
            Id_hotel: int,
            Id_quarto: int,
            DataC: datetime
        }


        novo_cancelamento = {
            'Id': len(cancelamentos) + 1,
            'Id_reserva': id_reserva,
            'Id_hotel': id_hotel,
            'Id_quarto': id_quarto,
            'DataC': 'datetime'
        }
        cancelamentos.append(novo_cancelamento)

        return jsonify(novo_cancelamento), 201
    elif response.status_code == 400:
        return jsonify({'message': 'Erro ao cancelar reserva: Bad Request'}), 400
    elif response.status_code == 404:
        return jsonify({'message': 'Erro ao cancelar reserva: Not Found'}), 404
    else:
        return jsonify({'message': 'Erro desconhecido ao cancelamentos'}), 400



if __name__ == '__main__':
    app.run(debug=True, port = '5003')