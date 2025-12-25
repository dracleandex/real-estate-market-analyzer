import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class StatisticalVisualizer:
    """
    Creates static visualizations (PNGs) for reports.
    Uses Seaborn for high-quality styling.
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Set the visual style
        sns.set_theme(style="whitegrid")
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_price_distribution(self, filename="price_histogram.png"):
        """
        Saves a histogram of property prices.
        """
        plt.figure(figsize=(10, 6))
        
        # Create the histogram
        sns.histplot(data=self.df, x="price", hue="city", kde=True, element="step")
        
        plt.title("Price Distribution by City", fontsize=16)
        plt.xlabel("Price ($)", fontsize=12)
        plt.ylabel("Number of Properties", fontsize=12)
        
        # Save and Close
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=300) # dpi=300 makes it high resolution
        plt.close()
        print(f"🖼️ Saved: {path}")

    def plot_price_vs_sqft(self, filename="price_vs_sqft.png"):
        """
        Saves a scatter plot showing correlation between size and price.
        """
        plt.figure(figsize=(10, 6))
        
        sns.scatterplot(
            data=self.df, 
            x="square_feet", 
            y="price", 
            hue="city", 
            size="bedrooms",
            sizes=(50, 200),
            alpha=0.7
        )
        
        plt.title("Price vs. Square Footage", fontsize=16)
        plt.xlabel("Square Feet", fontsize=12)
        plt.ylabel("Price ($)", fontsize=12)
        
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=300)
        plt.close()
        print(f"🖼️ Saved: {path}")

    def plot_price_box_plot(self, filename="price_boxplot.png"):
        """
        Saves a box plot (great for seeing price ranges and outliers).
        """
        plt.figure(figsize=(10, 6))
        
        sns.boxplot(data=self.df, x="city", y="price", palette="Set2")
        
        plt.title("Price Ranges by City", fontsize=16)
        plt.xlabel("City", fontsize=12)
        plt.ylabel("Price ($)", fontsize=12)
        
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=300)
        plt.close()
        print(f"🖼️ Saved: {path}")