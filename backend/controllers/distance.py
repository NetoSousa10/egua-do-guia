# backend/controllers/distance.py

import os
import requests
from flask import Blueprint, request, jsonify, current_app as app
from dotenv import load_dotenv

load_dotenv()
GMAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

distance_bp = Blueprint('distance', __name__, url_prefix='/api/distance')

@distance_bp.route('/', methods=['GET'])
def get_distance():
    lat1 = request.args.get('lat1')
    lng1 = request.args.get('lng1')
    lat2 = request.args.get('lat2')
    lng2 = request.args.get('lng2')
    if not all([lat1, lng1, lat2, lng2]):
        return jsonify({'error': 'Parâmetros faltando'}), 400

    # Monta a URL da API
    url = (
      'https://maps.googleapis.com/maps/api/distancematrix/json'
      f'?origins={lat1},{lng1}'
      f'&destinations={lat2},{lng2}'
      f'&key={GMAPS_KEY}'
      '&units=metric'
    )
    res = requests.get(url).json()
    try:
        elem = res['rows'][0]['elements'][0]
        if elem['status'] != 'OK':
            raise ValueError(f"Status API: {elem['status']}")
        distance_m = elem['distance']['value']
        return jsonify({'distance_km': distance_m / 1000})
    except Exception as e:
        app.logger.error("Erro Google Distance Matrix: %s", res)
        # devolve null para fallback no front
        return jsonify({'distance_km': None}), 200
