"""Interfaz de terminal del simulador."""

from simulator import simulate

DEFAULT_SEQUENCE = "ATGCCATGGAATGCTTAA"
DEFAULT_FRAGMENT_SIZE = 5


def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def show_steps(steps):
    for step in steps:
        print(f"\n{step['number']}. {step['title']} — {step['actor']}")
        print(f"   {step['description']}")
        print(f"   Resultado: {step['result']}")


def show_results(data):
    r = data["replication"]
    section("1. REPLICACIÓN")
    print(f"Líder  molde: 3′ {r['leading_strand']['template_aligned_3_5']} 5′")
    print(f"Líder  nueva: 5′ {r['leading_strand']['new_strand_5_3']} 3′")
    print(f"Rezag. molde: 5′ {r['lagging_strand']['template_5_3']} 3′")
    print(f"Rezag. nueva: 3′ {r['lagging_strand']['new_strand_aligned_3_5']} 5′")
    print("\nFragmentos de Okazaki:")
    for fragment in r["lagging_strand"]["okazaki_fragments"]:
        print(
            f"  {fragment['number']}. molde {fragment['template_start']}–"
            f"{fragment['template_end']} → 5′ {fragment['sequence_5_3']} 3′"
        )
    show_steps(r["steps"])

    t = data["transcription"]
    section("2. TRANSCRIPCIÓN")
    print(f"Codificante: 5′ {t['coding_5_3']} 3′")
    print(f"Molde:       3′ {t['template_aligned_3_5']} 5′")
    print(f"Pre-ARNm:    5′ {t['pre_mrna_5_3']} 3′")
    print("Procesamiento: cap 5′, cola poli-A y splicing se explican conceptualmente.")
    show_steps(t["steps"])

    tr = data["translation"]
    section("3. TRADUCCIÓN")
    if tr["status"] == "no_start":
        print("No se encontró AUG; en este modelo no comienza la traducción.")
    else:
        for step in tr["translation_steps"]:
            if step["type"] == "STOP":
                result = "STOP"
            else:
                result = (
                    f"{step['amino_acid']['name']} · anticodón 3′ "
                    f"{step['anticodon_3_5']} 5′"
                )
            print(f"{step['codon_number']}. {step['codon']} → {result}")
        print(f"Cadena: {tr['protein_3letter'] or '—'}")
    show_steps(tr["steps"])


def main():
    print("SIMULADOR DEL DOGMA CENTRAL · MODELO DIDÁCTICO EUCARIOTA")
    sequence = input(f"Hebra codificante 5′→3′ [ENTER = {DEFAULT_SEQUENCE}]: ").strip()
    try:
        data = simulate(sequence or DEFAULT_SEQUENCE, DEFAULT_FRAGMENT_SIZE)
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")
        return
    show_results(data)


if __name__ == "__main__":
    main()
