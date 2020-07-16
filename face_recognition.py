import cv2
import os
import sys
import json
import shutil


def detect_faces(image_path):
    '''Detects faces in a given image.

    Parameters
    ----------
        image_path : string
            Path to the image

    Returns
    -------
        json_file : string
            Path to the json file
    '''

    if not image_path or not isinstance(image_path, str):
        print('Expecting for image path!')
    else:
        extension = os.path.basename(image_path).split('.')[1]
        if not 'jpg' == extension and not 'jpeg' == extension \
            and not 'jpe' == extension and not 'jfif' == extension \
            and not 'gif' == extension and not 'png' == extension:

            print('This is not an image!')
        else:
            cascade_path = 'haarcascade_frontalface_default.xml'

            # Initializes with a given cascade
            face_cascade = cv2.CascadeClassifier(cascade_path)

            # Reads the image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Detects faces in the image
            # Hint: Play with scaleFactor to adjust face detection in an image
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.21, \
                                                  minNeighbors=5, \
                                                  minSize=(30, 30), \
                                                  flags=cv2.CASCADE_SCALE_IMAGE)

            # Creates a copy image
            image_path_copy = create_copy_image(image_path)
            image_copy = cv2.imread(image_path_copy)

            # Draws rectangles over faces
            for (x, y, w, h) in faces:
                cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Saves image with rectangles
            cv2.imwrite(image_path_copy, image_copy)
            
            # Writes amount of found faces and image path into a JSON file
            json_file = write_to_json(faces, image_path)

            return json_file

def create_copy_image(image_path):
    '''Creates a copy of given image in the same directory.
    
    Parameters
    ----------
        image_path : string
            Path to the image

    Returns
    -------
        image_path_copy : string
            Path to the image copy
    '''

    directory = os.path.dirname(image_path)
    file_name = os.path.basename(image_path).split('.')
    extension = file_name[1]
    file_name = file_name[0]

    image_path_copy = directory + '/' + file_name + '_copy.' + extension

    shutil.copyfile(image_path, image_path_copy)

    return image_path_copy

def write_to_json(faces, image_path):
    '''Writes amount of found faces and image path into a JSON file.
    
    Parameters
    ----------
        faces : object
            Contains details of found faces
        image_path : string
            Path to the image
    
    Returns
    -------
        json_file : string
            Path to the json file
    '''

    json_file = 'faces.json'

    data = {}
    data['countFaces'] = len(faces)
    data['imageLocation'] = image_path

    json.dump(data, open(json_file, 'w'))

    return json_file


def main():
    image_path = 'the_heavy.jpg'
    # image_path = sys.argv[1]
    json_file = detect_faces(image_path)

    print(json_file)


if __name__ == '__main__':
    main()