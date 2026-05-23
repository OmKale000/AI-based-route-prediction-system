import subprocess
from data.database import engine, Base
from scripts.generate_synthetic_data import generate_data
from scripts.train_models import trigger_retraining

def seed():
    print("Starting database seeding process...")
    # Initialize DB
    Base.metadata.create_all(bind=engine)
    
    # Generate mock data
    generate_data(num_drivers=10, num_locations=50, num_trips=1000)
    
    # Run initial training
    trigger_retraining()
    
    print("Seeding complete. The system is ready.")

if __name__ == "__main__":
    seed()
