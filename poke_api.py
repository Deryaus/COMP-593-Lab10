import requests, os, image_lib

POKEMON_SEARCH_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
   download_pokemon_artwork('steelix', r'C:\temp')
       
# Accept a parameter that specifies the name of the Pokémon or PokéDex number.
def search_for_pokemon(search_term):
    """ Gets info about a specified Pokemon from the PokeAPI.

    Args:
        search_term (str): Pokemon name or pokedex number.

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Convert the parameter to a string.
    # Remove any leading and trailing whitespace characters
    # Convert to all lowercase letters.
    clean_string = str(search_term).strip().lower()
    # Send GET request to the poke api.
    print(f'Getting information for {clean_string}....', end='')
    resp_msg = requests.get(POKEMON_SEARCH_URL + clean_string)
    # Check whether the GET request was successful.
    if resp_msg.ok:
        print('success.')
        pokemon_dict = resp_msg.json()
        return pokemon_dict
    else:
        print('failure.')
        print(f'Response code: {resp_msg.status_code} {resp_msg.reason}')


def get_pokemon_names(offset=0, limit=100000):
    """Gets a list of all pokemon names from the PokeAPI

    Args:
        offset (int, optional): Start of pokedex value to search for. Defaults to 0.
        limit (int, optional): End of pokedex value to search for. Defaults to 100000.

    Returns:
        list: list of all pokemon names if successful. Otherwise None
    """
    # Define get get request params.
    query_string_params={
        'offsett': offset,
        'limit': limit
    }

    print('Getting list of pokemon names')
    # Send get request.
    resp_msg = requests.get(POKEMON_SEARCH_URL, params=query_string_params)
    # Check if requeset was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        pokemon_dict = resp_msg.json()
        # Create pokemon list
        pokemon_names_list = [p['name'] for p in pokemon_dict['results']]
        return pokemon_names_list
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} {resp_msg.reason}')

def download_pokemon_artwork(pokemon_name, save_dir ):
    """ Downloades image of the specifed Pokemon and saves that image to disk.

    Args:
        pokemon_name (str): Pokemon name.
        save_dir (str): Path to save images.

    Returns:
        str: Path of saved image if successful. None otherwise.
    """
    # get all info for the specified pokemon.
    pokemon_info = search_for_pokemon(pokemon_name)
    if pokemon_info is None:
        print(f'Unable to retrieve infromation for Pokemon {pokemon_name}')
        return
    
    # Extract the artwork URL from the info dictionary.
    artwork_url = pokemon_info['sprites']['other']['official-artwork']['front_default']

    # Download the artwork
    image_bytes = image_lib.download_image(artwork_url)
    if image_bytes is None:
        return   
    # Determing image file path.
    file_ext = artwork_url.split('.')[-1]
    image_path = os.path.join(save_dir, f'{pokemon_name}.{file_ext}')

    # Save the Image file.
    if image_lib.save_image_file(image_bytes, image_path):
        return image_path
if __name__ == '__main__':
    main()