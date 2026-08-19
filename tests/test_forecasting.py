import pytest
import pandas as pd
import numpy as np
from src.forecaster import SupplyChainForecaster

@pytest.fixture
def forecaster():
    return SupplyChainForecaster()

def test_load_clean_data(forecaster):
    df = forecaster.load_clean_data()
    assert len(df) > 0
    assert 'Order_Demand' in df.columns
    assert np.issubdtype(df['Order_Demand'].dtype, np.number)
    assert np.issubdtype(df['Date'].dtype, np.datetime64)

def test_aggregate_monthly(forecaster):
    df = forecaster.load_clean_data()
    monthly = forecaster.aggregate_monthly_demand(df)
    assert len(monthly) > 0
    assert 'Order_Demand' in monthly.columns
    assert np.all(monthly['Order_Demand'] >= 0)
