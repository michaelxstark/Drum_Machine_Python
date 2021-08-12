
import numpy as np
import sounddevice as sd
from scipy import signal as sig
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(500, 500, 300, 310)
    win.setWindowTitle('XO_Drums')
    # sd.query_devices()
    # sd.default.device = 'BlackHole 16ch, Core Audio' only for scree-rec

    sr = 44100

    def play_kick():
        kick = sd.play(KICK, sr)

    def play_snare():
        snare = sd.play(SNARE, sr)

    def play_hihat():
        hihat = sd.play(HIHAT, sr)

    def play_hihat_o():
        hihat_o = sd.play(OPENHAT, sr)

    def play_claves():
        claves = sd.play(WOODBLOCK, sr)

    def play_midtom():
        midtom = sd.play(MIDTOM, sr)

    def stop():
        stop = sd.stop()

    button = QPushButton(win)
    button.setText('KICK')
    button2 = QPushButton(win)
    button2.setText('SNARE')
    button2.move(0, 30)
    button3 = QPushButton(win)
    button3.setText('HIHAT_C')
    button3.move(0, 60)
    button4 = QPushButton(win)
    button4.setText('HIHAT_O')
    button4.move(0, 90)
    button5 = QPushButton(win)
    button5.setText('CLAVES')
    button5.move(0, 120)
    button6 = QPushButton(win)
    button6.setText('TOM')
    button6.move(0, 150)

    button.clicked.connect(play_kick)
    button2.clicked.connect(play_snare)
    button3.clicked.connect(play_hihat)
    button4.clicked.connect(play_hihat_o)
    button5.clicked.connect(play_claves)
    button6.clicked.connect(play_midtom)

    kick_pat = QLineEdit(win)
    kick_pat.move(180, 5)
    kick_pat.resize(100, 20)
    snare_pat = QLineEdit(win)
    snare_pat.move(180, 35)
    snare_pat.resize(100, 20)
    hihat_pat = QLineEdit(win)
    hihat_pat.move(180, 65)
    hihat_pat.resize(100, 20)
    open_hat_pat = QLineEdit(win)
    open_hat_pat.move(180, 95)
    open_hat_pat.resize(100, 20)
    wood_block_pat = QLineEdit(win)
    wood_block_pat.move(180, 125)
    wood_block_pat.resize(100, 20)
    mid_tom_pat = QLineEdit(win)
    mid_tom_pat.move(180, 155)
    mid_tom_pat.resize(100, 20)

    rep = QLineEdit(win)
    rep.move(100, 200)
    rep.resize(100, 20)

    # Tempo for Duration
    tempo = QLineEdit(win)
    tempo.move(100, 225)
    tempo.resize(100, 20)

    run_button = QPushButton(win)
    run_button.setText('RUN')
    run_button.move(100, 250)

    stop_button = QPushButton(win)
    stop_button.setText('STOP')
    stop_button.move(100, 275)

    def run_pattern():
        duration = (60000 / int(tempo.text())) / 4

        # Instruments

        def kick(frq, dur):
            line = np.linspace(0, 1, int((sr / 1000) * dur))
            line2 = np.sqrt(line)
            line3 = line2 * frq - 0.15
            line4 = np.cos(line3)
            envexp = 0.5 ** (25 * line)
            kick = line4 * envexp
            sos = sig.butter(2, 300, 'lp', analog=False, fs=1000, output='sos')
            filtered = sig.sosfilt(sos, kick)
            return filtered * 3

        KICK = kick(30, duration)

        def snare(frq, dur):
            noise = np.random.random_sample(int((sr / 1000) * dur)) * 2 - 1
            line = np.linspace(0, 1, int((sr / 1000) * dur))
            envexp = 0.5 ** (12.5 * line)
            sos = sig.butter(4, 20, 'hp', analog=False, fs=1000, output='sos')
            filtered = sig.sosfilt(sos, (noise * envexp))
            sos = sig.butter(1, [5, 40], 'bp', fs=1000, output='sos')
            filtered_2 = sig.sosfilt(sos, filtered)

            def sine_tone(frq, dur):
                sr = 44100
                line = np.linspace(0, 1, int((sr / 1000) * dur))
                t = np.arange(int((sr / 1000) * dur)) / sr
                envexp = 0.5 ** (25 * line)
                sine = 1 * np.sin(2 * np.pi * frq * t) * envexp
                return sine
            snare = (filtered_2 + sine_tone(frq, dur)) * 4
            return snare

        SNARE = snare(250, duration)

        def hi_hat(dur):
            line = np.linspace(1, 0, int((sr / 1000) * dur))
            line2 = line ** 4

            def square_tone(frq, dur):
                sr = 44100
                line = np.linspace(0, 1, int((sr / 1000) * dur))
                t = np.arange(int((sr / 1000) * dur)) / sr
                envexp = 0.5 ** (25 * line)
                sine = 1 * np.sin(2 * np.pi * frq * t)
                square = np.where(sine > 0, 1, -1) * envexp
                return square
            noise = np.random.random_sample(int((sr / 1000) * dur)) * 2 - 1
            high_noise = square_tone(350, dur) + square_tone(800, dur) + (noise / 4)
            sos = sig.butter(10, 100, 'hp', analog=False, fs=1000, output='sos')
            filtered = sig.sosfilt(sos, high_noise)
            sos = sig.butter(2, 100, 'hp', analog=False, fs=1000, output='sos')
            filtered_2 = sig.sosfilt(sos, filtered)
            line3 = filtered_2 * line2 * 4
            return line3

        HIHAT = hi_hat(duration)

        def open_hat(dur):
            line = np.linspace(1, 0, int((sr / 1000) * dur))
            line2 = line ** 0.2

            def square_tone(frq, dur):
                sr = 44100
                line = np.linspace(0, 1, int((sr / 1000) * dur))
                t = np.arange(int((sr / 1000) * dur)) / sr
                envexp = 0.5 ** (25 * line)
                sine = 1 * np.sin(2 * np.pi * frq * t)
                square = np.where(sine > 0, 1, -1) * envexp
                return square
            noise = np.random.random_sample(int((sr / 1000) * dur)) * 2 - 1
            high_noise = square_tone(350, dur) + square_tone(800, dur) + (noise / 4)
            sos = sig.butter(10, 50, 'hp', analog=False, fs=1000, output='sos')
            filtered = sig.sosfilt(sos, high_noise)
            sos = sig.butter(2, 50, 'hp', analog=False, fs=1000, output='sos')
            filtered_2 = sig.sosfilt(sos, filtered)
            line3 = filtered_2 * line2 * 4
            return line3

        OPENHAT = open_hat(duration)

        def wood_block(frq, ratio, amount, dur):
            def sine_tone(frq, dur):
                sr = 44100
                line = np.linspace(0, 1, int((sr / 1000) * dur))
                t = np.arange(int((sr / 1000) * dur)) / sr
                envexp = 0.5 ** (25 * line)
                sine = 1 * np.sin(2 * np.pi * frq * t) * envexp
                return sine
            fm = frq + sine_tone(frq * ratio, dur) * amount
            sr = 44100
            line = np.linspace(0, 1, int((sr / 1000) * dur))
            t = np.arange(int((sr / 1000) * dur)) / sr
            envexp = 0.5 ** (25 * line)
            sine = 1 * np.sin(2 * np.pi * fm * t) * envexp
            return sine

        WOODBLOCK = wood_block(880, 2.25, 80, duration)

        def mid_tom(frq, dur):
            line = np.linspace(1, 0, int((sr / 1000) * dur))
            line2 = line ** 3.5
            freq = np.linspace(np.sqrt(frq + (frq * 0.5)), np.sqrt(frq), int((sr / 1000) * dur))
            freq2 = freq ** 2
            t = np.arange(int((sr / 1000) * dur)) / sr
            sine = 1 * np.sin(2 * np.pi * freq2 * t) * line2 * 2.5
            noise = np.random.random_sample(int((sr / 1000) * dur)) * 2 - 1
            sos = sig.butter(10, 70, 'hp', analog=False, fs=1000, output='sos')
            filtered = sig.sosfilt(sos, noise)
            sos = sig.butter(2, 30, 'lp', analog=False, fs=1000, output='sos')
            filtered_2 = sig.sosfilt(sos, filtered)
            tom = sine + ((filtered_2 * line2) * 0.085)
            return tom

        MIDTOM = mid_tom(175, duration)

        # simple panning - algorithm

        def panner(x, angle):
            # pan a mono audio source into stereo
            # x is a numpy array, angle is the angle in radiants
            left = np.sqrt(2)/2.0 * (np.cos(angle) - np.sin(angle)) * x
            right = np.sqrt(2)/2.0 * (np.cos(angle) + np.sin(angle)) * x
            return np.dstack((left, right))[0]

        def pause(note):
            pause = np.zeros_like(note)
            return pause

        kick_seq = np.concatenate([KICK if char == 'x' else pause(KICK)
                                   for char in kick_pat.text()])
        snare_seq = np.concatenate([SNARE if char == 'x' else pause(SNARE)
                                    for char in snare_pat.text()])
        hihat_seq = np.concatenate([HIHAT if char == 'x' else pause(HIHAT)
                                    for char in hihat_pat.text()])
        open_hat_seq = np.concatenate([OPENHAT if char == 'x' else pause(OPENHAT)
                                       for char in open_hat_pat.text()])
        wood_block_seq = np.concatenate(
            [WOODBLOCK if char == 'x' else pause(WOODBLOCK) for char in wood_block_pat.text()])
        mid_tom_seq = np.concatenate([MIDTOM if char == 'x' else pause(MIDTOM)
                                      for char in mid_tom_pat.text()])

        panning_values = [0.03, 0, -15, 15, -35, 35]
        instrument_seq = [kick_seq, snare_seq, hihat_seq, open_hat_seq, wood_block_seq, mid_tom_seq]
        panned_instruments = [panner(instrument_seq[i], panning_values[i])
                              for i in range(len(panning_values))]
        vol_mix_values = [1, 1, 0.38, 0.35, 0.6, 0.6]
        vol_pan_inst = [np.tile(panned_instruments[j] * vol_mix_values[j],
                                (int(rep.text()), 1)) for j in range(len(vol_mix_values))]
        beat = sum(vol_pan_inst)
        sd.play(beat * 0.5, sr)

    run_button.clicked.connect(run_pattern)
    stop_button.clicked.connect(stop)

    win.show()
    app.exec()


window()
