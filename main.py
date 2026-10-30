# main.py
# KP EPI DHIS2 Data Quality Dashboard
# Author: Dr. Syed Rashid Mansoor, MBBS | Health Systems QA
# Portfolio for UNICEF Health Officer NO-1, Islamabad

import pandas as pd
import matplotlib.pyplot as plt

# CONFIG - change for real Pakistan DHIS2 instance
USE_REAL_DHIS2 = False  # Set True when you get Pakistan DHIS2 access
DHIS2_URL = "https://play.dhis2.org/demo"
USERNAME = "admin"
PASSWORD = "district"

def fetch_dhis2_data():
    """Fetch from real DHIS2 API - aligned with UNICEF HMIS JD"""
    try:
        from dhis2 import Api
        api = Api(DHIS2_URL, USERNAME, PASSWORD)
        # Example: Fetch immunization dataset
        # In real PK instance: dataElement = Penta3, orgUnit = Peshawar
        response = api.get('analytics', params={
            'dimension': 'dx:fbfJHSPpUQD',  # demo Penta equivalent
            'dimension': 'ou:LEVEL-3',
            'filter': 'pe:LAST_12_MONTHS'
        })
        print("Connected to DHIS2 demo")
        return response.json()
    except Exception as e:
        print(f"DHIS2 API not available, using mock Peshawar data: {e}")
        return None

def load_mock_peshawar_data():
    """Mock data simulating KP DHIS2 for 6 BHUs - Peshawar District"""
    data = {
        'orgUnit': ['BHU Phandu', 'BHU Tehkal', 'RHC Chamkani', 'BHU Hayatabad', 'THQ Mathra', 'BHU University'],
        'Penta3_Coverage': [78, 92, 65, 88, 71, 95],
        'Data_Completeness': [85, 98, 70, 95, 80, 100],
        'Timeliness': [3, 4, 2, 4, 3, 4],  # out of 4 reports
        'StockOut_Days': [5, 0, 12, 2, 8, 0]
    }
    df = pd.DataFrame(data)
    return df

def analyze_and_flag(df):
    """Core UNICEF task: Data quality audit + low coverage flagging"""
    # 1. UNICEF Target: 80% Penta-3
    df['Status'] = df['Penta3_Coverage'].apply(lambda x: 'BELOW TARGET - Needs Supportive Supervision' if x < 80 else 'MEETING TARGET')
    
    # 2. Data Quality Issue flag (Completeness < 90%)
    df['Data_Quality_Flag'] = df['Data_Completeness'].apply(lambda x: 'Poor Reporting' if x < 90 else 'Good')
    
    # 3. Priority score for UNICEF field visit
    df['Priority'] = (80 - df['Penta3_Coverage']).clip(lower=0) + (100 - df['Data_Completeness']) * 0.3
    
    flagged = df[df['Penta3_Coverage'] < 80].sort_values('Priority', ascending=False)
    
    print("\n=== KP EPI DASHBOARD - PESHAWAR ===")
    print(df.to_string(index=False))
    print("\n=== FACILITIES FLAGGED FOR UNICEF SUPPORTIVE SUPERVISION ===")
    print(flagged[['orgUnit','Penta3_Coverage','Data_Completeness','Status']].to_string(index=False))
    
    return df, flagged

def plot_dashboard(df):
    """Generate visuals for GitHub README"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))
    fig.suptitle('KP EPI Data Quality Dashboard - Peshawar (DHIS2) | UNICEF Portfolio', fontsize=13, weight='bold')
    
    colors = ['#d9534f' if x < 80 else '#5cb85c' for x in df['Penta3_Coverage']]
    ax1.barh(df['orgUnit'], df['Penta3_Coverage'], color=colors)
    ax1.axvline(80, color='red', linestyle='--', label='UNICEF 80% Target')
    ax1.set_xlabel('Penta-3 Coverage %')
    ax1.legend()
    ax1.set_title('Coverage vs Target')
    
    ax2.scatter(df['Data_Completeness'], df['Penta3_Coverage'], c='blue')
    for i, txt in enumerate(df['orgUnit']):
        ax2.annotate(txt, (df['Data_Completeness'][i], df['Penta3_Coverage'][i]), fontsize=8)
    ax2.set_xlabel('Data Completeness % (DHIS2 Quality)')
    ax2.set_ylabel('Penta-3 Coverage %')
    ax2.set_title('Data Quality vs Performance')
    
    plt.tight_layout()
    plt.savefig('dashboard.png', dpi=300)
    print("\nChart saved as dashboard.png - upload to GitHub")

if __name__ == "__main__":
    fetch_dhis2_data()  # try real connection
    df = load_mock_peshawar_data()
    df, flagged = analyze_and_flag(df)
    plot_dashboard(df)
    # Export for UNICEF reporting
    flagged.to_csv('flagged_facilities_for_supervision.csv', index=False)
    print("\nExported flagged_facilities_for_supervision.csv - ready for UNICEF field plan")