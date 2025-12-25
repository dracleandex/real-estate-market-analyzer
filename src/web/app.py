print("🚀 Initializing PropTech Server...")  # Debug print to confirm start
import sys
import os

# 1. HANDLE PATHS (Prevents ModuleNotFoundError)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
import traceback # For debugging

# 2. IMPORT YOUR ANALYZERS
from src.core.database import DatabaseManager
from src.analyzers.price_analyzer import PriceAnalyzer
from src.analyzers.comparative_analyzer import ComparativeAnalyzer
from src.analyzers.market_analyzer import MarketAnalyzer
from src.analyzers.neighborhood_analyzer import NeighborhoodAnalyzer
from src.services.export_service import ExportService

app = Flask(__name__)
app.secret_key = "proptech_secure_key_123" 

def get_full_market_data():
    """Connects to database and runs analyzers with Fallback Logic for 'Day 1' data."""
    try:
        db = DatabaseManager()
        p_analyzer = PriceAnalyzer(db)
        m_analyzer = MarketAnalyzer(db)
        n_analyzer = NeighborhoodAnalyzer(db)
        c_analyzer = ComparativeAnalyzer(db)
        
        df = p_analyzer.get_dataframe()
        if df.empty:
            return None
            
        # 1. Try getting the official health report
        health_report = m_analyzer.get_market_health().to_dict()
        
        # --- FIX: FALLBACK LOGIC ---
        # If Volatility is empty (no history yet), calculate "Price Spread" instead
        volatility = {}
        if not health_report.get('Price Volatility'):
            # Calculate Standard Deviation of prices per city (Current Spread)
            for city in df['city'].unique():
                city_data = df[df['city'] == city]
                if len(city_data) > 1:
                    std_dev = city_data['price'].std()
                    mean_price = city_data['price'].mean()
                    # A score from 0 to 100 representing how "varied" prices are
                    volatility[city] = float((std_dev / mean_price) * 100) if mean_price else 0
                else:
                    volatility[city] = 0.0
        else:
            volatility = {k: float(v) for k, v in health_report.get('Price Volatility', {}).items()}

        # If Inventory is empty, calculate simple counts
        inventory = {}
        if not health_report.get('Inventory Count'):
            counts = df['city'].value_counts()
            inventory = {k: int(v) for k, v in counts.items()}
        else:
            inventory = {k: int(v) for k, v in health_report.get('Inventory Count', {}).items()}
        # ---------------------------

        # 2. Neighborhoods
        n_df = n_analyzer.compare_zip_codes().head(10)
        neighborhoods = []
        for index, row in n_df.iterrows():
            neighborhoods.append({
                "zip_code": str(index), 
                "avg_price": float(row.get('Avg Price', row.get('Average Price', 0))),
                "listing_count": int(row.get('Count', row.get('Listing Count', 0)))
            })

        # 3. City Counts for Bar Chart
        city_counts_raw = df['city'].value_counts()
        city_labels = city_counts_raw.index.tolist()
        city_counts = [int(v) for v in city_counts_raw.values]

        # 4. Deals
        deals_df = c_analyzer.find_deals(discount_threshold=0.10)
        deals = []
        if not deals_df.empty:
            for _, row in deals_df.iterrows():
                deals.append({
                    "address": row.get('address', 'Unknown'),
                    "price": float(row.get('price', 0)),
                    "market_avg": float(row.get('avg_market_price', row.get('market_avg', 0))),
                    "discount": float(row.get('market_diff_pct', 0)),
                    "url": row.get('url', '#')
                })
        
        stats = {
            "total": int(len(df)),
            "avg_price": f"${df['price'].mean():,.0f}",
            "city_labels": city_labels,
            "city_counts": city_counts,
            "volatility": volatility,
            "inventory": inventory
        }
        
        return {
            "df": df.to_dict('records'),
            "deals": deals,
            "neighborhoods": neighborhoods,
            "stats": stats
        }
    except Exception as e:
        traceback.print_exc()
        print(f"🔥 Backend Error: {e}")
        return None

# --- ROUTES ---

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['user'] = 'admin'
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid Credentials. Hint: admin / admin123"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    data = get_full_market_data()
    if not data:
        return "<h1>⚠️ No Data Found</h1><p>Please run the scraper/pipeline first.</p>"
    
    # Filter map points (only listings with GPS)
    map_points = [p for p in data['df'] if p.get('latitude') and p.get('longitude')]
    
    return render_template(
        'dashboard.html', 
        stats=data['stats'], 
        properties=data['df'], 
        deals=data['deals'],
        neighborhoods=data['neighborhoods'],
        map_points=map_points
    )

@app.route('/export/<fmt>')
def export_data(fmt):
    if 'user' not in session:
        return redirect(url_for('login'))
        
    db = DatabaseManager()
    df = PriceAnalyzer(db).get_dataframe()
    exporter = ExportService(df)
    
    if fmt == 'csv':
        path = exporter.to_csv()
    elif fmt == 'pdf':
        path = exporter.to_pdf()
    else:
        return "Unsupported format", 400
        
    return send_file(os.path.abspath(path), as_attachment=True)

# --- IMPORTANT: THIS BLOCK STARTS THE SERVER ---
if __name__ == '__main__':
    print("🌐 Starting Flask Server on http://127.0.0.1:5000")
    app.run(debug=True)