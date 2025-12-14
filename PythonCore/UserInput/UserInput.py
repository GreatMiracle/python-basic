first_name = input("Enter your first name: ")
days = input("How many days before your birthday? ")

print(first_name)

print('------------------------f-strings---------------------------------')
first_name = input("Enter your first name: ")
days = input("How many days before your birthday? ")

print(f"Hi {first_name}. Only {days} days before your birthday.")
print(
    f"Hi, {first_name}. "
    f"Only {days} days until your birthday!"
)

print('------------------------input() LUÔN là string ---------------------------------')
days = int(input("How many days? "))
print(days + 1)