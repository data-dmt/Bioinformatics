"""
output.py

Funciones encargadas de mostrar de forma clara y ordenada
los resultados del simulador en la consola.

Este módulo no realiza cálculos biológicos.
Únicamente presenta la información producida por:

- models.py
- replication.py
- transcription.py
- translation.py
"""


# ============================================================
# GENERAL FORMAT
# ============================================================

LINE_WIDTH = 70


def print_title(title: str):
    """
    Muestra un título principal.
    """

    print()
    print("=" * LINE_WIDTH)
    print(title.center(LINE_WIDTH))
    print("=" * LINE_WIDTH)
    print()


def print_section(title: str):
    """
    Muestra el encabezado de una sección.
    """

    print()
    print("-" * LINE_WIDTH)
    print(title)
    print("-" * LINE_WIDTH)


def print_subsection(title: str):
    """
    Muestra un encabezado secundario.
    """

    print()
    print(f">>> {title}")


# ============================================================
# SEQUENCE FORMAT
# ============================================================

def group_sequence(
    sequence: str,
    group_size: int = 3
) -> str:
    """
    Divide visualmente una secuencia en grupos.

    Por defecto se utilizan grupos de tres nucleótidos.

    Ejemplo:

        AUGCCAUGG

    pasa a:

        AUG CCA UGG
    """

    return " ".join(
        sequence[i:i + group_size]
        for i in range(
            0,
            len(sequence),
            group_size
        )
    )


# ============================================================
# INITIAL DNA
# ============================================================

def show_initial_dna(dna):
    """
    Muestra la molécula inicial de ADN.
    """

    print_section(
        "1. MOLÉCULA DE ADN INICIAL"
    )

    print()

    print(
        f"5' - {dna.strand_5_3} - 3'"
    )

    print(
        "     "
        + "|" * len(dna.strand_5_3)
    )

    print(
        f"3' - {dna.strand_3_5} - 5'"
    )

    print()

    print(
        f"Longitud: {dna.length()} pares de bases"
    )


# ============================================================
# EVENTS
# ============================================================

def show_events(
    events: list[str],
    title: str = "Eventos"
):
    """
    Muestra una lista de eventos producidos durante
    cualquier etapa del simulador.
    """

    print_subsection(title)

    for number, event in enumerate(
        events,
        start=1
    ):
        print(
            f"{number:02d}. {event}"
        )


# ============================================================
# REPLICATION
# ============================================================

def show_replication_result(result: dict):
    """
    Muestra el resultado completo de la replicación.
    """

    print_section(
        "2. REPLICACIÓN DEL ADN"
    )

    print()
    print(
        "La horquilla de replicación avanza:"
    )

    print(
        f"  {result['replication_fork_direction']}"
    )

    # --------------------------------------------------------
    # LEADING STRAND
    # --------------------------------------------------------

    leading = result["leading_strand"]

    print_subsection(
        "Cadena líder"
    )

    print(
        "Molde:"
    )

    print(
        f"3' - {leading['template']} - 5'"
    )

    print(
        "Nueva cadena:"
    )

    print(
        f"5' - {leading['new_strand']} - 3'"
    )

    print()

    print(
        "Tipo de síntesis: continua"
    )

    print(
        f"Número de cebadores: "
        f"{leading['primer_count']}"
    )

    # --------------------------------------------------------
    # LAGGING STRAND
    # --------------------------------------------------------

    lagging = result["lagging_strand"]

    print_subsection(
        "Cadena rezagada"
    )

    print(
        "Molde:"
    )

    print(
        f"5' - {lagging['template']} - 3'"
    )

    print(
        "Nueva cadena final:"
    )

    print(
        f"3' - {lagging['new_strand']} - 5'"
    )

    print()

    print(
        "Tipo de síntesis: discontinua"
    )

    print(
        f"Número de cebadores: "
        f"{lagging['primer_count']}"
    )

    # --------------------------------------------------------
    # OKAZAKI FRAGMENTS
    # --------------------------------------------------------

    print_subsection(
        "Fragmentos de Okazaki"
    )

    fragments = lagging[
        "okazaki_fragments"
    ]

    for fragment in fragments:

        print()

        print(
            f"Fragmento "
            f"{fragment['number']}"
        )

        print(
            f"  Posiciones del molde: "
            f"{fragment['template_start']} - "
            f"{fragment['template_end']}"
        )

        print(
            "  Segmento del molde "
            "(5' -> 3'): "
            f"{fragment['template_segment_5_3']}"
        )

        print(
            "  Lectura del molde "
            "(3' -> 5'): "
            f"{fragment['template_read_3_5']}"
        )

        print(
            "  Fragmento sintetizado "
            "(5' -> 3'): "
            f"{fragment['sequence_5_3']}"
        )

        print(
            "  Cebador: ARN"
        )

    # --------------------------------------------------------
    # FINAL DNA MOLECULES
    # --------------------------------------------------------

    print_subsection(
        "Moléculas resultantes"
    )

    molecule_1 = result[
        "molecule_1"
    ]

    molecule_2 = result[
        "molecule_2"
    ]

    print()
    print("Molécula 1")

    print(
        "5' - "
        f"{molecule_1['strand_5_3']['sequence']}"
        " - 3'"
        "   "
        f"({molecule_1['strand_5_3']['origin']})"
    )

    print(
        "3' - "
        f"{molecule_1['strand_3_5']['sequence']}"
        " - 5'"
        "   "
        f"({molecule_1['strand_3_5']['origin']})"
    )

    print()

    print("Molécula 2")

    print(
        "5' - "
        f"{molecule_2['strand_5_3']['sequence']}"
        " - 3'"
        "   "
        f"({molecule_2['strand_5_3']['origin']})"
    )

    print(
        "3' - "
        f"{molecule_2['strand_3_5']['sequence']}"
        " - 5'"
        "   "
        f"({molecule_2['strand_3_5']['origin']})"
    )

    print()

    print(
        "Resultado: replicación semiconservativa."
    )

    print(
        "Cada molécula contiene una cadena original "
        "y una cadena recién sintetizada."
    )

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    show_events(
        result["events"],
        "Eventos de la replicación"
    )


# ============================================================
# TRANSCRIPTION
# ============================================================

def show_transcription_result(result: dict):
    """
    Muestra el resultado completo de la transcripción.
    """

    print_section(
        "3. TRANSCRIPCIÓN"
    )

    coding = result[
        "coding_strand"
    ]

    template = result[
        "template_strand"
    ]

    mrna = result[
        "mrna"
    ]

    print_subsection(
        "Cadenas de ADN utilizadas"
    )

    print()

    print(
        "Cadena codificante:"
    )

    print(
        "5' - "
        f"{group_sequence(coding['sequence'])}"
        " - 3'"
    )

    print()

    print(
        "Cadena molde:"
    )

    print(
        "3' - "
        f"{group_sequence(template['sequence'])}"
        " - 5'"
    )

    # --------------------------------------------------------
    # mRNA
    # --------------------------------------------------------

    print_subsection(
        "ARN mensajero sintetizado"
    )

    print()

    print(
        "5' - "
        f"{group_sequence(mrna.sequence)}"
        " - 3'"
    )

    print()

    if result["sequences_match"]:

        print(
            "Comprobación: correcta."
        )

        print(
            "El ARNm coincide con la cadena "
            "codificante sustituyendo T por U."
        )

    else:

        print(
            "ADVERTENCIA: el ARNm no coincide "
            "con la cadena codificante esperada."
        )

    # --------------------------------------------------------
    # NUCLEOTIDE EVENTS
    # --------------------------------------------------------

    print_subsection(
        "Complementariedad nucleótido a nucleótido"
    )

    for event in result[
        "nucleotide_events"
    ]:
        print(
            f"- {event}"
        )

    # --------------------------------------------------------
    # GENERAL EVENTS
    # --------------------------------------------------------

    show_events(
        result["events"],
        "Eventos de la transcripción"
    )


# ============================================================
# TRANSLATION
# ============================================================

def show_translation_result(result: dict):
    """
    Muestra el resultado completo de la traducción.
    """

    print_section(
        "4. TRADUCCIÓN"
    )

    mrna = result[
        "mrna"
    ]

    print_subsection(
        "ARNm utilizado"
    )

    print()

    print(
        "5' - "
        f"{group_sequence(mrna.sequence)}"
        " - 3'"
    )

    # --------------------------------------------------------
    # START CODON
    # --------------------------------------------------------

    start_position = result[
        "start_position"
    ]

    if start_position == -1:

        print()
        print(
            "No se encontró ningún codón "
            "de inicio AUG."
        )

        print(
            "No puede realizarse la traducción."
        )

        show_events(
            result["events"],
            "Eventos de la traducción"
        )

        return

    print()

    print(
        "Codón de inicio AUG encontrado "
        f"en la posición {start_position}."
    )

    # --------------------------------------------------------
    # CODONS
    # --------------------------------------------------------

    print_subsection(
        "Marco de lectura"
    )

    codons = result[
        "codons"
    ]

    print()

    print(
        " | ".join(codons)
    )

    # --------------------------------------------------------
    # TRANSLATION STEPS
    # --------------------------------------------------------

    print_subsection(
        "Traducción codón a codón"
    )

    for step in result[
        "translation_steps"
    ]:

        print()

        codon_number = step[
            "codon_number"
        ]

        codon = step[
            "codon"
        ]

        if step["type"] == "STOP":

            print(
                f"Codón {codon_number}: {codon}"
            )

            print(
                "  -> STOP"
            )

            print(
                "  -> No existe ARNt correspondiente."
            )

            print(
                "  -> Actúa un factor de liberación."
            )

            print(
                "  -> Finaliza la traducción."
            )

            continue

        amino_acid = step[
            "amino_acid"
        ]

        print(
            f"Codón {codon_number}: "
            f"5'-{codon}-3'"
        )

        print(
            "  Anticodón ARNt: "
            f"3'-{step['anticodon']}-5'"
        )

        print(
            "  Aminoácido: "
            f"{amino_acid['name']} "
            f"({amino_acid['abbreviation']})"
        )

        print(
            "  Proteína parcial: "
            f"{step['protein_sequence']}"
        )

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    print_subsection(
        "Terminación"
    )

    if result["stop_codon"] is not None:

        print(
            f"Codón STOP detectado: "
            f"{result['stop_codon']}"
        )

        print(
            "Un factor de liberación finaliza "
            "la síntesis proteica."
        )

    else:

        print(
            "No se encontró ningún codón STOP "
            "antes de finalizar el ARNm."
        )

    # --------------------------------------------------------
    # PROTEIN
    # --------------------------------------------------------

    protein = result[
        "protein"
    ]

    print_subsection(
        "Proteína sintetizada"
    )

    print()

    if protein.length() == 0:

        print(
            "No se ha sintetizado ninguna proteína."
        )

    else:

        print(
            protein.sequence()
        )

        print()

        print(
            f"Longitud: "
            f"{protein.length()} aminoácidos"
        )

    # --------------------------------------------------------
    # GENERAL EVENTS
    # --------------------------------------------------------

    show_events(
        result["events"],
        "Eventos de la traducción"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

def show_final_summary(
    dna,
    transcription_result: dict,
    translation_result: dict
):
    """
    Muestra un resumen del flujo completo:

        ADN -> ARNm -> proteína
    """

    print_title(
        "RESUMEN FINAL DEL DOGMA CENTRAL"
    )

    # --------------------------------------------------------
    # DNA
    # --------------------------------------------------------

    print(
        "ADN codificante:"
    )

    print(
        "5' - "
        f"{group_sequence(dna.strand_5_3)}"
        " - 3'"
    )

    print()

    print(
        "ADN molde:"
    )

    print(
        "3' - "
        f"{group_sequence(dna.strand_3_5)}"
        " - 5'"
    )

    # --------------------------------------------------------
    # ARROW
    # --------------------------------------------------------

    print()
    print("             |")
    print("             | Transcripción")
    print("             v")
    print()

    # --------------------------------------------------------
    # mRNA
    # --------------------------------------------------------

    mrna = transcription_result[
        "mrna"
    ]

    print(
        "ARNm:"
    )

    print(
        "5' - "
        f"{group_sequence(mrna.sequence)}"
        " - 3'"
    )

    # --------------------------------------------------------
    # ARROW
    # --------------------------------------------------------

    print()
    print("             |")
    print("             | Traducción")
    print("             v")
    print()

    # --------------------------------------------------------
    # PROTEIN
    # --------------------------------------------------------

    protein = translation_result[
        "protein"
    ]

    print(
        "Proteína:"
    )

    if protein.length() > 0:

        print(
            protein.sequence()
        )

    else:

        print(
            "(No sintetizada)"
        )

    print()

    print(
        "Flujo representado:"
    )

    print(
        "ADN -> ADN -> ARNm -> proteína"
    )

    print()
    print("=" * LINE_WIDTH)