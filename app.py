from flask import Flask, render_template, Response
import cv2
app=Flask(__name__)

def capture_by_frames(): 
    global camera
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
        faces=detector.detectMultiScale(frame,1.2,6)
         #Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start',methods=['POST'])
def start():
    return render_template('index.html')

@app.route('/stop',methods=['POST'])
def stop():
    if camera.isOpened():
        camera.release()
    return render_template('stop.html')

@app.route('/video_capture')
def video_capture():
    return Response(capture_by_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True,use_reloader=False, port=8000)