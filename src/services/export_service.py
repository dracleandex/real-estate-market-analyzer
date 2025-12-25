import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

class ExportService:
    """
    Handles exporting database data to CSV, Excel, JSON, and PDF.
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.output_dir = "reports"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Generate a timestamped filename prefix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename_base = f"real_estate_data_{timestamp}"

    def to_csv(self):
        path = os.path.join(self.output_dir, f"{self.filename_base}.csv")
        self.df.to_csv(path, index=False)
        return path

    def to_excel(self):
        path = os.path.join(self.output_dir, f"{self.filename_base}.xlsx")
        self.df.to_excel(path, index=False, sheet_name="Properties")
        return path

    def to_json(self):
        path = os.path.join(self.output_dir, f"{self.filename_base}.json")
        self.df.to_json(path, orient="records", indent=4)
        return path

    def to_pdf(self):
        """
        Generates a multi-page PDF summary report.
        """
        path = os.path.join(self.output_dir, f"{self.filename_base}.pdf")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # --- TITLE PAGE ---
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(190, 10, txt="Real Estate Market Report", ln=1, align="C")
        pdf.ln(10)
        
        # Summary Stats
        pdf.set_font("Arial", size=12)
        pdf.cell(190, 10, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
        pdf.cell(190, 10, txt=f"Total Properties: {len(self.df)}", ln=1)
        
        # Calculate average safely
        avg_price = self.df['price'].mean() if not self.df.empty else 0
        pdf.cell(190, 10, txt=f"Average Price: ${avg_price:,.2f}", ln=1)
        pdf.ln(10)
        
        # --- TABLE HEADER FUNCTION ---
        def print_header():
            pdf.set_font("Arial", style="B", size=10)
            pdf.set_fill_color(200, 220, 255) # Light blue header
            pdf.cell(100, 10, "Address", 1, 0, 'C', True)
            pdf.cell(50, 10, "City", 1, 0, 'C', True)
            pdf.cell(40, 10, "Price", 1, 1, 'C', True) # '1' at end means new line
            pdf.set_font("Arial", size=10)

        # Print first header
        print_header()
        
        # --- TABLE ROWS (LOOP ALL DATA) ---
        # 1. We removed .head(20) so it loops EVERYTHING
        for _, row in self.df.iterrows():
            
            # 2. Check if we are at the bottom of the page (approx 270mm)
            if pdf.get_y() > 270:
                pdf.add_page() # Add new page
                print_header() # Reprint header on new page
            
            # Prepare data
            address = str(row['address'])[:50] # Truncate really long addresses
            city = str(row['city'])[:25]
            price = f"${row['price']:,.0f}" if pd.notnull(row['price']) else "N/A"
            
            # Print Row
            pdf.cell(100, 10, address, 1)
            pdf.cell(50, 10, city, 1)
            pdf.cell(40, 10, price, 1, 1) # '1' means move to next line
            
        pdf.output(path)
        return path