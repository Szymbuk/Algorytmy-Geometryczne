import matplotlib.pyplot as plt
# Upewnij się, że ścieżka importu jest poprawna dla Twojej struktury projektu
from bitalg.Projekt.utils.classes.Point import Point

def get_points_interactive(x_min=0, x_max=1000, y_min=0, y_max=1000):
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
                # Tworzymy obiekt Point zgodnie z Twoją klasą (teraz z ID)
                new_point = Point(event.xdata, event.ydata)
                points.append(new_point)


                # Rysujemy
                draw_point([event.xdata, event.ydata])
                print(f"Dodano punkt ID {new_point.get_id()}: ({new_point.get_x():.2f}, {new_point.get_y():.2f})")

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
    plt.show() # Usunięto block=True, aby zachować spójność z działającym przykładem

    return points