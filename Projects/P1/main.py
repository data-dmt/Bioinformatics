"""
main.py

Punto de entrada principal del simulador del
dogma central de la biología molecular.

Coordina:

1. Entrada y validación del ADN.
2. Creación de la molécula de ADN.
3. Replicación.
4. Transcripción.
5. Traducción.
6. Presentación de resultados.
"""

from models import DNA
from validation import validate_dna
from replication import replicate
from transcription import transcribe
from translation import translate


from output import (
    print_title,
    show_initial_dna,
    show_replication_result,
    show_transcription_result,
    show_translation_result,
    show_final_summary
)


# ============================================================
# DEFAULT SEQUENCE
# ============================================================

DEFAULT_SEQUENCE = "ATGCCATGGAATGCTTAA"


# ============================================================
# USER INPUT
# ============================================================

def request_dna_sequence() -> str:
    """
    Solicita al usuario una secuencia de ADN.

    La función continúa preguntando hasta que el usuario
    introduce una secuencia válida.

    Returns
    -------
    str
        Secuencia de ADN validada.
    """

    print()
    print("Introduce una secuencia de ADN.")
    print()
    print("Solo se permiten las bases:")
    print("A, T, C y G")
    print()

    print(
        "Puedes pulsar ENTER sin escribir nada "
        "para utilizar la secuencia de demostración:"
    )

    print()
    print(
        f"5' - {DEFAULT_SEQUENCE} - 3'"
    )
    print()

    while True:

        sequence = input(
            "Secuencia de ADN 5' -> 3': "
        ).strip()

        # Si el usuario pulsa ENTER,
        # utilizamos nuestra secuencia de prueba.
        if sequence == "":
            sequence = DEFAULT_SEQUENCE

            print()
            print(
                "Se utilizará la secuencia "
                "de demostración."
            )

        try:
            return validate_dna(sequence)

        except (ValueError, TypeError) as error:

            print()
            print(
                f"ERROR: {error}"
            )

            print()
            print(
                "Inténtalo de nuevo."
            )
            print()


# ============================================================
# COMPLETE SIMULATION
# ============================================================

def run_complete_simulation(
    sequence: str
):
    """
    Ejecuta el flujo completo del dogma central.

    Parameters
    ----------
    sequence : str
        Secuencia de ADN previamente validada.
    """

    # ========================================================
    # 1. CREATE DNA
    # ========================================================

    dna = DNA(
        sequence
    )

    show_initial_dna(
        dna
    )

    # ========================================================
    # 2. REPLICATION
    # ========================================================

    replication_result = replicate(
        dna
    )

    show_replication_result(
        replication_result
    )

    # ========================================================
    # 3. SELECT DNA MOLECULE
    # ========================================================

    # La replicación genera dos moléculas.
    #
    # Como ambas contienen la misma información genética,
    # utilizamos la molécula 1 para continuar el flujo
    # estándar del simulador.

    dna_for_transcription = (
        replication_result["molecule_1"]
    )

    # ========================================================
    # 4. TRANSCRIPTION
    # ========================================================

    transcription_result = transcribe(
        dna_for_transcription
    )

    show_transcription_result(
        transcription_result
    )

    # ========================================================
    # 5. TRANSLATION
    # ========================================================

    mrna = transcription_result[
        "mrna"
    ]

    translation_result = translate(
        mrna
    )

    show_translation_result(
        translation_result
    )

    # ========================================================
    # 6. FINAL SUMMARY
    # ========================================================

    show_final_summary(
        dna,
        transcription_result,
        translation_result
    )


# ============================================================
# MAIN MENU
# ============================================================

def show_menu():
    """
    Muestra el menú principal.
    """

    print()
    print("1. Ejecutar simulación completa")
    print("2. Salir")
    print()


def main():
    """
    Función principal del programa.
    """

    print_title(
        "SIMULADOR DEL DOGMA CENTRAL"
    )

    print(
        "Este programa simula el flujo de "
        "información genética:"
    )

    print()

    print(
        "ADN -> ADN -> ARNm -> proteína"
    )

    while True:

        show_menu()

        option = input(
            "Selecciona una opción: "
        ).strip()

        # ====================================================
        # RUN SIMULATION
        # ====================================================

        if option == "1":

            sequence = request_dna_sequence()

            print_title(
                "INICIO DE LA SIMULACIÓN"
            )

            run_complete_simulation(
                sequence
            )

            print()
            print(
                "Simulación completada."
            )

        # ====================================================
        # EXIT
        # ====================================================

        elif option == "2":

            print()
            print(
                "Simulador finalizado."
            )

            break

        # ====================================================
        # INVALID OPTION
        # ====================================================

        else:

            print()
            print(
                "Opción no válida."
            )

            print(
                "Selecciona 1 o 2."
            )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()