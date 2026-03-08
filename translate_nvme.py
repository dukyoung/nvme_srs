#!/usr/bin/env python3
"""
NVMe Spec Chapter 8 번역 스크립트
- 섹션 단위로 분할하여 claude CLI로 번역
- 체크포인트 기반 중단/재시작 지원
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

INPUT_FILE = Path("doc/spec/nvme22_08_extended_capabilities.md")
OUTPUT_FILE = Path("nvme_ch8_korean.md")
CHECKPOINT_FILE = Path("checkpoint.json")

MAX_CHUNK_LINES = 200

TRANSLATE_PROMPT = """다음 NVMe Spec 원문을 한국어로 번역해줘.
규칙:
- 원문 내용을 빠짐없이 완전히 번역
- 기술 용어(필드명, 명령어명, 레지스터명)는 한국어+영어 병기: 예) 비동기 이벤트(Asynchronous Event)
- shall → 해야 한다, should → 권장한다, may → 할 수 있다, shall not → 해서는 안 된다
- Figure 번호, 표 내용, 리스트 항목 모두 번역
- 번역문만 출력 (설명이나 주석 없이)

원문:
{text}"""

# 섹션 헤더 패턴: **8.x...** 또는 **제목** (Bold 단독 라인)
SECTION_HEADER_RE = re.compile(
    r"^(\*\*8\.\d+[\d.]*\*\*.*|"      # **8.x.y.z** ... 형태
    r"\*\*[A-Z][A-Za-z /:()–-]+\*\*)$"  # **Title Text** 형태
)


def is_section_header(line: str) -> bool:
    return bool(SECTION_HEADER_RE.match(line.strip()))


def split_into_sections(lines: list[str]) -> list[list[str]]:
    """파일을 섹션 헤더 기준으로 분할"""
    sections = []
    current = []

    for line in lines:
        if is_section_header(line) and current:
            sections.append(current)
            current = [line]
        else:
            current.append(line)

    if current:
        sections.append(current)

    return sections


def split_large_chunks(sections: list[list[str]], max_lines: int) -> list[list[str]]:
    """max_lines 초과 섹션을 빈 줄 기준으로 재분할"""
    chunks = []
    for section in sections:
        if len(section) <= max_lines:
            chunks.append(section)
            continue

        # 빈 줄(paragraph break) 기준으로 나누기
        sub = []
        for line in section:
            sub.append(line)
            if len(sub) >= max_lines and line.strip() == "":
                chunks.append(sub)
                sub = []
        if sub:
            chunks.append(sub)

    return chunks


def translate_chunk(text: str) -> str:
    """claude CLI를 subprocess로 호출하여 번역"""
    prompt = TRANSLATE_PROMPT.format(text=text)
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        env=env,
    )
    if result.returncode != 0:
        print(f"  [오류] claude 호출 실패: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8"))
    return {"completed": [], "total": 0}


def save_checkpoint(data: dict):
    CHECKPOINT_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main():
    if not INPUT_FILE.exists():
        print(f"입력 파일을 찾을 수 없습니다: {INPUT_FILE}")
        sys.exit(1)

    lines = INPUT_FILE.read_text(encoding="utf-8").splitlines(keepends=True)
    sections = split_into_sections(lines)
    chunks = split_large_chunks(sections, MAX_CHUNK_LINES)
    total = len(chunks)

    print(f"총 {total}개 청크로 분할 완료 (원본 {len(lines)}줄)")

    # 체크포인트 로드
    ckpt = load_checkpoint()
    completed = set(ckpt.get("completed", []))

    # 기존 번역 결과 로드 (있으면)
    translated: dict[int, str] = {}
    if ckpt.get("total") == total and OUTPUT_FILE.exists():
        # 이전 결과 파일에서 청크별 구분자로 복원
        pass  # 청크별로 개별 파일 대신 순차 append 방식 사용

    # 번역 실행
    for i, chunk in enumerate(chunks):
        chunk_id = i + 1
        if chunk_id in completed:
            print(f"  청크 {chunk_id}/{total} - 이미 완료, 건너뜀")
            continue

        chunk_text = "".join(chunk)
        print(f"  청크 {chunk_id}/{total} 번역 중...", flush=True)

        result = translate_chunk(chunk_text)
        translated[chunk_id] = result

        # 결과를 임시 파일에 저장
        chunk_file = Path(f".chunk_{chunk_id}.tmp")
        chunk_file.write_text(result, encoding="utf-8")

        completed.add(chunk_id)
        save_checkpoint({"completed": sorted(completed), "total": total})
        print(f"  청크 {chunk_id}/{total} 완료 ✓")

    # 최종 파일 조합
    print(f"\n번역 파일 조합 중...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i in range(total):
            chunk_id = i + 1
            chunk_file = Path(f".chunk_{chunk_id}.tmp")
            if chunk_file.exists():
                f.write(chunk_file.read_text(encoding="utf-8"))
            elif chunk_id in translated:
                f.write(translated[chunk_id])
            f.write("\n\n")

    # 임시 파일 정리
    for i in range(total):
        chunk_file = Path(f".chunk_{i + 1}.tmp")
        if chunk_file.exists():
            chunk_file.unlink()

    print(f"번역 완료: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
