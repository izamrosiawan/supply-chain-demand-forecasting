import os
import pandas as pd
import numpy as np

class SupplyChainForecaster:
    def __init__(self, data_path: str = None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_demand.csv')
            if not os.path.exists(data_path):
                data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_demand.csv')
        self.data_path = data_path

    def load_clean_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_path)
        col_demand = [c for c in df.columns if 'demand' in c.lower() or 'order' in c.lower()][0]
        col_date = [c for c in df.columns if 'date' in c.lower()][0]
        
        df['Order_Demand'] = pd.to_numeric(df[col_demand].astype(str).str.replace('(', '').str.replace(')', ''), errors='coerce')
        df['Date'] = pd.to_datetime(df[col_date], errors='coerce')
        return df[['Date', 'Order_Demand']].dropna()

    def aggregate_monthly_demand(self, df: pd.DataFrame = None) -> pd.DataFrame:
        if df is None:
            df = self.load_clean_data()
        monthly = df.set_index('Date').resample('ME')['Order_Demand'].sum().reset_index()
        return monthly
