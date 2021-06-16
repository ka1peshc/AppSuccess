import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
import datetime
import io
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import textwrap
import numpy as np
#import dash_dangerously_set_inner_html

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

df=pd.DataFrame()
l_o_c=None
l_o_n=None
l_o_d=None
which_screen="default_screen"
pehla_load=True
X_train=None
df_apps=None


navbar = dbc.NavbarSimple(
    brand="Google play store Anaylsis",
    brand_href="#",
    sticky="top",
    color = '#234d20',
    dark=True,
)
card_content = [
    dbc.CardHeader("Project",style = { 'backgroundColor' : '#234d20'},),
    dbc.CardBody(
        [
            html.H5("APP ANAYLSIS", className="card-title"),
            html.P(
                "Synopsis about project to be written here",
                className="card-text",
            ),
        ],style = { 'backgroundColor' : '#77ab59'},
    ),
]
#list of options in project
card_content1 = [
    dbc.CardHeader("App Anaylsis ",style = { 'backgroundColor' : '#234d20'},),
    dbc.CardBody(
        [
            dbc.ListGroup
            ([
        		dbc.ListGroupItem("Import Dataset",n_clicks_timestamp=0,id = 'l1',style = { 'backgroundColor' : '#77ab59'},),
        		dbc.ListGroupItem("View Graphs",n_clicks_timestamp=0,id = 'l2',style = { 'backgroundColor' : '#77ab59'},),
        		dbc.ListGroupItem("Classification",n_clicks_timestamp=0,id = 'l3',style = { 'backgroundColor' : '#77ab59'},),
        		dbc.ListGroupItem("Clustering",n_clicks_timestamp=0,id = 'l4',style = { 'backgroundColor' : '#77ab59'},),
    		], flush = True,),
        ],style = { 'backgroundColor' : '#77ab59'},
    ),
]

#Upload csv
card_content2 = [
    dbc.CardHeader("Dataset ",style = { 'backgroundColor' : '#234d20'},),
    dbc.CardBody(
        [
        dbc.Row([
        		dbc.Col([dcc.Upload(id='upload_file',children=[dbc.Button("Import Csv file", id = "icsv",color="primary", className="mr-1")])]),]),
        dbc.Row(
            [
            dbc.Col(id = 'dataset_info'),
            ]
        ),
        ],style = { 'backgroundColor' : '#77ab59'},
    ),
]
#Graph visualization
content_for_2d=[
	
	 dbc.Row(
            [dbc.Col(
                    [
                      html.Div([
						dcc.Dropdown(
					    options=[],
					    value='',
					    multi = True,
					    id = '2dx_axis_dropdown',
					    placeholder="X-axis"
							)],className = "dash-bootstrap")
                    ],width = 6
                ),
                dbc.Col(
                    [
                      html.Div([
        		dcc.Dropdown(
					    options=[],
					    value='',
					    multi = True,
					    id = '2dy_axis_dropdown',
					    placeholder="Y-axis"
							)],className = "dash-bootstrap")
                    ],width = 6
                	   ),
            ]),html.P(),html.P(),
	 dbc.Row(
            [
                dbc.Col(
                    [
                      html.Div([
        		dcc.Dropdown(
					    multi = True,
					    id = 'plot_dropdown',
					    placeholder="Select a plot type"
							)],className = "dash-bootstrap")
                    ],width = 12
                ),
            ]
        	),html.P(),html.P(),
	 dbc.Row([
	 	dbc.Col([dbc.Row([dbc.Col([html.Div([
        		dcc.Dropdown(
					    multi = True,
					    id = 'size_dd',
					    placeholder="Size Dimension",
					    disabled=True
							)],className = "dash-bootstrap")],width=6),dbc.Col([html.Div([
        		dcc.Dropdown(
					    multi = True,
					    id = 'color_dd',
					    placeholder="Color Dimension",
					    disabled=True
							)],className = "dash-bootstrap")],width=6)])
            ,],id='hidden_col',width=12),
	 	]),html.P(),html.P(),
	 dbc.Row([
	 	dbc.Col([dbc.Button("Plot graph", id = "plotbutton",color="primary", className="mr-1")],width=12),
	 	]),html.P(),html.P(),
	 dbc.Row([
	 	dbc.Col([html.Div(id='graphdiv')],width=12),
	 	])


]

card_contentvg = [
    dbc.CardHeader("Graph Ploting",style = { 'backgroundColor' : '#234d20'},),
    dbc.CardBody(
        [
        		html.Div([
        		dcc.Dropdown(
					    options=[{'label':'2-Dimensional plot','value':'2d'}],
					    value='2d',
					    multi = True,
					    id = 'general_dropdown',
					    placeholder="Select number of Dimensions"
							)],className = "dash-bootstrap"),
        		html.P(),html.P(),
        dbc.Row([
        		dbc.Col([html.Div(id='divgraphcontent')],width=12)
        		]),html.P(),html.P(),
        ],style = { 'backgroundColor' : '#77ab59'},
    ),	
]




loc=['ART_AND_DESIGN','AUTO_AND_VEHICLES','BEAUTY','BOOKS_AND_REFERENCE',
 'BUSINESS','COMICS','COMMUNICATION','DATING','EDUCATION','ENTERTAINMENT',
 'EVENTS','FINANCE','FOOD_AND_DRINK','HEALTH_AND_FITNESS','HOUSE_AND_HOME',
 'LIBRARIES_AND_DEMO','LIFESTYLE','GAME','FAMILY','MEDICAL','SOCIAL',
 'SHOPPING','PHOTOGRAPHY','SPORTS','TRAVEL_AND_LOCAL','TOOLS',
 'PERSONALIZATION','PRODUCTIVITY','PARENTING','WEATHER','VIDEO_PLAYERS',
 'NEWS_AND_MAGAZINES','MAPS_AND_NAVIGATION']
 
list_of_app_categories=[]
 
for i in range (0,33):
	list_of_app_categories.append({'label':loc[i],'value':loc[i]})
#Classification panel
card_content4 = [
    dbc.CardHeader("Classification ",style = { 'backgroundColor' : '#234d20'},),
    dbc.CardBody([
		dbc.Row(
			[
			dbc.Col([
				html.H5('Category :'),
			],width = 3),
			dbc.Col([
			html.Div([
        		dcc.Dropdown(
					    options=list_of_app_categories,
					    value='',
					    id = 'app_categories_dropdown',
						placeholder = 'Select category'
						)],className = "dash-bootstrap"),
			],width = 9),
			]
		),
		html.P(),
		dbc.Row([
            dbc.Col(html.H5('Enter App size :'),width = 3),
			dbc.Col([
			dcc.Input(id='app_size',placeholder = 'Size of the app in number',type = 'number'),
			],width = 9),
            ]),html.P(),
		dbc.Row([
            dbc.Col(html.H5('Type :'),width = 3),
			dbc.Col([dcc.RadioItems(
				id='type_radiobutton',
				options=[
					{'label':'Paid','value':1},
					{'label':'Free','value':0},
				],
				value=0,
				labelStyle={'display':'inline-block'}
			)],width = 9),
            ]),html.P(),
			
		dbc.Row([
            dbc.Col(html.H5('Price :'),width = 3),
			dbc.Col([
			dcc.Input(id='app_price',placeholder='If app is free then enter 0',type ='number')
			],width = 9),
            ]),html.P(),
		
		dbc.Row(
            [
			dbc.Col(html.H5('App Users type'),width = 3),
            dbc.Col([
			html.Div([
				dcc.Dropdown(
				options=[{'label':'Everyone','value':'Everyone'},{'label':'Teen','value':'Teen'},{'label':'Mature 17+','value':'Mature'}],
				value='',
				id='app_usertype_dropdown'
				)
			],className="dash-bootstrap")
			],width = 9),
            ]
        ),html.P(),
		dbc.Row(
			[
			dbc.Col([
				html.H5('Genre related to category :'),
			],width = 3),
			dbc.Col([
			html.Div([
        		dcc.Dropdown(
						options=[],
					    id = 'genre_classification',
						placeholder = 'Select genre'
						)],className = "dash-bootstrap"),
			],width = 9),
			]
		),		
		dbc.Row([
			dbc.Col(html.H5('Check accuracy for your dataset'),width = 3),
			dbc.Col([
			html.Div([
        		dcc.Dropdown(
				id='check_accuracy_dd',
				options = [
							{'label':'Decision tree','value':'dt'},
							{'label':'Random Forest','value':'rf'}
						],
				value='',				
			)],className = "dash-bootstrap"),
			],width=9),
		]),html.P(),
		
		dbc.Row(
		[
			dbc.Col(html.Div(id='Display_card_content4',className = "dash-bootstrap"),width=12),
		]),
	],style = { 'backgroundColor' : '#77ab59'},
	),
 ]

card_cluster=[
	dbc.CardHeader("Clustering ",style = { 'backgroundColor' : '#234d20'},),
	dbc.CardBody([
		dbc.Row(
			[
			dbc.Col([
				html.H5('Category :'),
			],width = 3),
			dbc.Col([
			html.Div([
        		dcc.Dropdown(
					    options=list_of_app_categories,
					    value='',
					    id = 'app_categories_dropdown_cluster',
						placeholder = 'Select category'
						)],className = "dash-bootstrap"),
			],width = 9),
			]
		),
		html.P(),
		dbc.Row([
            dbc.Col(html.H5('Enter App size :'),width = 3),
			dbc.Col([
			dcc.Input(id='app_size_cluster',placeholder = 'Size of the app in number',type = 'number'),
			],width = 9),
            ]),html.P(),
		dbc.Row([
            dbc.Col(html.H5('Type :'),width = 3),
			dbc.Col([dcc.RadioItems(
				id='type_radiobutton_cluster',
				options=[
					{'label':'Paid','value':1},
					{'label':'Free','value':0},
				],
				value=0,
				labelStyle={'display':'inline-block'}
			)],width = 9),
            ]),html.P(),
			
		dbc.Row([
            dbc.Col(html.H5('Price :'),width = 3),
			dbc.Col([
			dcc.Input(id='app_price_cluster',placeholder='If app is free then enter 0',type ='number')
			],width = 9),
            ]),html.P(),
		
		dbc.Row(
            [
			dbc.Col(html.H5('App Users type'),width = 3),
            dbc.Col([
			html.Div([
				dcc.Dropdown(
				options=[{'label':'Everyone','value':'Everyone'},{'label':'Teen','value':'Teen'},{'label':'Mature 17+','value':'Mature'}],
				value='',
				id='app_usertype_dropdown_cluster'
				)
			],className="dash-bootstrap")
			],width = 9),
            ]
        ),html.P(),
		dbc.Row(
			[
			dbc.Col([
				html.H5('Genre related to category :'),
			],width = 3),
			dbc.Col([
			html.Div([
        		dcc.Dropdown(
						options=[],
					    id = 'app_genres_dropdown_cluster',
						placeholder = 'Select genre'
						)],className = "dash-bootstrap"),
			],width = 9),
			]
		),
		dbc.Row([
			dbc.Col(dbc.Button("Display Cluster Result",id = "showcluster",color="primary",n_clicks_timestamp=0, className="mr-1"),width=12),
		]),
		dbc.Row(dbc.Col([html.Div(id = 'cluster_output')],width=12)),
	],style = { 'backgroundColor' : '#77ab59'})
 ]
 
 
#Container to hold card views
body = dbc.Container(
    [
        dbc.Row( 
            [
                dbc.Col(
                    [
                      dbc.Card(card_content1, color="dark", inverse=True)
                    ],width = 4
                ),
                dbc.Col(
                    [
                      dbc.Card(card_content, color="dark", inverse=True,id = 'changecontent'),
                    ],width = 8
                ),
            ]
        )
    ],
    className="mt-4",
    fluid = True,
    style = { 'paddingTop' : '4px', 'paddingBottom' : '4px'},
)


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([navbar,body])

#Graph ploting using 2 columns
@app.callback(
    [Output(component_id='plot_dropdown', component_property='options')],
    [Input(component_id='2dx_axis_dropdown', component_property='value')
    ,Input(component_id='2dy_axis_dropdown', component_property='value')]
)
def display_plots_available(xval,yval):
	global df
	list_of_plots=[]
	#print('main'+xval)
	if xval is not None and yval is not None:
		if isinstance(xval,str):
			if isinstance(yval,str):
				if df.shape[0]>0:
					print(xval+''+yval)
					if ((df[xval].dtype == np.float64 or df[xval].dtype == np.int64) and (df[yval].dtype == np.float64 or df[yval].dtype == np.int64)):
						if (df[xval].dtype == np.int64 and df[yval].dtype == np.int64):
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})			
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})
						else:
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})
					elif ((df[xval].dtype == np.float64) == False and (df[yval].dtype == np.float64) == False):
						if (df[xval].dtype == np.int64 and df[yval].dtype == np.int64):
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})			
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})
						else:
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})

					else:
						list_of_plots.append({'label':'Box plot','value':'bx'})
						list_of_plots.append({'label':'Voilin plot','value':'vl'})

#					return list_of_plots
			else:
				yvall=yval[len(yval)-1]
				if df.shape[0]>0:
					print(xval+''+yvall)
					if ((df[xval].dtype == np.float64 or df[xval].dtype == np.int64) and (df[yvall].dtype == np.float64 or df[yvall].dtype == np.int64)):
						if (df[xval].dtype == np.int64 and df[yvall].dtype == np.int64):
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})			
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})
						else:
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})
					elif ((df[xval].dtype == np.float64) == False and (df[yvall].dtype == np.float64) == False):
						if (df[xval].dtype == np.int64 and df[yvall].dtype == np.int64):
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})			
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})
						else:
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})
					else:
						list_of_plots.append({'label':'Box plot','value':'bx'})
						list_of_plots.append({'label':'Voilin plot','value':'vl'})

					#return list_of_plots
		else:
			xvall=xval[len(xval)-1]
			if isinstance(yval,str):
				if df.shape[0]>0:
					print(xvall+''+yval)
					if ((df[xvall].dtype == np.float64 or df[xvall].dtype == np.int64) and (df[yval].dtype == np.float64 or df[yval].dtype == np.int64)):
						if (df[xvall].dtype == np.int64 and df[yval].dtype == np.int64):
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})			
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})
						else:
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})
					elif ((df[xvall].dtype == np.float64) == False and (df[yval].dtype == np.float64) == False):
						if (df[xvall].dtype == np.int64 and df[yval].dtype == np.int64):
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})			
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})
						else:
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})

					else:
						list_of_plots.append({'label':'Box plot','value':'bx'})
						list_of_plots.append({'label':'Voilin plot','value':'vl'})

				#	return list_of_plots
			else:
				yvall=yval[len(yval)-1]
				if df.shape[0]>0:
					print(xvall+''+yvall)
					if ((df[xvall].dtype == np.float64 or df[xvall].dtype == np.int64) and (df[yvall].dtype == np.float64 or df[yvall].dtype == np.int64)):
						if (df[xvall].dtype == np.int64 and df[yvall].dtype == np.int64):
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})			
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})
						else:
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})
					elif ((df[xvall].dtype == np.float64) == False and (df[yvall].dtype == np.float64) == False):
						if (df[xvall].dtype == np.int64 and df[yvall].dtype == np.int64):
							list_of_plots.append({'label':'Scatter plot','value':'scatter'})
							list_of_plots.append({'label':'Line plot','value':'line'})
							list_of_plots.append({'label':'Bubble Chart','value':'bub'})			
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})
						else:
							list_of_plots.append({'label':'Stacked Bars','value':'stack'})
							list_of_plots.append({'label':'Multiple Bars','value':'mbars'})

					else:
						list_of_plots.append({'label':'Box plot','value':'bx'})
						list_of_plots.append({'label':'Voilin plot','value':'vl'})

					#return list_of_plots
	else:
		list_of_plots=[{}]

	print(list_of_plots)

	return [list_of_plots]

@app.callback(
    [Output(component_id='size_dd', component_property='disabled'),
    Output(component_id='color_dd', component_property='disabled')],
    [Input(component_id='plot_dropdown', component_property='value')]
)
def show_extra(value):
	new_val=''
	if isinstance(value,str):
		new_val=value
	else:
		new_val=value[len(value)-1]
	if new_val == 'scatter' or new_val == 'bub':
		return False,False
	elif new_val == 'bx' or new_val == 'vl' or new_val == 'line':
		return True,False
	else:
		return True,True


@app.callback(
    [Output(component_id='divgraphcontent', component_property='children'),
    Output(component_id='2dx_axis_dropdown', component_property='options'),
    Output(component_id='2dy_axis_dropdown', component_property='options'),
    Output(component_id='size_dd', component_property='options'),
    Output(component_id='color_dd', component_property='options')
    ],
    [Input(component_id='general_dropdown', component_property='value')]
)
def change_vg_child(value):
	global df
	if isinstance(value,str):
		selected_val=value
		if selected_val == '2d':
			lcc=[]
			colslist=[]
			if df.shape[0]>0:
				lc=df.columns
				for i in range(0,len(lc)):
					lcc.append({'label':lc[i],'value':lc[i]})
				for j in lc:
					if (df[j].dtype == np.float64 or df[j].dtype == np.int64) == False:
						colslist.append({'label':j,'value':j})

			return content_for_2d,lcc,lcc,lcc,colslist
		else:
			return [html.P('hello')],[{}],[{}]
	else:
		selected_val=value[len(value)-1]
		if selected_val == '2d':
			lcc=[]
			colslist=[]
			if df.shape[0]>0:
				lc=df.columns
				for i in range(0,len(lc)):
					lcc.append({'label':lc[i],'value':lc[i]})
				for j in lc:
					if (df[j].dtype == np.float64 or df[j].dtype == np.int64) == False:
						colslist.append({'label':j,'value':j})
			return content_for_2d,lcc,lcc,lcc,colslist
		else:
			return [html.P('hello')],[{}],[{}]


@app.callback(
	Output(component_id='2dx_axis_dropdown', component_property='value'),
    [Input(component_id='2dx_axis_dropdown', component_property='options')]
)
def setvalx(options):
	if len(options)>0:
		return options[0]['value']
	else:
		return None

@app.callback(
	Output(component_id='2dy_axis_dropdown', component_property='value'),
    [Input(component_id='2dy_axis_dropdown', component_property='options')]
)
def setvaly(options):
	if len(options)>0:
		return options[0]['value']
	else:
		return None

@app.callback(
    [Output(component_id='graphdiv', component_property='children')],
    [Input(component_id='plotbutton', component_property='n_clicks')],
    [State(component_id='general_dropdown',component_property='value'),State(component_id='2dx_axis_dropdown',component_property='value'),State(component_id='2dy_axis_dropdown',component_property='value'),
    State(component_id='plot_dropdown',component_property='value'),State(component_id='size_dd',component_property='value'),State(component_id='color_dd',component_property='value')]
)
def final_plot(n,dimensions,xcol,ycol,plot_type,sizecol,colorcol):
	dim=''
	xc=''
	yc=''
	plt=''
	szc=''
	cc=''
	global df
	if n>0:
		if isinstance(dimensions,str):
			dim=dimensions
		else:
			dim=dimensions[len(dimensions)-1]

		if isinstance(xcol,str):
			xc=xcol
		else:
			xc=xcol[len(xcol)-1]

		if isinstance(ycol,str):
			yc=ycol
		else:
			yc=ycol[len(ycol)-1]

		if isinstance(plot_type,str):
			plt=plot_type
		else:
			plt=plot_type[len(plot_type)-1]

		if isinstance(sizecol,str):
			szc=sizecol
		else:
			if sizecol is not None:
				if len(sizecol)>0:
					szc=sizecol[len(sizecol)-1]
				else:
					szc=None


		if isinstance(colorcol,str):
			cc=colorcol
		else:
			if colorcol is not None:
				if len(colorcol)>0:
					cc=colorcol[len(colorcol)-1]

				else:
					cc=None
			else:
				cc=None

			
		

		if dim is None or xc is None or yc is None or plt is None:
			return []
		else:
			if plt == 'scatter':
				if szc is not None and cc is not None:
					if szc in df.columns:
						fig = px.scatter(df, x=xc, y=yc, color=cc,size=szc)
						return [dcc.Graph(id='example-graph2',figure=fig)]
					else:
						fig = px.scatter(df, x=xc, y=yc, color=cc)
						return [dcc.Graph(id='example-graph2',figure=fig)]	



				elif szc is None and cc is not None:
					fig = px.scatter(df, x=xc, y=yc, color=cc)
					return [dcc.Graph(id='example-graph2',figure=fig)]					

				elif szc is not None and cc is None:
					if szc in df.columns:
						fig = px.scatter(df, x=xc, y=yc, color=cc,size=szc)
						return [dcc.Graph(id='example-graph2',figure=fig)]
					else:
						fig = px.scatter(df, x=xc, y=yc)
						return [dcc.Graph(id='example-graph2',figure=fig)]

				else:
					fig = px.scatter(df, x=xc, y=yc)
					return [dcc.Graph(id='example-graph2',figure=fig)]


			elif plt == 'line':
				if cc is not None:
					fig = px.line(df, x=xc, y=yc, color=cc)
					return [dcc.Graph(id='example-graph2',figure=fig)]

				else:
					fig = px.line(df, x=xc, y=yc)
					return [dcc.Graph(id='example-graph2',figure=fig)]


			elif plt == 'bub':
				if szc is not None and cc is not None:
					if szc in df.columns:
						fig = px.scatter(df, x=xc, y=yc, color=cc,size=szc)
						return [dcc.Graph(id='example-graph2',figure=fig)]
					else:
						fig = px.scatter(df, x=xc, y=yc, color=cc)
						return [dcc.Graph(id='example-graph2',figure=fig)]	



				elif szc is None and cc is not None:
					fig = px.scatter(df, x=xc, y=yc, color=cc)
					return [dcc.Graph(id='example-graph2',figure=fig)]					

				elif szc is not None and cc is None:
					if szc in df.columns:
						fig = px.scatter(df, x=xc, y=yc, color=cc,size=szc)
						return [dcc.Graph(id='example-graph2',figure=fig)]
					else:
						fig = px.scatter(df, x=xc, y=yc)
						return [dcc.Graph(id='example-graph2',figure=fig)]

				else:
					fig = px.scatter(df, x=xc, y=yc)
					return [dcc.Graph(id='example-graph2',figure=fig)]

			elif plt == 'mbars':
				x_unique_list=df[xc].unique()
				y_unique_list=df[yc].unique()
				data=[]
				for y_item in y_unique_list:
					list_for_each_value_of_x=[]
					for x_item in x_unique_list:
						new_df=df[(df[xc] == x_item) & (df[yc] == y_item)]
						cnt=new_df.shape[0]
						list_for_each_value_of_x.append(cnt)
					data.append(go.Bar(name=str(y_item),x=x_unique_list,y=list_for_each_value_of_x))
				fig = go.Figure(data=data)
				fig.update_layout(barmode='group')
				return [dcc.Graph(id='example-graph2',figure=fig)]


			elif plt == 'stack':
				x_unique_list=df[xc].unique()
				y_unique_list=df[yc].unique()
				data=[]
				for y_item in y_unique_list:
					list_for_each_value_of_x=[]
					for x_item in x_unique_list:
						new_df=df[(df[xc] == x_item) & (df[yc] == y_item)]
						cnt=new_df.shape[0]
						list_for_each_value_of_x.append(cnt)
					data.append(go.Bar(name=str(y_item),x=x_unique_list,y=list_for_each_value_of_x))
				fig = go.Figure(data=data)
				fig.update_layout(barmode='stack')
				return [dcc.Graph(id='example-graph2',figure=fig)]


			elif plt == 'bx':
				if cc is None:
					fig = px.box(df, x=xc, y=yc)
					return [dcc.Graph(id='example-graph2',figure=fig)]

				else:
					fig = px.box(df, x=xc, y=yc,color=cc)
					return [dcc.Graph(id='example-graph2',figure=fig)]
					


			else:
				if cc is None:
					fig = px.violin(df, x=xc, y=yc)
					return [dcc.Graph(id='example-graph2',figure=fig)]

				else:
					fig = px.violin(df, x=xc, y=yc,color=cc)
					return [dcc.Graph(id='example-graph2',figure=fig)]


	else:
		return []


#Classification
@app.callback(Output('Display_card_content4','children'),[Input('check_accuracy_dd','value')],
			[State('app_categories_dropdown','value'),State('type_radiobutton','value'),
			State('app_usertype_dropdown','value'),State('app_size','value'),State('app_price','value')])
def classalgo(algo,category,typee,users,sizee,pricee):
	global df_apps
	if category is not None and typee is not None and users is not None and algo is not None:
		df_apps = pd.read_csv("D:/RuparelMSc/kirti/googleplaystore.csv")
		a = df_apps.loc[df_apps["Category"] == "1.9"]
		#df_apps = df_apps.drop(int(a.index.values),axis=0)
		#df_apps = df_apps.drop(df_apps[df_apps['Rating'].isnull()].index, axis=0)
		df_apps.dtypes
		df_apps["Type"] = (df_apps["Type"] == "Paid").astype(int)
		
		popApps = df_apps.copy()
		popApps = popApps.drop_duplicates()
		popApps["Installs"] = popApps["Installs"].str.replace("+","") 
		popApps["Installs"] = popApps["Installs"].str.replace(",","")
		popApps["Installs"] = popApps["Installs"].astype("int64")
		popApps["Price"] = popApps["Price"].str.replace("$","")
		popApps["Price"] = popApps["Price"].astype("float64")
		popApps["Size"] = popApps["Size"].str.replace("Varies with device","0")
		popApps["Size"] = (popApps["Size"].replace(r'[kM]+$', '', regex=True).astype(float) *\
				popApps["Size"].str.extract(r'[\d\.]+([kM]+)', expand=False).fillna(1).replace(['k','M'], [10**3, 10**6]).astype(int))
		popApps["Reviews"] = popApps["Reviews"].astype("int64")
		popApps = popApps.sort_values(by="Installs",ascending=False)
		popApps.reset_index(inplace=True)
		popApps.drop(["index"],axis=1,inplace=True)
		popApps.loc[:40,['App','Installs','Content Rating']]
		popAppsCopy = popApps.copy()
		label_encoder = preprocessing.LabelEncoder()
		popAppsCopy['Category']= label_encoder.fit_transform(popAppsCopy['Category'])
		popAppsCopy['Content Rating']= label_encoder.fit_transform(popAppsCopy['Content Rating'])
		popAppsCopy['Genres']= label_encoder.fit_transform(popAppsCopy['Genres'])
		popAppsCopy = popAppsCopy.drop(["App","Last Updated","Current Ver","Android Ver"],axis=1)
		countPop = popAppsCopy[popAppsCopy["Installs"] > 100000].count()
		popAppsCopy["Installs"] = (popAppsCopy["Installs"] > 100000)*1 #Installs Binarized
		testPop1 = popAppsCopy[popAppsCopy["Installs"] == 1].sample(1010,random_state=0)
		popAppsCopy = popAppsCopy.drop(testPop1.index)
		testPop0 = popAppsCopy[popAppsCopy["Installs"] == 0].sample(766,random_state=0)
		popAppsCopy = popAppsCopy.drop(testPop0.index)
		testDf = testPop1.append(testPop0)
		trainDf = popAppsCopy
		testDf = testDf.sample(frac=1,random_state=0).reset_index(drop=True)
		trainDf = trainDf.sample(frac=1,random_state=0).reset_index(drop=True)
		y_train = trainDf.pop("Installs")
		X_train = trainDf.copy()
		y_test = testDf.pop("Installs")
		X_test = testDf.copy()
		
		X_train = X_train.drop(['Reviews', 'Rating','Genres'], axis=1)
		X_test = X_test.drop(['Reviews', 'Rating','Genres'], axis=1)
		
		
		
		category1=category
		
		typee1=typee
		users1=users
		size1=sizee
		price1=pricee
		
		data1 = [[category1,sizee,typee1,price1,users1]]
		dfff = pd.DataFrame(data1,columns = ['Category','Size','Type','Price','Content Rating'])
		dfff.iloc[:,0] = label_encoder.fit_transform(dfff.iloc[:,0])
		#dfff.iloc[:,2] = label_encoder.fit_transform(dfff.iloc[:,2])
		dfff.iloc[:,4] = label_encoder.fit_transform(dfff.iloc[:,4])
		print(dfff)
		#scaler = StandardScaler()
		pred=np.array(dfff.iloc[:,:])
		print(pred)
		#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
		if algo== 'rf':
			popularity_classifier = RandomForestClassifier()
			popularity_classifier.fit(X_train, y_train)
			predictions = popularity_classifier.predict(X_test)
			ac=accuracy_score(y_true = y_test, y_pred = predictions)
			pr = popularity_classifier.predict(pred)
			ac = ac * 100
			return [html.Div([
				html.P('Accuracy of Random Forest classifier is '+str(ac)),
				html.P('Successful : '+str(pr[0]))
				])]
		elif algo== 'dt':
			popularity_classifier = DecisionTreeClassifier(max_leaf_nodes=29, random_state=0)
			popularity_classifier.fit(X_train, y_train)
			predictions = popularity_classifier.predict(X_test)
			ac=accuracy_score(y_true = y_test, y_pred = predictions)
			pr = popularity_classifier.predict(pred)
			ac = ac * 100
			
			#output=clf.predict(pred)
			return [html.Div([
				html.P('Accuracy of Decision Tree Classifier is '+str(ac)),
				html.P('Successful: '+str(pr[0]))
				])]
		else:
			return html.P('Select algorithm')

			
#Clustering Result function
@app.callback(Output('cluster_output','children'),[Input('showcluster','n_clicks_timestamp')],
			[State('app_categories_dropdown_cluster','value'),State('type_radiobutton_cluster','value'),
			State('app_usertype_dropdown_cluster','value'),State('app_size_cluster','value'),State('app_price_cluster','value'),State('app_genres_dropdown_cluster','value')])			
def perform_cluster(n,cat,typee,contentrating,sizee,price,genre):
    
    if n > 0:
        df_apps = pd.read_csv("D:/RuparelMSc/kirti/googleplaystore.csv")
        #a = df_apps.loc[df_apps["Category"] == "1.9"]
        #df_apps = df_apps.drop(int(a.index.values),axis=0)
        df_apps = df_apps.drop(df_apps[df_apps['Rating'].isnull()].index, axis=0)
        df_apps.dtypes
        df_apps["Type"] = (df_apps["Type"] == "Paid").astype(int)
		
        popApps = df_apps.copy()
        popApps = popApps.drop_duplicates()
        popApps["Installs"] = popApps["Installs"].str.replace("+","",regex=True) 
        popApps["Installs"] = popApps["Installs"].str.replace(",","",regex=True)
        popApps["Installs"] = popApps["Installs"].astype("int64")
        popApps["Price"] = popApps["Price"].str.replace("$","",regex=True)
        popApps["Price"] = popApps["Price"].astype("float64")
        popApps["Size"] = popApps["Size"].str.replace("Varies with device","0",regex="True")
        popApps["Size"] = (popApps["Size"].replace(r'[kM]+$', '', regex=True).astype(float) *\
                popApps["Size"].str.extract(r'[\d\.]+([kM]+)', expand=False).fillna(1).replace(['k','M'], [10**3, 10**6]).astype(int))
        popApps["Reviews"] = popApps["Reviews"].astype("int64")
        popApps = popApps.sort_values(by="Installs",ascending=False)
        popApps.reset_index(inplace=True)
        popApps.drop(["index"],axis=1,inplace=True)
        popApps.loc[:40,['App','Installs','Content Rating']]
        popAppsCopy = popApps.copy()
        label_encoder_category = preprocessing.LabelEncoder()
        label_encoder_cr = preprocessing.LabelEncoder()
        label_encoder_genres = preprocessing.LabelEncoder()
        popAppsCopy['Category']= label_encoder_category.fit_transform(popAppsCopy['Category'])
        popAppsCopy['Content Rating']= label_encoder_cr.fit_transform(popAppsCopy['Content Rating'])
        popAppsCopy['Genres']= label_encoder_genres.fit_transform(popAppsCopy['Genres'])
        popAppsCopy = popAppsCopy.drop(["App","Last Updated","Current Ver","Android Ver"],axis=1)
        countPop = popAppsCopy[popAppsCopy["Installs"] > 100000].count()
        popAppsCopy["Installs"] = (popAppsCopy["Installs"] > 100000)*1 #Installs Binarized
        testPop1 = popAppsCopy[popAppsCopy["Installs"] == 1].sample(1010,random_state=0)
        popAppsCopy = popAppsCopy.drop(testPop1.index)
        testPop0 = popAppsCopy[popAppsCopy["Installs"] == 0].sample(766,random_state=0)
        popAppsCopy = popAppsCopy.drop(testPop0.index)
        testDf = testPop1.append(testPop0)
        trainDf = popAppsCopy
        testDf = testDf.sample(frac=1,random_state=0).reset_index(drop=True)
        trainDf = trainDf.sample(frac=1,random_state=0).reset_index(drop=True)
        y_train = trainDf.pop("Installs")
        X_train = trainDf.copy()
        y_test = testDf.pop("Installs")
        X_test = testDf.copy()
		
        X_train = X_train.drop(['Reviews', 'Rating'], axis=1)
        X_test = X_test.drop(['Reviews', 'Rating',], axis=1)
		
        cat1 = cat
        price1 = price
        cr = contentrating
        type1 = typee
        size1 = sizee
        genre1 = genre
		
        data1 = [[cat1,size1,type1,price1,cr,genre1]]
        le = LabelEncoder()
        dfff = pd.DataFrame(data1,columns = ['Category','Size','Type','Price','Content Rating','Genres'])
		
        dfff.iloc[:,0] = label_encoder_category.transform(dfff.iloc[:,0])
        dfff.iloc[:,4] = label_encoder_cr.transform(dfff.iloc[:,4])
        dfff.iloc[:,5] = label_encoder_genres.transform(dfff.iloc[:,5])
        #print(cat)
        #print('Category custom')
        #print(dfff.iloc[:,:])
		#dfff.iloc[:,1] = le.fit_transform(dfff.iloc[:,1])
		#dfff.iloc[:,2] = le.fit_transform(dfff.iloc[:,2])
		#dfff.iloc[:,3] = le.fit_transform(dfff.iloc[:,3])
        #dfff.iloc[:,4] = le.fit_transform(dfff.iloc[:,4])
		
        sc=StandardScaler()
        X=sc.fit_transform(np.array(X_train.iloc[:,:],dtype=int))
        cust_input=sc.transform(np.array(dfff.iloc[:,:],dtype=int))
        #print(cust_input)
        kmeans = KMeans(n_clusters = 5, init = 'k-means++', random_state = 42)
        #print(X)
        y_kmeans = kmeans.fit_predict(X)
        op=kmeans.predict(cust_input)
        #print(op)
        list_of_index = []
        #print(y_kmeans)
        for i in range(0,len(y_kmeans)):
            if y_kmeans[i] == op[0]:
                list_of_index.append(i)
        #print(list_of_index)
        l = len(list_of_index)
        apps_list = list(df_apps.iloc[list_of_index,0])
        print("----------------------In clustering----------------------")
        print("no of apps ",len(apps_list))
        if len(apps_list) == 0:
            apps_list.append("No similer App found.")
        p_tag_list = []
        tplist=[]
        html.P(str(apps_list[1]))
        for i in range(0,len(apps_list)):
                #print(apps_list[i])
                p_tag_list.append(html.P(str(apps_list[i])))
                tplist.append(str(apps_list[i]))
                if i > 10:
                        break
                #html.Div(html.P(str(apps_list[i])))
        print(p_tag_list)
        return [html.Div(p_tag_list)]
        
      
		
#Filling Genres in Cluster 
@app.callback(Output('app_genres_dropdown_cluster','options'),[Input('app_categories_dropdown_cluster','value')])
def update_cluster_genre_dd(text):
	genres_list = []
	df_apps = pd.read_csv("D:/RuparelMSc/kirti/googleplaystore.csv")
	df_apps = df_apps.drop(df_apps[df_apps['Rating'].isnull()].index, axis=0)
	text = str(text)
	new_df = df_apps[df_apps["Category"]==text]
	temp_list = new_df["Genres"].unique()
	for i in range(0,len(temp_list)):
		genres_list.append({'label':temp_list[i],'value':temp_list[i]})
	return genres_list
#Filling Genres in Cluster	
@app.callback(Output('genre_classification','options'),[Input('app_categories_dropdown','value')])
def update_cluster_genre_dd(text):
	genres_list = []
	df_apps = pd.read_csv("D:/RuparelMSc/kirti/googleplaystore.csv")
	df_apps = df_apps.drop(df_apps[df_apps['Rating'].isnull()].index, axis=0)
	text = str(text)
	new_df = df_apps[df_apps["Category"]==text]
	temp_list = new_df["Genres"].unique()
	for i in range(0,len(temp_list)):
		genres_list.append({'label':temp_list[i],'value':temp_list[i]})
	return genres_list
	
#Choose which item is selected from listview
@app.callback(
    Output(component_id='changecontent', component_property='children'),
    [Input(component_id='l1', component_property='n_clicks_timestamp'),Input(component_id='l2',component_property='n_clicks_timestamp'),Input(component_id='l3',component_property='n_clicks_timestamp'),Input('l4','n_clicks_timestamp')]
)
def update_output_div(n,n1,n2,n3):
	if int(n) > int(n1) and int(n) > int(n2) and int(n) > int(n3):
		print('List 1 is selected')
		global l_o_c
		global l_o_n
		global l_o_d
		l=[]
		if l_o_c is not None:
			l=[parse_contents(l_o_c,l_o_n,l_o_d)]
		return card_content2
	elif int(n1) > int(n) and int(n1) > int(n2) and int(n1) > int(n3):
		return card_contentvg
	elif int(n2) > int(n) and  int(n2) > int(n1) and int(n2) > int(n3):
		return card_content4
	elif int(n3) > int(n) and  int(n3) > int(n1) and int(n3) > int(n2):
		return card_cluster
	else:
		return card_content

#display CSV file detail
@app.callback(Output('dataset_info', 'children'),
              [Input('upload_file', 'contents')],
              [State('upload_file', 'filename'),
               State('upload_file', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
	global pehla_load
	if pehla_load == False:
		if list_of_contents is None:
			list_of_contents=l_o_c
			list_of_names=l_o_n
			print(l_o_n)
			list_of_dates=l_o_d
		else:
			if list_of_contents != l_o_c:
				print('new content'+list_of_names)
				l_o_c=list_of_contents
				l_o_n=list_of_names
				l_o_d=list_of_dates
			else:
				list_of_contents=l_o_c
				list_of_names=l_o_n
				print(l_o_n)
				list_of_dates=l_o_d
	else:
		l_o_c=list_of_contents
		l_o_n=list_of_names
		l_o_d=list_of_dates
	if list_of_contents is not None:
		children = [parse_contents(list_of_contents, list_of_names, list_of_dates)]
		return children
	
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    list_of_columns=[]
    name_of_columns=[]
    decoded = base64.b64decode(content_string)
    global df
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
			
            if df['Type'].isnull().any():
                df = df.dropna()
            print(df.head)
            s=df.shape;
            name_of_columns=list(df.columns.values)
            number_of_columns=s[1]
            for i in range(0,number_of_columns):
            	list_of_columns.append({'label' : name_of_columns[i],'value' : name_of_columns[i]})

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
			
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    sh=df.shape
    print(df.dtypes)

    return html.Div([
    	html.P(),
        html.H5('Name of file uploaded: '+filename),
        html.H5('Number of Rows: '+str(sh[0])),
        html.H5('Number of Columns: '+str(sh[1])),
        html.Div([
        		dcc.Dropdown(
					    options=list_of_columns,
					    value=list_of_columns[0]['value'],
					    multi = True,
					    id = 'columns_dropdown'
							)],className = "dash-bootstrap"),					    
        html.P(),
        dbc.Row([
        		dbc.Col([html.Div(id = 'column_details')],width=6),
        		dbc.Col([html.Div([dash_table.DataTable(
			            id = 'single_column_data',
			            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
			    		style_cell={
			        			'backgroundColor': '#232323',
			        			'color': 'white',
								'textAlign':'left'
			    					},),
					        ],className = "mycust2",style={
					   'height': 200},
					   )],width=6),
        		]),
        html.P(),
        html.H5("Data Distribution for selected column"),
        html.P(),
        html.Div([
        		dcc.Dropdown(
					    options=[],
					    value='',
					    multi = True,
					    id = 'graphtype_dropdown'
							)],className = "dash-bootstrap"),
        html.P(),
        html.Div([
            html.Center([dcc.Graph
            (
        id='example-graph',
        figure={}
    		)])]
    		),
    		html.P(),
    		html.H4('Data'),
    		html.P(),
        html.Div([dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    		style_cell={
        			'backgroundColor': '#232323',
        			'color': 'white',
					'textAlign' : 'left'
    					},
        ),
        ],className="mycust",style={
   'height': 500},
   )
         
    ],
   )

#display column details 
@app.callback(
    [Output('column_details', 'children'),Output('single_column_data','data'),Output('single_column_data','columns'),Output('example-graph','figure')],
    [Input('columns_dropdown', 'value'),Input('graphtype_dropdown', 'value')])
def update_output(value,value1):
	global df
	LAYOUT = {'height': 200}

	if isinstance(value,str):#Accept first selected item from the column drop down
		selected_column=df[value]
		col_dict=[{'name':value,'id':value}]
		col_stats=[html.P('Column name: '+value),html.P('Column datatype: '+str(df[value].dtype)),html.P('Contains missing values: '+str(df[value].isnull().any()))]
		data_list=[]
		if (df[value].dtype == np.float64 or df[value].dtype == np.int64):#for numeric column values
			col_stats.append(html.P('Minimum value: '+str(df[value].min())))
			col_stats.append(html.P('Maximum value: '+str(df[value].max())))
			col_stats.append(html.P('Mean: '+str(df[value].mean())))
			col_stats.append(html.P('Standard deviation: '+str(df[value].std())))
		else:#for String column values
			categories=""
			list_of_categories=df[value].unique()
			for z in range(0,len(df[value].unique())):
				if z == (len(df[value].unique())-1):
					categories=categories+list_of_categories[z]
				else:
					categories=categories+list_of_categories[z]+","

			col_stats.append(html.P('Possible values: '+categories))
				

#graph selected from dropdown menu
		for j in df[value]:
			data_list.append({value:j})
		if isinstance(value1,str):#only one is selected in dropdown
			if value1 == 'box':
				fig=px.box(df, y=value)
				fig.update_layout(width=500,height=500)
			elif value1 == 'hist':
				fig=px.histogram(df, x=value)
				fig.update_layout(width=500,height=500)
			elif value1 == 'pie':
				count_list=[]
				if (df[value].dtype == np.float64 or df[value].dtype == np.int64)== False:
					for i in list_of_categories:
						count_list.append((df[value] == i).sum())
					fig = go.Figure(data=[go.Pie(labels=list_of_categories, values=count_list)])
					fig.update_layout(width=500,height=500)
			elif value1 == 'donut':
				count_list=[]
				if (df[value].dtype == np.float64 or df[value].dtype == np.int64)== False:
					for i in list_of_categories:
						count_list.append((df[value] == i).sum())
					fig = go.Figure(data=[go.Pie(labels=list_of_categories, values=count_list,hole =.3)])
					fig.update_layout(width=500,height=500)
			else:
				fig=px.violin(df, y=value)
				fig.update_layout(width=500,height=500)
		else:#Accept last selected item from graph dropdown
			new_value1=value1[len(value1)-1]
			if new_value1 == 'box':
				fig=px.box(df, y=value)
				fig.update_layout(width=500,height=500)
			elif new_value1 == 'hist':
				fig=px.histogram(df, x=value)
				fig.update_layout(width=500,height=500)
			elif new_value1 == 'pie':
				count_list=[]
				if (df[value].dtype == np.float64 or df[value].dtype == np.int64)== False:
					for i in list_of_categories:
						count_list.append((df[value] == i).sum())
					fig = go.Figure(data=[go.Pie(labels=list_of_categories, values=count_list)])
					fig.update_layout(width=500,height=500)
			elif new_value1 == 'donut':
				count_list=[]
				if (df[value].dtype == np.float64 or df[value].dtype == np.int64)== False:
					for i in list_of_categories:
						count_list.append((df[value] == i).sum())
					fig = go.Figure(data=[go.Pie(labels=list_of_categories, values=count_list,hole = .3)])
					fig.update_layout(width=500,height=500)
			else:
				fig=px.violin(df, y=value)
				fig.update_layout(width=500,height=500)

	else:#accept last selected item from dropdown of the column name
		l=len(value)
		new_val=value[l-1]
		selected_column=df[new_val]
		col_stats=[html.P('Column name: '+new_val),html.P('Column datatype: '+str(df[new_val].dtype)),html.P('Contains missing values: '+str(df[new_val].isnull().any()))]
		col_dict=[{'name':new_val,'id':new_val}]

		if (df[new_val].dtype == np.float64 or df[new_val].dtype == np.int64):
			col_stats.append(html.P('Minimum value: '+str(df[new_val].min())))
			col_stats.append(html.P('Maximum value: '+str(df[new_val].max())))
			col_stats.append(html.P('Mean: '+str(df[new_val].mean())))
			col_stats.append(html.P('Standard deviation: '+str(df[new_val].std())))
		else:
			categories=""
			list_of_categories=df[new_val].unique()
			print(list_of_categories)
			for z in range(0,len(df[new_val].unique())):
				if z == (len(df[new_val].unique())-1):
					categories=categories+list_of_categories[z]
				else:
					categories=categories+list_of_categories[z]+","

			col_stats.append(html.P('Possible values: '+categories))

		data_list=[]
		for j in df[new_val]:
			data_list.append({new_val:j})

		if isinstance(value1,str):
			if value1 == 'box':
				fig=px.box(df, y=new_val)
				fig.update_layout(width=500,height=500)
			elif value1 == 'hist':
				fig=px.histogram(df, x=new_val)
				fig.update_layout(width=500,height=500)
			elif value1 == 'pie':
				count_list=[]
				if (df[new_val].dtype == np.float64 or df[new_val].dtype == np.int64)== False:
					for i in list_of_categories:
						count_list.append((df[new_val] == i).sum())
					fig = go.Figure(data=[go.Pie(labels=list_of_categories, values=count_list)])
					fig.update_layout(width=500,height=500)
			elif value1 == 'donut':
				count_list=[]
				if (df[new_val].dtype == np.float64 or df[new_val].dtype == np.int64) == False:
					for i in list_of_categories:
						count_list.append((df[new_val] == i).sum())
					fig = go.Figure(data=[go.Pie(labels=list_of_categories, values=count_list,hole = .3)])
					fig.update_layout(width=500,height=500)
			else:
				fig=px.violin(df, y=new_val)
				fig.update_layout(width=500,height=500)
		else:
			new_value1=value1[len(value1)-1]
			if new_value1 == 'box':
				fig=px.box(df, y=new_val)
				fig.update_layout(width=500,height=500)
			elif new_value1 == 'hist':
				fig=px.histogram(df, x=new_val)
				fig.update_layout(width=500,height=500)
			elif new_value1 == 'pie':
				count_list=[]
				if (df[new_val].dtype == np.float64 or df[new_val].dtype == np.int64)== False:
					for i in list_of_categories:
						count_list.append((df[new_val] == i).sum())
					fig = go.Figure(data=[go.Pie(labels=list_of_categories, values=count_list)])
					fig.update_layout(width=500,height=500)
			elif new_value1 == 'donut':
				count_list=[]
				if (df[new_val].dtype == np.float64 or df[new_val].dtype == np.int64)== False:
					for i in list_of_categories:
						count_list.append((df[new_val] == i).sum())
					fig = go.Figure(data=[go.Pie(labels=list_of_categories, values=count_list,hole=.3)])
					fig.update_layout(width=500,height=500)
			else:
				fig=px.violin(df, y=new_val)
				fig.update_layout(width=500,height=500)

	#return dash_dangerously_set_inner_html(col_det),data_list,col_dict,fig
	return col_stats,data_list,col_dict,fig

@app.callback(Output('graphtype_dropdown', 'options'),
              [Input('columns_dropdown', 'value')])
def update_graphtype(value):#Display  according to column type
	global df
	#print(df)
	op=[]
	if(isinstance(value,str)):#only one element is selected in dropdown
		if (df[value].dtype == np.float64 or df[value].dtype == np.int64):
			op.append({'label':'Box plot','value':'box'})
			op.append({'label':'Voilin plot','value':'voilin'})
			op.append({'label':'Histogram','value':'hist'})
			#print('numeric')
		else:
			op.append({'label':'Pie chart','value':'pie'})
			op.append({'label':'Donut chart','value':'donut'})
			op.append({'label':'Histogram','value':'hist'})
			#print('categorical')
	else:#n number of element is selected in dropdown then select its last element
		new_value1=value[len(value)-1]
		if (df[new_value1].dtype == np.float64 or df[new_value1].dtype == np.int64):
			op.append({'label':'Box plot','value':'box'})
			op.append({'label':'Voilin plot','value':'voilin'})
			op.append({'label':'Histogram','value':'hist'})
			#print('numeric')
		else:
			op.append({'label':'Pie chart','value':'pie'})
			op.append({'label':'Donut chart','value':'donut'})
			op.append({'label':'Histogram','value':'hist'})
	return op




if __name__ == "__main__":
    app.run_server()
