# main.py - DHIS2-style audit
import pandas as pd
# Pull from DHIS2 API (demo)
# from dhis2 import Api
# api = Api('https://play.dhis2.org/demo', 'admin', 'district')
# data = api.get('analytics', params={'dimension': 'dx:Penta3;ou:Peshawar'})

df = pd.DataFrame({
    'Facility': ['BHU Phandu','BHU Tehkal','RHC Chamkani','BHU Hayatabad','THQ Mathra','BHU University'],
    'Penta3_Coverage': [78,92,65,88,71,95],
    'Completeness': [85,98,70,95,80,100]
})
flagged = df[df['Penta3_Coverage'] < 80]
print("Facilities needing supportive supervision:")
print(flagged)