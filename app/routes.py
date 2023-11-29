from flask import jsonify, request
from app.models import Event
from app import app, Session
from datetime import datetime
import random


events = [
    {
        "customer_id":  123, 
        "event_type":  
        "email_click", 
        "timestamp":  "2023-10-23T14:30:00", 
        "email_id":  1234, 
        "clicked_link":  "https://example.com/some-link"
    },
    {
        "customer_id":  456, 
        "event_type":  "email_open", 
        "timestamp":  "2023-10-24T11:30:00", 
        "email_id":  998
    },
    {
        "customer_id":  456, 
        "event_type":  "email_unsubscribe", 
        "timestamp":  "2023-10-24T11:30:25", 
        "email_id":  998
    },
    {
        "customer_id":  123, 
        "event_type":  "purchase", 
        "timestamp":  "25-10-2023T15:33:00", 
        "email_id":  1234, 
        "product_id": 357, 
        "amount":  49.99
    }
]

@app.route('/events', methods=['POST'])
def receive_event(): 
    
    """
    # With webhook
    response = requests.get('https://api.example.com/data')
    if response.status_code == 200:
        event_data = request.get_json()
    else:
        print('Failed to fetch data')

    # correct timestamp if needed
    if 'timestamp' in event_data:
        timestamp_parts = event_data['timestamp'].split('T')
        date_parts = timestamp_parts[0].split('-')
        
        if len(date_parts[0]) == 2:
            event_data['timestamp'] = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"

    
    new_event = Event(**event_data)
    session = Session()
    session.add(new_event)

    session.commit()
    session.close()
    """

    # Load the 4 records 
    
    for event_data in events:
        if 'timestamp' in event_data:
            timestamp_parts = event_data['timestamp'].split('T')
            date_parts = timestamp_parts[0].split('-')
            
            if len(date_parts[0]) == 2:
                event_data['timestamp'] = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"+timestamp_parts[1]

        new_event = Event(**event_data)
        session = Session()
        session.add(new_event)

        session.commit()
    session.close()

    return jsonify({'message': 'Event received and stored successfully'}), 201




@app.route('/events', methods=['GET'])
def get_events():
    customer_id = request.args.get('customer_id')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    session = Session()

    query = session.query(Event)
    
    if customer_id:
        query = query.filter(Event.customer_id == int(customer_id))
    
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            query = query.filter(
                (Event.timestamp >= start_date) & (Event.timestamp <= end_date)
            )
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    events = query.all()
    
    event_dicts = [event.__dict__ for event in events]
    
    for event in event_dicts:
        event.pop('_sa_instance_state', None)

    session.close()

    return jsonify(event_dicts), 200