# pip install pandas geopy folium geocoder ipywidgets
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
import folium
from ipywidgets import HTML
import geocoder
from folium import IFrame
import base64

def createMap(df, printme = False):
  # Inicializa o geocodificador
  geolocator = Nominatim(user_agent="geoapiExercises")
  vep_lat = -14.802158819744324
  vep_long = -39.277382080808714

  # Função para converter endereço em latitude e longitude
  def geocode_address(address):
      try:
          location = geolocator.geocode(address)
          return location.latitude, location.longitude
      except:
          print('Not Found')
          return None, None

  def update_geocode(row):
    if pd.isnull(row['Latitude']) or pd.isnull(row['Longitude']):
        lat, lng = geocode_address(row['Endereco'])
        return lat, lng
    else:
        return row['Latitude'], row['Longitude']

  # Aplica a função de atualização ao DataFrame
  df['Latitude'], df['Longitude'] = zip(*df.apply(update_geocode, axis=1))

  # Cria um mapa
  m = folium.Map(location=[vep_lat, vep_long], zoom_start=12)

  # Adiciona um marcador para cada localização
  for _, row in df.iterrows():
      if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
          link = f"<a href='{row['Link']}' target='_blank'>{row['Telefone']}</a>"
          tooltip = f"{row['Nome']}\n📞{link}\n📍{row['Endereco']}\n{row['Dia']} - {row['Horario']}"         
          if "eleita" in row['Nome']:
            folium.Marker([row['Latitude'], row['Longitude']], popup=tooltip, icon=folium.Icon(color="green")).add_to(m)
          else:
            folium.Marker([row['Latitude'], row['Longitude']], popup=tooltip).add_to(m)

  # Adiciona um marcador para a localização do usuário
  if printme:
    # Obter localização atual do usuário
    user_location = geocoder.ip('me')
    user_lat, user_lng = user_location.latlng
    folium.Marker([user_lat, user_lng], popup='Sua Localização', icon=folium.Icon(color='red')).add_to(m)

  # Exibe o mapa
  return m
