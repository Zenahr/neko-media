import requests


def get_anime_info(anime_name):
  url = 'https://graphql.anilist.co'
  variables = {
    # cowboy bebop
    'query': anime_name
  }

  search_anime_by_name = '''
  query ($query: String) { # Define which variables will be used in the query (id)
    Media (search: $query, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
      id
      coverImage {
        large
      }
      title {
        english
        romaji
        native
      }
    }
  }
  '''
  response = requests.post(url, json={'query': search_anime_by_name, 'variables': variables})
  return response.json()