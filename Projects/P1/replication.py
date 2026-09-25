"""
replication.py

Simula la replicación del ADN utilizando un modelo
procariota simplificado basado principalmente en E. coli.

Se representan:

- topoisomerasa;
- helicasa;
- proteínas SSB;
- primasa;
- cebadores de ARN;
- ADN polimerasa III;
- cadena líder;
- cadena rezagada;
- fragmentos de Okazaki;
- ADN polimerasa I;
- ADN ligasa;
- replicación semiconservativa.

Simplificación:
se representa una única horquilla de replicación que
avanza de izquierda a derecha.
"""

from models import DNA
from enzymes import get_enzyme_description


# ============================================================
# CONFIGURATION
# ============================================================

# Los fragmentos reales son mucho mayores.
# Utilizamos un tamaño pequeño para que puedan observarse
# fácilmente durante la simulación.
OKAZAKI_FRAGMENT_SIZE = 5


# ============================================================
# AUXILIARY FUNCTIONS
# ============================================================

def _complement(sequence: str) -> str:
    """
    Devuelve la secuencia complementaria de ADN.

    A <-> T
    C <-> G
    """

    complement_map = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }

    return "".join(
        complement_map[base]
        for base in sequence
    )


def _add_event(
    events: list[str],
    enzyme: str,
    message: str
):
    """
    Añade un evento al registro de replicación.

    Parameters
    ----------
    events : list[str]
        Lista donde se almacenan los eventos.

    enzyme : str
        Clave de la enzima utilizada en enzymes.py.

    message : str
        Explicación concreta de lo que ocurre.
    """

    events.append(
        f"[{enzyme}] {message}"
    )


def _create_okazaki_fragments(
    template_5_3: str,
    fragment_size: int
) -> list[dict]:
    """
    Divide la cadena molde rezagada en fragmentos de Okazaki.

    La cadena molde está representada de izquierda a derecha:

        5' ------------------------ 3'

    Como la ADN polimerasa solo puede leer el molde 3' -> 5',
    cada fragmento de la nueva cadena se sintetiza en sentido
    contrario al avance de la horquilla.

    Por ello se procesan los segmentos desde el extremo derecho
    de la cadena hacia el izquierdo.

    Parameters
    ----------
    template_5_3 : str
        Cadena molde representada en dirección 5' -> 3'.

    fragment_size : int
        Tamaño didáctico de los fragmentos.

    Returns
    -------
    list[dict]
        Información de cada fragmento de Okazaki.
    """

    fragments = []

    fragment_number = 1

    # Empezamos por el extremo 3' de la cadena molde,
    # situado a la derecha en nuestra representación.
    end = len(template_5_3)

    while end > 0:

        start = max(
            0,
            end - fragment_size
        )

        # Segmento tal y como aparece en la cadena molde
        # representada 5' -> 3'.
        template_segment = template_5_3[start:end]

        # La ADN polimerasa debe leer ese segmento
        # en dirección 3' -> 5', por lo que lo recorremos
        # en sentido inverso.
        template_read_3_5 = template_segment[::-1]

        # Generamos el fragmento nuevo en dirección 5' -> 3'.
        new_fragment_5_3 = _complement(
            template_read_3_5
        )

        fragment = {
            "number": fragment_number,

            # Posiciones humanas: comenzamos en 1.
            "template_start": start + 1,
            "template_end": end,

            "template_segment_5_3": template_segment,

            "template_read_3_5": template_read_3_5,

            "sequence_5_3": new_fragment_5_3,

            "primer": "RNA primer"
        }

        fragments.append(fragment)

        fragment_number += 1
        end = start

    return fragments


# ============================================================
# DNA REPLICATION
# ============================================================

def replicate(
    dna: DNA,
    okazaki_fragment_size: int = OKAZAKI_FRAGMENT_SIZE
) -> dict:
    """
    Simula la replicación de una molécula de ADN.

    Se utiliza una única horquilla de replicación que
    avanza de izquierda a derecha.

    Esto implica:

    Cadena superior:
        5' ---------------- 3'
        Molde de la cadena rezagada.

    Cadena inferior:
        3' ---------------- 5'
        Molde de la cadena líder.

    La ADN polimerasa siempre:

        lee:       3' -> 5'
        sintetiza: 5' -> 3'

    Parameters
    ----------
    dna : DNA
        Molécula de ADN original.

    okazaki_fragment_size : int
        Tamaño utilizado para los fragmentos de Okazaki.

    Returns
    -------
    dict
        Resultado completo de la replicación.
    """

    if not isinstance(dna, DNA):
        raise TypeError(
            "replicate() necesita un objeto DNA."
        )

    if okazaki_fragment_size <= 0:
        raise ValueError(
            "El tamaño de los fragmentos de Okazaki "
            "debe ser mayor que cero."
        )

    events = []

    # ========================================================
    # STEP 1 - TOPOISOMERASE
    # ========================================================

    _add_event(
        events,
        "topoisomerase",
        (
            "La topoisomerasa actúa por delante de la "
            "horquilla y reduce la tensión generada "
            "durante la apertura del ADN."
        )
    )

    # ========================================================
    # STEP 2 - HELICASE
    # ========================================================

    _add_event(
        events,
        "helicase",
        (
            "La helicasa comienza a separar las dos "
            "cadenas de ADN y genera la horquilla "
            "de replicación."
        )
    )

    # ========================================================
    # STEP 3 - SSB PROTEINS
    # ========================================================

    _add_event(
        events,
        "ssb",
        (
            "Las proteínas SSB se unen a las cadenas "
            "separadas y evitan que vuelvan a aparearse."
        )
    )

    # ========================================================
    # IDENTIFY TEMPLATES
    # ========================================================

    # Nuestra horquilla avanza de izquierda a derecha.
    #
    # Cadena inferior:
    #
    # 3' ---------------------------- 5'
    #
    # Puede ser leída por la polimerasa 3' -> 5'
    # mientras la horquilla avanza.
    # Por tanto es el molde de la cadena líder.

    leading_template_3_5 = dna.strand_3_5

    # Cadena superior:
    #
    # 5' ---------------------------- 3'
    #
    # Tiene la orientación contraria respecto al avance
    # de la horquilla.
    # Por tanto se replica mediante fragmentos de Okazaki.

    lagging_template_5_3 = dna.strand_5_3

    # ========================================================
    # STEP 4 - PRIMASE
    # ========================================================

    _add_event(
        events,
        "primase",
        (
            "La primasa sintetiza un cebador de ARN "
            "para iniciar la cadena líder."
        )
    )

    # ========================================================
    # STEP 5 - LEADING STRAND
    # ========================================================

    # La nueva cadena líder se sintetiza continuamente
    # en dirección 5' -> 3'.
    leading_new_strand_5_3 = _complement(
        leading_template_3_5
    )

    _add_event(
        events,
        "dna_polymerase_iii",
        (
            "La ADN polimerasa III sintetiza la cadena "
            "líder de forma continua en dirección 5' -> 3'."
        )
    )

    leading_strand = {
        "template": leading_template_3_5,
        "template_orientation": "3' -> 5'",
        "new_strand": leading_new_strand_5_3,
        "new_strand_orientation": "5' -> 3'",
        "synthesis": "continuous",
        "primer_count": 1
    }

    # ========================================================
    # STEP 6 - LAGGING STRAND
    # ========================================================

    okazaki_fragments = _create_okazaki_fragments(
        lagging_template_5_3,
        okazaki_fragment_size
    )

    for fragment in okazaki_fragments:

        _add_event(
            events,
            "primase",
            (
                "La primasa coloca un cebador para el "
                f"fragmento de Okazaki {fragment['number']}."
            )
        )

        _add_event(
            events,
            "dna_polymerase_iii",
            (
                "La ADN polimerasa III sintetiza el "
                f"fragmento de Okazaki "
                f"{fragment['number']} en dirección 5' -> 3'."
            )
        )

    # Una vez finalizado todo el proceso, la cadena nueva
    # complementaria queda alineada respecto a la original
    # en orientación 3' -> 5'.
    lagging_new_strand_3_5 = _complement(
        lagging_template_5_3
    )

    lagging_strand = {
        "template": lagging_template_5_3,
        "template_orientation": "5' -> 3'",
        "new_strand": lagging_new_strand_3_5,
        "new_strand_orientation": "3' -> 5'",
        "synthesis": "discontinuous",
        "primer_count": len(okazaki_fragments),
        "okazaki_fragments": okazaki_fragments
    }

    # ========================================================
    # STEP 7 - DNA POLYMERASE I
    # ========================================================

    _add_event(
        events,
        "dna_polymerase_i",
        (
            "La ADN polimerasa I elimina los cebadores "
            "de ARN y reemplaza esas regiones por ADN."
        )
    )

    # ========================================================
    # STEP 8 - DNA LIGASE
    # ========================================================

    _add_event(
        events,
        "dna_ligase",
        (
            "La ADN ligasa sella las discontinuidades "
            "entre los fragmentos de Okazaki."
        )
    )

    # ========================================================
    # STEP 9 - SEMICONSERVATIVE REPLICATION
    # ========================================================

    # MOLÉCULA 1
    #
    # Conserva como original la cadena superior.
    #
    # 5' original ---------------- 3'
    # 3' nueva    ---------------- 5'

    molecule_1 = {
        "name": "DNA molecule 1",

        "strand_5_3": {
            "sequence": dna.strand_5_3,
            "origin": "original"
        },

        "strand_3_5": {
            "sequence": lagging_new_strand_3_5,
            "origin": "new"
        }
    }

    # MOLÉCULA 2
    #
    # Conserva como original la cadena inferior.
    #
    # 5' nueva    ---------------- 3'
    # 3' original ---------------- 5'

    molecule_2 = {
        "name": "DNA molecule 2",

        "strand_5_3": {
            "sequence": leading_new_strand_5_3,
            "origin": "new"
        },

        "strand_3_5": {
            "sequence": dna.strand_3_5,
            "origin": "original"
        }
    }

    events.append(
        (
            "[replication] La replicación ha finalizado. "
            "Se han obtenido dos moléculas de ADN, "
            "cada una formada por una cadena original "
            "y una cadena recién sintetizada."
        )
    )

    # ========================================================
    # RESULT
    # ========================================================

    return {
        "original_dna": dna,

        "replication_fork_direction": "left -> right",

        "leading_strand": leading_strand,

        "lagging_strand": lagging_strand,

        "molecule_1": molecule_1,

        "molecule_2": molecule_2,

        "events": events
    }


# ============================================================
# OPTIONAL INFORMATION
# ============================================================

def get_replication_enzymes() -> dict:
    """
    Devuelve las enzimas y factores utilizados durante
    la replicación junto con su función.

    Esta función será útil posteriormente para mostrar
    información explicativa al usuario.
    """

    enzyme_names = [
        "topoisomerase",
        "helicase",
        "ssb",
        "primase",
        "dna_polymerase_iii",
        "dna_polymerase_i",
        "dna_ligase"
    ]

    return {
        enzyme: get_enzyme_description(enzyme)
        for enzyme in enzyme_names
    }