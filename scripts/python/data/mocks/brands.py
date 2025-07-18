from faker import Faker
import random
from db.connection import get_connection
from utils import generate_timestamps

fake = Faker()
Faker.seed(42)
random.seed(42)

BRAND_NAMES = [
    # Electronics
    "ElectroMax", "TechNova", "GadgetPro", "Voltix", "NextGen Tech",
    # Home & Kitchen
    "HomeComfort", "KitchenKing", "CozyNest", "PureLiving", "ChefMate",
    # Fashion
    "Fashionista", "StyleHub", "TrendLine", "UrbanWear", "ChicCorner",
    # Health & Personal Care
    "HealthPlus", "PureCare", "WellnessWay", "GlowUp", "VitalEssence",
    # Sports & Outdoors
    "Sportify", "ActiveGear", "OutdoorX", "FitZone", "PeakPerformance",
    # Books
    "BookWorld", "PageTurner", "ReadMore", "LitHouse", "StoryTime",
    # Toys & Games
    "ToyLand", "FunZone", "PlayTime", "JoyBox", "GameWorld",
    # Office Supplies
    "OfficePro", "DeskMate", "WriteRight", "PaperTrail", "StationeryCo",
    # Automotive
    "AutoDrive", "MotorWorks", "CarZone", "RideSafe", "Speedster",
    # Beauty & Cosmetics
    "BeautyGlow", "CosmoCharm", "GlamourX", "PureBeauty", "LuxeLooks",
    # Pet Supplies
    "PetPal", "FurryFriends", "HappyPaws", "PetJoy", "AnimalCare",
    # Groceries
    "GroceryKing", "FreshFarm", "DailyHarvest", "MarketPlace", "GreenLeaf",
    # Baby Products
    "BabyJoy", "TinySteps", "LittleStars", "MommyCare", "SnuggleTime",
    # Tools & Hardware
    "ToolMaster", "BuildRight", "FixIt", "PowerTools", "HardHat",
    # Garden & Outdoor
    "GardenFresh", "OutdoorLiving", "GreenThumb", "NatureNest", "PlantPro",
    # Jewelry
    "JewelCraft", "SparkleTime", "GemGlow", "LuxuryLinks", "Ornate",
    # Musical Instruments
    "MusicWave", "SoundCraft", "TuneMaster", "RhythmHouse", "NoteWorks",
    # Footwear
    "FootFlex", "ShoeStyle", "StepUp", "WalkWell", "SoleMate",
    # Mobile Accessories
    "MobilePro", "CaseKing", "ChargeHub", "ScreenGuard", "SoundBoost",
    # Computer & Accessories
    "CompuTech", "ByteWorks", "TechGear", "NetConnect", "DataLine",
]


def generate_brands(names, inactive_ratio=0.05, delete_ratio=0.02):
    brands = []

    for name in names:
        created_at, updated_at = generate_timestamps(3)

        brands.append({
            "name": name,
            "is_active": True,   
            "is_delete": False,  
            "created_at": created_at,
            "updated_at": updated_at
        })

    return brands

def insert_brands(brands):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO brands (
            name, is_active, is_delete, created_at, updated_at
        )
        VALUES (%(name)s, %(is_active)s, %(is_delete)s, %(created_at)s, %(updated_at)s);
    """

    cursor.executemany(query, brands)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(brands)} brands inserted.")

if __name__ == "__main__":
    brands = generate_brands(BRAND_NAMES)
    insert_brands(brands)
