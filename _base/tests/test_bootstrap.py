"""초기화(init_project.py) 수락 시험. 템플릿 저장소 복사본에서 실행한다.

실행: python -m unittest discover -s _base/tests -v
"""
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "_base" / "scripts"))
import knowledge  # noqa: E402

IS_TEMPLATE = (knowledge.load_project(ROOT).get("base") or {}).get("role") == "template"


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
        shutil.rmtree(self.tmp, ignore_errors=True)

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


if __name__ == "__main__":
    unittest.main()
