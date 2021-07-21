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

  names = ["2021",
           "90's",
           "A Letter to Momo",
           "A Silent Voice",
           "Angels of Death",
           "Fall 2020",
           "Ghost in the Shell Stand Alone Complex_2045",
           "Koutetsujou no Kabaneri",
           "Makai Ouji - Devils and Realist",
           "Ranma TV Episodes BDrip 1080p Dual-Audio",
           "Sora yori mo Tooi Basho",
           "Spyce",
           "Summer 2020",
           "Tensei Shitara Slime Datta Ken 01-25",
           "upload",
           "Koutetsujou no Kabaneri",
           "The Sky Crawlers",
           "Ghost in the Shell",
           "Kaguya-sama wa Kokurasetai Tensai-tachi no Ren'ai Zunousen",
           "Kekkai Sensen & Beyond",
  ]

  for name in names:
    print(get_anime_info(name))