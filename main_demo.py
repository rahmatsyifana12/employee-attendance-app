# This file with start.py contains both face recognition program and GUI
import cv2
import numpy as np
import face_recognition
import os
import datetime
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox

class UIDialog(QDialog):
    def __init__(self):
        super(UIDialog, self).__init__()
        loadUi("./main.ui", self)

        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        self.date_label.setText(current_date)
        self.time_label.setText(current_time)
        self.image = None

    @pyqtSlot()
    def startVideo(self, camera_name):
        if len(camera_name) == 1:
            self.capture = cv2.VideoCapture(int(camera_name))
        else:
        	self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)  # Create Timer
        path = 'Images'
        images = []
        self.person_names = []
        self.known_encoded_imgs = []
        img_list = os.listdir(path)
        for raw_img in img_list:
            curr_img = cv2.imread(f'{path}/{raw_img}')
            # insert images in BGR version into list of images
            images.append(curr_img)

            # insert images name into list of names
            self.person_names.append(os.path.splitext(raw_img)[0])
        
        for img in images:
            # converting image from BGR into RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # encoding the image
            encode_img = face_recognition.face_encodings(img)[0]
            self.known_encoded_imgs.append(encode_img)

        print('Encoding complete . . .')

        self.timer.timeout.connect(self.update_frame)
        self.timer.start(40)

    def face_recog(self, frame, known_encoded_imgs, person_names):
        def mark_attendance(name):
            if self.clock_in_btn.isChecked():
                self.clock_in_btn.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                    if name != 'unknown':
                        btn_reply = QMessageBox.question(self, 'Welcome ' + name, 'Are you Clocking in?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if btn_reply == QMessageBox.Yes:
                            date_time_string = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            f.writelines(f'\n{name},{date_time_string},Clock In')
                            self.clock_in_btn.setChecked(False)

                            self.name_label.setText(name)
                            self.status_label.setText('Clocked In')

                            self.Time1 = datetime.datetime.now()
                            self.clock_in_btn.setEnabled(True)
                        else:
                            print('Not Clicked.')
                            self.clock_in_btn.setEnabled(True)
            elif self.clock_out_btn.isChecked():
                self.clock_out_btn.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                    if name != 'unknown':
                        btn_reply = QMessageBox.question(self, 'Cheers ' + name, 'Are you Clocking out?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if btn_reply == QMessageBox.Yes:
                            date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            f.writelines(f'\n{name},{date_time_string},Clock Out')
                            self.clock_out_btn.setChecked(False)

                            self.name_label.setText(name)
                            self.status_label.setText('Clocked Out')
                            self.Time2 = datetime.datetime.now()

                            self.clock_out_btn.setEnabled(True)
                        else:
                            print('Not Clicked.')
                            self.clock_out_btn.setEnabled(True)
                            
        image_small = cv2.resize(frame, (0, 0), None, 0.25, 0.25)

        # converting the captured image from BGR into RGB
        image_small = cv2.cvtColor(image_small, cv2.COLOR_BGR2RGB)

        # find location of the face in cam
        face_curr_frame = face_recognition.face_locations(image_small)

        # encoding the captured image
        encoded_curr_frame = face_recognition.face_encodings(image_small, face_curr_frame)

        # grab the encoding of encoded_face from encoded_curr_frame and face_loc from face_curr_frame
        # using zip because we want in the same loop
        for encoded_face, face_loc in zip(encoded_curr_frame, face_curr_frame):
            # matching the known encoded images with the face from camera
            matches = face_recognition.compare_faces(known_encoded_imgs, encoded_face)

            # getting the distance difference between the known encoded images with the face from camera
            face_dis = face_recognition.face_distance(known_encoded_imgs, encoded_face)
            # getting the best match based on the lowest number
            match_idx = np.argmin(face_dis)

            # getting the name of the best match face
            if matches[match_idx]:
                name = person_names[match_idx].upper()
                print(name)

                # getting face coordinates
                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

                # creating a rectangle to mark the face
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                # cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                mark_attendance(name)
        
        return frame

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.known_encoded_imgs, self.person_names, 1)

    # displaying image of camera to pyQt
    def displayImage(self, image, encode_list, class_names, window=1):
        image = self.face_recog(image, encode_list, class_names)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.img_label.setPixmap(QPixmap.fromImage(outImage))
            self.img_label.setScaledContents(True)