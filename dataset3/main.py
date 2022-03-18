import pandas as pd
import folium
from flask import Flask, render_template

corona = pd.read_csv("covid-19-dataset-3.csv")
byCountry = corona.groupby("Country_Region").sum()[["Confirmed", "Deaths", "Recovered", "Active"]]
confirmed = byCountry.nlargest(15, "Confirmed")[["Confirmed"]]
pairs=[(country,confirmed) for country,confirmed in zip(confirmed.index,confirmed['Confirmed'])]

corona = corona[['Lat','Long_','Confirmed']]
corona = corona.dropna()
map = folium.Map(location=[34.223334,-82.461707], tiles="Stamen toner", zoom_start=8)

def circle_maker(x):
    folium.Circle(location=[x[0],x[1]], radius=float(x[2]), color="red", popup='confirmed cases:{}'.format(x[2])).add_to(map)
corona.apply(lambda x:circle_maker(x),axis=1)
html_map=map._repr_html_()

app=Flask(__name__)
@app.route('/')
def home():
    return render_template("home.html",table=confirmed, cmap=html_map,pairs=pairs)
if __name__=="__main__":
    app.run(debug=True)
