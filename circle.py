import time
from turtle import *

# Ekran ayarları
screen = Screen()
screen.setup(width=900, height=600)
screen.bgcolor("black")
screen.tracer(
    0
)  # Animasyonun akıcı ve hızlı çalışması için ekran güncellemelerini kapatıyoruz

# Yazı için kaplumbağa
writer = Turtle()
writer.hideturtle()
writer.penup()

# İz efekti için arka plan kaplumbağası (Kuyruk efekti)
tracer_t = Turtle()
tracer_t.hideturtle()
tracer_t.speed(0)

colors = ["yellow", "red"]

# Uçuş animasyonu (Ekranın sol altından sağ üstüne doğru)
x = -350
y = -250

for i in range(120):
  writer.clear()  # Önceki yazıyı sil

  # Arkadaki kuyruk/parçacık efekti
  tracer_t.penup()
  tracer_t.goto(x - 15, y - 15)
  tracer_t.color(colors[i % 2])
  tracer_t.dot(25)  # Her adımda arkaya renkli noktalar bırakır

  # Yazıyı konumlandır ve yaz (Uzun yazı olduğu için boyutu dengeledik)
  writer.goto(x, y)
  writer.color(colors[i % 2])  # Sarı-Kırmızı yanıp sönme efekti
  writer.write(
      "Günlerden_Galatasaray",
      align="center",
      font=("Arial", int(25 + (i * 0.3)), "bold"),
  )

  screen.update()  # Ekranı yenile
  time.sleep(0.02)  # Hata burada düzeltildi: 0,2 yerine 0.02 yapıldı

  # Yazıyı çapraz yukarı ve sağa hareket ettir
  x += 5
  y += 4

# Son duruşta ekranda kalmasını sağla
done()