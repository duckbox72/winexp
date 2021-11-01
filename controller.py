import os
import requests

from flask import redirect, render_template, request, session
from functools import wraps


def format_date(date_month, date_year):
    
    """Format date as month, year."""
    months = ["Jan", "Fev", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Set", "Oct", "Nov", "Dec"]

    date_month = int(date_month)

    for month in range(len(months)):
        if month+1 == date_month:
            date_month = months[month]

    date = f"{date_month}, {date_year}"
        
    return date


def format_score(value):
    """Format value as USD."""
    return f"{value:,.2f}"


def format_vscore(value):
    """Format value as USD."""
    return f"{value:,.0f}"


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(wine, vintage):
    
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        headers = {'Authorization': f'Token {api_key}'}
        
        lim = 100
        limit = f"limit={lim}"
        ordering= "ordering=-score"
        
        if wine == "" and vintage != "":
            response = requests.get(f"https://api.globalwinescore.com/globalwinescores/latest?wine=&vintage={vintage}&{limit}&{ordering}", headers=headers)
    
        else:
            response = requests.get(f"https://api.globalwinescore.com/globalwinescores/latest?wine={wine}&{limit}&{ordering}", headers=headers)
    
    except:
        return None     

    # Parse response 
    try: 
        rows = []
        count = response.json()["count"]
        if count > lim:
            count = lim
        
        query = response.json()
        for i in range(count):
            rows.append({"rank": i+1, "wine": query['results'][i]['wine'],
                        "score": format_score(query['results'][i]['score']),
                        "vintage": query['results'][i]['vintage'],
                        "date": query['results'][i]['date'],
                        "regions": query['results'][i]['regions'],
                        "appellation": query['results'][i]['appellation'],
                        "country": query['results'][i]['country'],
                        "color": query['results'][i]['color'],
                        "confidence_index": query['results'][i]['confidence_index'],
                        "journalist_count": query['results'][i]['journalist_count'],
                        "lwin": query['results'][i]['lwin']})

        if not rows:
            winevint= None
        
        else:
            winevint = rows[0]
            if vintage != "" and wine != "":       
                for row in rows:
                    if vintage == row["vintage"]:
                        winevint = row

    except:    
        return None
    print(f"WINEVINT {winevint}")
    return rows, winevint  #response.json()