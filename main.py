import telebot
import requests


url = "https://hotels4.p.rapidapi.com/locations/v2/search"

querystring = {"query": "new york", "locale": "en_US", "currency": "USD"}

headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "bae1651a05msh66bdf614f9bc0e9p1a06dfjsn581c7e145db3"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
