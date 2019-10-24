# Facial Recognition GUI
A Python GUI which detects and recognises faces in a dataset

This application was created as part of my second year group project, sponsored by Capital One. 

Before a customer can be granted a credit card a series of AML (Anti Money Laundering) checks with external third parties need to be completed.
The project will consist of a workflow that resembles potential customers applying for a credit card, using automated photo/passport validation, verification against sanction lists and credit bureaus.

Facial Recognition is the first step in this process: 

1. A customer uploads a picture of a valid form ID.
2. The image from the ID is scanned and using facial recognition it will be compared to a database which acts as a blacklist. Any person whos image is in this database cannot apply for a credit card and therefore fails the checks (i.e a person who has applied already)


In this application, pictures of celebrities are used as the dataset and are therefore 'blacklisted'. 

1. Navigate through the dataset using the arrows at the bottom of the screen. This shows all the individuals in the dataset and what images of them were used for training. 
2. Press ‘Browse’ to choose an image to run through the system. 
3. After this image is uploaded, press the ‘Process’ button to run the algorithm. 
4. If there is no match in the dataset, a red box will appear around the face with the label ‘Unknown’ 
5. If there is a match, a green box will appear around the face, labelled with the name of a person. A pop up will also appear showing the matched individual from the dataset with the images of them used for training. 

## Screenshots 

[Screenshot](https://github.com/humaira99/FacialRecognition/blob/master/application.png?raw=true)
