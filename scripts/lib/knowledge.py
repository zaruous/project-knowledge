"""프로젝트 지식 레지스트리를 읽고 레코드를 검증하는 공용 모듈.

유형·ID·상태·관계는 _base/registry/*.yml이 단일 원천이다.
프로젝트 확장은 _config/types.yml에 두며 base 유형·접두어·집합·관계를 덮어쓸 수 없다.
"""
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = Path("_base/registry")
TEMPLATE_DIR = Path("_base/templates")
PROJECT_TYPES = Path("_config/types.yml")


def utf8_stdio():
    """파이프·리다이렉트에서도 한국어가 깨지지 않도록 표준 출력을 UTF-8로 고정한다."""
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def read_meta(path):
    """md는 front matter, yml은 파일 전체를 메타데이터로 읽는다. 메타데이터가 없으면 None."""
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if path.suffix == ".md":
        if not text.startswith("---\n"):
            return None
        end = text.find("\n---\n", 4)
        if end < 0:
            return None
        text = text[4:end]
    data = yaml.safe_load(text)
    return data if isinstance(data, dict) else None


def values(meta, path):
    """'a', 'a.b', 'a[].b' 경로의 값을 비어 있지 않은 문자열 목록으로 돌려준다."""
    items = [meta]
    for part in path.split("."):
        many = part.endswith("[]")
        key = part[:-2] if many else part
        nxt = []
        for item in items:
            if not isinstance(item, dict):
                continue
            v = item.get(key)
            if many:
                nxt.extend(v if isinstance(v, list) else [])
            else:
                nxt.append(v)
        items = nxt
    out = []
    for v in items:
        for x in v if isinstance(v, list) else [v]:
            if isinstance(x, str) and x:
                out.append(x)
    return out


def id_pattern(fmt):
    """'REQ-####', 'SNAP-YYYYMMDD-###' 같은 형식을 정규식으로 바꾼다."""
    rx = re.escape(fmt)
    for token, sub in (("YYYY", r"\d{4}"), ("MM", r"\d{2}"), ("DD", r"\d{2}"), (r"\#", r"\d"), ("#", r"\d")):
        rx = rx.replace(token, sub)
    return re.compile(f"^{rx}$")


def top_key(path):
    return path.split(".")[0].removesuffix("[]")


@dataclass
class Registry:
    types: dict
    status_sets: dict
    result_sets: dict
    relations: dict
    coverage: list
    errors: list = field(default_factory=list)

    def relation_field(self, name):
        return self.relations[name].get("field", name)

    @property
    def inverse_names(self):
        return {r["inverse"] for r in self.relations.values()}


def load_registry(root=ROOT):
    types_doc = load_yaml(root / REGISTRY_DIR / "types.yml")
    sets_doc = load_yaml(root / REGISTRY_DIR / "status-sets.yml")
    rel_doc = load_yaml(root / REGISTRY_DIR / "relations.yml")
    reg = Registry(
        types={k: dict(v, _template_root=str(TEMPLATE_DIR)) for k, v in (types_doc.get("types") or {}).items()},
        status_sets=dict(sets_doc.get("status_sets") or {}),
        result_sets=dict(sets_doc.get("result_sets") or {}),
        relations=dict(rel_doc.get("relations") or {}),
        coverage=list(rel_doc.get("coverage") or []),
    )
    ext_path = root / PROJECT_TYPES
    if ext_path.exists():
        ext = load_yaml(ext_path)
        prefixes = {t["prefix"]: name for name, t in reg.types.items() if t.get("prefix")}
        for name, spec in (ext.get("types") or {}).items():
            if name in reg.types:
                reg.errors.append(f"{PROJECT_TYPES.as_posix()}: base 유형 '{name}'을 덮어쓸 수 없다")
            elif spec.get("prefix") in prefixes:
                reg.errors.append(f"{PROJECT_TYPES.as_posix()}: 접두어 '{spec['prefix']}'는 base 유형 '{prefixes[spec['prefix']]}'가 쓰고 있다")
            else:
                reg.types[name] = dict(spec, _template_root=".")
        for key, target in (("status_sets", reg.status_sets), ("result_sets", reg.result_sets), ("relations", reg.relations)):
            for name, spec in (ext.get(key) or {}).items():
                if name in target:
                    reg.errors.append(f"{PROJECT_TYPES.as_posix()}: base {key} '{name}'을 덮어쓸 수 없다")
                else:
                    target[name] = spec
    for spec in reg.types.values():
        spec["_rx"] = id_pattern(spec["id"]) if spec.get("id") else None
    return reg


def check_registry(root, reg):
    """레지스트리 자체와 템플릿의 정합성을 검사한다."""
    errors = []
    allowed_tops = defaultdict(set)
    relation_tops = set()
    for name, rel in reg.relations.items():
        top = top_key(reg.relation_field(name))
        relation_tops.add(top)
        for t in rel.get("from", []):
            allowed_tops[t].add(top)
        for t in rel.get("from", []) + ([] if rel.get("to") == "*" else rel.get("to", [])):
            if t not in reg.types:
                errors.append(f"relations.{name}: 등록되지 않은 유형 '{t}'")
        if not rel.get("inverse"):
            errors.append(f"relations.{name}: inverse가 없다")
    for rule in reg.coverage:
        if rule.get("type") not in reg.types:
            errors.append(f"coverage: 등록되지 않은 유형 '{rule.get('type')}'")
        if rule.get("inverse") and rule["inverse"] not in reg.inverse_names:
            errors.append(f"coverage: 등록되지 않은 역방향 관계 '{rule['inverse']}'")

    for name, spec in reg.types.items():
        where = f"types.{name}"
        for key in ("module", "kind", "format", "path"):
            if not spec.get(key):
                errors.append(f"{where}: '{key}'가 없다")
        if spec.get("id") and not spec["id"].startswith(f"{spec.get('prefix')}-"):
            errors.append(f"{where}: id 형식 '{spec['id']}'이 접두어 '{spec.get('prefix')}'로 시작하지 않는다")
        if spec.get("status_set") and spec["status_set"] not in reg.status_sets:
            errors.append(f"{where}: 등록되지 않은 status_set '{spec['status_set']}'")
        for fld, rset in (spec.get("fields") or {}).items():
            if rset not in reg.result_sets:
                errors.append(f"{where}: 필드 '{fld}'의 결과 집합 '{rset}'이 없다")
        if not spec.get("template"):
            continue
        tpl = Path(spec["_template_root"]) / spec["template"]
        if not (root / tpl).is_file():
            errors.append(f"{where}: 템플릿 {tpl.as_posix()}이 없다")
            continue
        meta = read_meta(root / tpl) or {}
        users = [n for n, s in reg.types.items() if s.get("template") == spec["template"]]
        ttype = meta.get("type")
        if ttype not in users:
            errors.append(f"{tpl.as_posix()}: type '{ttype}'이 이 템플릿을 쓰는 유형 {users}와 맞지 않는다")
            continue
        if ttype != name:
            continue  # 공용 템플릿은 템플릿에 적힌 대표 유형 기준으로 한 번만 검사한다
        if spec["_rx"] and not spec["_rx"].match(str(meta.get("id"))):
            errors.append(f"{tpl.as_posix()}: id '{meta.get('id')}'가 형식 {spec['id']}와 맞지 않는다")
        if spec.get("status_set") and meta.get("status") not in reg.status_sets.get(spec["status_set"], []):
            errors.append(f"{tpl.as_posix()}: status '{meta.get('status')}'가 '{spec['status_set']}' 집합에 없다")
        for key in meta:
            if key in reg.inverse_names:
                errors.append(f"{tpl.as_posix()}: 역방향 관계 '{key}'를 필드로 두면 안 된다")
            elif key in relation_tops and key not in allowed_tops[ttype]:
                errors.append(f"{tpl.as_posix()}: '{ttype}'은 관계 필드 '{key}'를 가질 수 없다")
    return errors


@dataclass
class Record:
    path: Path  # 저장소 루트 기준
    meta: dict
    type: str
    has_id: bool  # ID 형식이 있는 유형인가 (wiki 등은 id 필드가 있어도 ID로 보지 않는다)

    @property
    def id(self):
        return self.meta.get("id") if self.has_id else None

    @property
    def key(self):
        return self.id or self.path.as_posix()


def file_rule(spec):
    return spec.get("file") or ("{id}.{format}" if spec.get("id") else "**/*.{format}")


def scan(root, reg):
    """레지스트리에 등록된 위치의 레코드를 모은다."""
    records, errors = [], []
    locations = defaultdict(list)
    for name, spec in reg.types.items():
        locations[(spec["path"], spec["format"])].append(name)
    seen = set()
    for (base, fmt), names in sorted(locations.items()):
        folder = root / base
        if not folder.is_dir():
            continue
        patterns = {file_rule(reg.types[n]).format(id="*", format=fmt) for n in names}
        needs_meta = any(reg.types[n].get("id") for n in names)
        files = sorted({f for p in patterns for f in folder.glob(p) if f.is_file()})
        for f in files:
            rel = f.relative_to(root)
            if rel in seen or f.name.startswith(".") or f.name == "README.md":
                continue
            seen.add(rel)
            try:
                meta = read_meta(f)
            except yaml.YAMLError as e:
                errors.append(f"{rel.as_posix()}: YAML을 읽을 수 없다 ({e.__class__.__name__})")
                continue
            if not meta or "type" not in meta:
                if needs_meta:
                    errors.append(f"{rel.as_posix()}: 메타데이터(type)가 없다")
                continue
            if meta["type"] not in names:
                if meta["type"] in reg.types:
                    errors.append(f"{rel.as_posix()}: 유형 '{meta['type']}'은 {base}에 둘 수 없다 (위치: {reg.types[meta['type']]['path']})")
                else:
                    errors.append(f"{rel.as_posix()}: 등록되지 않은 유형 '{meta['type']}'")
                continue
            records.append(Record(rel, meta, meta["type"], bool(reg.types[meta["type"]].get("id"))))
    return records, errors


@dataclass
class Result:
    registry: Registry
    records: list
    by_id: dict
    edges: list  # (출발 Record, 관계 이름, 도착 Record)
    inverse: dict  # 도착 ID -> 역방향 관계 이름 -> [출발 key]
    errors: list
    warnings: list


def validate(root=ROOT):
    root = Path(root)
    reg = load_registry(root)
    errors = list(reg.errors) + check_registry(root, reg)
    warnings = []
    records, scan_errors = scan(root, reg)
    errors += scan_errors

    by_id = {}
    for r in records:
        spec = reg.types[r.type]
        where = r.path.as_posix()
        if spec.get("id"):
            if not isinstance(r.id, str) or not spec["_rx"].match(r.id):
                errors.append(f"{where}: id '{r.id}'가 형식 {spec['id']}와 맞지 않는다")
                continue
            expected = file_rule(spec).format(id=r.id, format=spec["format"]).removeprefix("**/")
            under_base = r.path.relative_to(Path(spec["path"])).as_posix()
            if under_base != expected and not under_base.endswith("/" + expected):
                errors.append(f"{where}: 파일 경로가 ID와 맞지 않는다 (기대: {expected})")
            if r.id in by_id:
                errors.append(f"{where}: 중복 ID {r.id} (먼저 나온 곳: {by_id[r.id].path.as_posix()})")
                continue
            by_id[r.id] = r
        for key in spec.get("required", []):
            if r.meta.get(key) in (None, "", []):
                errors.append(f"{where}: 필수 필드 '{key}'가 비어 있다")
        sset = spec.get("status_set")
        if sset and r.meta.get("status") not in reg.status_sets.get(sset, []):
            errors.append(f"{where}: status '{r.meta.get('status')}'가 '{sset}' 집합에 없다")
        for fld, rset in (spec.get("fields") or {}).items():
            for v in values(r.meta, fld):
                if v not in reg.result_sets.get(rset, []):
                    errors.append(f"{where}: {fld} '{v}'가 '{rset}' 집합에 없다")
        for inv in reg.inverse_names & set(r.meta):
            errors.append(f"{where}: '{inv}'는 역방향 관계라 직접 쓰지 않는다 (스크립트가 계산)")

    edges = []
    inverse = defaultdict(lambda: defaultdict(list))
    for r in records:
        for name, rel in reg.relations.items():
            vals = values(r.meta, reg.relation_field(name))
            if not vals:
                continue
            if r.type not in rel["from"]:
                errors.append(f"{r.path.as_posix()}: '{r.type}'은 관계 '{name}'을 가질 수 없다")
                continue
            for v in vals:
                target = by_id.get(v)
                if target is None:
                    errors.append(f"{r.path.as_posix()}: {name} → {v}: 존재하지 않는 ID")
                elif rel["to"] != "*" and target.type not in rel["to"]:
                    errors.append(f"{r.path.as_posix()}: {name} → {v}: 대상 유형 '{target.type}'은 허용되지 않는다 (허용: {', '.join(rel['to'])})")
                else:
                    edges.append((r, name, target))
                    inverse[target.id][rel["inverse"]].append(r.key)

    for rule in reg.coverage:
        for r in records:
            if r.type != rule["type"] or (rule.get("when_status") and r.meta.get("status") not in rule["when_status"]):
                continue
            if rule.get("field"):
                ok = bool(values(r.meta, rule["field"]))
            else:
                ok = bool(r.id and inverse[r.id][rule["inverse"]])
                if not ok and rule.get("via"):
                    hops = [t for s, n, t in edges if s is r and n in rule["via"]]
                    ok = any(inverse[t.id][rule["inverse"]] for t in hops)
            if not ok:
                (errors if rule.get("severity") == "error" else warnings).append(f"{r.path.as_posix()}: {rule['message']}")

    return Result(reg, records, by_id, edges, inverse, errors, warnings)


def missing_type_paths(root, reg, modules=None):
    """레지스트리 유형의 저장 위치 중 없는 것 (modules가 주어지면 해당 모듈만)."""
    return sorted({s["path"] for s in reg.types.values()
                   if (modules is None or s["module"] in modules) and not (Path(root) / s["path"]).is_dir()})
