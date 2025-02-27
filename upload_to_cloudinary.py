import cloudinary
import cloudinary.uploader
import cloudinary.api
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Cloudinary
cloudinary.config(
    cloud_name='dyxgxraqp',
    api_key='241575254575594',
    api_secret='9X1peEQxh0j7spHgRLSbeDKFcGI'
)

# Initialize Firebase
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://wce-surveillance-default-rtdb.firebaseio.com/'
})

def upload_image(image_path):
    # Upload image to Cloudinary
    response = cloudinary.uploader.upload(image_path)
    image_url = response['secure_url']

    # Create JSON object
    image_data = {
        "URL": image_url,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
        "Latitude": "000",  # Placeholder value
        "Longitude": "111",  # Placeholder value
        "Category": "Crowd Detection"  # Placeholder value
    }

    # Store JSON object in Firebase Realtime Database
    ref = db.reference('images')
    new_image_ref = ref.push()
    new_image_ref.set(image_data)

    print(f"Image uploaded and data stored in Firebase: {image_data}")

if __name__ == "__main__":
    image_path = 'demo1.jpg'  # Replace with your image path
    upload_image(image_path)



# import cloudinary
# import cloudinary.uploader
# import cloudinary.api
# import firebase_admin
# from firebase_admin import credentials, db
# import os

# # Initialize Cloudinary
# cloudinary.config(
#     cloud_name='dyxgxraqp',
#     api_key='241575254575594',
#     api_secret='9X1peEQxh0j7spHgRLSbeDKFcGI'
# )

# # Initialize Firebase
# cred = credentials.Certificate('firebase_credentials.json')
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://wce-surveillance-default-rtdb.firebaseio.com/'
# })

# def upload_image(image_path):
#     # Upload image to Cloudinary
#     response = cloudinary.uploader.upload(image_path)
#     image_url = response['secure_url']
    
#     # Store URL in Firebase Realtime Database
#     ref = db.reference('images')
#     new_image_ref = ref.push()
#     new_image_ref.set({
#         'url': image_url
#     })
    
#     print(f"Image uploaded and URL stored in Firebase: {image_url}")

# if __name__ == "__main__":
#     image_path = 'demo.jpg'  # Replace with your image path
#     upload_image(image_path)