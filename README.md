# Web AI Object Detection

This project is a FastAPI-based web application that utilizes an Ultralytics YOLO model for object detection. It provides a simple web interface to upload images or select existing test images and view the resulting bounding boxes and detection confidence scores.

## Features
- Upload an image for object detection.
- Select from existing test images.
- Real-time prediction using YOLO (`yolo11n.pt`).
- View the image with bounding boxes drawn over detected objects.
- See a table of detected classes and their confidence scores.

## Requirements
- Docker
- (Alternatively) Python 3.11+ and `uv` package manager if running locally without Docker.

## How to Use (with Docker)

1. **Build the Docker image:**
   Open a terminal in the project root directory and build the Docker image:
   ```bash
   docker build -t web-ai .
   ```

2. **Run the container:**
   Start the application and mount the `static` directory to persist and access images on your host OS:
   ```bash
   docker run -p 8000:8000 -v $(pwd)/static:/app/static web-ai
   ```

3. **Access the application:**
   Open your web browser and go to:
   [http://localhost:8000](http://localhost:8000)

4. **Make a Prediction:**
   - Choose a file to upload or select a test image from the list.
   - Submit the form to perform detection.
   - The annotated image and detection results will be shown on the screen.

## Project Structure
- `app.py`: The main FastAPI application logic.
- `dockerfile`: Contains the instructions to build the web app container.
- `static/`: Contains static assets, including uploaded, tested, and result images.
- `templates/`: Contains HTML templates for the web interface (`index.html`).
- `model/`: Directory storing the YOLO model file (`yolo11n.pt`).
