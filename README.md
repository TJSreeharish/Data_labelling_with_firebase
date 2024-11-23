# IDK-hackathon-project
 Developed during a VVCE hackathon, this project simplifies dataset creation for computer vision. Using Firebase for storage and Django for the backend, authenticated users can annotate images to earn incentives. Annotations are stored for training models, with a simple HTML and CSS frontend for interaction.


ignoring all the ph/placeholders this is a typical django project make use of hack for the main folder. hack_app is the app created here.
there is one more thing since we have used firebase we have added an api key to our file so you will have to generate an api key and make necessary changes.the steps are below.

Firebase Service Account Integration
This project integrates Firebase for handling image uploads and related operations. To enable Firebase functionality, the provided service account JSON file must be set up correctly.

Steps to Use the Firebase Service Account Key
Place the File:

Save the service account JSON file (e.g., firebase-service-account.json) in the same directory as your Django main folder (where the manage.py file is located).
Install Required Libraries:

Ensure you have the Firebase Admin SDK installed in your environment:
      pip install firebase-admin

Update Django Settings:

In your Django project, configure Firebase in a settings or utility file:
      import firebase_admin
      from firebase_admin import credentials
      # Path to your service account JSON file
      cred = credentials.Certificate("firebase-service-account.json")
      firebase_admin.initialize_app(cred)
Usage:

Once initialized, you can use Firebase services such as Firestore, Storage, etc., in your project.
Example for uploading files:
      from firebase_admin import storage
      bucket = storage.bucket()
      blob = bucket.blob("path/to/your/file.jpg")
      blob.upload_from_filename("local/file.jpg")
By following these steps, your Firebase service account will integrate seamlessly with your Django project.
