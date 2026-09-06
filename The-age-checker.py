import datetime

def get_birth_year():
    try:
        age = input("How old are you?")
        age_int = int(age) # potential ValueError

        current_year = 2026
        birth_year = current_year - age_int

        print(f"You were born around {birth_year}")

    except ValueError:
        print("Error: You didnt enter valid number for your age")

# if we dodnt use try/except, the program dies here if this input is "ten"
get_birth_year()
print("program continues to run other tasks...")
