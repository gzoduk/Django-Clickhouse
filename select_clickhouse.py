from clickhouse_driver import Client

client = Client('localhost')

print(client.execute("""
SELECT  
    count(event_id) as count_event_id,
    user_id,
    user_name,
    formatDateTime(event_time, '%Y-%m-%d') as date
FROM task_manager
GROUP BY date, user_id, user_name
"""))