#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
myself 个人知识系统骨架初始化脚本 (Python 跨平台版)
适用于 Android、iOS、Linux、macOS、Windows 等所有支持 Python 3 的环境。
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 映射表：(模板文件名, 目标相对路径)
FILE_MAPPINGS = [
    ("AGENTS.md.template", "AGENTS.md"),
    ("README.md.template", "README.md"),
    ("CHANGELOG.md.template", "CHANGELOG.md"),
    ("gitignore.template", ".gitignore"),
    ("00_specification.md.template", "docs/00_存储与内容格式规范.md"),
    ("01_raw_statements.md.template", "docs/01_原始自述.md"),
    ("02_complete_narrative.md.template", "docs/02_完整自述（整合版）.md"),
    ("03_timeline.md.template", "docs/03_事实、人物与时间线.md"),
    ("04_ai_evolution.md.template", "docs/04_AI分析与认知演化.md"),
    ("05_understanding_model.md.template", "context/05_当前理解模型.md"),
    ("06_ai_context.md.template", "context/06_AI_CONTEXT.md"),
    ("baseline_questions.md.template", "docs/基线认知测试题组.md"),
]

CORE_DIRS = [
    "source/chats",
    "source/documents",
    "docs/increments",
    "context",
]


def resolve_templates_dir() -> Path:
    """寻找 templates 目录（支持从 scripts/ 运行或从 skill 根目录运行）"""
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir.parent / "templates",      # skills/self-init/scripts/ -> skills/self-init/templates
        script_dir / "templates",             # skills/self-init/ -> templates
        Path.cwd() / "skills/self-init/templates",
        Path.cwd() / ".agents/skills/self-init/templates",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    raise FileNotFoundError(f"无法找到 templates 目录，检索路径: {[str(c) for c in candidates]}")


def main():
    parser = argparse.ArgumentParser(description="个人知识系统 (myself) 骨架初始化程序 (Python 版)")
    parser.add_argument("--target", default=".", help="目标仓库工作目录（默认为当前目录）")
    parser.add_argument("--force", action="store_true", help="是否覆盖已存在的文件（默认为 false）")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    today = datetime.now().strftime("%Y-%m-%d")

    print("==================================================")
    print("🚀 个人知识系统 (myself) 骨架初始化程序 (Python)")
    print(f"📂 目标路径: {target_dir}")
    print(f"📅 基线日期: {today}")
    print("==================================================")

    try:
        templates_dir = resolve_templates_dir()
    except Exception as e:
        print(f"❌ 查找模板目录失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 1. 创建核心目录
    for d in CORE_DIRS:
        p = target_dir / d
        p.mkdir(parents=True, exist_ok=True)
        print(f"📁 [DIR]  {d}")

    # 2. 写入骨架文档
    created_count = 0
    skipped_count = 0

    for tmpl_name, target_rel in FILE_MAPPINGS:
        target_file = target_dir / target_rel
        tmpl_file = templates_dir / tmpl_name

        if target_file.exists() and not args.force:
            print(f"⏩ [SKIP] {target_rel} (已存在，未覆盖)")
            skipped_count += 1
            continue

        if not tmpl_file.is_file():
            print(f"❌ 找不到模板文件: {tmpl_file}", file=sys.stderr)
            sys.exit(1)

        try:
            content = tmpl_file.read_text(encoding="utf-8")
            rendered = content.replace("{{DATE}}", today)

            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(rendered, encoding="utf-8")
            print(f"✅ [FILE] {target_rel}")
            created_count += 1
        except Exception as e:
            print(f"❌ 写入文件失败 {target_rel}: {e}", file=sys.stderr)
            sys.exit(1)

    print("--------------------------------------------------")
    print(f"🎉 初始化完成！新建文件: {created_count} 个，跳过文件: {skipped_count} 个。")
    print("==================================================")
    print("🔐 【重要隐私与安全声明】")
    print("1. 私有仓库保护：本系统包含你高度隐私的身心感受与人际经历。若将本仓库推送到 GitHub/GitLab 等平台，请务必设为【Private 私有仓库】！")
    print("2. 模型训练授权：在使用的 AI 工具设置中，建议关闭「允许使用我的数据训练公共模型」选项。")
    print("--------------------------------------------------")
    print("💡 【极简启动指引】")
    print("现在直接在 AI 聊天框中对它说：")
    print("👉 「你来采访我吧」或「开始建立我的个人档案」")
    print("AI 将自动进入基线破冰访谈，开启你的第一份认知档案！")
    print("==================================================")


if __name__ == "__main__":
    main()
