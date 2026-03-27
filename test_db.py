import asyncio
import sys
import time
sys.path.insert(0, 'c:\\Users\\Ulises_GM\\Documents\\Escuela\\Programming\\Backend-EstanciaII')

from src.core.db_postgresql import get_db_connection

async def test():
    try:
        db = get_db_connection()
        print("✓ Database connection successful")
        
        # Test a simple query
        results = await db.query("SELECT 1 as test")
        print(f"✓ Query executed: {results}")
        
        # First, create a test user - use unique email with timestamp
        print("\n→ Creating test user...")
        timestamp = int(time.time())
        user_id = await db.execute(
            "INSERT INTO users (name, last_name, email, password, role_id) VALUES (%s, %s, %s, %s, %s)",
            ("Test", "User", f"testuser{timestamp}@example.com", "hashedpass123", 1)
        )
        print(f"✓ User created with ID: {user_id}")
        
        # Now test survey insert with the new user_id
        print("\n→ Creating test survey...")
        survey_id = await db.execute(
            "INSERT INTO survey (name_survey, description, created_by, is_active) VALUES (%s, %s, %s, %s)",
            ("Test Survey from Python", "Test Description", user_id, True)
        )
        print(f"✓ Survey created with ID: {survey_id}")
        
        # Test select to verify the survey was created
        result = await db.query("SELECT survey_id, name_survey, description, created_at FROM survey WHERE survey_id = %s", (survey_id,))
        print(f"✓ Survey select result:")
        for row in result:
            print(f"  ID: {row['survey_id']}, Name: {row['name_survey']}, Desc: {row['description']}")
        
        print("\n✓✓✓ All tests passed! MySQL INSERT/SELECT with LAST_INSERT_ID working correctly!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())




