"""
models.py

Contiene las clases principales utilizadas para representar
las moléculas y estructuras biológicas del simulador.
"""


# ============================================================
# DNA
# ============================================================

class DNA:
    """
    Representa una molécula de ADN de doble cadena.

    La primera cadena se almacena en dirección 5' -> 3'
    y su cadena complementaria en dirección 3' -> 5'.

    Ejemplo:

        5' - ATGCCG - 3'
             ||||||
        3' - TACGGC - 5'
    """

    DNA_COMPLEMENT = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }

    def __init__(self, strand_5_3: str):
        """
        Crea una molécula de ADN a partir de una cadena 5' -> 3'.

        Parameters
        ----------
        strand_5_3 : str
            Secuencia de ADN en dirección 5' -> 3'.
        """

        self.strand_5_3 = strand_5_3

        # Generamos automáticamente la cadena complementaria.
        # Al representarse debajo de la primera cadena,
        # su orientación será 3' -> 5'.
        self.strand_3_5 = self._complementary_strand(strand_5_3)

    def _complementary_strand(self, strand: str) -> str:
        """
        Genera la cadena complementaria de ADN.

        Reglas:
        A <-> T
        C <-> G
        """

        return "".join(
            self.DNA_COMPLEMENT[base]
            for base in strand
        )

    def length(self) -> int:
        """
        Devuelve el número de pares de bases de la molécula.
        """

        return len(self.strand_5_3)

    def display(self) -> str:
        """
        Devuelve una representación textual de la doble cadena.
        """

        bonds = "|" * self.length()

        return (
            f"5' - {self.strand_5_3} - 3'\n"
            f"     {bonds}\n"
            f"3' - {self.strand_3_5} - 5'"
        )

    def __str__(self) -> str:
        return self.display()


# ============================================================
# MESSENGER RNA
# ============================================================

class MessengerRNA:
    """
    Representa una molécula de ARN mensajero.

    El ARNm se almacena siempre en dirección 5' -> 3'.
    """

    def __init__(self, sequence: str):
        self.sequence = sequence

    def find_start_codon(self) -> int:
        """
        Busca el primer codón de inicio AUG.

        Returns
        -------
        int
            Posición inicial de AUG.

            Devuelve -1 si no se encuentra.
        """

        return self.sequence.find("AUG")

    def get_codons(self, start: int = 0) -> list[str]:
        """
        Divide el ARNm en codones de tres nucleótidos.

        Parameters
        ----------
        start : int
            Posición desde la que comienza la lectura.

        Returns
        -------
        list[str]
            Lista de codones completos.
        """

        if start < 0:
            raise ValueError(
                "La posición inicial no puede ser negativa."
            )

        return [
            self.sequence[i:i + 3]
            for i in range(
                start,
                len(self.sequence) - 2,
                3
            )
        ]

    def length(self) -> int:
        """
        Devuelve el número de nucleótidos del ARNm.
        """

        return len(self.sequence)

    def display(self) -> str:
        """
        Devuelve la representación del ARNm.
        """

        return f"5' - {self.sequence} - 3'"

    def __str__(self) -> str:
        return self.display()


# ============================================================
# AMINO ACID
# ============================================================

class AminoAcid:
    """
    Representa un aminoácido.
    """

    def __init__(
        self,
        name: str,
        abbreviation: str
    ):
        self.name = name
        self.abbreviation = abbreviation

    def __str__(self) -> str:
        return self.abbreviation


# ============================================================
# PROTEIN
# ============================================================

class Protein:
    """
    Representa la cadena polipeptídica sintetizada
    durante el proceso de traducción.
    """

    def __init__(self):
        self.amino_acids: list[AminoAcid] = []

    def add_amino_acid(self, amino_acid: AminoAcid):
        """
        Añade un aminoácido a la cadena polipeptídica.
        """

        self.amino_acids.append(amino_acid)

    def length(self) -> int:
        """
        Devuelve el número de aminoácidos de la proteína.
        """

        return len(self.amino_acids)

    def sequence(self) -> str:
        """
        Devuelve la proteína utilizando abreviaturas
        de tres letras.

        Ejemplo:

        Met-Pro-Trp-Asn
        """

        return "-".join(
            amino_acid.abbreviation
            for amino_acid in self.amino_acids
        )

    def __str__(self) -> str:
        if not self.amino_acids:
            return "(proteína vacía)"

        return self.sequence()


# ============================================================
# TRANSFER RNA
# ============================================================

class TransferRNA:
    """
    Representa una molécula de ARN de transferencia.

    El anticodón se almacena en dirección 3' -> 5'
    porque se empareja de forma antiparalela con
    el codón del ARNm, que se lee 5' -> 3'.

    Ejemplo:

        ARNm:
            5' - AUG - 3'

        ARNt:
            3' - UAC - 5'
    """

    def __init__(
        self,
        anticodon_3_5: str,
        amino_acid: AminoAcid
    ):
        self.anticodon_3_5 = anticodon_3_5
        self.amino_acid = amino_acid

    def __str__(self) -> str:
        return (
            f"ARNt 3'-{self.anticodon_3_5}-5' "
            f"-> {self.amino_acid.name}"
        )


# ============================================================
# RIBOSOME
# ============================================================

class Ribosome:
    """
    Representación simplificada de un ribosoma.

    El ribosoma lee el ARNm codón a codón.

    Los sitios A, P y E se explicarán durante la
    simulación de la traducción, pero no se mantienen
    como estados internos de esta clase.
    """

    def read(
        self,
        mrna: MessengerRNA,
        start: int
    ) -> list[str]:
        """
        Devuelve los codones del ARNm desde una posición.
        """

        return mrna.get_codons(start)