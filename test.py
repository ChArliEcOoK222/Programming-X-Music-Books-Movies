import requests

code = "AQC43RByad6X8oL4sKEAkYeuSNxxjs9fIh5eHn441hhtExLqPmSVdKV-hJgIFkHf1ienEgAXODaQiox2cbChOpmwoftYN82BGlu91qE3zHqlbO2Q4ZDT5WCDKmKk5XqbiJuAFWt8RBIRF9d42GeyilPpWsYYl4NwSdgBzL8XvEQ1ffDmiuS2yZBPZ4LPRSMeGKpeZplS-a4XRXJ1p2luFOd52_q75dctHQc"

response = requests.post(
    "https://accounts.spotify.com/api/token",
    data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:3000/callback",
        "client_id": "e80250d0f61d458ab9daadaff344c420",
        "client_secret": "8c0a6f87de0041ccbc40f3329289d754",
    }
)

print(response.json())