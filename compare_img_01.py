import face_recognition
from pathlib import Path
import time
import numpy as np
from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
from pathlib import Path
import pandas as pd
import datetime
import urllib.parse


folder_ref_path = "img_ref"
known_encodings = []
stream = BytesIO()
camera = PiCamera()
camera.start_preview()
camera.resolution = (240, 240)
sleep(1)
camera.stop_preview()
camera.close()
# camera.led = False



# def loadImageTobuffer():
#     # path_list = Path(folder_ref_path).glob("img_*.jpg")
#     # print(path_list)
#     # print("path")
#     for image_path in Path(folder_ref_path).glob("*.jpg"):
#         print(image_path)
#         known_image = face_recognition.load_image_file(image_path)
#         known_encoding = face_recognition.face_encodings(known_image)[0]
#         known_encodings.append(known_encoding)

def loadImageTobuffer(column_array):
    # path_list = Path(folder_ref_path).glob("img_*.jpg")
    # print(path_list)
    # print("path")
    arr3 = np.zeros((240, 240, 3))
    # Convert the data type to uint8
    arr3_uint8 = arr3.astype(np.uint8)
    for image_path in column_array:
        try:
            known_image = face_recognition.load_image_file("img_ref/"+image_path)
            known_encoding = face_recognition.face_encodings(known_image)[0]
            known_encodings.append(known_encoding)
            print(image_path)
        except:
            known_encodings.append(arr3_uint8)



def compare_face(index_img,face_image):
    known_image_encoding = known_encodings[index_img-1]
    unknown_encodings = face_recognition.face_encodings(face_image)
    # Get the face distance between the known person and all the faces in this image
    try:
        face_distance = face_recognition.face_distance(unknown_encodings, known_image_encoding)[0]
    except:
        face_distance = 1.0
    print("Distance : ", face_distance)
    if (face_distance <= 0.45):
        print("ture")
        return True
    else:
        print("false")
        return False


def capture_face():
    # Create the in-memory stream
    # stream = BytesIO()
    camera = PiCamera()
    camera.start_preview()
    camera.resolution = (240, 240)
    #camera.led = True
    sleep(1.2)
    camera.capture(stream, format='jpeg')
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    image = Image.open(stream)
    imgArray = np.asarray(image)
    print(imgArray.shape)
    #camera.led = False
    camera.stop_preview()
    camera.close()
    return imgArray 

def save_img(ID_Data,image_save):
    image_save1 = Image.fromarray(image_save)
    year_1 = str(now.year)
    month_1 = str(now.month)
    day_1 = str(now.month)
    hour_1 = str(now.month)
    minute_1 = str(now.minute)
    second_1 =str(now.second)
    ID_Data = str(ID_Data)
    date_time_1 = year_1+month_1+day_1+hour_1+minute_1+second_1
    path_save_img = "img_save/"+"/ID_0"+ID_Data+"/ID_0"+ID_Data+date_time_1+".jpg"
    # save a image using extension 
    im1 = image_save1.save(path_save_img) 
    return path_save_img


if __name__ == "__main__":
    Read_data_csv = pd.read_csv("Data_ID.csv")
    column_array = Read_data_csv['Face_Img'].to_numpy()
    print(column_array[0])
    start_time = time.time()
    loadImageTobuffer(column_array)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed Time: {elapsed_time:.6f} seconds")

    while (True):
        input_text = int(input("Enter ID: "))
        face_steam = capture_face()
        result_img = compare_face(input_text, face_steam)
        if (result_img == True):
            now = datetime.datetime.now()
            path_save_img = save_img(str(input_text),face_steam)
        else:
            print("not true")


    # print(known_encodings[0])
