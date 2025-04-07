# app.py
from flask import Flask, render_template, request
from services.pokeapi_service import get_pokemons

app = Flask(__name__)

# Variable global para almacenar los Pokémon (cache simple)
all_pokemons_cache = []

@app.route('/')
def index():
    global all_pokemons_cache
    search_term = request.args.get('search', '').lower() # Obtener término de búsqueda

    if not all_pokemons_cache: # Cargar solo si la caché está vacía
        print("Fetching Pokémon from API...")
        all_pokemons_cache = get_pokemons()
    else:
        print("Using cached Pokémon data...")

    # Filtrar si hay término de búsqueda
    if search_term:
        displayed_pokemons = [
            p for p in all_pokemons_cache
            if search_term in p['name'].lower()
        ]
    else:
        displayed_pokemons = all_pokemons_cache

    return render_template('index.html', pokemons=displayed_pokemons, search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True) # debug=True para desarrollo