"""초기화(init_project.py) 수락 시험. 템플릿 저장소 복사본에서 실행한다.

실행: python -m unittest discover -s _base/tests -v
"""
import hashlib
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "_base" / "scripts"))
import knowledge  # noqa: E402

IS_TEMPLATE = (knowledge.load_project(ROOT).get("base") or {}).get("role") == "template"


def remove_tree(path):
    """Windows에서 읽기 전용인 .git 객체도 지운다."""
    def retry(func, target, _):
        os.chmod(target, stat.S_IWRITE)
        func(target)
    shutil.rmtree(path, onerror=retry)


def tree_digest(root):
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if ".git" in rel.parts or "__pycache__" in rel.parts:  # 실행할 때 생기는 Python 캐시는 비교하지 않는다
            continue
        h.update(rel.as_posix().encode())
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()


@unittest.skipUnless(IS_TEMPLATE, "처음 초기화 시험은 템플릿 저장소에서만 의미가 있다")
class BootstrapTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))
        self.manifest = knowledge.load_manifest(self.root)

    def tearDown(self):
        remove_tree(self.tmp)

    def run_script(self, name, *args):
        return subprocess.run([sys.executable, str(self.root / "_base/scripts" / name), *args],
                              capture_output=True, encoding="utf-8")

    def init(self, *args, check=True):
        proc = self.run_script("init_project.py", "--name", "MES: 1차 구축", "--code", "MES-001", *args)
        if check:
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc

    def assertValid(self):
        proc = self.run_script("validate.py")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def config(self):
        return knowledge.load_project(self.root)

    def dirs(self, module):
        return self.manifest["modules"][module]["dirs"]

    def test_template_copy_is_valid(self):
        self.assertValid()

    def test_development_profile(self):
        self.init("--profile", "development")
        cfg = self.config()
        self.assertEqual(cfg["modules"], ["core", "dev"])
        self.assertEqual(cfg["base"]["role"], "project")
        self.assertEqual(cfg["base"]["version"], self.manifest["version"])
        self.assertEqual(cfg["project"]["phase"], "01_proposal")
        for d in self.dirs("dev"):
            self.assertTrue((self.root / d).is_dir(), d)
        for d in self.dirs("eval"):
            self.assertFalse((self.root / d).exists(), d)
        self.assertIn("## 필수 산출물", (self.root / "wiki/02_analysis-design/README.md").read_text(encoding="utf-8"))
        self.assertFalse((self.root / "governance").exists())
        readme = knowledge.read_meta(self.root / "README.md")
        self.assertEqual(readme["title"], "MES: 1차 구축")
        self.assertEqual(readme["version"], "0.1.0")
        self.assertValid()

    def test_evaluation_profile_with_monitor(self):
        self.init("--profile", "evaluation", "--modules", "+monitor")
        self.assertEqual(self.config()["modules"], ["core", "eval", "monitor"])
        self.assertTrue((self.root / "data/events").is_dir())
        self.assertTrue((self.root / "wiki/03_evaluate/README.md").exists())
        self.assertFalse((self.root / "entities/requirements").exists())
        self.assertValid()

    def test_development_with_evaluation_module(self):
        self.init("--profile", "development", "--modules", "+eval")
        self.assertEqual(self.config()["modules"], ["core", "dev", "eval"])
        self.assertTrue((self.root / "evaluation/models").is_dir())
        self.assertValid()

    def test_rerun_is_non_destructive(self):
        self.init("--profile", "development")
        stage = self.root / "wiki/01_proposal/README.md"
        stage.write_text("# 고친 단계 문서\n", encoding="utf-8")
        before = tree_digest(self.root)
        self.assertIn("변경 없음", self.init().stdout)
        self.assertEqual(tree_digest(self.root), before)
        self.init("--modules", "+monitor")  # 모듈은 나중에 켤 수 있다
        self.assertTrue((self.root / "data/events").is_dir())
        self.assertEqual(stage.read_text(encoding="utf-8"), "# 고친 단계 문서\n")
        self.assertValid()

    def test_dry_run_changes_nothing(self):
        before = tree_digest(self.root)
        proc = self.init("--profile", "evaluation", "--dry-run")
        self.assertIn("[dry-run] remove governance/", proc.stdout)
        self.assertEqual(tree_digest(self.root), before)

    def test_rejects_bad_options(self):
        for args in (["--modules", "+foo"], ["--modules", "+governance"], ["--modules", "dev,+eval"],
                     ["--profile", "unknown"]):
            self.assertNotEqual(self.init(*args, check=False).returncode, 0, args)
        self.init("--profile", "development")
        proc = self.init("--profile", "evaluation", check=False)
        self.assertIn("프로필은 바꿀 수 없다", proc.stderr)

    def test_validate_reports_outdated_base_version(self):
        self.init("--profile", "development")
        path = self.root / "_config/project.yml"
        cfg = self.config()
        cfg["base"]["version"] = "0.0.1"
        path.write_text(yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")
        proc = self.run_script("validate.py")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("base.version 0.0.1이 설치된 base", proc.stdout)

    @unittest.skipUnless(shutil.which("git"), "git이 필요하다")
    def test_refuses_to_run_in_template_repository(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "remote", "add", "origin",
                        f"https://github.com/{self.manifest['template_repository']}.git"], check=True)
        proc = self.init(check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("템플릿 저장소", proc.stderr)
        self.assertTrue((self.root / "governance").exists())


    # 수락 시험 (결정 문서의 3.0.0 배포 조건) -----------------------------------
    def instantiate(self, name, spec, record_id):
        """등록된 템플릿으로 레코드 하나를 만든다. 필수 필드와 필수 관계만 채운다."""
        tpl = self.root / spec["_template_root"] / spec["template"]
        text = tpl.read_text(encoding="utf-8")
        body = ""
        if spec["format"] == "md":
            meta, body = knowledge.read_meta(tpl), text.split("\n---\n", 1)[1]
        else:
            meta = yaml.safe_load(text)
        meta["type"] = name
        if record_id:
            meta["id"] = record_id
        for key in spec.get("required", []):
            meta[key] = meta.get(key) or "샘플"
        meta.update({"test-case": {"verifies": ["REQ-0001"]},
                     "evaluation": {"applies": ["EVM-0001"], "based_on": ["SNAP-20260924-001"]}}.get(name, {}))
        if record_id:
            rule = spec.get("file", "{id}.{format}").format(id=record_id, format=spec["format"]).removeprefix("**/")
            rel = Path(spec["path"]) / rule
        else:
            rel = Path(spec["path"]) / f"00_project/sample-{name}.md"
        dumped = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
        (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.root / rel).write_text(f"---\n{dumped}---\n{body}" if spec["format"] == "md" else dumped, encoding="utf-8")

    def test_every_template_instantiates_a_valid_record(self):
        self.init("--profile", "development", "--modules", "+eval,+monitor")
        reg = knowledge.load_registry(self.root)
        modules = set(self.config()["modules"])
        targets = [(n, s) for n, s in reg.types.items() if s["module"] in modules and s.get("template")]
        for name, spec in targets:
            record_id = None
            if spec.get("id"):
                record_id = spec["id"].replace("YYYYMMDD", "20260924").replace("####", "0001").replace("###", "001")
            self.instantiate(name, spec, record_id)
        res = knowledge.validate(self.root)
        self.assertEqual(res.errors, [])
        self.assertEqual(len([r for r in res.records if r.path.name.startswith(("sample-",)) or r.id]), len(targets))
        self.assertValid()

    @unittest.skipUnless(shutil.which("git") and (ROOT / ".git").exists(), "git 저장소에서만 실행한다")
    def test_tracked_files_alone_are_valid(self):
        listed = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z"], capture_output=True).stdout
        remove_tree(self.root)
        for rel in filter(None, listed.decode("utf-8").split("\0")):
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, self.root / rel)
        self.assertValid()
        self.init("--profile", "evaluation")
        self.assertValid()

    @unittest.skipUnless(shutil.which("git"), "git이 필요하다")
    def test_payload_policy(self):
        self.init("--profile", "development")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        ds = self.root / "data/manifests/datasets/DS-0001.yml"
        ds.write_text(yaml.safe_dump({"id": "DS-0001", "type": "dataset", "name": "로그", "status": "active",
                                      "security": {"classification": "confidential"}}), encoding="utf-8")
        raw = self.root / "data/raw/DS-0001/2026-09-24/a.log"
        raw.parent.mkdir(parents=True)
        raw.write_text("x" * 2048, encoding="utf-8")
        self.assertValid()  # 기본적으로 raw는 Git에서 제외된다
        with (self.root / ".gitignore").open("a", encoding="utf-8") as f:
            f.write("\n!data/raw/DS-0001/**\n")
        proc = self.run_script("validate.py")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("데이터셋 DS-0001의 보안 등급 'confidential'은 Git에 둘 수 없다", proc.stdout)
        ds.write_text(ds.read_text(encoding="utf-8").replace("confidential", "internal"), encoding="utf-8")
        self.assertValid()
        policy = self.root / "_config/security-policy.yml"
        policy.write_text(policy.read_text(encoding="utf-8").replace("max_file_mb: 5", "max_file_mb: 0.001"), encoding="utf-8")
        self.assertIn("MB를 넘는다", self.run_script("validate.py").stdout)

    def test_evaluation_follows_model_config(self):
        """계산은 평가 모델 파일을 읽어서 한다. 설정을 바꾸면 결과가 바뀌고, 과거 평가는 재평가 대상으로 보고된다."""
        self.init("--profile", "evaluation")

        def write(rel, meta):
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            dumped = yaml.safe_dump(meta, allow_unicode=True)
            path.write_text(f"---\n{dumped}---\n" if rel.endswith(".md") else dumped, encoding="utf-8")

        def model(version, weight):
            write("evaluation/models/EVM-0001.yml", {"id": "EVM-0001", "type": "evaluation-model", "title": "모델",
                                                     "status": "approved", "version": version,
                                                     "criteria": [{"id": "CRIT-0001", "metric": "MET-0001", "weight": weight}]})

        def calculate(eval_id, supersedes=()):
            evm = yaml.safe_load((self.root / "evaluation/models/EVM-0001.yml").read_text(encoding="utf-8"))
            results = []
            for f in sorted((self.root / "entities/evidence").glob("*.yml")):
                ev = yaml.safe_load(f.read_text(encoding="utf-8"))
                total = sum(c["weight"] * ev["value"][c["metric"]] for c in evm["criteria"])
                results.append({"candidate": ev["about"][0], "evidence": [ev["id"]], "total": total})
            write(f"entities/evaluations/{eval_id}.yml", {"id": eval_id, "type": "evaluation", "status": "final",
                                                        "applies": ["EVM-0001"], "based_on": ["SNAP-20260924-001"],
                                                        "pinned": {"EVM-0001": evm["version"]}, "supersedes": list(supersedes),
                                                        "results": results})
            return [r["total"] for r in results]

        write("entities/objectives/OBJ-0001.md", {"id": "OBJ-0001", "type": "objective", "title": "목표", "status": "approved"})
        write("entities/criteria/CRIT-0001.md", {"id": "CRIT-0001", "type": "criterion", "title": "기준", "status": "approved",
                                                  "version": "1.0.0"})
        write("entities/metrics/MET-0001.yml", {"id": "MET-0001", "type": "metric", "title": "지표", "status": "approved",
                                                 "version": "1.0.0", "measures": ["CRIT-0001"]})
        write("data/manifests/datasets/DS-0001.yml", {"id": "DS-0001", "type": "dataset", "name": "데이터", "status": "active"})
        write("data/snapshots/SNAP-20260924-001/snapshot.yml", {"id": "SNAP-20260924-001", "type": "snapshot",
                                                                "datasets": ["DS-0001"]})
        for i, value in ((1, 80), (2, 60)):
            write(f"entities/candidates/CAND-000{i}.md", {"id": f"CAND-000{i}", "type": "candidate", "title": f"후보{i}",
                                                          "status": "active"})
            write(f"entities/evidence/EVD-000{i}.yml", {"id": f"EVD-000{i}", "type": "evidence", "about": [f"CAND-000{i}"],
                                                        "snapshot_id": "SNAP-20260924-001", "value": {"MET-0001": value}})
        model("1.0.0", 1.0)
        first = calculate("EVAL-0001")
        self.assertValid()
        model("1.1.0", 0.5)
        self.assertIn("재평가 필요: EVAL-0001는 EVM-0001 1.0.0을 썼지만 현재 1.1.0", self.run_script("trace.py").stderr)
        second = calculate("EVAL-0002", supersedes=["EVAL-0001"])
        self.assertNotEqual(first, second)
        self.assertNotIn("재평가 필요", self.run_script("trace.py").stderr)  # 대체된 평가는 다시 보고하지 않는다
        self.assertValid()

if __name__ == "__main__":
    unittest.main()
