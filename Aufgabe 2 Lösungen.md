David Weiser  
Matrikelnummer: 4119665   
Wintersemester 2021  
Seminar FOSSGIS  
Dozentin: Christina Ludwig  
Fachsemester: 3  
Abgabetermin: 11.12.2020

# Assignment 2: GIS analyses using GRASS GIS

## 1. Create new location in GRASS GIS

Zunächst wird Grass Gis geöffnet und eine neue Location erstellt und benannt. Als Koordinatensystem soll jenes vom Global Human SettlementLayer benutzt werden. Das Kooridnatensystem ist World_Mollweide, EPSG 54009.

## 2. Import data

### 2.1. Motorways

`v.import motorways.shp`

### 2.2. Administrative Districts of Baden-Württemberg

`v.in.ogr input=gadm28_adm2_germany.shp layer=gadm28_adm2_germany output=Baden_Wuerttemberg__unproj where=ID_1=1 snap=1e-009 location=side_loc`

`v.proj location=side_loc input=BW_adm2_unproj output=Baden_Wuerttemberg_district`
### 2.3. Global Human Settlement Layer

Die Datei wurde mit `r.import GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3.tif` hinzugefügt

## 3. Calculate the total population of the districts

### 3.1. Set the region

Unter Einstellungen --> Computational region --> Region definieren (g.region) bzw. mit dem Befehl `g.region vector=Baden_Wuerttemberg_district res=250`

### 3.2. Rasterize the districts

Unter Vektor --> Kartentypumwandlung --> Vektor zu Raster. Als Eingabe-Vektorkarte  wählt man Baden_Wuerttemberg_district.

Als Quelle der Rasterwerte wählt man "attr", als Name der Spalte für den Parameter attr: "OBJECTID". 

Alternativ kann man auch den Befehl

`v.to.rast input=Baden_Wuerttemberg_district output=Baden_Wuerttemberg_district_raster  type=point,line,area use=attr attribute_column=OBJECTID` nutzen.

### 3.3 Calculate the population of each district
 
Unter Raster --> Karten überlagern --> Statistik Überlagerung. Einstellungen:
 
Name der Basis-Rasterkarte:
Baden_Wuerttemberg_district_raster

Name der Bedeckungs-Rasterkarte:
GlobalHumanSettlement

Methode der objektbasierten Statistik:
sum

Resultant raster map:
Population_per_district

Alternativ mit dem Befehl `r.stats.zonal base=Baden_Wuerttemberg_district_raster cover=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3 method=sum output=Population_per_district`

### 3.4. Evaluate the population estimate

Die Genauigkeit von fünf unterschiedlichen Regionen wird genauer untersucht.<br/> Als Referenzdatensatz werden hierfür die Daten des Statistischen Landesamt Baden-Württemberg verwendet.<br/> Um eine umfassende Genauigkeit zu erreichen, werden Regionen mit verschiedenen Bevölkerungsstrukturen verglichen, ländliche und städtische Regionen in verschiedenen Gebieten des Bundeslandes.

Datensatzdaten:<br/>

Stadtkreis Mannheim: 287.601 Einwohner<br/>
Landkreis Zollernalbkreis: 184.682 Einwohner<br/>
Stadtkreis Stuttgart: 600.081 Einwohner<br/>
Landkreis Bodenseekreis: 204.204 Einwohner

Daten vom Statistischen Landesamt:<br/>

Stadtkreis Mannheim: 310.658 (2013) <br/>
Landkreis Zollernalbkreis: 189.363 Einwohner<br/>
Stadtkreis Stuttgart: 635.911 Einwohner<br/>
Landkreis Bodenseekreis: 217.470 Einwohner

Die Daten vom Statistischen Bundeamt beziehen sich auf das Jahr 2019 mit Basis des Zensus 2011.

Differenz Mannheim: - 23.057 Einwohner (-8 %)<br/>
Differenz Zollernalbkreis: - 4681 Einwohner (-3 %)<br/>
Differenz Stuttgart: -35.830 Einwohner (-6 %)<br/>
Differenz Bodenseekreis: 13.266 Einwohner (- 6 %)

Aufgrund der dynamischeren Bevölkerungsentwicklung ist die Differenz in den zwei betrachteten Städten Mannheim und Stuttgart höher als die der Landkreise. <br/> Interessant ist, dass prozentual betrachtet die Differenz in Mannheim größer ist als in Stuttgart, obwohl Stuttgart deutlich mehr Einwohner besitzt. 
## 4. Calculate total population living within 1km of motorways

Zuerst wird die Region auf ein ein Kilometer großes Umfeld um die Autobahnen begrenzt.

`g.region vector=motorways.shp`

`v.buffer input=motorways.shp output=motorways_buffered.shp type=line distance=1000`

Dann wird, damit die Berechnung möglich ist, die motorways.shp in ein Raster umgewandelt.

`v.to.rast input=motorways_buffered.shp output=motorways_buffered_raster use=cat`

Da die Datenbank des Buffers nicht mit seiner Datenbank verbunden ist, muss noch folgender Befehl durchgeführt werden. 

`v.db.addtable motorways_buffered`

Jetzt wird die Bevölkerung innerhalb des Rasters bis zu einem ein Kilometer Umfeld von der Autobahn berechnet.

`r.stats.zonal base=motorways_buffered_raster cover=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3 method=sum output=motorways_population`

Insgesamt wohnen im betrachteten Untersuchungsgebiet 
299.503 Einwohner innerhalb eines maximalen Umkreises von einem Kilometer rund um eine oder mehrere Autobahnen.

## 5. Convert the script to Python

Für das Skript siehe "Aufgabe 2.5..py"



### Quellen

https://www.statistik-bw.de/BevoelkGebiet/
