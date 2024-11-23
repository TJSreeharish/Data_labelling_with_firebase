from firebase_admin import credentials, initialize_app, _apps

def initialize():
    # Check if Firebase is already initialized to avoid re-initialization
    if not _apps:
        # Replace with the path to your Firebase service account key
        cred = credentials.Certificate("base-caf29-firebase-adminsdk-2b5vf-040a65f4cf.json")
        
        # Initialize the app with a storage bucket
        app = initialize_app(cred, {
            "storageBucket": "base-caf29.appspot.com"
        })
        return app
    else:
        # Firebase is already initialized
        return _apps["[DEFAULT]"]  # Return the default Firebase app if already initialized