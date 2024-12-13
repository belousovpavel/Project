def load_users(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_parties(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_age_range(age_range):
    start_age, end_age = map(int, age_range.split('-'))
    return start_age, end_age


def is_party_suitable(user, party):
    user_age = user['Возраст']
    party_age_range = parse_age_range(party['Желаемый возраст'])
    suitable_age = party_age_range[0] <= user_age <= party_age_range[1]

    suitable_genres = any(genre in user['Любимые жанры'] for genre in party['Жанры'])
    suitable_activities = any(activity in user['Активности'] for activity in party['Активности'])
    suitable_place = user['Место'] and party['Место'] in user['Место']

    # Введение поясняющих переменных
    is_age_suitable = suitable_age
    is_genre_suitable = suitable_genres
    is_activity_suitable = suitable_activities
    is_place_suitable = suitable_place

    return is_age_suitable and is_genre_suitable and is_activity_suitable and is_place_suitable


def recommend_parties(user_id):
    users = load_users('users.json')
    parties = load_parties('parties.json')

    user = next((u for u in users if u['ID'] == user_id), None)

    if not user:
        return "Пользователь не найден."

    suitable_parties = [party for party in parties if is_party_suitable(user, party)]

    if not suitable_parties:
        return "Нет доступных вечеринок в данный момент."

    return user, sorted(suitable_parties, key=lambda x: x['Название вечеринки'])  # можно сортировать по другим критериям
