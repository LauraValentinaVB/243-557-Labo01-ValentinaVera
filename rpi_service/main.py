"""Point d'entrée du service Raspberry."""

import time

from rpi_service.raspberry_controller import (
    RaspberryController,
)


def main() -> None:
    """Exécute le service Raspberry."""

    controller = RaspberryController()
    controller.start()

    print("Service Raspberry démarré.")

    try:
        while True:
            controller.publish_measurements()
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nArrêt du service Raspberry.")

    finally:
        controller.stop()


if __name__ == "__main__":
    main()