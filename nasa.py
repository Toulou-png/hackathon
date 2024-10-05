import requests

# URL de l'API
url = "https://power.larc.nasa.gov/api/temporal/daily/point"

# Paramètres de la requête
params = {
    "start": "20210101",          # Date de début
    "end": "20240131",            # Date de fin
    "latitude": 48.8566,          # Latitude (exemple : Paris)
    "longitude": 2.3522,          # Longitude
    "parameters": "T2M,PRECTOT,RH2M,WS2M,ALLSKY_SFC_SW_DWN",  # Paramètres demandés
    "community": "AG",            # Secteur d'application (AG pour agriculture)
    "format": "CSV",              # Format de la réponse
}

# Effectuer la requête GET
response = requests.get(url, params=params)

# Vérifier que la requête a réussi (code 200)
if response.status_code == 200:
    # Récupérer le contenu CSV
    csv_data = response.text

    # Chemin complet pour sauvegarder le fichier
    file_path = "/Users/michelbertrandmamatoulou/Desktop/NASA-env/nasa_power_data.csv"

    # Sauvegarder le contenu dans un fichier CSV
    with open(file_path, "w") as file:
        file.write(csv_data)
    
    print(f"Données sauvegardées avec succès dans '{file_path}'")
else:
    print(f"Erreur lors de la requête : {response.status_code}")
