# services/pokeapi_service.py
import flask
import requests

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/ability"
LIMIT = 20 # Cuántos Pokémon cargar inicialmente

def get_pokemon_details(url):
    """Obtiene detalles de un Pokémon específico."""
    try:
        response = requests.get(url)
        response.raise_for_status() # Lanza error si la petición falla
        data = response.json()
        # Extraemos solo lo necesario: nombre, imagen, tipos
        return {
            "name": data.get("name", "N/A"),
            "image": data.get("sprites", {}).get("front_default"),
            "types": [t["type"]["name"] for t in data.get("types", [])]
            # Descripción es más compleja, omitida por simplicidad inicial
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_pokemons():
    """Obtiene una lista de Pokémon con sus detalles básicos."""
    pokemons_list_url = f"{POKEAPI_BASE_URL}?limit={LIMIT}"
    detailed_pokemons = []
    try:
        response = requests.get(pokemons_list_url)
        response.raise_for_status()
        results = response.json().get("results", [])

        for p in results:
            details = get_pokemon_details(p["url"])
            if details:
                detailed_pokemons.append(details)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Pokémon list: {e}")
        # Podrías devolver una lista vacía o manejar el error como prefieras
        return []

    return detailed_pokemons