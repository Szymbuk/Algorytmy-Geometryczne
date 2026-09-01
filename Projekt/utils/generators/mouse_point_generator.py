import matplotlib.pyplot as plt
from Projekt.utils.classes.Point import Point
import numpy as np

def get_points_interactive(x_min=0, x_max=1000, y_min=0, y_max=1000) -> np.array:
    # W Jupyter Notebook odkomentuj poniższą linię (w czystym Pythonie jest zbędna dzięki plt.ion())
    # %matplotlib tk

    points = []
    active = True

    # Funkcja rysująca pojedynczy punkt
    def draw_point(point):
        plt.scatter(point[0], point[1], color="red")
        plt.show()

    def onclick(event):
        nonlocal active

        # Sprawdzenie czy kliknięcie było wewnątrz osi wykresu
        if event.xdata is None or event.ydata is None:
            return

        if event.dblclick and active:
            # Mouse1 (Lewy Przycisk) - Dodaj punkt
            if event.button == 1:
                new_point = np.array([event.xdata, event.ydata])
                points.append(new_point)


                # Rysujemy
                draw_point([event.xdata, event.ydata])
                print(f"Dodano punkt: ({new_point[0]:.2f}, {new_point[1]:.2f})")

            # Mouse3 (Prawy Przycisk) - Wyjdź
            elif event.button == 3:
                active = False
                print(f"Zakończono. Zebrano {len(points)} punktów.")
                plt.pause(1)
                plt.close()

    fig, ax = plt.subplots()

    # Konfiguracja wyglądu
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')
    ax.set_title("Lewy przycisk (2x): Dodaj punkt | Prawy przycisk (2x): Zakończ")

    # Podpięcie zdarzenia
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    # Wyświetlenie
    plt.tight_layout()
    plt.ion()  # Włączenie trybu interaktywnego (kluczowe dla działania draw_point)
    plt.show()

    return np.array(points)