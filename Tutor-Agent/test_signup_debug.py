#!/usr/bin/env python3
"""
Debug script to test signup functionality
"""
import sys
import traceback
from tutor_agent.core.database import SessionLocal, init_db
from tutor_agent.core.security import get_password_hash
from tutor_agent.models.user import User
from datetime import datetime

# Initialize database
init_db()

# Create a test user
try:
    db = SessionLocal()

    # Check if user exists
    existing_user = db.query(User).filter(User.email == "debug@test.com").first()
    if existing_user:
        print(f"User already exists: {existing_user.email}")
        db.delete(existing_user)
        db.commit()
        print("Deleted existing user")

    # Hash password
    print("Hashing password...")
    hashed_password = get_password_hash("testpass123")
    print(f"Hashed password: {hashed_password[:50]}...")

    # Create new user
    print("Creating user...")
    new_user = User(
        email="debug@test.com",
        hashed_password=hashed_password,
        full_name="Debug Test",
        programming_experience="intermediate",
        ai_experience="basic",
        learning_style="visual",
        preferred_language="en",
        last_login=datetime.utcnow(),
    )

    print("Adding to database...")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(f"✅ SUCCESS! Created user ID: {new_user.id}, Email: {new_user.email}")

except Exception as e:
    print(f"❌ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()
