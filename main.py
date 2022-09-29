from unittest import result
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

SERVICE_ACCOUNT_CRED_FILE = "./service_account.json"


def print_addresses(addresses, selection_mode = False):
  print(
    f"{'Option ' if selection_mode else '':<}" \
    f"{'Street':<30} {'City':<20} {'State':<20} {'Zip':<10}"
  )

  choice_number = 1
  for address_document in addresses:
    address = address_document.to_dict()

    print(
      f"{str(choice_number) + ' ' if selection_mode else ''}" \
      f"{address.get('street', ''):<30} {address.get('city', ''):<20} {address.get('state', ''):<20} {address.get('zip_code', ''):<10}"
    )
    
    choice_number += 1

  print()

def print_address(address_obj):
  address = address_obj.to_dict()

  print(address["street"])
  print(address["city"] + ",", address["state"], address["zip_code"])


def print_all_addresses(db):
  results = db.collection("addresses").get()

  print_addresses(results)

  

  

def search_addresses(db):
  print("Search by")
  print("1 Zip Code")
  print("2 City")
  print("3 State")
  print("4 Street Address")
  print("0 Return to Main Menu")
  print()
  selection = input("Option: ")
  print()

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
  selection = None
  if len(results) > 1:
    print_addresses(results, selection_mode = True)
    print("There were more than one addresses found. Please choose which address you would like to select")
    selection = input("Option: ")
    print()
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

  # Validate and compile data

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
  address = select_address(db)

  if address == None:
    return

  print("Selected Address:")
  print_address(address)
  print()

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

  for key in list(data.keys()):
    if data[key] == ".":
      del data[key]


  db.collection("addresses").document(address.id).update(data)


def delete_address(db):
  '''
  Select then delete an address
  '''
  address = select_address(db)

  if address == None:
    return

  print("Selected Address:")
  print_address(address)
  print()
  confirmation = input("Are you sure you want to delete this address? (Y/N): ")
  print()

  if confirmation.lower() in ["y", "yes", "si", "sí", "affimative", "activate address shredder", "murder it"]:
    db.collection("addresses").document(address.id).delete()
    print("Address was deleted.")
  else:
    print("Address was spared.")
  print()



def init_database():
  creds = credentials.Certificate(SERVICE_ACCOUNT_CRED_FILE)

  app = firebase_admin.initialize_app(creds)

  db = firestore.client()

  return db



def main():
  # Setup the database connection
  db = init_database()

  selection = None
  while selection != "0":
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

