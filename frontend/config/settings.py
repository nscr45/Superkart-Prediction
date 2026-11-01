import datetime
import os

# The frontend Space calls the separately deployed Flask backend Space.
# Set BACKEND_URL in the frontend Space Variables panel.
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://sricharan451706-superkart-api-backend.hf.space",
).rstrip("/")

PAGE_CONFIG = {
    "page_title": "SuperKart Sales Predictor",
    "page_icon": None,
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

PERFORMANCE_THRESHOLDS = {
    "low": 1500,
    "high": 4000,
}

CURRENT_YEAR = datetime.datetime.now().year
VALIDATION_LIMITS = {
    "product_weight": {"min": 0.1, "max": 100},
    "product_mrp": {"min": 1, "max": 1000},
    "allocated_area": {"min": 0.001, "max": 0.200},
    "store_year": {"min": 1980, "max": CURRENT_YEAR},
}

REQUIRED_COLUMNS = [
    "Product_Id",
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_Type",
    "Product_MRP",
    "Store_Establishment_Year",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
]

PRODUCT_OPTIONS = {
    "sugar_content": ["", "Low Fat", "Regular", "No Sugar"],
    "product_types": [
        "",
        "Dairy",
        "Soft Drinks",
        "Meat",
        "Fruits and Vegetables",
        "Household",
        "Baking Goods",
        "Snack Foods",
        "Frozen Foods",
        "Breakfast",
        "Health and Hygiene",
        "Hard Drinks",
        "Canned",
        "Breads",
        "Starchy Foods",
        "Others",
        "Seafood",
    ],
    "store_sizes": ["", "Small", "Medium", "High"],
    "city_types": ["", "Tier 1", "Tier 2", "Tier 3"],
    "store_types": [
        "",
        "Supermarket Type1",
        "Supermarket Type2",
        "Supermarket Type3",
        "Grocery Store",
    ],
}
