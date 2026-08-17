import unittest
from browserguard.fixtures import EXTENSIONS
from browserguard.engine import assess, blast_radius
from browserguard.report import build_report
class TestBrowserGuard(unittest.TestCase):
    def test_all_expected(self): self.assertTrue(all(assess(e).decision==e.expected for e in EXTENSIONS))
    def test_critical_ai_helper(self): self.assertEqual(assess(EXTENSIONS[1]).risk_score,100)
    def test_cookie_reason(self): self.assertIn('cookie access increases session exposure',assess(EXTENSIONS[1]).reasons)
    def test_permission_drift_reason(self): self.assertIn('recent permission expansion',assess(EXTENSIONS[1]).reasons)
    def test_normal_baseline(self): self.assertEqual(assess(EXTENSIONS[0]).decision.value,'NORMAL')
    def test_blast_radius(self): self.assertGreater(blast_radius(EXTENSIONS[1])['nodes'],600)
    def test_report_count(self): self.assertEqual(build_report()['summary']['extensions'],8)
    def test_matches(self): self.assertEqual(build_report()['summary']['expected_outcomes_matched'],8)
if __name__=='__main__': unittest.main()
