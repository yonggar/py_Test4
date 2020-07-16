import pandas as pd
import numpy as np
import folium
import webbrowser
import chardet
import json


def center_calc(points_df):
    x = points_df.x
    y = points_df.y

    X = (max(x)+min(x))/2.
    Y = (max(y)+min(y))/2.

    return X, Y


def points_array(points):

    final_points = []

    for x in range(0, len(points)):

        if len(points[x]) == 2:
            final_points.append(points[x])
        else:
            target = points[x]
            for y in range(0, len(target)):
                final_points.append(target[y])

    return final_points


state_path = 'GOS/CTPRVN_wgs84.json'
state_geo = json.load(open(state_path, encoding='utf-8'))

state_unemployment = 'GOS/Total_People_2020_6_2.csv'
state_data = pd.read_csv(state_unemployment, encoding='EUC-KR')
state_data = state_data.astype({'CODE': 'str', 'POPULATION': 'float'})

center_locations = pd.DataFrame()
codes = []
names = []
x_list = []
y_list = []
for x in range(0, len(state_geo['features'])):
    code = state_geo['features'][x]['properties']['CTPRVN_CD']
    name = state_geo['features'][x]['properties']['CTP_KOR_NM']
    # 중앙값 생성
    points = state_geo['features'][x]['geometry']['coordinates'][0]
    points = points_array(points)
    points_df = pd.DataFrame(points)
    points_df.columns = ['x', 'y']
    X, Y = center_calc(points_df)

    # 결과
    codes.append(code)
    names.append(name)
    x_list.append(X)
    y_list.append(Y)

# 데이터 프레임 생성
center_locations['CODE'] = codes
center_locations['NAME'] = names
center_locations['X'] = x_list
center_locations['Y'] = y_list

# for row in state_data :
target_df = pd.merge(state_data, center_locations, how='left', on='CODE')
target_df = target_df[~np.isnan(target_df['X'])]  # 위치 정보 없는 값 제외

m = folium.Map(location=[36, 127], tiles="OpenStreetMap", zoom_start=7)

for i in range(0, len(target_df)):
    latitude = target_df.iloc[i]['Y']
    longitude = target_df.iloc[i]['X']
    location = (latitude, longitude)
    folium.CircleMarker(location, radius=target_df.iloc[i]['POPULATION']/250000,
                        color='#3186cc', fill_color='#3186cc', popup=target_df.iloc[i]['NAME']).add_to(m)


folium.LayerControl(collapsed=False).add_to(m)

m.save('kr_polulation.html')
webbrowser.open_new("kr_polulation.html")