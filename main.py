from unittest import result
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

# Firestore Credentials File
SERVICE_ACCOUNT_CRED_FILE = "./service_account.json"


def print_addresses(addresses, selection_mode = False):
  '''
  Displays addresses in a neat table.
  
  Selection mode displays numbers increasing from one
  in the first column of the table.
  '''
  # Calculate the horizontal bar for the table
  bar_string = "-" * (92 + (6 if selection_mode else 0))

  # Display the table header
  print(bar_string)
  print(
    f"{'| Opt | ' if selection_mode else '| '}" \
    f"{'Street':<30} | {'City':<20} | {'State':<20} | {'Zip':<10}|"
  )
  print(bar_string)

  # Display addresses
  choice_number = 1   # Used for "Opt" column in selection_mode
  for address_document in addresses:
    # Get a readable type
    address = address_document.to_dict()

    # Display the address row
    print(
      f"{f'| {str(choice_number):^3} | ' if selection_mode else '| '}" \
      f"{address.get('street', ''):<30} | {address.get('city', ''):<20} | {address.get('state', ''):<20} | {address.get('zip_code', ''):<10}|"
    )
    
    # Increment option number
    choice_number += 1

  # Bottom bar of table
  print(bar_string)
  print()

  # When viewing data, pause to allow user to read.
  if not selection_mode:
    input("Press enter to continue...")
    print()

def print_address(address_obj):
  '''
  Prints a single address in standard format.
  '''
  address = address_obj.to_dict()

  print(address["street"])
  print(address["city"] + ",", address["state"], address["zip_code"])


def print_all_addresses(db):
  '''
  Gets and displays all addresses from database
  '''
  results = db.collection("addresses").get()

  print_addresses(results)

def search_addresses(db):
  '''
  Interface to search for an address by one of its fields.
  '''
  # Display search menu
  print("Search by")
  print("1 Zip Code")
  print("2 City")
  print("3 State")
  print("4 Street Address")
  print("0 Return to Main Menu")
  print()
  selection = input("Option: ")
  print()

  # Perform requested search
  results = None
  if selection == "1":
    search = input("Zip Code: ")
    results = db.collection("addresses").where("zip_code", "==", search).get()
  elif selection == "2":
    search = input("City: ")
    results = db.collection("addresses").where("city", "==", search).get()
  elif selection == "3":
    search = input("State: ")
    results = db.collection("addresses").where("state", "==", search).get()
  elif selection == "4":
    search = input("Street Address: ")
    results = db.collection("addresses").where("street", "==", search).get()
  elif selection == "0":
    return

  print()

  # Display results
  if results and len(results) > 0:
    print_addresses(results)
  else:
    print("No addresses were found matching your search.")
  print()

def select_address(db):
  '''
  Takes user input to select an address and
  returns the selection.
  '''
  # Input Search
  zip_code = input("Zip Code : ")
  street = input("Street: ")
  print()

  # Perform Query
  results = db.collection("addresses").where("zip_code", "==", zip_code).where("street", "==", street).get()

  # Check for no results
  if len(results) == 0:
    print("No matches found!")
    print()
    return None

  # Check for and handle multiple results
  selection = 1
  if len(results) > 1:
    # Displays addresses with option values
    print_addresses(results, selection_mode = True)
    # Get user's choice
    print("There were more than one addresses found. Please choose which address you would like to select")
    selection = input("Option: ")
    print()

    # Convert selection to int and validate
    try:
      selection = int(selection)
      if selection < 0 or selection > len(results):
        raise ValueError
    except TypeError:
      print("Invalid selection. Expected an integer.")
      print()
      return None
    except ValueError:
      print(f"Section was out of range [1-{len(results)}]")
      print()
      return None

  # Return the selected address's id
  return results[selection - 1]

def add_address(db):
  '''
  Gets an address from the user and adds it
  to the database.
  '''
  # Get input
  street = input("Street: ")
  city = input("City: ")
  state = input("State: ")
  zip_code = input("Zip Code: ")
  print()

  # Compile data
  data = {
    "street": street,
    "city": city,
    "state": state,
    "zip_code": zip_code,
  }

  # Add record
  db.collection("addresses").add(data)

def update_address(db):
  '''
  Select then update an address
  '''
  # Get address from user. Check for failed selection.
  address = select_address(db)
  if address == None:
    return

  # Display the selected address
  print("Selected Address:")
  print_address(address)
  print()

  # Request input on fields of address
  print("Edit fields. Use \".\" to signify no change.")
  street = input("Street: ")
  city = input("City: ")
  state = input("State: ")
  zip_code = input("Zip Code: ")
  print()

  data = {
    "street": street,
    "city": city,
    "state": state,
    "zip_code": zip_code,
  }

  # Don't update fields that were signified as "no change"
  for key in list(data.keys()):
    if data[key] == ".":
      del data[key]

  # If no fields were changed, do nothing
  if not data:
    return

  # Only update specified fields
  db.collection("addresses").document(address.id).update(data)


def delete_address(db):
  '''
  Select then delete an address
  '''
  # Get address from user. Check for failed selection.
  address = select_address(db)
  if address == None:
    return

  # Display selected address
  print("Selected Address:")
  print_address(address)
  print()
  
  # Confirm deletion with user
  confirmation = input("Are you sure you want to delete this address? (Y/N): ")
  print()

  # Check confirmation response
  if confirmation.lower() in ["y", "yes", "si", "sí", "affimative", "activate address shredder", "murder it"]:
    db.collection("addresses").document(address.id).delete()
    print("Address was deleted.")
  else:
    print("Address was spared.")
  print()

def init_database():
  '''
  Sets up and returns the Firestore database client.
  '''
  creds = credentials.Certificate(SERVICE_ACCOUNT_CRED_FILE)
  app = firebase_admin.initialize_app(creds)

  db = firestore.client()

  return db



def main():
  # Setup the database connection
  db = init_database()

  selection = None
  while selection != "0":
    # Display menu
    print("Available Operations:")
    print("1 Add an address")
    print("2 Update an address")
    print("3 Delete an address")
    print("4 Search for an address")
    print("5 Display all addresses")
    print("0 Exit program")
    print()
    selection = input("Select Operation: ")
    print()

    if selection == "1":
      add_address(db)
    elif selection == "2":
      update_address(db)
    elif selection == "3":
      delete_address(db)
    elif selection == "4":
      search_addresses(db)
    elif selection == "5":
      print_all_addresses(db)
    elif selection != "0":
      print("Invalid selection.")
      print()

if __name__ == "__main__":
  main()