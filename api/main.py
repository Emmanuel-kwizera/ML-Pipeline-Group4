from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine
import seed

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/dataset/seed/")
def seed_dataset(db: Session = Depends(get_db)):
    # select all provinces, districts, households, egg productions
    provinces = db.query(models.Province).all()
    districts = db.query(models.District).all()
    households = db.query(models.Household).all()
    egg_productions = db.query(models.EggProduction).all()

    # seed provinces
    for province in seed.rwandan_provinces:
        # existing province from all provinces variable
        db_province = next((p for p in provinces if p.id == province["id"]), None)
        if db_province:
            db_province.province_name = province["province_name"]
        else:
            db_province = models.Province(**province)
            db.add(db_province)
    # Seed districts
    for district in seed.rwandan_districts:
        db_district = next((d for d in districts if d.id == district["id"]), None)
        if db_district:
            db_district.district_name = district["district_name"]
            db_district.province_id = district["province_id"]
        else:
            db_district = models.District(**district)
            db.add(db_district)
    dataset = seed.load_filtered_egg_production_data()
    # seed households
    for household in dataset['households']:
        db_household = next((h for h in households if h.id == household["id"]), None)
        if db_household:
            db_household.province_id = household["province_id"]
            db_household.district_id = household["district_id"]
            db_household.clust = household["clust"]
            db_household.owner = household["owner"]
            db_household.household_weight = household["household_weight"]
            db_household.yield_field = household["yield_field"]
            db_household.produced_eggs_last_six_months = household["produced_eggs_last_six_months"]
        else:
            db_household = models.Household(**household)
            db.add(db_household)

    # seed egg productions
    for egg_production in dataset['egg_productions']:
        db_egg_production = next((e for e in egg_productions if e.id == egg_production["id"]), None)
        if db_egg_production:
            db_egg_production.household_id = egg_production["household_id"]
            db_egg_production.month = egg_production["month"]
            db_egg_production.laying_hens = egg_production["laying_hens"]
            db_egg_production.eggs_produced = egg_production["eggs_produced"]
            db_egg_production.eggs_consumed = egg_production["eggs_consumed"]
            db_egg_production.eggs_sold = egg_production["eggs_sold"]
            db_egg_production.egg_unit_price = egg_production["egg_unit_price"]
            db_egg_production.hatched_eggs = egg_production["hatched_eggs"]
            db_egg_production.eggs_for_other_usages = egg_production["eggs_for_other_usages"]
        else:
            db_egg_production = models.EggProduction(**egg_production)
            db.add(db_egg_production)

    db.commit()
    return {
        "data_count": {
            "provinces": len(seed.rwandan_provinces),
            "districts": len(seed.rwandan_districts),
            "households": len(dataset['households']),
            "egg_productions": len(dataset['egg_productions']),
        },
        "dataset_seeded": True,
        "message": "Dataset seeded successfully"
    }
