import pandas as pd

def load_price_data(path: str = "two_years_up_to_yesterday.csv") -> pd.DataFrame:
    """
    Loads and sorts price data from a CSV file.
    """
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df.sort_index()


def compute_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes daily returns from price data.
    """
    return price_df.pct_change().dropna()
