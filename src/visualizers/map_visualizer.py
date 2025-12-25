import folium
from folium.plugins import MarkerCluster, HeatMap
import pandas as pd
import os

class MapVisualizer:
    """
    Generates a standalone HTML map report.
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_interactive_map(self, filename="market_heatmap.html"):
        """
        Creates an HTML file with Pins and Heatmap layers.
        """
        # 1. Filter for valid coordinates
        map_data = self.df.dropna(subset=['latitude', 'longitude'])
        
        if map_data.empty:
            print("⚠️ No coordinates found. Cannot generate map.")
            return

        # 2. Start the map at the average location
        start_coords = [map_data['latitude'].mean(), map_data['longitude'].mean()]
        m = folium.Map(location=start_coords, zoom_start=10, tiles="cartodbpositron")

        # 3. Add Heatmap Layer (Red = High Price)
        # We normalize price to make the heatmap meaningful
        heat_data = map_data[['latitude', 'longitude', 'price']].values.tolist()
        HeatMap(heat_data, radius=15).add_to(m)

        # 4. Add Marker Clusters (Pins)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in map_data.iterrows():
            # Create the popup text
            popup_html = f"""
            <b>{row['address']}</b><br>
            Price: ${row['price']:,.0f}<br>
            Beds: {row['bedrooms']}<br>
            City: {row['city']}
            """
            
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"${row['price']/1000:.0f}k",
                icon=folium.Icon(color="blue", icon="home", prefix="fa")
            ).add_to(marker_cluster)

        # 5. Save
        save_path = os.path.join(self.output_dir, filename)
        m.save(save_path)
        print(f"🗺️ Map Report saved: {save_path}")