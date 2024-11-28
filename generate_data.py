import os
import random
from faker import Faker
import django

# Initialize Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate_management.settings")  # Replace with your Django project name
django.setup()

from users.models import User
from estates.models import Estate

fake = Faker()


# Generate random users
def generate_users(n_users):
    roles = [User.ADMIN, User.CLIENT]
    users = []
    existing_emails = set(User.objects.values_list('email', flat=True))  # Existing emails in DB

    for _ in range(n_users):
        email = fake.email()

        # Ensure unique email
        while email in existing_emails:
            email = fake.email()

        user = User(
            email=email,
            username=email,  # Ensuring uniqueness
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=random.choice(roles)
        )
        user.set_password("password123")  # Default password for testing
        users.append(user)
        existing_emails.add(email)  # Add to existing emails set

    User.objects.bulk_create(users)
    return User.objects.all()[:n_users]

# Generate random estates for each user
def generate_estates(users, estates_per_user):
    property_types = ['House', 'Apartment']
    estates = []
    for user in users:
        for _ in range(estates_per_user):
            estate = Estate(
                property_name=fake.street_name(),
                address=fake.address(),
                owner=user,
                property_type=random.choice(property_types),
                rent_amount=round(random.uniform(500, 5000), 2),
            )
            estates.append(estate)
    Estate.objects.bulk_create(estates)

# Main function
def main():
    n_users = 200  # Number of users
    estates_per_user = 5  # Estates per user

    print("Generating users...")
    users = generate_users(n_users)
    print(f"{len(users)} users created.")

    print("Generating estates...")
    generate_estates(users, estates_per_user)
    print(f"{n_users * estates_per_user} estates created.")

if __name__ == "__main__":
    main()
