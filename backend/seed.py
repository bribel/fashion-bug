import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.models.database import SessionLocal
from app.models.models import Designer, Look

designers_data = [
    "Chanel",
    "Dior",
    "Gucci",
    "Prada",
    "Balenciaga",
]

looks_data = [
    # (designer_name, season, gender, collection_type, image_url)
    ("Chanel", "Fall 2024", "F", "Ready-to-Wear", "https://picsum.photos/seed/chanel1/400/600"),
    ("Chanel", "Fall 2024", "F", "Ready-to-Wear", "https://picsum.photos/seed/chanel2/400/600"),
    ("Chanel", "Fall 2024", "F", "Haute Couture", "https://picsum.photos/seed/chanel3/400/600"),
    ("Dior", "Spring 2024", "F", "Ready-to-Wear", "https://picsum.photos/seed/dior1/400/600"),
    ("Dior", "Spring 2024", "F", "Haute Couture", "https://picsum.photos/seed/dior2/400/600"),
    ("Dior", "Fall 2024", "F", "Ready-to-Wear", "https://picsum.photos/seed/dior3/400/600"),
    ("Gucci", "Spring 2024", "M", "Ready-to-Wear", "https://picsum.photos/seed/gucci1/400/600"),
    ("Gucci", "Spring 2024", "F", "Ready-to-Wear", "https://picsum.photos/seed/gucci2/400/600"),
    ("Gucci", "Fall 2024", "M", "Ready-to-Wear", "https://picsum.photos/seed/gucci3/400/600"),
    ("Prada", "Spring 2024", "F", "Ready-to-Wear", "https://picsum.photos/seed/prada1/400/600"),
    ("Prada", "Fall 2024", "F", "Ready-to-Wear", "https://picsum.photos/seed/prada2/400/600"),
    ("Prada", "Fall 2024", "M", "Ready-to-Wear", "https://picsum.photos/seed/prada3/400/600"),
    ("Balenciaga", "Spring 2024", "F", "Ready-to-Wear", "https://picsum.photos/seed/bal1/400/600"),
    ("Balenciaga", "Fall 2024", "F", "Ready-to-Wear", "https://picsum.photos/seed/bal2/400/600"),
    ("Balenciaga", "Fall 2024", "M", "Ready-to-Wear", "https://picsum.photos/seed/bal3/400/600"),
]

def seed():
    db = SessionLocal()
    try:
        for name in designers_data:
            if not db.query(Designer).filter_by(name=name).first():
                db.add(Designer(name=name))
        db.commit()

        for designer_name, season, gender, collection_type, image_url in looks_data:
            designer = db.query(Designer).filter_by(name=designer_name).first()
            if not db.query(Look).filter_by(image_url=image_url).first():
                db.add(Look(
                    designer_id=designer.id,
                    season=season,
                    gender=gender,
                    collection_type=collection_type,
                    image_url=image_url,
                ))
        db.commit()
        print(f"Seeded {len(designers_data)} designers and {len(looks_data)} looks.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
