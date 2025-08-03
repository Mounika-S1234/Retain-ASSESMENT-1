from flask import Blueprint, request, jsonify, redirect
from app.storage import store_url, get_url_data, increment_clicks
from app.utils import generate_short_code, is_valid_url

shorten_bp = Blueprint('shortener', __name__)

@shorten_bp.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    if not long_url or not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    store_url(short_code, long_url)
    short_url = f"http://localhost:5000/{short_code}"
    return jsonify({"short_code": short_code, "short_url": short_url}), 201

@shorten_bp.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    url_data = get_url_data(short_code)
    if not url_data:
        return jsonify({"error": "Short URL not found"}), 404

    increment_clicks(short_code)
    return redirect(url_data['url'])

@shorten_bp.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    url_data = get_url_data(short_code)
    if not url_data:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "url": url_data['url'],
        "clicks": url_data['clicks'],
        "created_at": url_data['created_at'].isoformat()
    }), 200
