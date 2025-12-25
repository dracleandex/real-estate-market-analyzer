import os
import sys

# 1. Get the path to the project root (real-estate-analyzer)
# We go up two levels from 'config/settings.py'
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))

# 2. CRITICAL: Force Python to "stand" in the project root
# This ensures that "data/real_estate.db" always means the right thing
os.chdir(project_root)

# 3. Define the data folder relative to the root
DATA_DIR = os.path.join(project_root, "data")

# 4. Create the folder if it's missing
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
        print(f"📁 Created data directory at: {DATA_DIR}")
    except OSError as e:
        print(f"❌ Error creating directory: {e}")

# 5. THE FIX: Use a Simple Relative Path
# This avoids the confusing "C:/Users/..." path that Windows/OneDrive hates.
DATABASE_URL = "sqlite:///data/real_estate.db"

print(f"⚙️  Active Database URL: {DATABASE_URL}")