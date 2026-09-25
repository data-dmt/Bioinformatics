"""
validation.py

Funciones encargadas de validar y normalizar
las secuencias de ADN introducidas por el usuario.
"""


def validate_dna(sequence: str) -> str:
    """
    Valida y normaliza una secuencia de ADN.

    La función:
    - comprueba que la entrada sea texto;
    - elimina espacios, tabulaciones y saltos de línea;
    - convierte la secuencia a mayúsculas;
    - comprueba que no esté vacía;
    - comprueba que solo contenga A, T, C y G;
    - comprueba que tenga una longitud mínima.

    Parameters
    ----------
    sequence : str
        Secuencia de ADN introducida por el usuario.

    Returns
    -------
    str
        Secuencia normalizada y validada.

    Raises
    ------
    TypeError
        Si la entrada no es una cadena de texto.

    ValueError
        Si la secuencia está vacía, contiene caracteres
        inválidos o es demasiado corta.
    """

    # Comprobamos que la entrada sea texto.
    if not isinstance(sequence, str):
        raise TypeError(
            "La secuencia de ADN debe ser una cadena de texto."
        )

    # Convertimos a mayúsculas y eliminamos cualquier
    # espacio, tabulación o salto de línea.
    sequence = "".join(sequence.upper().split())

    # La secuencia no puede estar vacía.
    if not sequence:
        raise ValueError(
            "La secuencia de ADN no puede estar vacía."
        )

    # Bases permitidas en una molécula de ADN.
    valid_bases = {"A", "T", "C", "G"}

    # Buscamos cualquier carácter no permitido.
    invalid_bases = {
        base
        for base in sequence
        if base not in valid_bases
    }

    if invalid_bases:
        invalid_text = ", ".join(sorted(invalid_bases))

        raise ValueError(
            f"La secuencia contiene bases no válidas: "
            f"{invalid_text}. "
            f"Solo se permiten A, T, C y G."
        )

    # Usamos una longitud mínima para evitar secuencias
    # demasiado pequeñas para mostrar correctamente
    # los procesos del simulador.
    if len(sequence) < 6:
        raise ValueError(
            "La secuencia es demasiado corta. "
            "Debe contener al menos 6 nucleótidos."
        )

    return sequence