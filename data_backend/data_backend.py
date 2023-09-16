from flask import Flask, jsonify
from rfid import RFIDReader
from weigh import WeighBridgeReader

app = Flask(__name__)

# Initialize RFID and WeighBridge readers
reader = RFIDReader('127.0.0.1', 12345)
weighbridge = WeighBridgeReader('127.0.0.1', 12346)


# API endpoint to fetch RFID data
@app.route('/rfid-data', methods=['GET']) 
def get_rfid_data():
    received_data = reader.get_data()
    return jsonify({"rfid_data": received_data})


# API endpoint to fetch WeighBridge data
@app.route('/weighbridge-data', methods=['GET'])
def get_weighbridge_data():
    weighdata = weighbridge.get_data()
    return jsonify({"weighbridge_data": weighdata})



if __name__ == "__main__":
    reader.connect()
    weighbridge.connect()
    app.run(debug=True, port=80)
