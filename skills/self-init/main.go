package main

import (
	"embed"
	"flag"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
	"time"
)

//go:embed templates/*
var templateFS embed.FS

type FileMapping struct {
	TemplateName string
	TargetPath   string
}

func main() {
	targetDir := flag.String("target", ".", "目标仓库工作目录（默认为当前目录）")
	force := flag.Bool("force", false, "是否覆盖已存在的文件（默认为 false）")
	flag.Parse()

	absTarget, err := filepath.Abs(*targetDir)
	if err != nil {
		fmt.Fprintf(os.Stderr, "❌ 解析目标路径失败: %v\n", err)
		os.Exit(1)
	}

	today := time.Now().Format("2006-01-02")

	fmt.Println("==================================================")
	fmt.Println("🚀 个人知识系统 (myself) 骨架初始化程序")
	fmt.Printf("📂 目标路径: %s\n", absTarget)
	fmt.Printf("📅 基线日期: %s\n", today)
	fmt.Println("==================================================")

	// 1. 创建核心目录
	dirs := []string{
		"source/chats",
		"source/documents",
		"docs/increments",
		"context",
	}

	for _, d := range dirs {
		p := filepath.Join(absTarget, d)
		if err := os.MkdirAll(p, 0755); err != nil {
			fmt.Fprintf(os.Stderr, "❌ 创建目录失败 %s: %v\n", d, err)
			os.Exit(1)
		}
		fmt.Printf("📁 [DIR]  %s\n", d)
	}

	// 2. 映射表
	mappings := []FileMapping{
		{"AGENTS.md.template", "AGENTS.md"},
		{"README.md.template", "README.md"},
		{"CHANGELOG.md.template", "CHANGELOG.md"},
		{"gitignore.template", ".gitignore"},
		{"00_specification.md.template", "docs/00_存储与内容格式规范.md"},
		{"01_raw_statements.md.template", "docs/01_原始自述.md"},
		{"02_complete_narrative.md.template", "docs/02_完整自述（整合版）.md"},
		{"03_timeline.md.template", "docs/03_事实、人物与时间线.md"},
		{"04_ai_evolution.md.template", "docs/04_AI分析与认知演化.md"},
		{"05_understanding_model.md.template", "context/05_当前理解模型.md"},
		{"06_ai_context.md.template", "context/06_AI_CONTEXT.md"},
		{"baseline_questions.md.template", "docs/基线认知测试题组.md"},
	}

	createdCount := 0
	skippedCount := 0

	for _, m := range mappings {
		targetFile := filepath.Join(absTarget, m.TargetPath)

		if _, err := os.Stat(targetFile); err == nil && !*force {
			fmt.Printf("⏩ [SKIP] %s (已存在，未覆盖)\n", m.TargetPath)
			skippedCount++
			continue
		}

		contentBytes, err := fs.ReadFile(templateFS, "templates/"+m.TemplateName)
		if err != nil {
			fmt.Fprintf(os.Stderr, "❌ 读取内嵌模板失败 %s: %v\n", m.TemplateName, err)
			os.Exit(1)
		}

		content := strings.ReplaceAll(string(contentBytes), "{{DATE}}", today)

		// 确保父目录存在
		if err := os.MkdirAll(filepath.Dir(targetFile), 0755); err != nil {
			fmt.Fprintf(os.Stderr, "❌ 创建父目录失败: %v\n", err)
			os.Exit(1)
		}

		if err := os.WriteFile(targetFile, []byte(content), 0644); err != nil {
			fmt.Fprintf(os.Stderr, "❌ 写入文件失败 %s: %v\n", m.TargetPath, err)
			os.Exit(1)
		}

		fmt.Printf("✅ [FILE] %s\n", m.TargetPath)
		createdCount++
	}

	fmt.Println("--------------------------------------------------")
	fmt.Printf("🎉 初始化完成！新建文件: %d 个，跳过文件: %d 个。\n", createdCount, skippedCount)
	fmt.Println("==================================================")
	fmt.Println("🔐 【重要隐私与安全声明】")
	fmt.Println("1. 私有仓库保护：本系统包含你高度隐私的身心感受与人际经历。若将本仓库推送到 GitHub/GitLab 等平台，请务必设为【Private 私有仓库】！")
	fmt.Println("2. 模型训练授权：在使用的 AI 工具（如 Cursor/Claude Code/网页端）设置中，建议关闭「允许使用我的数据训练公共模型」选项。")
	fmt.Println("--------------------------------------------------")
	fmt.Println("💡 【极简启动指引】")
	fmt.Println("现在直接在 AI 聊天框中对它说：")
	fmt.Println("👉 「你来采访我吧」或「开始建立我的个人档案」")
	fmt.Println("AI 将自动进入基线破冰访谈，开启你的第一份认知档案！")
	fmt.Println("==================================================")
}
