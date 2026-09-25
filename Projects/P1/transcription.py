"""
transcription.py

Simula la transcripción de ADN a ARN mensajero (ARNm).

En el modo estándar del simulador:

- strand_3_5 actúa como cadena molde;
- strand_5_3 actúa como cadena codificante;
- la ARN polimerasa lee el molde en dirección 3' -> 5';
- el ARNm se sintetiza en dirección 5' -> 3'.

Ejemplo:

ADN codificante:
5' - ATGCCATGG - 3'

ADN molde:
3' - TACGGTACC - 5'

ARNm:
5' - AUGCCAUGG - 3'
"""

from models import MessengerRNA
from enzymes import get_enzyme_description


# ============================================================
# TRANSCRIPTION COMPLEMENT
# ============================================================

DNA_TO_RNA_COMPLEMENT = {
    "A": "U",
    "T": "A",
    "C": "G",
    "G": "C"
}


# ============================================================
# AUXILIARY FUNCTIONS
# ============================================================

def _add_event(
    events: list[str],
    stage: str,
    message: str
):
    """
    Añade un evento al registro de transcripción.
    """

    events.append(
        f"[{stage}] {message}"
    )


def _transcribe_template(template_3_5: str) -> str:
    """
    Genera una secuencia de ARN complementaria a una
    cadena molde de ADN escrita en dirección 3' -> 5'.

    La nueva molécula de ARN queda escrita en dirección
    5' -> 3'.

    Parameters
    ----------
    template_3_5 : str
        Cadena molde de ADN en dirección 3' -> 5'.

    Returns
    -------
    str
        Secuencia de ARN en dirección 5' -> 3'.
    """

    return "".join(
        DNA_TO_RNA_COMPLEMENT[base]
        for base in template_3_5
    )


# ============================================================
# TRANSCRIPTION
# ============================================================

def transcribe(dna_molecule: dict) -> dict:
    """
    Simula la transcripción de una molécula de ADN replicada.

    Se espera recibir una de las moléculas producidas por
    replicate(), por ejemplo:

        replication_result["molecule_1"]

    La estructura esperada es:

        {
            "name": "...",

            "strand_5_3": {
                "sequence": "...",
                "origin": "original" o "new"
            },

            "strand_3_5": {
                "sequence": "...",
                "origin": "original" o "new"
            }
        }

    Para la simulación estándar:

        strand_3_5 = cadena molde
        strand_5_3 = cadena codificante

    Parameters
    ----------
    dna_molecule : dict
        Una de las moléculas de ADN obtenidas tras
        la replicación.

    Returns
    -------
    dict
        Resultado completo de la transcripción.
    """

    # ========================================================
    # VALIDATION
    # ========================================================

    if not isinstance(dna_molecule, dict):
        raise TypeError(
            "transcribe() necesita una molécula de ADN "
            "representada mediante un diccionario."
        )

    required_keys = {
        "strand_5_3",
        "strand_3_5"
    }

    if not required_keys.issubset(dna_molecule.keys()):
        raise ValueError(
            "La molécula de ADN no contiene las dos "
            "cadenas necesarias para la transcripción."
        )

    try:
        coding_strand_5_3 = (
            dna_molecule["strand_5_3"]["sequence"]
        )

        template_strand_3_5 = (
            dna_molecule["strand_3_5"]["sequence"]
        )

    except (KeyError, TypeError):
        raise ValueError(
            "La estructura de la molécula de ADN "
            "no es válida."
        )

    events = []

    # ========================================================
    # STEP 1 - TEMPLATE SELECTION
    # ========================================================

    _add_event(
        events,
        "transcription",
        (
            "Se selecciona la cadena de ADN orientada "
            "3' -> 5' como cadena molde."
        )
    )

    _add_event(
        events,
        "transcription",
        (
            "La cadena orientada 5' -> 3' queda definida "
            "como cadena codificante."
        )
    )

    # ========================================================
    # STEP 2 - RNA POLYMERASE BINDING
    # ========================================================

    _add_event(
        events,
        "rna_polymerase",
        (
            "La ARN polimerasa se une a la región de inicio "
            "y abre localmente la doble cadena de ADN."
        )
    )

    # ========================================================
    # STEP 3 - TEMPLATE READING
    # ========================================================

    _add_event(
        events,
        "rna_polymerase",
        (
            "La ARN polimerasa comienza a leer la cadena "
            "molde en dirección 3' -> 5'."
        )
    )

    # ========================================================
    # STEP 4 - RNA ELONGATION
    # ========================================================

    mrna_sequence = ""

    nucleotide_events = []

    for position, dna_base in enumerate(
        template_strand_3_5,
        start=1
    ):
        rna_base = DNA_TO_RNA_COMPLEMENT[dna_base]

        mrna_sequence += rna_base

        nucleotide_event = (
            f"Posición {position}: "
            f"ADN molde {dna_base} -> ARN {rna_base}"
        )

        nucleotide_events.append(nucleotide_event)

    _add_event(
        events,
        "rna_polymerase",
        (
            "La ARN polimerasa sintetiza el ARNm "
            "complementario en dirección 5' -> 3'."
        )
    )

    # ========================================================
    # CREATE mRNA OBJECT
    # ========================================================

    mrna = MessengerRNA(
        mrna_sequence
    )

    # ========================================================
    # STEP 5 - TERMINATION
    # ========================================================

    _add_event(
        events,
        "transcription",
        (
            "La transcripción finaliza y se libera "
            "la molécula de ARNm."
        )
    )

    # ========================================================
    # CONSISTENCY CHECK
    # ========================================================

    # La cadena codificante debe tener la misma secuencia
    # que el ARNm, sustituyendo T por U.
    expected_mrna = coding_strand_5_3.replace(
        "T",
        "U"
    )

    sequences_match = (
        expected_mrna == mrna_sequence
    )

    if sequences_match:
        _add_event(
            events,
            "transcription",
            (
                "Comprobación correcta: el ARNm coincide "
                "con la cadena codificante sustituyendo "
                "timina (T) por uracilo (U)."
            )
        )
    else:
        _add_event(
            events,
            "warning",
            (
                "El ARNm generado no coincide con la "
                "cadena codificante esperada."
            )
        )

    # ========================================================
    # RESULT
    # ========================================================

    return {
        "dna_molecule": dna_molecule,

        "coding_strand": {
            "sequence": coding_strand_5_3,
            "orientation": "5' -> 3'"
        },

        "template_strand": {
            "sequence": template_strand_3_5,
            "orientation": "3' -> 5'"
        },

        "mrna": mrna,

        "mrna_sequence": mrna_sequence,

        "nucleotide_events": nucleotide_events,

        "sequences_match": sequences_match,

        "events": events
    }


# ============================================================
# OPTIONAL INFORMATION
# ============================================================

def get_transcription_enzyme() -> dict:
    """
    Devuelve información sobre la ARN polimerasa utilizada
    durante la transcripción.
    """

    return {
        "rna_polymerase":
            get_enzyme_description("rna_polymerase")
    }