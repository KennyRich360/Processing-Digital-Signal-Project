# Bibliotecas e pacotes necessários para implementação dos filtros e janelas
import librosa
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import time
from scipy.signal import butter, filtfilt
from scipy.io import wavfile


caminho_sinal = librosa.ex('trumpet') ## caminho pro arquivo a ser carregado


sinal, freq_amostragem = librosa.load(caminho_sinal)

figura, eixo = plt.subplots(2,1, sharex = True)

# Plota gráfico de tempo
librosa.display.waveshow(sinal, sr = freq_amostragem, ax = eixo[0])

# Plota espectograma
D = librosa.amplitude_to_db(np.abs(librosa.stft(sinal)), ref = np.max)
librosa.display.specshow(D, y_axis = 'linear', x_axis = 's', sr = freq_amostragem, ax = eixo[1])

eixo[0].set_title("Sinal Original")
eixo[1].set_title("Espectograma")
eixo[0].set_xlabel("")
eixo[1].set_xlabel("tempo (s)")

# Plota dft
dft = librosa.stft(sinal)
magnitude = np.mean(np.abs(dft), axis = 1)
frequencias = librosa.fft_frequencies(sr = freq_amostragem)

plt.plot(frequencias, magnitude)
plt.xlabel('Frequências (Hz)')
plt.ylabel('Magnitude')
plt.xlim([0, freq_amostragem / 2])  # Plota até o limie de nyquist
plt.ylim([0,np.max(magnitude) + 0.5])
plt.show()

# Extrai magnitude e fase dos componentes da  dft do sinal
magnitude_ruido = np.abs(librosa.stft(sinal))
fase = np.angle(librosa.stft(sinal))

# Faixa de banda a qual vai ser adcionada o ruído.
freq_inferior = 5000
freq_superior = 7000

# Índices da faixa de banda no vetor de magnitude
indice_inferior = librosa.core.fft_frequencies(sr = freq_amostragem).searchsorted(freq_inferior)
indice_superior = librosa.core.fft_frequencies(sr = freq_amostragem).searchsorted(freq_superior)

# Adciona ruído gaussiano ao vetor da dft
nivel_de_ruido = 10
magnitude_ruido[indice_inferior:indice_superior, :] += nivel_de_ruido * np.random.randn(indice_superior - indice_inferior, magnitude_ruido.shape[1])

# Reconstroi sinal com ruído
dft_ruido = magnitude_ruido * np.exp(1j * fase)
sinal_ruido = librosa.istft(dft_ruido)

# Plota sinal e DTF com ruído
figura, eixo = plt.subplots(2,2, sharex = 'col', figsize=(10,10))

librosa.display.waveshow(sinal, sr = freq_amostragem, ax = eixo[0,0]) # Sinal original

librosa.display.waveshow(sinal_ruido, sr = freq_amostragem, ax = eixo[1,0]) # Sinal com ruído

dft = librosa.stft(sinal) # dft original
magnitude = np.mean(np.abs(dft), axis = 1)
frequencias = librosa.fft_frequencies(sr = freq_amostragem)
eixo[0,1].plot(frequencias, magnitude)

dft = librosa.stft(sinal_ruido) # dft com ruído
magnitude_ruido = np.mean(np.abs(dft_ruido), axis = 1)
frequencias = librosa.fft_frequencies(sr = freq_amostragem)
eixo[1,1].plot(frequencias, magnitude_ruido)

# Legenda da figura
eixo[0,0].set(title = "Sinais")
eixo[0,0].set_xlabel('')
eixo[0,1].set(title = "Transformadas")
eixo[1,0].set_xlabel("tempo (s)")
eixo[1,1].set_xlabel("frequência (Hz)")
eixo[0,0].set_ylabel("Original")
eixo[1,0].set_ylabel("Com Ruído")

sd.play(sinal, freq_amostragem)
time.sleep(10)
sd.stop()

sd.play(sinal_ruido, freq_amostragem)
time.sleep(10)
sd.stop()

D# Define parametros necessarios ao filtro
freq_corte = 5000
ordem = 6

# Normaliza frequência em relação frequência de nyquist
freq_nyquist = 0.5 * freq_amostragem
freq_normalizada = freq_corte / freq_nyquist

# Define o filtro passa baixa
b, a = butter(ordem, freq_normalizada, btype = 'low', analog = False)

# Aplica filtro a sinal com ruído
sinal_filtrado1 = filtfilt(b, a, sinal_ruido)

# Plota sinal filtrado
grafico, eixo = plt.subplots(3,1, figsize=(10,16))
librosa.display.waveshow(sinal_filtrado1, sr = freq_amostragem, ax = eixo[0])

# Plota espectograma do sinal filtrado
Decibeis = librosa.amplitude_to_db(np.abs(librosa.stft(sinal_filtrado1)), ref = np.max)
librosa.display.specshow(Decibeis, sr = freq_amostragem, ax = eixo[1],
                         y_axis = 'linear', x_axis = 's')

# Plot  dft do sinal filtrado
dft = librosa.stft(sinal_filtrado1)
magnitudes = np.mean(np.abs(dft), axis = 1)
frequencias = librosa.fft_frequencies(sr = freq_amostragem)
eixo[2].plot(frequencias, magnitudes)

# Legenda do gráfico
eixo[0].set_xlabel("tempo (s)")
eixo[0].set_title("Sinal Filtrado")
eixo[1].set_title("Espectograma Sinal Filtrado")
eixo[1].set_xlabel("tempo (s)")
eixo[2].set_title("DTF do Sinal Filtrado")
eixo[2].set_xlabel("frequência (Hz)")

sd.play(sinal_filtrado1, freq_amostragem)
time.sleep(10)
sd.stop()

# Define parametros necessarios ao filtro
freq_corte = 5000
ordem = 6

# Normaliza frequência em relação frequência de nyquist
freq_nyquist = 0.5 * freq_amostragem
freq_normalizada = freq_corte / freq_nyquist

# Define o filtro passa baixa
b, a = butter(ordem, freq_normalizada, btype = 'high', analog = False)

# Aplica filtro a sinal com ruído
sinal_filtrado2 = filtfilt(b, a, sinal_ruido)

# Plota sinal filtrado
grafico, eixo = plt.subplots(3,1, figsize=(10,16))
librosa.display.waveshow(sinal_filtrado2, sr = freq_amostragem, ax = eixo[0])

# Plota espectograma do sinal filtrado
Decibeis = librosa.amplitude_to_db(np.abs(librosa.stft(sinal_filtrado2)), ref = np.max)
librosa.display.specshow(Decibeis, sr = freq_amostragem, ax = eixo[1],
                         y_axis = 'linear', x_axis = 's')

# Plota dft do sinal filtrado
dft = librosa.stft(sinal_filtrado2)
magnitudes = np.mean(np.abs(dft), axis = 1)
frequencias = librosa.fft_frequencies(sr = freq_amostragem)
eixo[2].plot(frequencias, magnitudes)

# Legenda do gráfico
eixo[0].set_xlabel("tempo (s)")
eixo[0].set_title("Sinal Filtrado")
eixo[1].set_title("Espectograma Sinal Filtrado")
eixo[1].set_xlabel("tempo (s)")
eixo[2].set_title("DTF do Sinal Filtrado")
eixo[2].set_xlabel("frequência (Hz)")

sd.play(sinal_filtrado2, freq_amostragem)
time.sleep(10)
sd.stop()

tamanho_janela = int(sinal_ruido.shape[0] / 10)
janela = np.hanning(tamanho_janela)

# Define janela do sinal
janela_sinal_ruido = sinal_ruido[:tamanho_janela] * janela

# Plota janela
grafico, eixo = plt.subplots(2,2, figsize=(13,10))
eixo[0,0].plot(np.arange(tamanho_janela), janela)

# Plota janela do sinal com ruído
librosa.display.waveshow(janela_sinal_ruido, sr = freq_amostragem, ax = eixo[0,1])

# Plota módulo da dft da janela do sinal com ruído
dft_ruido = librosa.stft(janela_sinal_ruido)
magnitudes = np.mean(np.abs(dft_ruido), axis = 1)
frequencias = librosa.fft_frequencies(sr = freq_amostragem)
eixo[1,0].plot(frequencias, magnitudes)

# Plota fase da dft da janela do sinal
fases = np.mean(np.angle(dft_ruido), axis = 1)
frequencias = librosa.fft_frequencies(sr = freq_amostragem)
eixo[1,1].plot(frequencias, fases)


# Legenda do grafico
eixo[0,0].set_title("Janela de Hann")
eixo[0,0].set_xlabel("amostra (n)")
eixo[0,1].set_xlabel("tempo (s)")
eixo[0,1].set_title("Janela do Sinal Com Ruído")
eixo[1,0].set_title("DTF da Janela do sinal com Ruído")
eixo[1,0].set_xlabel("frequência (Hz)")
eixo[1,1].set_title("Fase da DTF da Janela do Sinal com Ruído")
eixo[1,1].set_xlabel("frequência (Hz)")

tamanho_janela = int(sinal_ruido.shape[0] / 10)
janela = np.bartlett(tamanho_janela)

# Define janela do sinal
janela_sinal_ruido = sinal_ruido[:tamanho_janela] * janela

# Plota janela
grafico, eixo = plt.subplots(2,2, figsize=(13,10))
eixo[0,0].plot(np.arange(tamanho_janela), janela)

# Plota janela do sinal com ruído
librosa.display.waveshow(janela_sinal_ruido, sr = freq_amostragem, ax = eixo[0,1])

# Plota módulo da dft da janela do sinal com ruído
dft_ruido = librosa.stft(janela_sinal_ruido)
magnitudes = np.mean(np.abs(dft_ruido), axis = 1)
frequencias = librosa.fft_frequencies(sr = freq_amostragem)
eixo[1,0].plot(frequencias, magnitudes)

# Plota fase da dft da janela do sinal
fases = np.mean(np.angle(dft_ruido), axis = 1)
frequencias = librosa.fft_frequencies(sr = freq_amostragem)
eixo[1,1].plot(frequencias, fases)


# Legenda do gráfico
eixo[0,0].set_title("Janela de Bartlett")
eixo[0,0].set_xlabel("amostra (n)")
eixo[0,1].set_xlabel("tempo (s)")
eixo[0,1].set_title("Janela do Sinal Com Ruído")
eixo[1,0].set_title("DTF da Janela do sinal com Ruído")
eixo[1,0].set_xlabel("frequência (Hz)")
eixo[1,1].set_title("Fase da DTF da Janela do Sinal com Ruído")
eixo[1,1].set_xlabel("frequência (Hz)")

# Escreve sinais filtrados por passa baixa e alta em arquivos 1 e 2
arquivo_saida = 'sinal_filtrado1.wav'
wavfile.write(arquivo_saida, freq_amostragem, sinal_filtrado1)
arquivo_saida = 'sinal_filtrado2.wav'
wavfile.write(arquivo_saida, freq_amostragem, sinal_filtrado2)