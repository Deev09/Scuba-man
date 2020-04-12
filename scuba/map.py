import folium

m = folium.Map(location=[43, -71], zoom_start=12)

tooltip='Click for more'

logoIcon=folium.features.CustomIcon('logo.png', icon_size=(50,50))

#create markers
folium.Marker([43, -71], popup='<strong> Location </strong>',
                            tooltip=tooltip).add_to(m),

folium.Marker([43.005, -71], popup='<strong> Location </strong>',
                            tooltip=tooltip,
                            icon=folium.Icon(color='green', icon='cloud')).add_to(m),
folium.Marker([43.01, -71], popup='<strong> Location </strong>',
                            tooltip=tooltip,
                            icon=folium.Icon(color='green', icon='cloud')).add_to(m),

folium.Marker([43.02, -71], popup='<strong> Location </strong>',
                            tooltip=tooltip,
                            icon=logoIcon).add_to(m)
folium.CircleMarker(
    location=[43.03, -71],
    radius=50,
    popup='cool stuff',
    color='#428bca',
    fill=True,
    fill_color='#428bca'
).add_to(m)




m.save('map.html')
