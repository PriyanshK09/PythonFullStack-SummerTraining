import requests
BASE_URL = "https://reqres.in/api/users"
HEADERS = {
   "x-api-key": "reqres-free-v1"
}

# GET
def get_users():
   response = requests.get(f"{BASE_URL}?page=2", headers=HEADERS)
   print("GET Response:", response.status_code)
   print(response.json())

# POST
def create_user():
   payload = {
       "name": "Priyansh",
       "job": "Full Stack Developer"
   }
   response = requests.post(BASE_URL, json=payload, headers=HEADERS)
   print("POST Response:", response.status_code)
   print(response.json())

# PUT
def update_user_put(user_id=2):
   payload = {
       "name": "Priyansh",
       "job": "Senior Full Stack Developer"
   }
   response = requests.put(f"{BASE_URL}/{user_id}", json=payload, headers=HEADERS)
   print("PUT Response:", response.status_code)
   print(response.json())

# PATCH
def update_user_patch(user_id=2):
   payload = {
       "job": "Tech Lead"
   }
   response = requests.patch(f"{BASE_URL}/{user_id}", json=payload, headers=HEADERS)
   print("PATCH Response:", response.status_code)
   print(response.json())

# DELETE
def delete_user(user_id=2):
   response = requests.delete(f"{BASE_URL}/{user_id}", headers=HEADERS)
   print("DELETE Response:", response.status_code)  # Expect 204


# Run all
if __name__ == "__main__":
   print("GET Users")
   get_users()
   print("Create User")
   create_user()
   print("Update User (PUT)")
   update_user_put()
