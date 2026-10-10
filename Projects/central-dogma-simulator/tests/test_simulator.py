import unittest

from Bio.Seq import Seq

from simulator import replicate, simulate, transcribe, translate, validate_dna


class SimulatorTests(unittest.TestCase):
    def test_validate_normalizes(self):
        self.assertEqual(validate_dna(" atg cc\n"), "ATGCC")

    def test_validate_rejects_invalid_base(self):
        with self.assertRaises(ValueError):
            validate_dna("ATGN")

    def test_replication_is_semiconservative_and_complementary(self):
        result = replicate(Seq("ATGCC"), fragment_size=2)
        self.assertEqual(result["leading_strand"]["new_strand_5_3"], "ATGCC")
        self.assertEqual(result["lagging_strand"]["new_strand_5_3"], "GGCAT")
        self.assertEqual(result["molecule_1"]["top_origin"], "parental")
        self.assertEqual(result["molecule_1"]["bottom_origin"], "nueva")

    def test_okazaki_fragments_reconstruct_lagging_strand(self):
        result = replicate(Seq("ATGCCATGGA"), fragment_size=3)
        reconstructed = "".join(
            fragment["sequence_5_3"]
            for fragment in reversed(result["lagging_strand"]["okazaki_fragments"])
        )
        self.assertEqual(reconstructed, result["lagging_strand"]["new_strand_5_3"])

    def test_transcription_matches_coding_with_u(self):
        coding = Seq("ATGCCAT")
        result = transcribe(coding, coding.reverse_complement())
        self.assertEqual(result["pre_mrna_5_3"], "AUGCCAU")
        self.assertFalse(result["processing_applied_to_sequence"])

    def test_translation_completed(self):
        result = translate(Seq("AUGCCAUAA"))
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["protein_3letter"], "Met-Pro")
        self.assertEqual(result["stop_codon"], "UAA")

    def test_translation_no_start(self):
        result = translate(Seq("CCCGGGAUU"))
        self.assertEqual(result["status"], "no_start")
        self.assertEqual(result["protein_length"], 0)

    def test_translation_no_stop(self):
        result = translate(Seq("AUGCCAGGG"))
        self.assertEqual(result["status"], "no_stop")
        self.assertEqual(result["protein_3letter"], "Met-Pro-Gly")

    def test_stop_outside_frame_is_not_used(self):
        result = translate(Seq("AUGCCUAAA"))
        self.assertEqual(result["status"], "no_stop")

    def test_sequence_profile(self):
        result = simulate("ATGC")
        profile = result["dna"]["profile"]
        self.assertEqual(profile["gc_percent"], 50.0)
        self.assertEqual(profile["hydrogen_bonds"], 10)

    def test_default_example(self):
        result = simulate("ATGCCATGGAATGCTTAA")
        self.assertEqual(result["translation"]["protein_3letter"], "Met-Pro-Trp-Asn-Ala")
        self.assertEqual(result["translation"]["stop_codon"], "UAA")


if __name__ == "__main__":
    unittest.main()
