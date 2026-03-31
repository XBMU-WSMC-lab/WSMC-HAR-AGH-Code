# The WSMC-HAR-AGH Dataset: Multimodal Wearable Sensor Data for Human Activity Recognition

This repository contains the source code (Hardware Firmware & Software Implementation) for the paper: **"The WSMC-HAR-AGH Dataset: Multimodal Wearable Sensor Data for Human Activity Recognition"** submitted to *Scientific Data*.

## 📌 Project Overview
The WSMC-HAR-AGH dataset is a comprehensive multimodal database for Human Activity Recognition (HAR), capturing synchronized inertial (accelerometer, gyroscope) and physiological (heart rate, SpO2) data. 

This repository provides the complete pipeline:
1.  **Hardware Firmware**: Embedded code for the custom Arm-Wearable Equipment (AWE).
2.  **Data Visualisation**: Tools for signal inspection.
3.  **Deep Learning Models**: The proposed **Multichannel CNN-BiGRU** (based on the Four-Fusion Scheme) and several baseline models (SVM, VGG, ResNet) for performance comparison.

---

## 🛠 Repository Structure
Based on the `XBMU-WSMC-lab` environment:

```text
├── Hardware_Firmware/           # Embedded C/C++ code for STM32 & Sensors
├── Data visualisation.py        # Script for plotting IMU and Physiological signals
├── Mulichannel CNN-BiGRU-model.py # Proposed main model (Four-Fusion Scheme)
├── RestNet_har_train.py         # Baseline: ResNet-based HAR training
├── SVM_har_train.py             # Baseline: Support Vector Machine implementation
├── VGG_har_train.py             # Baseline: VGG-based HAR training
├── README.md                    # Project documentation
└── (Requirements.txt)           # Python dependencies (Recommended to add)

🔧 Hardware Implementation
The data was acquired using a custom-designed Arm-Wearable Equipment (AWE) developed at Northwest Minzu University.

MCU: STM32F103ZET6.
IMU: MPU-6050 (Accelerometer & Gyroscope).
Physiological Sensor: MAX30102 (PPG for Heart Rate & SpO2).
Transmission: ZigBee-based wireless communication (CC2530).
Firmware source code can be found in the Hardware_Firmware/ directory.

💻 Software & AI Models
We provide the implementation of the proposed model and three baseline models used in the paper's experimental section.

1. Proposed Model: Multichannel CNN-BiGRU
The script Mulichannel CNN-BiGRU-model.py implements the Four-Fusion Scheme described in the paper, which effectively integrates features from different sensor modalities.

2. Baseline Comparisons
To reproduce the results in Table 4 and Table 5 of the paper, we provide:

SVM_har_train.py: Traditional machine learning approach.
VGG_har_train.py: Standard VGG architecture adapted for 1D sensor signals.
RestNet_har_train.py: Residual Network implementation for HAR.

3.Usage

# 1. Clone the repository
git clone https://github.com/XBMU-WSMC-lab/WSMC-HAR-AGH-Code.git

# 2. Visualise the data
python "Data visualisation.py"

# 3. Train the proposed model
python "Mulichannel CNN-BiGRU-model.py"


📊 Data Availability
Due to ethical and privacy considerations, the dataset is shared in two tiers:

Publicly Available: The de-identified IMU (Inertial) sensor data is available at [Link to Zenodo/Figshare/GitHub].
Restricted Access: The Physiological signal data is restricted due to institutional privacy policies. Access may be granted for academic purposes upon reasonable request to the corresponding author and signing a Data Use Agreement (DUA).


