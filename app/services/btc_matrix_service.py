# %%

import numpy as np
import pandas as pd
import plotly.express as px

class BTCMatrixService:
    # Class-level constants for default parameters
    DEFAULT_BTC_PARAMS = {
        'min_btc': 100_000,
        'max_btc': 2_000_000,
        'min_cagr': 0.025,
        'max_cagr': 0.375,
        'btc_steps': 20,
        'cagr_steps': 15,
        'year_to_buy_btc_by': 2029,
        'num_years_to_acquire': 5,
        'holding_years': 20,
        'current_price_for_year': 200_000,
    }

    def __init__(self):
        self._cached_matrix = None
        self._cached_params = None


    def _calc_reserve_value(self, num_coins: int, cagr: float, params: dict) -> float:
        """Internal method to calculate reserve value for a single BTC/CAGR combination"""

        cell = num_coins * (params['current_price_for_year'] * (1 + cagr) **24) / 1_000_000_000_000
        return cell

    def generate_reserve_matrix(self, **override_params) -> pd.DataFrame:
        """
        Generates a matrix of BTC reserve values in trillions USD.
        
        Returns:
            pd.DataFrame: Matrix with BTC amounts as index and CAGR rates as columns
        """
        # Combine default params with any overrides
        params = {**self.DEFAULT_BTC_PARAMS, **override_params}
        
        # Generate arrays for BTC amounts and CAGR rates
        btc_amounts = np.linspace(params['min_btc'], params['max_btc'], params['btc_steps'])
        cagr_rates = np.linspace(params['min_cagr'], params['max_cagr'], params['cagr_steps'])
        
        # Calculate matrix values
        matrix = np.zeros((len(btc_amounts), len(cagr_rates)))
        for i, btc in enumerate(btc_amounts):
            for j, cagr in enumerate(cagr_rates):
                matrix[i, j] = self._calc_reserve_value(btc, cagr, params)
        
        # Create formatted DataFrame
        df = pd.DataFrame(
            matrix,
            index=[f"{int(btc):,.0f}" for btc in btc_amounts],
            columns=[f"{cagr:.1%}" for cagr in cagr_rates]
        )
        
        df.index.name = f"BTC Acquired by {params['year_to_buy_btc_by']}"
        df.columns.name = f"BTC Price CAGR ({params['year_to_buy_btc_by']} - {params['year_to_buy_btc_by'] + params['holding_years']})"
        
        self._cached_matrix = df
        self._cached_params = params
        
        return df.round(2)

    def generate_pct_matrix(self, starting_debt: int, debt_cagr: float) -> pd.DataFrame:
        """
        Generates a matrix showing the percentage of debt covered by BTC reserves.
        
        Args:
            starting_debt (int): Initial debt amount in USD
            debt_cagr (float): Annual debt growth rate as decimal
            
        Returns:
            pd.DataFrame: Matrix showing percentage of debt covered by reserves
        """
        if self._cached_matrix is None:
            self._cached_matrix = self.generate_reserve_matrix()

        
        
        final_debt = starting_debt * (1 + debt_cagr) ** 24
        final_debt_trillions = final_debt / 1_000_000_000_000
        
        # Calculate percentage coverage
        pct_matrix = (self._cached_matrix / final_debt_trillions) * 100
        
        return pct_matrix.round(2)

