import sqlite3
import pandas as pd
import json
#import pandahouse as ph
from clickhouse_driver import Client
#from datetime import datetime


#Read json for last event_id from Sqlite
last_event_id="0"
with open('//opt/collector/last_id.json','r', encoding='utf-8') as readfile:
    data = json.load(readfile)
    last_event_id = data['last_event_id']
if last_event_id != 'nan':
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    query = """SELECT
	ev.id as event_id, 
	ev.time as event_time, 
	ev.action_id, 
	ev.target_id_id as task_id, 
	ev.user_id_id as user_id,
	us.join_date as user_join_date,
	us.registration_date as user_egistration_date,
	us.name as user_name,
	us.email as user_email,
	us.guest as user_guest,
	tas.task_name
	FROM task_manager_events as ev
	LEFT JOIN task_manager_users us 
	ON ev.user_id_id=us.id
	LEFT JOIN task_manager_tasks tas
	ON ev.target_id_id=tas.id
	where event_id>{0}
	ORDER BY ev.id DESC
	""".format(last_event_id)

    # Take data from sqlite and save as dataframe
    cursor.execute(query)
    df = pd.DataFrame(list(cursor.fetchall()),columns=[col[0] for col in cursor.description])
    conn.close()
    df['event_time'] =  pd.to_datetime(df['event_time'], format='%Y-%m-%d %H:%M:%S')
    df['user_join_date'] =  pd.to_datetime(df['user_join_date'],format='%Y-%m-%d')
    df['user_egistration_date'] =  pd.to_datetime(df['user_egistration_date'], format='%Y-%m-%d')
    df['action_id'] = pd.to_numeric(df['action_id'])
    df['user_guest'] = pd.to_numeric(df['user_guest'])
    
    total_rows = df['event_id'].count()

    if total_rows > 0:
        # Save last event_id, for next query
        last_event_id = {'last_event_id': str(df['event_id'].max())}
        with open('//opt/collector/last_id.json','w', encoding='utf-8') as f:
            json.dump(last_event_id, f,ensure_ascii=False, indent=4)
        
        json_data = df.to_json(orient='records',date_unit='s')
        dlist = json.loads(json_data)
        
        #save data to clickhouse

        #connection = {'host':'http://127.0.0.1:8123/', 'database':'default'}
        #affected_rows = ph.to_clickhouse(df, table='task_manager', connection=connection, index=False)
        #pandahouse.read_clickhouse('SELECT * FROM task_manager', index_col='event_id', connection=connection)

        client = Client('localhost')
        client.execute('INSERT INTO task_manager VALUES', [row for row in dlist])
        print(client.execute('SELECT * FROM task_manager'))
        
