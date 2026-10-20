import cv2
import mediapipe as mp
import numpy as np

# MediaPipe yüz örgü (Face Mesh) modülünü başlat
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Kamerayı başlat (0 genelde dahili web kamerasıdır)
cap = cv2.VideoCapture(0)

# Öklid mesafesi hesaplamak için yardımcı fonksiyon
def calculate_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Kamera görüntüsü alınamadı.")
        break

    # Performans için görüntüyü yatay çevir ve RGB formatına dönüştür
    image = cv2.flip(image, 1)
    h, w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Yüz analizi yap
    results = face_mesh.process(rgb_image)
    
    duygu = "Analiz Ediliyor..."
    renk = (255, 255, 255)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Landmark'ları piksel koordinatlarına çevir
            landmarks = []
            for lm in face_landmarks.landmark:
                landmarks.append((int(lm.x * w), int(lm.y * h)))

            if len(landmarks) > 468:
                # Önemli noktaların indeksleri (MediaPipe Face Mesh Map)
                # Dudak üst ve alt: 13, 14
                # Ağız sol ve sağ kenarları: 61, 291
                # Göz alt ve üst kapakları (sol göz için örnek): 159, 145
                # Kaş ve göz mesafesi için örnek indeksler
                
                # Dudak açıklığı oranı
                upper_lip = landmarks[13]
                lower_lip = landmarks[14]
                lip_distance = calculate_distance(upper_lip, lower_lip)
                
                # Ağız genişliği
                left_mouth = landmarks[61]
                right_mouth = landmarks[291]
                mouth_width = calculate_distance(left_mouth, right_mouth)
                
                # Basit bir oranlama (Gülümseme / Şaşkınlık tespiti için)
                mouth_ratio = lip_distance / mouth_width if mouth_width > 0 else 0

                # Basit kural tabanlı duygu eşikleri (Ortam ışığına göre ayarlanabilir)
                if mouth_ratio > 0.35:
                    duygu = "Saskin / Heyecanli (Surprised)"
                    renk = (0, 255, 255) # Sarı
                elif mouth_ratio > 0.18:
                    duygu = "Mutlu / Gülümsüyor (Happy)"
                    renk = (0, 255, 0) # Yeşil
                else:
                    duygu = "Notr / Sakin (Neutral)"
                    renk = (255, 0, 0) # Mavi

    # Ekrana duygu durumunu yazdır
    cv2.putText(image, f"Duygu: {duygu}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, renk, 2, cv2.LINE_AA)
    cv2.putText(image, "Cikis icin 'q' tusuna basin", (30, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    # Görüntüy göster
    cv2.imshow('MediaPipe Duygu Analizi', image)

    # 'q' tuşuna basılırsa döngüyü kır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()