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
  response = requests.post(url, json={'query': search_anime_by_name, 'variables': variables}).json()['data']
  if not response['Media']:
    return dict(result='Not Found.')
  return dict(info=response, thumb=response['Media']['coverImage']['large'])

if __name__ == '__main__':
  pass

'''
{'info': 
{'Media': 
    {'id': 119675, 'coverImage': 
    {'large': 'https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx119675-ziQ6Lb80zEx4.png'},
    'title': 
    {'english': 'SHAMAN KING (2021)', 'romaji': 'SHAMAN KING (2021)', 'native': 'SHAMAN KING (2021)'}}}, 'thumb': 'https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx119675-ziQ6Lb80zEx4.png'}
'''