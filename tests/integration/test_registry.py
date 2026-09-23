"""레지스트리 기반 검증기의 수락 시험.

올바른 레코드는 통과하고, 잘못된 레코드는 반드시 실패해야 한다.
실행: python -m unittest discover -s tests -v
"""
from collections import defaultdict
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import knowledge  # noqa: E402


class RegistryValidationTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        shutil.copytree(ROOT / "_base", self.root / "_base")

    def tearDown(self):
        shutil.rmtree(self.root)

    # helpers ---------------------------------------------------------------
    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def md(self, rel, **meta):
        self.write(rel, "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\n# 본문\n")

    def yml(self, rel, **meta):
        self.write(rel, yaml.safe_dump(meta, allow_unicode=True, sort_keys=False))

    def result(self):
        return knowledge.validate(self.root)

    def assertError(self, fragment):
        errors = self.result().errors
        self.assertTrue(any(fragment in e for e in errors), f"'{fragment}' 오류가 없다: {errors}")

    def dev_chain(self):
        self.md("entities/requirements/REQ-0001.md", id="REQ-0001", type="requirement", title="요구", status="approved")
        self.md("entities/features/DEV-0001.md", id="DEV-0001", type="feature", title="기능", status="approved",
                implements=["REQ-0001"], uses=["API-0001"])
        self.md("entities/apis/API-0001.md", id="API-0001", type="api", title="API", status="draft")
        self.md("entities/test-cases/TC-0001.md", id="TC-0001", type="test-case", title="시험", status="draft",
                verifies=["API-0001"], result="pass")

    def eval_chain(self, metric_version="1.0.0"):
        self.md("entities/objectives/OBJ-0001.md", id="OBJ-0001", type="objective", title="목표", status="approved")
        self.md("entities/candidates/CAND-0001.md", id="CAND-0001", type="candidate", title="후보", status="active",
                serves=["OBJ-0001"])
        self.md("entities/criteria/CRIT-0001.md", id="CRIT-0001", type="criterion", title="가격", status="approved",
                version="1.0.0")
        self.yml("entities/metrics/MET-0001.yml", id="MET-0001", type="metric", title="매매가", status="approved",
                 version=metric_version, measures=["CRIT-0001"])
        self.yml("data/manifests/datasets/DS-0001.yml", id="DS-0001", type="dataset", name="매물", status="active")
        self.yml("data/snapshots/SNAP-20260921-001/snapshot.yml", id="SNAP-20260921-001", type="snapshot",
                 datasets=["DS-0001"])
        self.yml("entities/evidence/EVD-0001.yml", id="EVD-0001", type="evidence", about=["CAND-0001"],
                 snapshot_id="SNAP-20260921-001")
        self.yml("evaluation/models/EVM-0001.yml", id="EVM-0001", type="evaluation-model", title="모델",
                 status="approved", version="1.1.0", serves=["OBJ-0001"],
                 criteria=[{"id": "CRIT-0001", "metric": "MET-0001", "weight": 20}])
        self.yml("entities/evaluations/EVAL-0001.yml", id="EVAL-0001", type="evaluation", status="final",
                 applies=["EVM-0001"], based_on=["SNAP-20260921-001"],
                 pinned={"EVM-0001": "1.1.0", "MET-0001": "1.0.0"},
                 results=[{"candidate": "CAND-0001", "evidence": ["EVD-0001"], "gate": "pass"}])

    # 통과해야 하는 경우 ------------------------------------------------------
    def test_repository_itself_is_valid(self):
        res = knowledge.validate(ROOT)
        self.assertEqual(res.errors, [])

    def test_dev_chain_passes_and_inverse_is_computed(self):
        self.dev_chain()
        res = self.result()
        self.assertEqual(res.errors, [])
        self.assertEqual(res.warnings, [])  # DEV는 사용하는 API를 거쳐 검증된다
        self.assertEqual(res.inverse["REQ-0001"]["implemented_by"], ["DEV-0001"])
        self.assertEqual(res.inverse["API-0001"]["verified_by"], ["TC-0001"])

    def test_eval_chain_passes(self):
        self.eval_chain()
        res = self.result()
        self.assertEqual(res.errors, [])
        self.assertEqual(res.inverse["EVD-0001"]["cited_in"], ["EVAL-0001"])
        self.assertEqual(res.inverse["CRIT-0001"]["combined_in"], ["EVM-0001"])

    def test_project_extension_type_is_accepted(self):
        self.write("_config/types.yml", yaml.safe_dump({
            "types": {"inspection": {"prefix": "INSP", "id": "INSP-####", "module": "dev", "kind": "entity",
                                     "format": "md", "path": "entities/inspections/",
                                     "template": "templates/inspection.md", "status_set": "document"}},
            "relations": {"inspects": {"from": ["inspection"], "to": ["table"], "inverse": "inspected_by"}},
        }))
        self.md("templates/inspection.md", id="INSP-0000", type="inspection", title="", status="draft", inspects=[])
        self.md("entities/tables/DB-0001.md", id="DB-0001", type="table", title="테이블", status="draft")
        self.md("entities/inspections/INSP-0001.md", id="INSP-0001", type="inspection", title="점검",
                status="draft", inspects=["DB-0001"])
        res = self.result()
        self.assertEqual(res.errors, [])
        self.assertEqual(res.inverse["DB-0001"]["inspected_by"], ["INSP-0001"])

    # 실패해야 하는 경우 ------------------------------------------------------
    def test_duplicate_id(self):
        for folder in ("candidates", "adopted"):
            self.md(f"governance/adoption/{folder}/ADOPT-0001.md", id="ADOPT-0001", type="adoption-proposal",
                    title="후보", status="candidate")
        self.assertError("중복 ID ADOPT-0001")

    def test_broken_reference(self):
        self.md("entities/features/DEV-0001.md", id="DEV-0001", type="feature", title="기능", status="draft",
                implements=["REQ-0099"])
        self.assertError("implements → REQ-0099: 존재하지 않는 ID")

    def test_wrong_relation_target_type(self):
        self.md("entities/decisions/DEC-0001.md", id="DEC-0001", type="decision", title="결정", status="accepted")
        self.md("entities/test-cases/TC-0001.md", id="TC-0001", type="test-case", title="시험", status="draft",
                verifies=["DEC-0001"])
        self.assertError("verifies → DEC-0001: 대상 유형 'decision'은 허용되지 않는다")

    def test_relation_not_allowed_for_type(self):
        self.dev_chain()
        self.md("entities/requirements/REQ-0002.md", id="REQ-0002", type="requirement", title="요구", status="draft",
                verifies=["REQ-0001"])
        self.assertError("'requirement'은 관계 'verifies'을 가질 수 없다")

    def test_unregistered_status(self):
        self.md("entities/requirements/REQ-0001.md", id="REQ-0001", type="requirement", title="요구", status="done")
        self.assertError("status 'done'가 'document' 집합에 없다")

    def test_result_field_outside_set(self):
        self.dev_chain()
        self.md("entities/test-cases/TC-0002.md", id="TC-0002", type="test-case", title="시험", status="draft",
                verifies=["REQ-0001"], result="ok")
        self.assertError("result 'ok'가 'test-result' 집합에 없다")

    def test_filename_must_match_id(self):
        self.md("entities/requirements/REQ-0001.md", id="REQ-0002", type="requirement", title="요구", status="draft")
        self.assertError("파일 경로가 ID와 맞지 않는다")

    def test_wrong_location_for_type(self):
        self.md("entities/features/REQ-0001.md", id="REQ-0001", type="requirement", title="요구", status="draft")
        self.assertError("유형 'requirement'은 entities/features/에 둘 수 없다")

    def test_missing_metadata_in_record_location(self):
        self.write("entities/requirements/REQ-0001.md", "# 메타데이터 없음\n")
        self.assertError("메타데이터(type)가 없다")

    def test_handwritten_inverse_relation(self):
        self.dev_chain()
        self.md("entities/requirements/REQ-0002.md", id="REQ-0002", type="requirement", title="요구", status="draft",
                implemented_by=["DEV-0001"])
        self.assertError("'implemented_by'는 역방향 관계라 직접 쓰지 않는다")

    def test_project_extension_cannot_override_base(self):
        self.write("_config/types.yml", yaml.safe_dump({"types": {
            "requirement": {"prefix": "RQ", "id": "RQ-####", "module": "dev", "kind": "entity", "format": "md",
                            "path": "entities/requirements/"},
            "my-requirement": {"prefix": "REQ", "id": "REQ-####", "module": "dev", "kind": "entity", "format": "md",
                               "path": "entities/my-requirements/"},
        }}))
        self.assertError("base 유형 'requirement'을 덮어쓸 수 없다")
        self.assertError("접두어 'REQ'는 base 유형 'requirement'가 쓰고 있다")

    def test_template_must_match_registry(self):
        path = self.root / "_base/templates/entities/issue.md"
        path.write_text(path.read_text(encoding="utf-8").replace("type: issue", "type: risk"), encoding="utf-8")
        self.assertError("_base/templates/entities/issue.md: type 'risk'이 이 템플릿을 쓰는 유형 ['issue']와 맞지 않는다")

    def test_coverage_rules(self):
        self.md("entities/requirements/REQ-0001.md", id="REQ-0001", type="requirement", title="요구", status="approved")
        self.md("entities/test-cases/TC-0001.md", id="TC-0001", type="test-case", title="시험", status="draft")
        res = self.result()
        self.assertIn("entities/test-cases/TC-0001.md: 테스트 케이스에 검증 대상(verifies)이 없다", res.errors)
        self.assertIn("entities/requirements/REQ-0001.md: 승인된 요구사항을 구현하는 기능이 없다", res.warnings)

    # 추적 매트릭스 ----------------------------------------------------------
    def trace(self):
        return subprocess.run([sys.executable, str(ROOT / "scripts/traceability/build_trace_matrix.py"), str(self.root)],
                              capture_output=True, encoding="utf-8")

    def test_trace_matrix_lists_relations(self):
        self.dev_chain()
        proc = self.trace()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("REQ-0001,requirement,approved,entities/requirements/REQ-0001.md,,implemented_by=DEV-0001", proc.stdout)
        self.assertIn("REQ → DEV 구현 1/1, REQ → TC 검증(기능 경유 포함) 0/1", proc.stderr)

    def test_trace_reports_reevaluation_when_definition_changes(self):
        self.eval_chain(metric_version="1.1.0")  # EVAL은 MET-0001 1.0.0을 고정했다
        proc = self.trace()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("재평가 필요: EVAL-0001는 MET-0001 1.0.0을 썼지만 현재 1.1.0", proc.stderr)


class RegistryDocsTest(unittest.TestCase):
    def test_naming_doc_matches_registry(self):
        text = (ROOT / "framework/standards/naming.md").read_text(encoding="utf-8")
        documented = {m.group(1): {p.strip() for p in m.group(2).split(",")}
                      for m in re.finditer(r"^- (core|dev|eval|governance): ([A-Z, ]+)", text, re.M)}
        registry = defaultdict(set)
        for spec in knowledge.load_registry(ROOT).types.values():
            if spec.get("prefix"):
                registry[spec["module"]].add(spec["prefix"])
        self.assertEqual(documented, dict(registry))


if __name__ == "__main__":
    unittest.main()
