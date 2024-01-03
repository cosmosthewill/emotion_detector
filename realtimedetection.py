import cv2
from keras.models import model_from_json
import numpy as np
import time
import tkinter as tk
from tkinter import ttk
import os
import matplotlib.pyplot as plt
from IPython.display import HTML, display

json_file = open("model/facialemotionmodel.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)

model.load_weights("model/facialemotionmodel.h5")
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)


def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature/255.0


webcam = cv2.VideoCapture(0)
labels = {0: 'angry', 1: 'disgust', 2: 'fear',
          3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

emotion_count = {label: 0 for label in labels.values()}  #  init emo count
emotion_count_per_second = {label: 0 for label in labels.values()} #emo time count 
last_emotion_images = {emotion: None for emotion in labels.values()}
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

# Clear the contents of the output folder
for file_name in os.listdir(output_folder):
    file_path = os.path.join(output_folder, file_name)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")

start_time = time.time()
current_second = int(start_time)
no_emotion_time = 0
total_faces_detected = 0
last_face_detection_time = start_time
no_face_timeout = 10  # 10 seconds timeout for no face detection

while True:
    #time calc
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    i, im = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(im, 1.3, 5)
    
    try:
        if len(faces) == 0:
            no_emotion_time += time.time() - current_time
            # Check if no face has been detected for the timeout period
            if current_time - last_face_detection_time >= no_face_timeout:
                break
        else:
            total_faces_detected += len(faces)
            last_face_detection_time = current_time  # Update the last face detection time
            
        for (p, q, r, s) in faces:
            #đhs chạy đúng
            face_region = im[q:q+s, p:p+r].copy() 
            image = gray[q:q+s, p:p+r]
            cv2.rectangle(im, (p, q), (p+r, q+s), (255, 0, 0), 2)
            image = cv2.resize(image, (48, 48))
            
            img = extract_features(image)
            pred = model.predict(img)
            prediction_label = labels[pred.argmax()]
            
            # Save last image for each emotion
            last_emotion_images[prediction_label] = face_region
            
            
            emotion_count[prediction_label] += 1 
            
            cv2.putText(im, '% s' % (prediction_label), (p-10, q-10),
                        cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("Output", im)
        key = cv2.waitKey(1)
        if key == 27:  # ESC quit
            break  
    except cv2.error:
        pass


webcam.release()
cv2.destroyAllWindows()

total_time = time.time() - start_time
print(f"Run time: {total_time} sec")
print(f"Nothing time: {no_emotion_time} sec")
print(f"Total faces detected: {total_faces_detected}")

# Count and display percentages
percentages = {}
for emotion, count in emotion_count.items():
    percentage = (count / total_faces_detected) * 100 if total_faces_detected > 0 else 0
    percentages[emotion] = percentage
    print(f"{emotion}: {percentage:.2f}%")


# Save the last image for each emotion in the output folder
for emotion, last_image in last_emotion_images.items():
    if last_image is not None:
        emotion_image_filename = os.path.join(output_folder, f"{emotion}_last.png")
        cv2.imwrite(emotion_image_filename, last_image)

# Create an HTML file with the chart and images
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Emotion Detection Results</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Emotion Detection Results</h1>
    <div id="chart"></div>
"""

# Additional Information
for emotion, percentage in percentages.items():
    if emotion == 'neutral' and percentage >= 70:
        html_content += f'<h1 style="color:green;font-size:50px">GOOD</h1>'
    if emotion == 'happy' and percentage >= 40:
        if  emotion == 'neutral' and percentage >= 30:
            html_content += f'<h1 style="color:yellow;font-size:50px">CAUTIOUS</h1>'         
    else:
        html_content += f'<h1 style="color:red;font-size:50px">WARNING</h1>'
        break

html_content += f'<h2>Emotion Images</h2>'
# Display images
for emotion, image_path in last_emotion_images.items():
    if image_path is not None:
        html_content += f"<h3>{emotion}</h3>"
        html_content += f'<img src="{emotion}_last.png" alt="{emotion}" style="width:200px;height:200px">'

# Create a bar chart
fig, ax = plt.subplots()
bars = ax.bar(percentages.keys(), percentages.values(), color='blue')
ax.set_ylabel('Percentage (%)')
ax.set_title(f"Car Run time: {total_time:.1f} sec")
# Add percentage labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}%', ha='center', va='bottom')

# Save the chart as an image
chart_filename = os.path.join(output_folder, 'emotion_chart.png')
plt.savefig(chart_filename, bbox_inches='tight')


plt.close()

# Add the chart image to the HTML content
html_content += '<h2>Emotion Detection Chart</h2>'
html_content += f'<img src="{os.path.abspath(chart_filename)}" alt="Emotion Chart" style="width:600px;">'

# Close the HTML file
html_content += """
</body>
</html>
"""

# Save the HTML file
html_filename = os.path.join(output_folder, 'emotion_results.html')
with open(html_filename, 'w') as html_file:
    html_file.write(html_content)

# Open the HTML file using the default web browser
try:
    import webbrowser
    webbrowser.open('file://' + os.path.abspath(html_filename))
except Exception as e:
    print(f"Error opening HTML file: {e}")
    
# import menu
# menu.mainmenu()