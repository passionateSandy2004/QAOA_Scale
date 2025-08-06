from .data_loader import load_price_data, compute_returns
from .qaoa_solver import make_qaoa_circuit, select_portfolio

__all__ = [
    "load_price_data",
    "compute_returns",
    "make_qaoa_circuit",
    "select_portfolio",
    "optimize_today"
]

def optimize_today(
    path: str,
    budget: int,
    depth: int,
    grid: int,
    shots: int
) -> list:
    """
    Loads data, computes returns, and selects optimal portfolio for the latest day.
    """
    price_df = load_price_data(path)
    returns = compute_returns(price_df)
    mu = returns.mean().fillna(0).values
    cov = returns.cov().fillna(0).values
    tickers = list(price_df.columns)
    picks = select_portfolio(mu, cov, tickers, budget, depth, grid, shots)
    return picks
