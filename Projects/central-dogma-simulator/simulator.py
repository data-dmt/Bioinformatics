"""Núcleo de cálculo del simulador del dogma central."""

from Bio.Seq import Seq
from Bio.SeqUtils import seq3

from biology_content import (
    DOGMA_SPECIAL_CASES,
    INTRON_EXON_CONTEXT,
    MODEL_ASSUMPTIONS,
    MODEL_NAME,
    REPLICATION_EVIDENCE,
    REPLICATION_MACHINERY,
    REPLICATION_MODELS,
    REPLICATION_STEPS,
    RNA_PROCESSING,
    RNA_TYPES,
    TRANSCRIPTION_MACHINERY,
    TRANSCRIPTION_STEPS,
    TRANSLATION_MACHINERY,
    TRANSLATION_STEPS,
)

GENETIC_CODE_TABLE = 1
RNA_COMPLEMENT = str.maketrans("AUCG", "UAGC")

AMINO_ACIDS = {
    "Ala": "Alanina", "Arg": "Arginina", "Asn": "Asparagina",
    "Asp": "Ácido aspártico", "Cys": "Cisteína", "Gln": "Glutamina",
    "Glu": "Ácido glutámico", "Gly": "Glicina", "His": "Histidina",
    "Ile": "Isoleucina", "Leu": "Leucina", "Lys": "Lisina",
    "Met": "Metionina", "Phe": "Fenilalanina", "Pro": "Prolina",
    "Ser": "Serina", "Thr": "Treonina", "Trp": "Triptófano",
    "Tyr": "Tirosina", "Val": "Valina",
}


def validate_dna(sequence: str) -> str:
    """Normaliza y valida una secuencia de ADN formada por A, T, C y G."""
    if not isinstance(sequence, str):
        raise TypeError("La secuencia de ADN debe ser texto.")

    normalized = "".join(sequence.upper().split())
    if not normalized:
        raise ValueError("La secuencia no puede estar vacía.")

    invalid = set(normalized) - set("ATCG")
    if invalid:
        raise ValueError("Bases no válidas: " + ", ".join(sorted(invalid)))

    return normalized


def sequence_profile(sequence: str) -> dict:
    """Calcula métricas básicas útiles para contextualizar la secuencia."""
    length = len(sequence)
    counts = {base: sequence.count(base) for base in "ATCG"}
    gc_pairs = counts["G"] + counts["C"]
    at_pairs = counts["A"] + counts["T"]

    return {
        "length": length,
        "counts": counts,
        "gc_percent": round((gc_pairs / length) * 100, 1) if length else 0.0,
        "at_pairs": at_pairs,
        "gc_pairs": gc_pairs,
        "hydrogen_bonds": at_pairs * 2 + gc_pairs * 3,
    }


def replicate(dna: Seq, fragment_size: int = 5) -> dict:
    """Simula una horquilla de replicación semiconservativa simplificada."""
    if type(fragment_size) is not int or fragment_size <= 0:
        raise ValueError("El tamaño de los fragmentos debe ser un entero positivo.")

    coding_5_3 = dna
    complementary_5_3 = coding_5_3.reverse_complement()
    complementary_aligned_3_5 = complementary_5_3[::-1]

    fragments = []
    for start in range(0, len(coding_5_3), fragment_size):
        end = min(start + fragment_size, len(coding_5_3))
        template_segment = coding_5_3[start:end]
        fragment_5_3 = template_segment.reverse_complement()
        fragments.append(
            {
                "number": len(fragments) + 1,
                "template_start": start + 1,
                "template_end": end,
                "template_sequence_5_3": str(template_segment),
                "sequence_5_3": str(fragment_5_3),
            }
        )

    lagging_new_5_3 = "".join(
        fragment["sequence_5_3"] for fragment in reversed(fragments)
    )
    leading_new_5_3 = str(coding_5_3)

    if lagging_new_5_3 != str(complementary_5_3):
        raise RuntimeError("Error interno al reconstruir la hebra rezagada.")

    return {
        "fork_direction": "left_to_right",
        "fragment_size": fragment_size,
        "leading_strand": {
            "template_aligned_3_5": str(complementary_aligned_3_5),
            "new_strand_5_3": leading_new_5_3,
            "synthesis": "continuous",
        },
        "lagging_strand": {
            "template_5_3": str(coding_5_3),
            "new_strand_5_3": lagging_new_5_3,
            "new_strand_aligned_3_5": lagging_new_5_3[::-1],
            "okazaki_fragments": fragments,
            "synthesis": "discontinuous",
        },
        "molecule_1": {
            "top_aligned_5_3": str(coding_5_3),
            "bottom_aligned_3_5": lagging_new_5_3[::-1],
            "top_origin": "parental",
            "bottom_origin": "nueva",
        },
        "molecule_2": {
            "top_aligned_5_3": leading_new_5_3,
            "bottom_aligned_3_5": str(complementary_aligned_3_5),
            "top_origin": "nueva",
            "bottom_origin": "parental",
        },
        "steps": REPLICATION_STEPS,
        "machinery": REPLICATION_MACHINERY,
        "models": REPLICATION_MODELS,
        "evidence": REPLICATION_EVIDENCE,
    }


def transcribe(coding_dna: Seq, template_dna: Seq) -> dict:
    """Simula ADN → pre-ARNm y aporta el contexto del procesamiento eucariota."""
    if template_dna != coding_dna.reverse_complement():
        raise ValueError("La hebra molde no es complementaria a la codificante.")

    pre_mrna = coding_dna.transcribe()

    return {
        "coding_5_3": str(coding_dna),
        "template_5_3": str(template_dna),
        "template_aligned_3_5": str(template_dna[::-1]),
        "pre_mrna_5_3": str(pre_mrna),
        "mrna_for_translation_5_3": str(pre_mrna),
        "processing_applied_to_sequence": False,
        "base_pairing": {"A": "U", "T": "A", "C": "G", "G": "C"},
        "steps": TRANSCRIPTION_STEPS,
        "machinery": TRANSCRIPTION_MACHINERY,
        "rna_types": RNA_TYPES,
        "rna_processing": RNA_PROCESSING,
        "intron_exon_context": INTRON_EXON_CONTEXT,
    }


def translate(mrna: Seq) -> dict:
    """Traduce desde el primer AUG hasta STOP o hasta el final del ARNm."""
    start = mrna.find("AUG")
    result = {
        "start_position_0_based": start,
        "start_position_1_based": None if start == -1 else start + 1,
        "translation_steps": [],
        "protein_3letter": "",
        "protein_1letter": "",
        "protein_length": 0,
        "stop_codon": None,
        "stop_position_1_based": None,
        "completed": False,
        "status": "no_start",
        "sequence_before_start": str(mrna) if start == -1 else str(mrna[:start]),
        "untranslated_after_stop": "",
        "incomplete_codon": "",
        "steps": TRANSLATION_STEPS,
        "machinery": TRANSLATION_MACHINERY,
    }

    if start == -1:
        return result

    coding_region = mrna[start:]
    complete_length = len(coding_region) // 3 * 3
    translated = str(
        coding_region[:complete_length].translate(table=GENETIC_CODE_TABLE)
    )

    stop_index = translated.find("*")
    completed = stop_index != -1
    symbol_count = stop_index + 1 if completed else len(translated)

    abbreviations = []
    one_letter = []

    for index, symbol in enumerate(translated[:symbol_count]):
        relative_start = index * 3
        codon = str(coding_region[relative_start : relative_start + 3])
        absolute_start = start + relative_start + 1
        absolute_end = absolute_start + 2

        amino_acid = None
        anticodon_3_5 = None
        if symbol != "*":
            abbreviation = seq3(symbol)
            abbreviations.append(abbreviation)
            one_letter.append(symbol)
            amino_acid = {
                "name": AMINO_ACIDS[abbreviation],
                "abbreviation": abbreviation,
                "one_letter": symbol,
            }
            anticodon_3_5 = codon.translate(RNA_COMPLEMENT)

        result["translation_steps"].append(
            {
                "codon_number": index + 1,
                "codon": codon,
                "mrna_start_1_based": absolute_start,
                "mrna_end_1_based": absolute_end,
                "type": "STOP" if symbol == "*" else "amino_acid",
                "role": (
                    "stop" if symbol == "*" else "start" if index == 0 else "elongation"
                ),
                "amino_acid": amino_acid,
                "anticodon_3_5": anticodon_3_5,
                "recognized_by": "factor_terminacion" if symbol == "*" else "ARNt",
                "peptide_after_step": "-".join(abbreviations),
            }
        )

    if completed:
        stop_position = start + stop_index * 3 + 1
        untranslated_after_stop = str(coding_region[symbol_count * 3 :])
        incomplete_codon = ""
    else:
        stop_position = None
        untranslated_after_stop = ""
        incomplete_codon = str(coding_region[complete_length:])

    result.update(
        {
            "protein_3letter": "-".join(abbreviations),
            "protein_1letter": "".join(one_letter),
            "protein_length": len(abbreviations),
            "completed": completed,
            "status": "completed" if completed else "no_stop",
            "stop_codon": (
                result["translation_steps"][-1]["codon"] if completed else None
            ),
            "stop_position_1_based": stop_position,
            "untranslated_after_stop": untranslated_after_stop,
            "incomplete_codon": incomplete_codon,
        }
    )
    return result


def simulate(sequence: str, fragment_size: int = 5) -> dict:
    """Ejecuta replicación, transcripción y traducción sobre la misma entrada."""
    coding_dna = Seq(validate_dna(sequence))
    template_dna = coding_dna.reverse_complement()

    replication = replicate(coding_dna, fragment_size)
    transcription = transcribe(coding_dna, template_dna)
    mrna = Seq(transcription["mrna_for_translation_5_3"])
    translation = translate(mrna)

    return {
        "model_name": MODEL_NAME,
        "dna": {
            "coding_5_3": str(coding_dna),
            "template_5_3": str(template_dna),
            "template_aligned_3_5": str(template_dna[::-1]),
            "profile": sequence_profile(str(coding_dna)),
        },
        "replication": replication,
        "transcription": transcription,
        "translation": translation,
        "dogma_special_cases": DOGMA_SPECIAL_CASES,
        "model_assumptions": MODEL_ASSUMPTIONS,
    }
