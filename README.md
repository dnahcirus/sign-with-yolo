# Sign Language Recognition (ASL A–J)

This project is a Sign Language Recognition system that detects American Sign Language (ASL) hand gestures for the alphabets A to J. It uses uploaded images of hand signs and processes them using a trained machine learning model and computer vision techniques.

---

## 🚀 Features

* ASL detection (A–J) from uploaded images
* Machine learning using YOLOv8
* React-based frontend UI with Tailwind CSS
* Dockerized for easy deployment
* Git version control

---

## ⚙️ Technologies Used

### 🧠 Model and Training

* Model: YOLOv8
* Dataset used: [American Sign Language (A–J) Dataset](https://www.kaggle.com/datasets/kapillondhe/american-sign-language)
* Evaluation: `train_test_split`, `accuracy_score` from `sklearn.model_selection` and `sklearn.metrics`

### 🧰 Libraries & Tools

* scikit-learn – Model evaluation
* numpy – Numerical array handling
* React + Tailwind CSS – Frontend UI
* Docker – Containerized deployment
* Git – Version control

---

## 🧪 Setup & Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/sign-language-recognition.git
   cd sign-language-recognition
   ```

2. Docker Option (Optional):

   ```bash
   docker-compose up --build
   ```

---

## 📸 Input and Output

* Input: Uploaded hand sign images (not live webcam)
* Output: Predicted ASL alphabet (A–J) displayed on screen

---

## 📋 Requirements for Input Images

To ensure accurate predictions:

1. Use a white or plain background
2. Make hand signs clearly and consistently
3. Ensure proper lighting
4. Capture images using a webcam (not downloaded or low-quality sources)

---

## ⚠️ Important Notes

* If the application doesn’t run:

  * Disable any security software that might block webcam/photo access
  * Allow third-party permissions for image uploads
* Keep the background and lighting optimal as per the input requirements

---

## 🤝 Credits

Made by Chand Suri
