import os
import time
from dotenv import load_dotenv
from faker import Faker
from supabase import create_client, Client
from supabase_auth.errors import AuthApiError

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

fake = Faker()

TOTAL_USERS = 250

# Spinner characters
symbols = ["|", "/", "—", "\\"]
spinner_index = 0

for created_accounts, _ in enumerate(range(TOTAL_USERS)):
    try:
        first_name = fake.first_name()
        last_name = fake.last_name()
        mobile_number = ""  # Provide a default mobile number for all users or generate one using Faker if needed

        email = fake.unique.email()
        password = ""  # Provide a default password for all users

        supabase.auth.admin.create_user(
            {
                "email": email,
                "password": password,
                "email_confirm": True,
                "user_metadata": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "mobile_number": mobile_number,
                    "username": fake.user_name()[:24],
                },
            }
        )

        created_accounts += 1

        # Update spinner
        spinner_index += 1

        # Select and display the next spinner symbol in sequence to
        # create a rotating loading animation in the terminal.
        spinner = symbols[spinner_index % len(symbols)]

        print(
            f"\r{spinner} Creating user(s) ... {created_accounts}/{TOTAL_USERS}",
            end="",
            flush=True,
        )

        # small delay so spinner animation is visible
        time.sleep(0.05)

    except AuthApiError as err:
        error_msg = "user with this email address has already been registered"

        if error_msg in str(err):
            continue
        else:
            print(f"\nUnexpected error: {err}")
            continue

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        break


print(f"\n{created_accounts}/{TOTAL_USERS} user accounts created successfully!")
