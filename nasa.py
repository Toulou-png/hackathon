import requests
import pandas as pd

# URL de l'API
url = "https://power.larc.nasa.gov/api/temporal/daily/point"

# Paramètres de la requête
params = {
    "start": "20200101",          # Date de début
    "end": "20240131",            # Date de fin
    "latitude": 48.8566,          # Latitude (exemple : Paris)
    "longitude": 2.3522,          # Longitude
    "parameters": "T2M,PRECTOT,RH2M,WS2M,ALLSKY_SFC_SW_DWN,TMAX,TMIN,PS,QV10M,SNODP,TS,U10M,U2M,U50M,V10M,V2M,PSC,WD10M,WD2M,WS10M",  # Paramètres corrigés (maximum 20)
    "community": "AG",            # Secteur d'application (AG pour agriculture)
    "format": "JSON",             # Changer le format à JSON
    "site-elevation": "35"        # Altitude du site (nécessaire pour le paramètre PSC)
}

# Effectuer la requête GET
response = requests.get(url, params=params)

# Vérifier que la requête a réussi (code 200)
if response.status_code == 200:
    # Récupérer le contenu JSON
    data = response.json()

    # Afficher une partie des données JSON pour débogage
    print("Données JSON reçues:\n", data)

    try:
        # Extraire les paramètres disponibles dans la réponse JSON
        parameters = data['properties']['parameter']

        # Afficher les clés pour voir les paramètres disponibles
        print("Available parameters in JSON:", parameters.keys())

        # Extraire les dates et créer une colonne de dates
        dates = pd.date_range(start=params['start'], end=params['end'], freq='D')

        # Créer un DataFrame à partir des paramètres disponibles et ajouter la colonne Date
        df = pd.DataFrame(parameters)
        df.insert(0, 'Date', dates)

        # Vérifier les colonnes dans le DataFrame
        available_columns = list(df.columns)
        print("Colonnes disponibles dans le DataFrame :", available_columns)

        # Afficher les premières lignes du DataFrame
        print(df.head())

        # Sauvegarder le DataFrame dans un fichier JSON
        data_file_path_json = "nasa_power_data_with_date.json"
        df.to_json(data_file_path_json, orient='records', lines=True)
        print(f"Données sauvegardées avec succès dans '{data_file_path_json}'")

        # Sauvegarder le DataFrame dans un fichier CSV
        data_file_path_csv = "nasa_power_data_with_date.csv"
        df.to_csv(data_file_path_csv, index=False)
        print(f"Données sauvegardées avec succès dans '{data_file_path_csv}'")

        # Création d'une description des paramètres (vous devez ajouter les descriptions manquantes)
        metadata = {
            'T2M': 'Temperature at 2 meters above ground level (°C)',
            'PRECTOT': 'Total precipitation (mm)',
            'RH2M': 'Relative humidity at 2 meters above ground level (%)',
            'WS2M': 'Wind speed at 2 meters above ground level (m/s)',
            'ALLSKY_SFC_SW_DWN': 'Downward solar radiation at the surface (W/m²)',
            'TMAX': 'Maximum Temperature (°C)',
            'TMIN': 'Minimum Temperature (°C)',
            'PS': 'Surface Pressure (Pa)',
            'QV10M': 'Specific Humidity at 10 meters',
            'SNODP': 'Snow Depth (cm)',
            'TS': 'Surface Skin Temperature (K)',
            'U10M': 'Zonal Wind Speed at 10 meters (m/s)',
            'U2M': 'Zonal Wind Speed at 2 meters (m/s)',
            'U50M': 'Zonal Wind Speed at 50 meters (m/s)',
            'V10M': 'Meridional Wind Speed at 10 meters (m/s)',
            'V2M': 'Meridional Wind Speed at 2 meters (m/s)',
            'PSC': 'Probability of Scattering Cloud (%)',
            'WD10M': 'Wind Direction at 10 meters (degrees)',
            'WD2M': 'Wind Direction at 2 meters (degrees)',
            'WS10M': 'Wind Speed at 10 meters (m/s)',
        }

        # Sauvegarder les métadonnées dans un fichier texte
        metadata_file_path = "nasa_power_metadata.txt"
        with open(metadata_file_path, 'w') as meta_file:
            meta_file.write("Descriptions des paramètres:\n\n")
            for param, description in metadata.items():
                meta_file.write(f"{param}: {description}\n")

        print(f"Descriptions des paramètres sauvegardées dans '{metadata_file_path}'")

    except KeyError as e:
        print(f"Erreur lors de l'extraction des données: {e}")
else:
    print(f"Erreur lors de la requête : {response.status_code}")
    print(response.text)  # Affiche le contenu de la réponse pour le débogage
