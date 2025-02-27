import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, render_template_string
import threading
import json
import webbrowser
import os

# Initialize Firebase
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://wce-surveillance-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)

# Global variable to store the latest image data
latest_image_data = None

# Variable to track the last processed data
last_processed_data = None

# Variable to track if the browser has been opened
browser_opened = False

def listen_for_image_updates():
    global latest_image_data, last_processed_data, browser_opened

    def callback(event):
        global latest_image_data, last_processed_data, browser_opened
        try:
            # Parse the event data
            if event.data:
                # If event.data is a string, parse it as JSON
                if isinstance(event.data, str):
                    data = json.loads(event.data)
                else:
                    data = event.data

                # Handle the data based on its structure
                if isinstance(data, dict):
                    # If the data is a dictionary, extract the image data
                    if data:
                        # Check if the dictionary contains nested data (e.g., push IDs)
                        if any(isinstance(value, dict) for value in data.values()):
                            # Get the last key in the dictionary
                            last_key = list(data.keys())[-1]
                            # Extract the image data from the last item
                            latest_image_data = data[last_key]
                        else:
                            # If the dictionary is flat, assume it contains the image data directly
                            latest_image_data = data

                        # Skip duplicate events
                        if latest_image_data != last_processed_data:
                            print(f"New image data received: {latest_image_data}")
                            last_processed_data = latest_image_data

                            # Open the browser if not already opened
                            if not browser_opened:
                                webbrowser.open('http://127.0.0.1:5000/')
                                browser_opened = True
                    else:
                        print("No images found in the dataset.")
                elif isinstance(data, str):
                    # If the data is a string, assume it's a direct JSON string
                    latest_image_data = json.loads(data)
                    if latest_image_data != last_processed_data:
                        print(f"New image data received: {latest_image_data}")
                        last_processed_data = latest_image_data

                        # Open the browser if not already opened
                        if not browser_opened:
                            webbrowser.open('http://127.0.0.1:5000/')
                            browser_opened = True
                else:
                    print(f"Unexpected data format: {data}")
            else:
                # Ignore empty events
                pass
        except Exception as e:
            print(f"Error processing event: {e}")

    # Listen to the 'images' reference
    ref = db.reference('images')
    ref.listen(callback)

@app.route('/')
def display_image():
    global latest_image_data
    if latest_image_data:
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Display Image</title>
                <meta http-equiv="refresh" content="5"> <!-- Refresh the page every 5 seconds -->
            </head>
            <body>
                <h1>Latest Uploaded Image</h1>
                <img src="{{ image_data.URL }}" alt="Uploaded Image" style="max-width: 100%; height: auto;">
                <p><strong>Time:</strong> {{ image_data.Time }}</p>
                <p><strong>Latitude:</strong> {{ image_data.Latitude }}</p>
                <p><strong>Longitude:</strong> {{ image_data.Longitude }}</p>
                <p><strong>Category:</strong> {{ image_data.Category }}</p>
            </body>
            </html>
        ''', image_data=latest_image_data)
    else:
        return "No image uploaded yet."

@app.after_request
def add_header(response):
    # Disable caching
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == "__main__":
    # Start listening to Firebase in a separate thread
    threading.Thread(target=listen_for_image_updates, daemon=True).start()

    # Run Flask app
    app.run(debug=True)


# import firebase_admin
# from firebase_admin import credentials, db
# from flask import Flask, render_template_string
# import threading
# import json
# import webbrowser
# import os

# # Initialize Firebase
# cred = credentials.Certificate('firebase_credentials.json')
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://wce-surveillance-default-rtdb.firebaseio.com/'
# })

# app = Flask(__name__)

# # Global variable to store the latest image URL
# latest_image_url = None

# # Variable to track the last processed URL
# last_processed_url = None

# # Variable to track if the browser has been opened
# browser_opened = False

# def listen_for_image_updates():
#     global latest_image_url, last_processed_url, browser_opened

#     def callback(event):
#         global latest_image_url, last_processed_url, browser_opened
#         try:
#             # Parse the event data
#             if event.data:
#                 # If event.data is a string, parse it as JSON
#                 if isinstance(event.data, str):
#                     data = json.loads(event.data)
#                 else:
#                     data = event.data

#                 # Handle the data based on its structure
#                 if isinstance(data, dict):
#                     # If the data is a dictionary, extract the URL of the last added image
#                     if data:
#                         # Check if the dictionary contains nested data (e.g., push IDs)
#                         if any(isinstance(value, dict) for value in data.values()):
#                             # Get the last key in the dictionary
#                             last_key = list(data.keys())[-1]
#                             # Extract the URL from the last item
#                             latest_image_url = data[last_key].get('url')
#                         else:
#                             # If the dictionary is flat, assume it contains the URL directly
#                             latest_image_url = data.get('url')

#                         # Skip duplicate events
#                         if latest_image_url != last_processed_url:
#                             print(f"New image URL received: {latest_image_url}")
#                             last_processed_url = latest_image_url

#                             # Open the browser if not already opened
#                             if not browser_opened:
#                                 webbrowser.open('http://127.0.0.1:5000/')
#                                 browser_opened = True
#                     else:
#                         print("No images found in the dataset.")
#                 elif isinstance(data, str):
#                     # If the data is a string, assume it's a direct URL
#                     latest_image_url = data
#                     if latest_image_url != last_processed_url:
#                         print(f"New image URL received: {latest_image_url}")
#                         last_processed_url = latest_image_url

#                         # Open the browser if not already opened
#                         if not browser_opened:
#                             webbrowser.open('http://127.0.0.1:5000/')
#                             browser_opened = True
#                 else:
#                     print(f"Unexpected data format: {data}")
#             else:
#                 # Ignore empty events
#                 pass
#         except Exception as e:
#             print(f"Error processing event: {e}")

#     # Listen to the 'images' reference
#     ref = db.reference('images')
#     ref.listen(callback)

# @app.route('/')
# def display_image():
#     global latest_image_url
#     if latest_image_url:
#         return render_template_string('''
#             <!DOCTYPE html>
#             <html>
#             <head>
#                 <title>Display Image</title>
#                 <meta http-equiv="refresh" content="5"> <!-- Refresh the page every 5 seconds -->
#             </head>
#             <body>
#                 <h1>Latest Uploaded Image</h1>
#                 <img src="{{ image_url }}" alt="Uploaded Image" style="max-width: 100%; height: auto;">
#             </body>
#             </html>
#         ''', image_url=latest_image_url)
#     else:
#         return "No image uploaded yet."

# @app.after_request
# def add_header(response):
#     # Disable caching
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '-1'
#     return response

# if __name__ == "__main__":
#     # Start listening to Firebase in a separate thread
#     threading.Thread(target=listen_for_image_updates, daemon=True).start()

#     # Run Flask app
#     app.run(debug=True)