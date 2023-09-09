
# Find My Kid

Welcome to Find My Kid, an app dedicated to helping users find their lost children and facilitating the sharing of information about found children. This application employs facial recognition technology to match photos of lost children with those posted by users who have found a child. Our mission is to bring families back together during challenging times.

## Facial Recognition using Machine Learing

We have implemented a facial recognition system using the face_recognition library in pyhton. The model detects if there are any faces in the input image and then extracts the facial features of the face.
The input is fed to the model through a firebase-collection listener. The listner is subcribed to the found-child collection and if an user uploads the details of any found child. 
The model compares the facial features of the lost child against the images of the children in the lost-child database. If a match is found then the details of the child is updated in the matched_children database and deleted from both the lost and found databases
The app serves as a platform for user to upload their queries into the database.

### Setting up the model and listener
First install the requirements from requirements.txt:

```
pip install -r requirements

```
After this run the listener.py file
