
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.sidebar.header("Hangi Mevki ?")
a = st.sidebar.selectbox('Mevki Seçiniz', ['SeçimYok','Defans','Orta Saha','Forvet'])

if a == "SeçimYok":
	
	st.markdown("""
		# Merhabalar
		## Ben Hüseyin Efkan Alp 

		* Yönetim Bilişim Sistemleri 3. sınıf öğrencisiyim ve kendimi Veri Bilimi alanında geliştirmeye çalışıyorum.
		 Bu alanda kendimi geliştirmek için bolca proje yapmaya özen gösteriyorum ve bu projeler benim için hem öğrenme sürecimdeki 
		 en önemli araçlardan biri hem de gelecekteki kariyer hedeflerime ulaşmamı sağlayacak deneyimlerim olacak.
		
		* Web olarak yaptığım ilk projem olmasına rağmen, bu projede öğrendiğim birçok şey oldu. 
		Ayrıca, diğer projelerime bakmak için [Github](https://github.com/HuseyinEfkanAlp) ve [Linkedin](https://www.linkedin.com/in/efkanalp/) hesaplarımı paylaştım. 
		Bu hesaplar sayesinde daha önce yaptığım projeleri inceleyebilir ve gelecekteki projelerimde de ilerleme kaydedebilirim.

		* Bu yazıda, web olarak yaptığım ilk projemden bahsedeceğim. Projemde, [Kaggle](https://www.kaggle.com/datasets/vivovinco/20212022-football-player-stats)'dan 
		aldığım 2021-2022 futbolcu istatistikleri veri setini kullanarak, sezonun ve mevkisinin en iyi futbolcularını sizin belirlediğiniz ağırlıklara göre seçeceğiz. 
		Ayrıca, [Kaggle](https://www.kaggle.com/datasets/vivovinco/20222023-football-player-stats)'dan indirdiğim 
		2022-2023 istatistikleri ile futbolcuların performanslarındaki yükselişi veya düşüşü gözlemleyeceğiz.

		* Bu iki veri seti beni oldukça uğraştırdı, çünkü çok ham ve ayrıntılı istatistiklere sahiptiler. 143 adet sütunu ayıklamak ve oyuncuların
		 mevkilerine göre özelliklerini seçmek, hem zor hem de futbol bilgisi gerektirdi.(Neyse ki o bilgi bende vardı :))
		* 143 adet sütunu ayıklamak ve oyuncuları mevkisine göre özelliklerini seçmek haliyle hem zor hem de futbol bilgisi gerektirdi.

		 
	""")
	st.info("Sol üstte ok tuşuna basıp mevki seçimi ve ağırlık verme işlemelerini yapabilirsiniz.")

	st.markdown(""" 
	### Umarım projemi beğenirsiniz. Teşekkür ederim.
	### Saygılarımla,
	""")





	
	
##************ DEFANSS **********
defans_df = pd.read_csv('Datasets/defans_df.csv')
print(defans_df.head())
defans_df2 = pd.read_csv('Datasets/defans_df2.csv')
defansdict = {"Baskı": 0,"Pass":0,"Gol":0,"Blok":0}
toplamdef = 0


#Function
def def_rate(def_df,blok = 30,baski = 35, pas = 25, gol = 10):
	#Rate
	def_df["Rate"] = (def_df["Blok"]*blok/100 + def_df["Baskı"]*baski/100\
		 + def_df["Pas"]* pas/100 + def_df["Gole_katkı"]*gol/100)*90/100 + (def_df["Dakika"]*10/100)
	#Sort
	def_df.sort_values("Rate", ascending=False, inplace=True)
	#Rate
	def_df["YourRate"] = pd.cut(def_df['Rate'].iloc[:10], 5,labels = [1,2,3,4,5])
	return def_df

def def_cross(df,name,pos,nation,team,born,blok = 30,baski = 35,pas = 25, gol = 10):
	feature_df = def_rate(def_df=df,blok=blok,baski=baski,pas=pas,gol=gol)
	s = feature_df[(feature_df["Name"]== name)|((feature_df["Nation"] == nation) & (feature_df["Team"] == team)\
		 & (feature_df["Pos"] == pos)& (feature_df["Born"] == born))]
	return s

#---


if a == 'Defans':
	baskiRate = st.sidebar.slider("Baskı", 0,100-toplamdef, step = 1,)
	toplamdef += baskiRate
	defansdict["Baskı"] = baskiRate
	if toplamdef < 100:
		passRate = st.sidebar.slider("Pass", 0,100-toplamdef, step = 1,)
		toplamdef += passRate
		defansdict["Pass"] = passRate
	if toplamdef < 100:
		golRate = st.sidebar.slider("Gol", 0,100-toplamdef, step = 1,)
		toplamdef += golRate
		defansdict["Gol"] = golRate
	if toplamdef < 100:
		blokRate = st.sidebar.slider("Bloklar", 0,100-toplamdef, step = 1,)
		toplamdef += blokRate
		defansdict["Blok"] = blokRate
	#Bilgilendirme
	if toplamdef == 100:
		st.sidebar.header("Ağırlıklarınız")
		st.sidebar.write(f"""

		|         Baskı           | Pass                  | Gol'e Katkı           |   Blok     |
		| :-----------            |    :-----------:      |     :--------:        |  ------------:      |
		|  {defansdict["Baskı"]}  | {defansdict["Pass"]} | {defansdict["Gol"]} |  {defansdict["Blok"]}  |

		""")
		#MainBar
		st.subheader("Ağırlıklarınıza göre 2021-2022 sezonunun en iyi 10 defansı")
		#Table
		top10defans = def_rate(def_df = defans_df, blok=defansdict["Blok"],baski=defansdict["Baskı"],\
			pas=defansdict["Pass"], gol=defansdict["Gol"])
		st.table(top10defans.iloc[0:10,[2,3,4,5,6,7,8,15]])
		st.success(f"Seçtiğiniz Kriterlerde En İyi Defans Oyuncusu : " + top10defans["Name"].iloc[0])
		#Graph
		df_fig_rate = pd.DataFrame(dict(r=top10defans["YourRate"][:10].values,
    	theta=top10defans["Name"][:10].values))
		fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
		tab1, tab2, tab3, tab4, tab5 = st.tabs(["Puan", "Blok","Baskı","Pas","Gol'e Katkı"])
		
		with tab1:
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab2:
			df_fig_rate = pd.DataFrame(dict(r=top10defans["Blok"][:10].values,
    		theta=top10defans["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab3:
			df_fig_rate = pd.DataFrame(dict(r=top10defans["Baskı"][:10].values,
    		theta=top10defans["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab4:
			df_fig_rate = pd.DataFrame(dict(r=top10defans["Pas"][:10].values,
    		theta=top10defans["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab5:
			df_fig_rate = pd.DataFrame(dict(r=top10defans["Gole_katkı"][:10].values,
    		theta=top10defans["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		#Cross Feature
		st.subheader("Bir Oyuncu seçin eğer gelecek sezon verileri var ise karşılaştıralım")
		st.info("Maalesef Bazı Oyuncular Veri Seti Farklılığından Dolayı Karşılaştırılamıyor")
		selected_name = st.selectbox('Seçiniz', top10defans["Name"][:10].values)
		player = top10defans[top10defans["Name"]== selected_name]
		selected_player_f = def_cross(df=defans_df2,name=selected_name,pos=player["Pos"].values[0],nation=player["Nation"].values[0]\
			,team=player["Team"].values[0],born=player["Born"].values[0],blok=defansdict["Blok"],baski=defansdict["Baskı"],\
			pas=defansdict["Pass"], gol=defansdict["Gol"])
		selected_player = top10defans[top10defans["Name"]==selected_name]

		cross = pd.DataFrame(dict(r=selected_player.iloc[:,9:13].values.reshape(4,),
		theta=selected_player.iloc[:,9:13].columns))

		cross2 = pd.DataFrame(dict(r=selected_player_f.iloc[:,9:13].values.reshape(4,),
		theta=selected_player_f.iloc[:,9:13].columns))
		
		fig2 = go.Figure()
		fig2.add_trace(go.Scatterpolar(
      		r=cross["r"],
      		theta=cross["theta"],
      		fill='toself',
      		name= selected_name ))
		fig2.add_trace(go.Scatterpolar(
			r=cross2["r"],
      		theta=cross2["theta"],
      		fill='toself',
      		name= f"{selected_name}2023"
		))
		fig2.update_layout(
  			polar=dict(
    			radialaxis=dict(
      				visible=True
          				)),
    			template = 'plotly_dark',
  
  			showlegend=True
		)
		st.plotly_chart(fig2, theme=None, use_container_width=True)
	else:
		st.sidebar.error("Ağırlıkların Toplamı 100 olmalı")

	
#---
#          ################Forvet######################
#---
# DataSet
forvet_df = pd.read_csv('Datasets/forvet_df.csv')
forvet_df2 = pd.read_csv('Datasets/forvet_df2.csv')
#--
# Function
def for_rate(for_df,press = 15,pas = 15, sut = 25, gol = 30,dripling=15):
	#Rate
	for_df["Rate"] = (for_df["Press"]*press/100 + for_df["Pas"]*pas/100 + for_df["Dripling"]*dripling/100
		 + for_df["Şut"]* sut/100 + for_df["Gole_katkı"]*gol/100)*93/100 + (for_df["Dakika"]*7/100)
	#Sort
	for_df.sort_values("Rate", ascending=False, inplace=True)
	#Rate
	for_df["YourRate"] = pd.cut(for_df['Rate'].iloc[:10], 5,labels = [1,2,3,4,5])
	return for_df
def for_cross(df,name,pos,nation,team,born,press = 15,pas = 15, sut = 25, gol = 30,dripling=15):
	feature_df = for_rate(for_df=df,press = press,pas = pas, sut = sut, gol = gol,dripling=dripling)
	s = feature_df[(feature_df["Name"]== name)|((feature_df["Nation"] == nation) & (feature_df["Team"] == team)\
		 & (feature_df["Pos"] == pos)& (feature_df["Born"] == born))]
	return s
#----
#

toplamFor = 0
forvetDict = {"Press": 0,"Pass":0,"Şut":0,"Gol":0,"Dripling":0}
if a == 'Forvet':
	pressRate = st.sidebar.slider("Press", 0,100-toplamFor, step = 1,)
	toplamFor += pressRate
	forvetDict["Press"] = pressRate
	if toplamFor < 100:
		passRate = st.sidebar.slider("Pass", 0,100-toplamFor , step = 1,)
		toplamFor += passRate
		forvetDict["Pass"] = passRate
	if toplamFor < 100:
		sutRate = st.sidebar.slider("Şut", 0,100-toplamFor , step = 1,)
		toplamFor += sutRate
		forvetDict["Şut"] = sutRate
	if toplamFor < 100:
		golRate = st.sidebar.slider("Gol", 0,100-toplamFor, step = 1,)
		toplamFor += golRate
		forvetDict["Gol"] = golRate
	if toplamFor < 100:
		dripRate = st.sidebar.slider("Dripling", 0,100-toplamFor, step = 1,)
		toplamFor += dripRate
		forvetDict["Dripling"] = dripRate
	#Bilgilendirme
	if toplamFor == 100:
		st.sidebar.header("Ağırlıklarınız")
		st.sidebar.write(f"""

		|         Press           | Pass                  |    Şut              | Gol                   |   Dripling     |
		| :-----------            |    :-----------:      |    :--------:       |    :--------:        |  ------------:      |
		|  {forvetDict["Press"]}  | {forvetDict["Pass"]} |{forvetDict["Şut"]}   |{forvetDict["Gol"]} |  {forvetDict["Dripling"]}  |

		""")
		#MainBar
		st.subheader("Ağırlıklarınıza göre 2021-2022 sezonunun en iyi 10 Forveti")
		#Table
		top10forvet = for_rate(for_df = forvet_df, press=forvetDict["Press"],pas=forvetDict["Pass"],\
			sut=forvetDict["Şut"], gol=forvetDict["Gol"], dripling=forvetDict["Dripling"])
		st.table(top10forvet.iloc[0:10,[2,3,4,5,6,7,8,15]])
		st.success(f"Seçtiğiniz Kriterlerde En İyi Forvet Oyuncusu : " + top10forvet["Name"].iloc[0])
		#Graph
		df_fig_rate = pd.DataFrame(dict(r=top10forvet["YourRate"][:10].values,
    	theta=top10forvet["Name"][:10].values))
		fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
		tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Puan", "Press","Pas","Şut","Gol'e Katkı","Dripling"])
		
		with tab1:
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab2:
			df_fig_rate = pd.DataFrame(dict(r=top10forvet["Press"][:10].values,
    		theta=top10forvet["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab3:
			df_fig_rate = pd.DataFrame(dict(r=top10forvet["Pas"][:10].values,
    		theta=top10forvet["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab4:
			df_fig_rate = pd.DataFrame(dict(r=top10forvet["Şut"][:10].values,
    		theta=top10forvet["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab5:
			df_fig_rate = pd.DataFrame(dict(r=top10forvet["Gole_katkı"][:10].values,
    		theta=top10forvet["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab6:
			df_fig_rate = pd.DataFrame(dict(r=top10forvet["Dripling"][:10].values,
    		theta=top10forvet["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		#Cross Feature
		st.subheader("Bir Oyuncu seçin eğer gelecek sezon verileri var ise karşılaştıralım")
		st.info("Maalesef Bazı Oyuncular Veri Seti Farklılığından Dolayı Karşılaştırılamıyor")
		selected_name = st.selectbox('Seçiniz', top10forvet["Name"][:10].values)
		player = top10forvet[top10forvet["Name"]== selected_name]
		selected_player_f = for_cross(df=forvet_df2,name=selected_name,pos=player["Pos"].values[0],nation=player["Nation"].values[0]\
			,team=player["Team"].values[0],born=player["Born"].values[0],press=forvetDict["Press"],pas=forvetDict["Pass"],\
			sut=forvetDict["Şut"], gol=forvetDict["Gol"], dripling=forvetDict["Dripling"])

		selected_player = top10forvet[top10forvet["Name"]==selected_name]

		cross = pd.DataFrame(dict(r=selected_player.iloc[:,9:14].values.reshape(5,),
		theta=selected_player.iloc[:,9:14].columns))

		cross2 = pd.DataFrame(dict(r=selected_player_f.iloc[:,9:14].values.reshape(5,),
		theta=selected_player_f.iloc[:,9:14].columns))
		
		fig2 = go.Figure()
		fig2.add_trace(go.Scatterpolar(
      		r=cross["r"],
      		theta=cross["theta"],
      		fill='toself',
      		name= selected_name ))
		fig2.add_trace(go.Scatterpolar(
			r=cross2["r"],
      		theta=cross2["theta"],
      		fill='toself',
      		name= f"{selected_name}2023"
		))
		fig2.update_layout(
  			polar=dict(
    			radialaxis=dict(
      				visible=True
          				)),
    			template = 'plotly_dark',
  
  			showlegend=True
		)
		st.plotly_chart(fig2, theme=None, use_container_width=True)
		
	else:
		st.sidebar.error("Ağırlıkların Toplamı 100 olmalı")

#---

#Orta Saha
#          ################Orta Saha######################
#---
# DataSet
orta_df = pd.read_csv('Datasets/orta_df.csv')
orta_df2 = pd.read_csv('Datasets/orta_df2.csv')
#--
# Function
def ort_rate(orta_df,press = 15,pas = 15, sut = 25, gol = 30,dripling=15):
	#Rate
	orta_df["Rate"] = (orta_df["Press"]*press/100 + orta_df["Pas"]*pas/100 + orta_df["Dripling"]*dripling/100
		 + orta_df["Şut"]* sut/100 + orta_df["Gole_katkı"]*gol/100)*93/100 + (orta_df["Dakika"]*7/100)
	#Sort
	orta_df.sort_values("Rate", ascending=False, inplace=True)
	#Rate
	orta_df["YourRate"] = pd.cut(orta_df['Rate'].iloc[:10], 5,labels = [1,2,3,4,5])
	return orta_df
def ort_cross(df,name,pos,nation,team,born,press = 15,pas = 15, sut = 25, gol = 30,dripling=15):
	feature_df = ort_rate(orta_df=df,press = press,pas = pas, sut = sut, gol = gol,dripling=dripling)
	s = feature_df[(feature_df["Name"]== name)|((feature_df["Nation"] == nation) & (feature_df["Team"] == team)\
		 & (feature_df["Pos"] == pos)& (feature_df["Born"] == born))]
	return s
	
	
#----
#

toplamOrt = 0
ortaDict = {"Press": 0,"Pass":0,"Şut":0,"Gol":0,"Dripling":0}

if a == 'Orta Saha':
	pressRate = st.sidebar.slider("Press", 0,100-toplamOrt, step = 1,)
	toplamOrt += pressRate
	ortaDict["Press"] = pressRate
	if toplamOrt < 100:
		passRate = st.sidebar.slider("Pass", 0,100-toplamOrt , step = 1,)
		toplamOrt += passRate
		ortaDict["Pass"] = passRate
	if toplamOrt < 100:
		sutRate = st.sidebar.slider("Şut", 0,100-toplamOrt , step = 1,)
		toplamOrt += sutRate
		ortaDict["Şut"] = sutRate
	if toplamOrt < 100:
		golRate = st.sidebar.slider("Gol", 0,100-toplamOrt, step = 1,)
		toplamOrt += golRate
		ortaDict["Gol"] = golRate
	if toplamOrt < 100:
		dripRate = st.sidebar.slider("Dripling", 0,100-toplamOrt, step = 1,)
		toplamOrt += dripRate
		ortaDict["Dripling"] = dripRate
	#Bilgilendirme
	if toplamOrt == 100:
		st.sidebar.header("Ağırlıklarınız")
		st.sidebar.write(f"""

		|         Press           | Pass                  |    Şut              | Gol                   |   Dripling     |
		| :-----------            |    :-----------:      |    :--------:       |    :--------:        |  ------------:      |
		|  {ortaDict["Press"]}  | {ortaDict["Pass"]} |{ortaDict["Şut"]}   |{ortaDict["Gol"]} |  {ortaDict["Dripling"]}  |

		""")
		#MainBar
		st.subheader("Ağırlıklarınıza göre 2021-2022 sezonunun en iyi 10 Orta Sahası")
		#Table
		top10orta = ort_rate(orta_df = orta_df, press=ortaDict["Press"],pas=ortaDict["Pass"],\
			sut=ortaDict["Şut"], gol=ortaDict["Gol"], dripling=ortaDict["Dripling"])
		st.table(top10orta.iloc[0:10,[2,3,4,5,6,7,8,15]])
		st.success(f"Seçtiğiniz Kriterlerde En İyi Orta Saha Oyuncusu : " + top10orta["Name"].iloc[0])
		#Graph
		df_fig_rate = pd.DataFrame(dict(r=top10orta["YourRate"][:10].values,
    	theta=top10orta["Name"][:10].values))
		fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
		tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Puan", "Press","Pas","Şut","Gol'e Katkı","Dripling"])
		
		with tab1:
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab2:
			df_fig_rate = pd.DataFrame(dict(r=top10orta["Press"][:10].values,
    		theta=top10orta["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab3:
			df_fig_rate = pd.DataFrame(dict(r=top10orta["Pas"][:10].values,
    		theta=top10orta["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab4:
			df_fig_rate = pd.DataFrame(dict(r=top10orta["Şut"][:10].values,
    		theta=top10orta["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab5:
			df_fig_rate = pd.DataFrame(dict(r=top10orta["Gole_katkı"][:10].values,
    		theta=top10orta["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		with tab6:
			df_fig_rate = pd.DataFrame(dict(r=top10orta["Dripling"][:10].values,
    		theta=top10orta["Name"][:10].values))
			fig = px.line_polar(df_fig_rate, r='r', theta='theta', line_close=True)
			st.plotly_chart(fig, theme=None, use_container_width=True)
		#Cross Feature
		st.subheader("Bir futbolcu seçin eğer gelecek sezon verileri var ise karşılaştıralım")
		st.info("Maalesef Bazı Oyuncular Veri Seti Farklılığından Dolayı Karşılaştırılamıyor")
		selected_name = st.selectbox('Seçiniz', top10orta["Name"][:10].values)
		player = top10orta[top10orta["Name"]== selected_name]
		selected_player_f = ort_cross(df=orta_df2,name=selected_name,pos=player["Pos"].values[0],nation=player["Nation"].values[0]\
			,team=player["Team"].values[0],born=player["Born"].values[0],press=ortaDict["Press"],pas=ortaDict["Pass"],\
			sut=ortaDict["Şut"], gol=ortaDict["Gol"], dripling=ortaDict["Dripling"])

		selected_player = top10orta[top10orta["Name"]==selected_name]

		cross = pd.DataFrame(dict(r=selected_player.iloc[:,9:14].values.reshape(5,),
		theta=selected_player.iloc[:,9:14].columns))

		cross2 = pd.DataFrame(dict(r=selected_player_f.iloc[:,9:14].values.reshape(5,),
		theta=selected_player_f.iloc[:,9:14].columns))
		
		fig2 = go.Figure()
		fig2.add_trace(go.Scatterpolar(
      		r=cross["r"],
      		theta=cross["theta"],
      		fill='toself',
      		name= selected_name ))
		fig2.add_trace(go.Scatterpolar(
			r=cross2["r"],
      		theta=cross2["theta"],
      		fill='toself',
      		name= f"{selected_name}2023"
		))
		fig2.update_layout(
  			polar=dict(
    			radialaxis=dict(
      				visible=True
          				)),
    			template = 'plotly_dark',
  
  			showlegend=True
		)
		st.plotly_chart(fig2, theme=None, use_container_width=True)
		
	else:
		st.sidebar.error("Ağırlıkların Toplamı 100 olmalı")

#---
st.markdown("""
## Hüseyin Efkan Alp
[Github Hesabıma Buradan Ulaşabilirsiniz.](https://github.com/HuseyinEfkanAlp)

[Linkedin Hesabıma Buradan Ulaşabilirsiniz.](https://www.linkedin.com/in/efkanalp/)
""")






