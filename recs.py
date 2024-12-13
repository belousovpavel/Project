import folium
import requests
import polyline

# Ваш API ключ для OpenRouteService
ORS_API_KEY = '5b3ce3597851110001cf6248e1a10ab2b5204f558a599db50fd9302e'


def get_route(start, end):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/json"
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }
    payload = {
        "coordinates": [start, end],
        "format": "json",
        "preference": "recommended"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        route_data = response.json()
        if 'routes' in route_data and route_data['routes']:
            return route_data['routes'][0]
        else:
            print("Маршрут не найден в данных ответа API.")
            return None
    else:
        print(f"Ошибка получения маршрута: {response.status_code} - {response.text}")
        return None


def show_route_on_map(start, end, route_data):
    if route_data is None:
        print("Нет данных маршрута для отображения.")
        return

    m = folium.Map(location=[start[1], start[0]], zoom_start=13)

    folium.Marker(
        location=[start[1], start[0]],
        popup="Текущая позиция",
        icon=folium.Icon(color='green')
    ).add_to(m)

    folium.Marker(
        location=[end[1], end[0]],
        popup="Целевая точка",
        icon=folium.Icon(color='red')
    ).add_to(m)

    decoded_route = polyline.decode(route_data['geometry'])

    folium.PolyLine(
        locations=[[lat, lon] for lat, lon in decoded_route],
        color='blue',
        weight=5,
        opacity=0.7
    ).add_to(m)
    m.save("route_map.html")
    print("Карта сохранена в файл route_map.html")


# Основная функция
def inmaps(start_point, end_point):
    # Преобразуем строки в списки координат
    start_coords = [float(coord) for coord in start_point.split(",")]
    end_coords = [float(coord) for coord in end_point.split(",")]
    route_data = get_route(start_coords, end_coords)
    show_route_on_map(start_coords, end_coords, route_data)
    if not user:
        return "Пользователь не найден."

    suitable_parties = [party for party in parties if is_party_suitable(user, party)]

    if not suitable_parties:
        return "Нет доступных вечеринок в данный момент."

    return user, sorted(suitable_parties, key=lambda x: x['Название вечеринки'])  # можно сортировать по другим критериям
