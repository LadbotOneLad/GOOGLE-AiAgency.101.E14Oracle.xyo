import os
import json
from datetime import datetime
import numpy as np
import yfinance as yf
import sympy as sp
import pandas as pd
from fastapi import FastAPI

# Initialize FastAPI app engine matching Google's deployment specifications
app = FastAPI(title="XYO Market Oracle Engine")

class XYO_MARKET_ENGINE:
    def __init__(self):
        self.node_int = 402094010905358040954964079801471389996151223464
        self.entropy_seed = 16785678681128842408

    def execute_pipeline(self):
        x = sp.Symbol('x')
        poly = sp.Poly(self.node_int * x**2 + x + 1, x, domain='ZZ')
        lattice_coords = (1192, 2179)
        
        df = yf.download("AAPL", period="5d")
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        market_summary = df.tail().to_dict(orient="index")
        formatted_summary = {str(k): {str(col): float(val) for col, val in v.items()} for k, v in market_summary.items()}
        
        raw_close = df['Close'].iloc[-1]
        last_close = int(float(raw_close))

        markov_matrix = sp.Matrix([[2/25, 23/25], [23/25, 2/25]])
        state_vector = sp.Matrix([[1], [0]])
        next_state = markov_matrix * state_vector

        return {
            "timestamp": datetime.now().isoformat(),
            "node_integer": str(self.node_int),
            "lattice": lattice_coords,
            "entropy_seed": str(self.entropy_seed),
            "market_data_last_5_days": formatted_summary,
            "last_close_int": last_close,
            "markov_transition_result": next_state.tolist()
        }

@app.get("/")
def home_endpoint():
    """Root route for Google Cloud health checks"""
    return {"status": "ONLINE", "engine": "XYO ORACLE v1.0.0"}

@app.get("/run")
def run_calculations():
    """Trigger path for cloud pipelines"""
    engine = XYO_MARKET_ENGINE()
    return engine.execute_pipeline()

if __name__ == "__main__":
    import uvicorn
    # Google Cloud Run injects the target port variable dynamically
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
