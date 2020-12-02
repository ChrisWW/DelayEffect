import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write
import math

samplerate, data = wavfile.read('Struna 2 - A.wav') #Plik mono!!!!!

print ("Częstotliwość próbkowania ......... " + str(samplerate))
print ("Liczba próbek ..................... " + str(len(data)))


# Delay w sekundach
print("O jaką wartość sekund przesunąć?: ")
Przesuniecie_sekundy = float(input())

if Przesuniecie_sekundy < 0:
    print("Wartosc jest mniejsza od 0, wstaw wartość dodatnią")
    Przesuniecie_sekundy = float(input())

# Ilość probek o którą przesuwamy dane
Przesuniecie_probki = round(Przesuniecie_sekundy * samplerate, 0)
Przesuniecie_probki = int(Przesuniecie_probki)

##########################
print("O jaką wartość wzmocnić sygnał od 0 do 1: ")
Opoznienie_rate = float(input())

if Opoznienie_rate < 0:
    print("Wartosc jest mniejsza od 0, wstaw wartość w przedziale <0, 1>")
    Opoznienie_rate = float(input())

elif Opoznienie_rate > 1:
    print("Wartosc jest większa od 1, wstaw wartość w przedziale <0, 1>")
    Opoznienie_rate = float(input())

##########################

# o probek przesunac data
Przesuniecie_probki = int(Przesuniecie_sekundy * samplerate)

# tworzenie ilosci przesunietych probek
Dane_zerowe = np.zeros_like(data[0:Przesuniecie_probki])

# tworzenie przesunietej data
Dane_przesuniete = np.append(Dane_zerowe, data[0:len(data)])

# zmiana wartosci probek
Dane_przesuniete = np.multiply(Dane_przesuniete, Opoznienie_rate)
Dane_przesuniete = Dane_przesuniete.astype(np.int16)

# wyrownanie liczby elementow
Dane_1 = np.append(data, Dane_zerowe)

# uzycie funkcji add, w celu dodania dwoch tabel o tej samej ilosci danych
Przesuniete_dane_1 = np.add(Dane_1, Dane_przesuniete)

print("Prosze poczekać na wszystkie wyniki\nProcessing...")

write("output_delay.wav", samplerate, Przesuniete_dane_1) #Zapisuje plik .wav po zmianie

# Obliczenie mocy

suma_poczatek = 0.0
for x in data:
    suma_poczatek = suma_poczatek + float(x ** 2)
moc0_pocz = float(2**15) # Przy liczbie bitow 16 -> 2^(M-1) = 2^15
moc1_pocz = (suma_poczatek / len(data))
dB_pocz = float(10*math.log10(moc1_pocz/moc0_pocz))

print("Przed efektem:")
print("Wartość mocy wynosi : ", moc1_pocz)
print("Wartość dB wynosi : ", dB_pocz)

print("")

suma_out = 0.0
for x in Przesuniete_dane_1:
    suma_out = suma_out + float(x ** 2)
moc0 = float(2**15) # Przy liczbie bitow 16 -> 2^(M-1) = 2^15
moc1 = (suma_out / len(Przesuniete_dane_1))
dB = float(10*math.log10(moc1/moc0))

print("Po efekcie:")
print("Wartość mocy wynosi : ", moc1)
print("Wartość dB wynosi : ", dB)
print("")


#Rysowanie wykresu
print("Czy narysowac wykres? Odpowiedz Tak/Nie")
wykres = str(input())

if wykres == "Tak" or wykres == "tak" or wykres == "t":

    data_x = range(len(Przesuniete_dane_1))
    plt.plot(data_x, Przesuniete_dane_1)
    plt.show()

elif wykres == "Nie" or wykres == "nie" or wykres == "n":
    print("Wybrałeś, aby nie rysować wykresu")
else:
    print("Niepoprawny wybór")

