import argparse
import cv2
import time
import torch
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import deque, defaultdict

from fall_detection_module import DetectionConfig, MultiPersonFallDetector, COCO_SKELETON_EDGES
from action_recognition_module import LSTMActionRecognizer, FRAME_VECTOR_SIZE

YOLO_POSE_MODEL = "yolo11s-pose.pt"
OLD_ACTION_MODEL = r"C:\Users\Tai\Desktop\DoAnBD\Fallsense\runs\pose_action\pose-skeleton-fall\weights\best.pt"
OLD_ACTION_META = r"C:\Users\Tai\Desktop\DoAnBD\Fallsense\runs\pose_action\pose-skeleton-fall\pose_classifier_meta.json"
LSTM_MODEL_PATH = r"C:\Users\Tai\Desktop\DoAnBD\Fallsense\Fallsense\runs\action_training\lstm-fall-detector\weights\best.pt"
EXCEL_LOG_PATH = "fall_detection_logs.xlsx"

SEQ_LENGTH = 150
LSTM_CONF_THRESHOLD = 0.7  # Tăng ngưỡng tin cậy của LSTM lên cao hơn
STATIC_CONF_THRESHOLD = 0.6 # Tăng ngưỡng của module cũ để tránh báo sai khi đứng
ALERT_COOLDOWN = 5

def load_lstm(path, device):
    ckpt = torch.load(path, map_location=device)
    model = LSTMActionRecognizer(
        input_size=FRAME_VECTOR_SIZE,
        hidden_size=ckpt["hidden_size"],
        num_layers=ckpt["num_layers"],
        num_classes=len(ckpt["labels"]),
        dropout=ckpt["dropout"]
    )
    model.load_state_dict(ckpt["state_dict"])
    model.to(device)
    model.eval()
    return model, ckpt["labels"]

def update_excel_log(data_dict):
    df = pd.DataFrame([data_dict])
    if not Path(EXCEL_LOG_PATH).exists():
        df.to_excel(EXCEL_LOG_PATH, index=False, engine='openpyxl')
    else:
        with pd.ExcelWriter(EXCEL_LOG_PATH, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            try:
                existing_df = pd.read_excel(EXCEL_LOG_PATH)
                updated_df = pd.concat([existing_df, df], ignore_index=True)
                updated_df.to_excel(writer, index=False)
            except Exception:
                df.to_excel(writer, index=False)

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    config = DetectionConfig(
        yolo_model_path=YOLO_POSE_MODEL,
        action_model_path=OLD_ACTION_MODEL,
        action_meta_path=OLD_ACTION_META,
        device=device
    )
    detector = MultiPersonFallDetector(config)
    lstm_model, lstm_labels = load_lstm(LSTM_MODEL_PATH, device)
    
    person_buffers = defaultdict(lambda: deque(maxlen=SEQ_LENGTH))
    last_alert_time = defaultdict(float)
    
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success: break

            events = detector.process_frame(frame)
            for event in events:
                track_id = event.track_id
                
                # Trích xuất Keypoints
                kpts_array = np.array(event.keypoints)
                current_kpts = kpts_array.flatten().tolist()
                person_buffers[track_id].append(current_kpts)
                
                # 1. Tính toán Heuristic bổ sung: Tỷ lệ Box (Chiều cao / Chiều rộng)
                x1, y1, x2, y2 = event.bbox
                box_h = y2 - y1
                box_w = x2 - x1
                is_horizontal = box_w > box_h  # Người nằm ngang thì chiều rộng thường lớn hơn chiều cao
                
                # 2. Lấy kết quả Module cũ
                is_static_fall = event.fall and event.confidence > STATIC_CONF_THRESHOLD
                
                # 3. Lấy kết quả LSTM
                is_lstm_fall = False
                lstm_conf = 0.0
                if len(person_buffers[track_id]) == SEQ_LENGTH:
                    input_data = torch.tensor([list(person_buffers[track_id])], dtype=torch.float32).to(device)
                    with torch.no_grad():
                        logits = lstm_model(input_data)
                        probs = torch.softmax(logits, dim=1)
                        conf, idx = torch.max(probs, dim=1)
                        if lstm_labels[idx.item()].lower() == "fall":
                            lstm_conf = conf.item()
                            is_lstm_fall = lstm_conf > LSTM_CONF_THRESHOLD

                # LOGIC KẾT HỢP CHỐNG SAI SỐ:
                # Phải thỏa mãn LSTM báo ngã VÀ (Module tĩnh báo ngã HOẶC người đang nằm ngang)
                final_fall = is_lstm_fall and (is_static_fall or is_horizontal)
                
                if final_fall:
                    current_time = time.time()
                    if current_time - last_alert_time[track_id] > ALERT_COOLDOWN:
                        update_excel_log({
                            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Person_ID": track_id,
                            "Static_Conf": round(event.confidence, 2),
                            "LSTM_Conf": round(lstm_conf, 2),
                            "Status": "FALL CONFIRMED"
                        })
                        last_alert_time[track_id] = current_time

                color = (0, 0, 255) if final_fall else (0, 255, 0)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(frame, f"ID:{track_id} {'FALL' if final_fall else 'OK'}", (int(x1), int(y1)-25), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                for start, end in COCO_SKELETON_EDGES:
                    if start < len(event.keypoints) and end < len(event.keypoints):
                        p1, p2 = event.keypoints[start], event.keypoints[end]
                        if len(p1) >= 3 and len(p2) >= 3 and p1[2] > 0.1 and p2[2] > 0.1:
                            cv2.line(frame, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), color, 2)

            cv2.imshow("Fallsense Hybrid - Anti False Positive", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()