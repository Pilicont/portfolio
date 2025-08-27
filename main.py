import cv2 
import os
import re
subdirs = [
    "parametrs",
    "images",
    "recognized_objects",
    "videos",
    "recognized_videos"
]
base_dir = os.path.dirname(os.path.abspath(__file__)) #get oath to current position

cascades = {
    'eyes': cv2.CascadeClassifier(os.path.join(base_dir,'haarcascade_eye.xml')),
    'faces': cv2.CascadeClassifier(os.path.join(base_dir, 'haarcascade_frontalface_default.xml')),
    'fullbody': cv2.CascadeClassifier(os.path.join(base_dir,'haarcascade_fullbody.xml')),
    'smile': cv2.CascadeClassifier(os.path.join(base_dir,'haarcascade_smile.xml'))
}

paths = {name: os.path.join(base_dir, name) for name in subdirs} #get path to folders



def objectsPath(cascades): #Function for transfers objects in another functions
    results = []
    for folder in ['videos', 'images']:
        folder_path = os.path.join(base_dir, folder)
        for file in os.listdir(folder_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', 'mp4', '.vlc')): # find files in the folder
                object_path = os.path.join(folder_path, file) #get object path
            
                if file.lower().endswith(('.png', '.jpg', '.jpeg')): #find files with photo resolution
                    object = cv2.imread(object_path)
                    if object is None:
                        print(f"Could not read {file}")
                        continue

                elif file.lower().endswith(('mp4', '.vlc')): # find files with video resolution
                    cap = cv2.VideoCapture(object_path)
                    video_results = []
                    while True:
                        ret, frame = cap.read() #if we have file read it
                        if not ret:
                            break
                        proceseed = withoutWindows(frame)
                        video_results.append(proceseed)
                    cap.release()
                    results.append((file, video_results))
    return results

def withoutWindows(object, file): # function for show windows or not  
    user_choice = input('Do you want to see and select objects?')
    if user_choice == 'y':
        if object == file.lower().endswith(('.png', '.jpg', '.jpeg')): 
            cv2.imshow('Detected Objects', object)
            cv2.waitKey(1) 
            cv2.destroyWindow('Detected Objects') 
        elif object == file.lower().endswith(('mp4', '.vlc')):
            cap = cv2.VideoCapture(object)
            while(cap.isOpened()):
                result,frame = cap.read()
                if result == True:
                    cv2.imshow('Video', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            cap.release()
            cv2.destroyAllWindows()
    elif user_choice == 'n':
        return None

def recofnizedFunc(user_input_parametrs, object, cascades, save_dir=None): #this func recognize objects
    ext = object.lower().split('.')[-1]

    if ext in ['png', 'jpg', 'jpeg']:
        img = cv2.imread(object)
        if img is None:
            print(f'Can\'t read {object}')
            return
        
        for user_input_parametrs in cascades:
            for cascades in cascades.values():
                    recognized = recognized.detectMultiScale(img, scaleFactor=1.1, minNeighbors=3)
                    for (x, y, w, h) in recognized:
                        cv2.rectangle(object, (x, y), (x + w, y + h), (50, 100, 50), 2) 

    elif ext in ['mp4', 'avi', 'vlc']:
        cap = cv2.VideoCapture(object)
        if save_dir:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out_path = os.path.join(save_dir, os.path.basename(object))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
        else:
            out = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            for cascades in cascades.values():
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                detected_video = detected_video.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
                for (x, y, w, h) in detected_video:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
def saveObjects (user_input_parametrs, cascades ):
    if user_input_parametrs in cascades:
        for values in user_input_parametrs:
            if values == cascades.values():
                if not os.path.exists(base_dir, 'recognized_objects'):
                    recognized_folder = os.path.join(base_dir, 'recognized_objects')
                    os.makedirs(recognized_folder, exist_ok=True)
                    saveFolders = os.path.join(base_dir, values + '_recognized_object')
                    os.makedirs(saveFolders, exist_ok=True)





user_input = input('Enter the parameters separated by space: ')
user_input_parametrs = re.split(r'[,\s]+', user_input.strip()) #allow to user write like (face, smile) or (face , smile)

#теперь нужно все это допилить и запустить. остановился я на том, что сделал обработку всех изображений в папках
##пути сохранения для файлов,
#Теперь их нужно сохранять, хотя бы списками уже, потом от пользоватлея передадим
#Потом автоматически сохранять в те папке, благодаря которым распозналось, что бы было понятно что мы узнали. 
# 

## Вообще в самом конце это допилить код и вычистить его от мусора. 


#Написать теперь для человека выбор из каких параметров.//Yes
# Выводить на экран или сохранять все?//Yes
# функции для распознования каждого объекта в словаре//Yes
# 
