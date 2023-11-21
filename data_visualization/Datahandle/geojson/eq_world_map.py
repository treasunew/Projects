import plotly.express as px
from pathlib import Path
import json
import pandas as pd

# 一天的数据
# path = Path("Projects/data_visualization/Datahandle/geojson/data/eq_data_1_day_m1.geojson")
# contents = path.read_text()

# 一个月的数据
path = Path("Projects/data_visualization/Datahandle/geojson/data/eq_data_30_day_m1.geojson")
try:
    contents = path.read_text()
except:
    contents = path.read_text(encoding='utf-8')


all_eq_data = json.loads(contents)
all_eq_dicts = all_eq_data['features']
print(len(all_eq_dicts))


mags, titles, lons, lats = [], [], [], []
for eq_dict in all_eq_dicts:
    # mag = eq_dict['properties']['mag']
    # title = eq_dict['properties']['title']
    # lon = eq_dict['geometry']['coordinates'][0]
    # lat = eq_dict['geometry']['coordinates'][1]
    # mags.append(mag)
    # titles.append(title)
    # lons.append(lon)
    # lats.append(lat)
    # reconstruct
    mags.append(eq_dict['properties']['mag'])
    titles.append(eq_dict['properties']['title'])
    lons.append(eq_dict['geometry']['coordinates'][0])
    lats.append(eq_dict['geometry']['coordinates'][1])


data = pd.DataFrame(data=zip(lons, lats, titles, mags), columns=['经度', '纬度', '位置', '震级'])    

# print(data)

# NOTE 方案1
# fig = px.scatter(
#     x=lons,
#     y=lats,
#     labels={'x':'经度', 'y':'纬度'},
#     range_x=[-200,200],
#     range_y=[-90,90],
#     width=800,
#     height=800,
#     title='全球地震散点图'
# )

# NOTE 方案2
fig = px.scatter(
    data,
    x='经度',
    y='纬度',
    range_x=[-200,200],
    range_y=[-90,90],
    width=800,
    height=800,
    title='全球地震散点图',
    size='震级',
    size_max=10,
    color='震级',
    hover_name='位置',
)


# fig.write_html('Projects/data_visualization/Datahandle/geojson/data/global_earthquakes.html')
fig.show()