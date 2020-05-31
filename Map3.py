import folium
import pandas as pd
import json

data=pd.read_csv("original (2).txt") #dataframe for volcano csv file

data_json = open("World.json",'r',encoding='utf-8-sig').read() #reading json file, itf-8 allows to read the unicode characters embedded within the file

#accessing the lists within the volcano file
latitude=list(data["LAT"])   
longitude=list(data["LON"])  
elevation=list(data["ELEV"])
name=list(data["NAME"])

#adding links on the html pop ups 
html = """Volcano name:<br><a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(height): 
    if height < 1000:
        return 'green'
    elif 1000<=height<3000:
        return 'orange'
    else: 
        return 'red'


def enterLocation(lati,loni):
     return lati,loni

lat_user=input("Please enter the latitude for your chosen location: ")
lon_user=input("Please enter the longitude for your chosen location: ")
user_input=enterLocation(lat_user,lon_user)




map = folium.Map(location=user_input,zoom_start=2,tiles="Stamen Terrain")
Figure_1=folium.FeatureGroup(name="Volcanoes")


for lat,lon,el,name in zip(latitude,longitude,elevation,name):
    designated_color = color_producer(el)
    html_link = folium.IFrame(html= html % (name, name, el), width=200, height=100)
    Figure_1.add_child(folium.Marker(location=[lat, lon], popup=folium.Popup(html_link), icon = folium.Icon(color = designated_color)))


Figure_2=folium.FeatureGroup(name="Population")
Figure_2.add_child(folium.GeoJson(data=data_json, style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005']<10000000 else 'orange' if  10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(Figure_1)
map.add_child(Figure_2)
map.add_child(folium.LayerControl())


map.save("Map4.html")