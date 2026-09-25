"""
translation.py

Simula la traducción del ARN mensajero a una proteína.

Se representan:

- búsqueda del codón de inicio AUG;
- establecimiento del marco de lectura;
- lectura del ARNm por el ribosoma;
- división de la secuencia en codones;
- código genético;
- ARN de transferencia (ARNt);
- anticodones;
- sitios A, P y E del ribosoma;
- incorporación de aminoácidos;
- formación progresiva de la cadena polipeptídica;
- reconocimiento de codones STOP;
- factores de liberación.

El modelo es una simplificación didáctica del proceso real.
"""

from models import (
    MessengerRNA,
    AminoAcid,
    Protein,
    TransferRNA,
    Ribosome
)


# ============================================================
# GENETIC CODE
# ============================================================

# Cada codón está asociado a:
#
# (
#     nombre del aminoácido,
#     abreviatura de tres letras
# )
#
# Los codones STOP se representan mediante None.

GENETIC_CODE = {

    # --------------------------------------------------------
    # U
    # --------------------------------------------------------

    "UUU": ("Fenilalanina", "Phe"),
    "UUC": ("Fenilalanina", "Phe"),
    "UUA": ("Leucina", "Leu"),
    "UUG": ("Leucina", "Leu"),

    "UCU": ("Serina", "Ser"),
    "UCC": ("Serina", "Ser"),
    "UCA": ("Serina", "Ser"),
    "UCG": ("Serina", "Ser"),

    "UAU": ("Tirosina", "Tyr"),
    "UAC": ("Tirosina", "Tyr"),
    "UAA": None,
    "UAG": None,

    "UGU": ("Cisteína", "Cys"),
    "UGC": ("Cisteína", "Cys"),
    "UGA": None,
    "UGG": ("Triptófano", "Trp"),

    # --------------------------------------------------------
    # C
    # --------------------------------------------------------

    "CUU": ("Leucina", "Leu"),
    "CUC": ("Leucina", "Leu"),
    "CUA": ("Leucina", "Leu"),
    "CUG": ("Leucina", "Leu"),

    "CCU": ("Prolina", "Pro"),
    "CCC": ("Prolina", "Pro"),
    "CCA": ("Prolina", "Pro"),
    "CCG": ("Prolina", "Pro"),

    "CAU": ("Histidina", "His"),
    "CAC": ("Histidina", "His"),
    "CAA": ("Glutamina", "Gln"),
    "CAG": ("Glutamina", "Gln"),

    "CGU": ("Arginina", "Arg"),
    "CGC": ("Arginina", "Arg"),
    "CGA": ("Arginina", "Arg"),
    "CGG": ("Arginina", "Arg"),

    # --------------------------------------------------------
    # A
    # --------------------------------------------------------

    "AUU": ("Isoleucina", "Ile"),
    "AUC": ("Isoleucina", "Ile"),
    "AUA": ("Isoleucina", "Ile"),
    "AUG": ("Metionina", "Met"),

    "ACU": ("Treonina", "Thr"),
    "ACC": ("Treonina", "Thr"),
    "ACA": ("Treonina", "Thr"),
    "ACG": ("Treonina", "Thr"),

    "AAU": ("Asparagina", "Asn"),
    "AAC": ("Asparagina", "Asn"),
    "AAA": ("Lisina", "Lys"),
    "AAG": ("Lisina", "Lys"),

    "AGU": ("Serina", "Ser"),
    "AGC": ("Serina", "Ser"),
    "AGA": ("Arginina", "Arg"),
    "AGG": ("Arginina", "Arg"),

    # --------------------------------------------------------
    # G
    # --------------------------------------------------------

    "GUU": ("Valina", "Val"),
    "GUC": ("Valina", "Val"),
    "GUA": ("Valina", "Val"),
    "GUG": ("Valina", "Val"),

    "GCU": ("Alanina", "Ala"),
    "GCC": ("Alanina", "Ala"),
    "GCA": ("Alanina", "Ala"),
    "GCG": ("Alanina", "Ala"),

    "GAU": ("Ácido aspártico", "Asp"),
    "GAC": ("Ácido aspártico", "Asp"),
    "GAA": ("Ácido glutámico", "Glu"),
    "GAG": ("Ácido glutámico", "Glu"),

    "GGU": ("Glicina", "Gly"),
    "GGC": ("Glicina", "Gly"),
    "GGA": ("Glicina", "Gly"),
    "GGG": ("Glicina", "Gly")
}


# ============================================================
# CONSTANTS
# ============================================================

START_CODON = "AUG"

STOP_CODONS = {
    "UAA",
    "UAG",
    "UGA"
}


RNA_COMPLEMENT = {
    "A": "U",
    "U": "A",
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
    Añade un evento al registro de traducción.
    """

    events.append(
        f"[{stage}] {message}"
    )


def get_anticodon(codon: str) -> str:
    """
    Obtiene el anticodón complementario de un codón de ARNm.

    El codón se recibe en dirección:

        5' -> 3'

    y el anticodón se devuelve en dirección:

        3' -> 5'

    Ejemplo:

        codón:
        5' - AUG - 3'

        anticodón:
        3' - UAC - 5'

    Parameters
    ----------
    codon : str
        Codón de ARNm.

    Returns
    -------
    str
        Anticodón en dirección 3' -> 5'.
    """

    if len(codon) != 3:
        raise ValueError(
            "Un codón debe contener exactamente "
            "tres nucleótidos."
        )

    return "".join(
        RNA_COMPLEMENT[base]
        for base in codon
    )


def get_amino_acid(codon: str) -> AminoAcid:
    """
    Obtiene el aminoácido correspondiente a un codón.

    Parameters
    ----------
    codon : str
        Codón de ARNm.

    Returns
    -------
    AminoAcid
        Aminoácido correspondiente.

    Raises
    ------
    ValueError
        Si el codón es STOP o no existe.
    """

    if codon not in GENETIC_CODE:
        raise ValueError(
            f"El codón '{codon}' no es válido."
        )

    amino_acid_data = GENETIC_CODE[codon]

    if amino_acid_data is None:
        raise ValueError(
            f"El codón {codon} es un codón STOP "
            "y no codifica ningún aminoácido."
        )

    name, abbreviation = amino_acid_data

    return AminoAcid(
        name=name,
        abbreviation=abbreviation
    )


def create_transfer_rna(codon: str) -> TransferRNA:
    """
    Crea el ARNt correspondiente a un codón.

    Los codones STOP no generan ARNt porque son
    reconocidos por factores de liberación.

    Parameters
    ----------
    codon : str
        Codón del ARNm.

    Returns
    -------
    TransferRNA
        ARNt con su anticodón y aminoácido.
    """

    if codon in STOP_CODONS:
        raise ValueError(
            "Los codones STOP no son reconocidos "
            "por ARNt, sino por factores de liberación."
        )

    anticodon = get_anticodon(codon)

    amino_acid = get_amino_acid(codon)

    return TransferRNA(
        anticodon_3_5=anticodon,
        amino_acid=amino_acid
    )


# ============================================================
# TRANSLATION
# ============================================================

def translate(mrna: MessengerRNA) -> dict:
    """
    Simula la traducción de una molécula de ARNm.

    El proceso:

    1. El ribosoma se une al ARNm.
    2. Se busca el primer codón AUG.
    3. Se establece el marco de lectura.
    4. Se leen los codones uno a uno.
    5. Para cada codón no STOP:
       - se genera el ARNt correspondiente;
       - entra en el sitio A;
       - se incorpora su aminoácido;
       - se forma el enlace peptídico;
       - ocurre la translocación;
       - el ARNt pasa por los sitios P y E.
    6. Si aparece UAA, UAG o UGA:
       - no se crea ningún ARNt;
       - actúa un factor de liberación;
       - termina la traducción.

    Parameters
    ----------
    mrna : MessengerRNA
        ARN mensajero que va a traducirse.

    Returns
    -------
    dict
        Resultado completo de la traducción.
    """

    # ========================================================
    # VALIDATION
    # ========================================================

    if not isinstance(mrna, MessengerRNA):
        raise TypeError(
            "translate() necesita un objeto MessengerRNA."
        )

    events = []

    translation_steps = []

    protein = Protein()

    ribosome = Ribosome()

    # ========================================================
    # STEP 1 - RIBOSOME BINDS TO mRNA
    # ========================================================

    _add_event(
        events,
        "ribosome",
        (
            "El ribosoma se asocia con la molécula "
            "de ARNm."
        )
    )

    # ========================================================
    # STEP 2 - FIND START CODON
    # ========================================================

    start_position = mrna.find_start_codon()

    if start_position == -1:

        _add_event(
            events,
            "translation",
            (
                "No se ha encontrado ningún codón de "
                "inicio AUG. La traducción no puede comenzar."
            )
        )

        return {
            "mrna": mrna,
            "start_position": -1,
            "codons": [],
            "protein": protein,
            "translation_steps": [],
            "stop_codon": None,
            "completed": False,
            "events": events
        }

    _add_event(
        events,
        "translation",
        (
            f"Se encuentra el codón de inicio AUG "
            f"en la posición {start_position}."
        )
    )

    _add_event(
        events,
        "ribosome",
        (
            "El codón AUG establece el marco de lectura "
            "de la traducción."
        )
    )

    # ========================================================
    # STEP 3 - GET CODONS
    # ========================================================

    codons = ribosome.read(
        mrna,
        start_position
    )

    _add_event(
        events,
        "ribosome",
        (
            f"El ARNm se leerá en {len(codons)} "
            "codones completos a partir de AUG."
        )
    )

    # ========================================================
    # STEP 4 - ELONGATION
    # ========================================================

    stop_codon = None

    completed = False

    for codon_number, codon in enumerate(
        codons,
        start=1
    ):

        # ----------------------------------------------------
        # STOP CODON
        # ----------------------------------------------------

        # Es fundamental comprobar STOP antes de crear ARNt.
        # UAA, UAG y UGA no son reconocidos por ARNt.

        if codon in STOP_CODONS:

            stop_codon = codon

            _add_event(
                events,
                "termination",
                (
                    f"El ribosoma alcanza el codón STOP "
                    f"{codon}."
                )
            )

            _add_event(
                events,
                "release_factor",
                (
                    "Un factor de liberación reconoce "
                    "el codón STOP. No entra ningún ARNt."
                )
            )

            _add_event(
                events,
                "termination",
                (
                    "La cadena polipeptídica se libera "
                    "del ribosoma."
                )
            )

            translation_steps.append(
                {
                    "codon_number": codon_number,
                    "codon": codon,
                    "type": "STOP",
                    "anticodon": None,
                    "amino_acid": None,
                    "protein_sequence": protein.sequence()
                }
            )

            completed = True

            break

        # ----------------------------------------------------
        # tRNA
        # ----------------------------------------------------

        transfer_rna = create_transfer_rna(
            codon
        )

        amino_acid = transfer_rna.amino_acid

        # ----------------------------------------------------
        # SITE A
        # ----------------------------------------------------

        _add_event(
            events,
            "site_A",
            (
                f"Codón {codon_number}: "
                f"5'-{codon}-3'. "
                f"Entra un ARNt con anticodón "
                f"3'-{transfer_rna.anticodon_3_5}-5' "
                f"transportando {amino_acid.name}."
            )
        )

        # ----------------------------------------------------
        # PEPTIDE BOND
        # ----------------------------------------------------

        protein.add_amino_acid(
            amino_acid
        )

        _add_event(
            events,
            "peptide_bond",
            (
                f"Se incorpora {amino_acid.name} "
                f"({amino_acid.abbreviation}) "
                "a la cadena polipeptídica."
            )
        )

        # ----------------------------------------------------
        # SITE P
        # ----------------------------------------------------

        _add_event(
            events,
            "site_P",
            (
                "Tras la formación del enlace peptídico, "
                "el ARNt asociado a la cadena en crecimiento "
                "ocupa funcionalmente el sitio P."
            )
        )

        # ----------------------------------------------------
        # TRANSLOCATION / SITE E
        # ----------------------------------------------------

        _add_event(
            events,
            "translocation",
            (
                "El ribosoma avanza un codón sobre el ARNm."
            )
        )

        _add_event(
            events,
            "site_E",
            (
                "El ARNt que ya ha transferido su aminoácido "
                "abandona el ribosoma a través del sitio E."
            )
        )

        # ----------------------------------------------------
        # SAVE STEP
        # ----------------------------------------------------

        translation_steps.append(
            {
                "codon_number": codon_number,

                "codon": codon,

                "type": "amino_acid",

                "anticodon": (
                    transfer_rna.anticodon_3_5
                ),

                "amino_acid": {
                    "name": amino_acid.name,
                    "abbreviation":
                        amino_acid.abbreviation
                },

                "protein_sequence":
                    protein.sequence()
            }
        )

    # ========================================================
    # NO STOP CODON FOUND
    # ========================================================

    if stop_codon is None:

        _add_event(
            events,
            "warning",
            (
                "Se ha alcanzado el final de los codones "
                "completos del ARNm sin encontrar un "
                "codón STOP."
            )
        )

    # ========================================================
    # INCOMPLETE FINAL CODON
    # ========================================================

    translated_length = (
        len(codons) * 3
    )

    remaining_nucleotides = (
        len(mrna.sequence)
        - start_position
        - translated_length
    )

    if remaining_nucleotides > 0:

        remaining_sequence = (
            mrna.sequence[
                len(mrna.sequence)
                - remaining_nucleotides:
            ]
        )

        _add_event(
            events,
            "translation",
            (
                f"Quedan {remaining_nucleotides} "
                f"nucleótido(s) sin traducir "
                f"('{remaining_sequence}') porque no "
                "forman un codón completo."
            )
        )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    _add_event(
        events,
        "translation",
        (
            "Secuencia polipeptídica obtenida: "
            f"{protein.sequence() or '(vacía)'}"
        )
    )

    return {
        "mrna": mrna,

        "start_position": start_position,

        "codons": codons,

        "protein": protein,

        "translation_steps": translation_steps,

        "stop_codon": stop_codon,

        "completed": completed,

        "events": events
    }