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
import textwrap
#import dash_dangerously_set_inner_html

df=pd.DataFrame()

navbar = dbc.NavbarSimple(
    brand="Google Play Store Rating Review",
    brand_href="#",
    sticky="top",
    color = '#232323',
    dark=True,
)
card_content = [
    dbc.CardHeader("Project",style = { 'backgroundColor' : '#232323'},),
    dbc.CardBody(
        [
            html.H5("ANAYLSIS OF APP", className="card-title"),
            html.P(
                "Synopsis about project to be written here",
                className="card-text",
            ),
        ],style = { 'backgroundColor' : '#232323'},
    ),
]

card_content1 = [
    dbc.CardHeader("Anaylsis OF APP",style = { 'backgroundColor' : '#232323'},),
    dbc.CardBody(
        [
            dbc.ListGroup
            ([
        		dbc.ListGroupItem("Import Dataset",n_clicks=0,id = 'l1',style = { 'backgroundColor' : '#232323'},),
        		dbc.ListGroupItem("View Graphs",style = { 'backgroundColor' : '#232323'},),
        		dbc.ListGroupItem("Classification",style = { 'backgroundColor' : '#232323'},),
        		dbc.ListGroupItem("Clustering",style = { 'backgroundColor' : '#232323'},),
        		dbc.ListGroupItem("Association",style = { 'backgroundColor' : '#232323'},),
    		], flush = True,),
        ],style = { 'backgroundColor' : '#232323'},
    ),
]

card_content2 = [
    dbc.CardHeader("Dataset ",style = { 'backgroundColor' : '#232323'},),
    dbc.CardBody(
        [
        dbc.Row([
        		dbc.Col([dcc.Upload(id='upload_file',children=[dbc.Button("Import Csv/Xls file", id = "icsv",color="primary", className="mr-1")])]),]),
        dbc.Row(
            [
            dbc.Col(id = 'dataset_info'),
            ]
        ),
        ],style = { 'backgroundColor' : '#232323'},
    ),
]


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


@app.callback(
    Output(component_id='changecontent', component_property='children'),
    [Input(component_id='l1', component_property='n_clicks')]
)
def update_output_div(n):
	if n>0:
		return card_content2
	else:
		return card_content



@app.callback(Output('dataset_info', 'children'),
              [Input('upload_file', 'contents')],
              [State('upload_file', 'filename'),
               State('upload_file', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(list_of_contents, list_of_names, list_of_dates)]
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
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
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
        		dbc.Col([html.P(id = 'column_details')],width=6),
        		dbc.Col([html.Div([dash_table.DataTable(
			            id = 'single_column_data',
			            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
			    		style_cell={
			        			'backgroundColor': '#232323',
			        			'color': 'white'
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
					    options=[{'label': 'Box plot','value': 'box'},{'label': 'Voilin plot','value': 'voilin'},{'label': 'Histogram','value': 'hist'}],
					    value='box',
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
        html.Div([dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    		style_cell={
        			'backgroundColor': '#232323',
        			'color': 'white'
    					},
        ),
        ],className="mycust",style={
   'height': 500},
   )
        
    ],
   )

@app.callback(
    [Output('column_details', 'children'),Output('single_column_data','data'),Output('single_column_data','columns'),Output('example-graph','figure')],
    [Input('columns_dropdown', 'value'),Input('graphtype_dropdown', 'value')])
def update_output(value,value1):
	global df
	LAYOUT = {'height': 200}

	if isinstance(value,str):
		selected_column=df[value]
		col_dict=[{'name':value,'id':value}]
		data_list=[]
		for j in df[value]:
			data_list.append({value:j})
		col_det='Column name: '+value+'<br>Column datatype: '+str(df[value].dtype)+''
		if isinstance(value1,str):
			if value1 == 'box':
				fig=px.box(df, y=value)
				fig.update_layout(width=500,height=500)
			elif value1 == 'hist':
				fig=px.histogram(df, x=value)
				fig.update_layout(width=500,height=500)
			else:
				fig=px.violin(df, y=value)
				fig.update_layout(width=500,height=500)
		else:
			new_value1=value1[len(value1)-1]
			if new_value1 == 'box':
				fig=px.box(df, y=value)
				fig.update_layout(width=500,height=500)
			elif new_value1 == 'hist':
				fig=px.histogram(df, x=value)
				fig.update_layout(width=500,height=500)
			else:
				fig=px.violin(df, y=value)
				fig.update_layout(width=500,height=500)

	else:
		l=len(value)
		new_val=value[l-1]
		selected_column=df[new_val]
		col_dict=[{'name':new_val,'id':new_val}]
		data_list=[]
		for j in df[new_val]:
			data_list.append({new_val:j})
		col_det='Column name: '+new_val+'<br>Column datatype: '+str(df[new_val].dtype)+''		
		if isinstance(value1,str):
			if value1 == 'box':
				fig=px.box(df, y=new_val)
				fig.update_layout(width=500,height=500)
			elif value1 == 'hist':
				fig=px.histogram(df, x=new_val)
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
			else:
				fig=px.violin(df, y=new_val)
				fig.update_layout(width=500,height=500)

	#return dash_dangerously_set_inner_html(col_det),data_list,col_dict,fig
	return col_det,data_list,col_dict,fig


if __name__ == "__main__":
    app.run_server()