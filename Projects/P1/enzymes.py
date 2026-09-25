"""
enzymes.py

Contiene la información de las principales enzimas
y factores moleculares utilizados en el simulador.

Se adopta un modelo procariota simplificado,
principalmente basado en E. coli.
"""


ENZYMES = {
    "topoisomerase": (
        "Reduce la tensión de torsión del ADN "
        "generada durante la apertura de la doble hélice."
    ),

    "helicase": (
        "Separa las dos cadenas de ADN al romper "
        "las interacciones entre las bases complementarias."
    ),

    "ssb": (
        "Las proteínas SSB se unen al ADN monocatenario "
        "para mantener separadas las cadenas y evitar "
        "que vuelvan a aparearse."
    ),

    "primase": (
        "Sintetiza pequeños cebadores de ARN que proporcionan "
        "un extremo 3'-OH desde el que la ADN polimerasa "
        "puede comenzar la síntesis."
    ),

    "dna_polymerase_iii": (
        "Realiza la mayor parte de la síntesis del ADN nuevo "
        "en dirección 5' -> 3'. Participa en la síntesis "
        "continua de la cadena líder y en los fragmentos "
        "de Okazaki de la cadena rezagada."
    ),

    "dna_polymerase_i": (
        "Elimina los cebadores de ARN y sustituye "
        "los nucleótidos de ARN por nucleótidos de ADN."
    ),

    "dna_ligase": (
        "Sella las discontinuidades existentes entre "
        "fragmentos de ADN, uniendo especialmente "
        "los fragmentos de Okazaki."
    ),

    "rna_polymerase": (
        "Lee una cadena molde de ADN en dirección 3' -> 5' "
        "y sintetiza una molécula de ARN complementaria "
        "en dirección 5' -> 3'."
    )
}


def get_enzyme_description(name: str) -> str:
    """
    Devuelve la descripción de una enzima o factor molecular.

    Parameters
    ----------
    name : str
        Nombre utilizado como clave en el diccionario ENZYMES.

    Returns
    -------
    str
        Descripción de la función biológica.

    Raises
    ------
    KeyError
        Si la enzima no está registrada.
    """

    if name not in ENZYMES:
        raise KeyError(
            f"No existe ninguna enzima registrada como '{name}'."
        )

    return ENZYMES[name]