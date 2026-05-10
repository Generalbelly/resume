# Resume Project

## ドキュメント構成

| ファイル | 用途 |
|---|---|
| `README.md` | 日本語職務経歴書・GitHubポートフォリオ・転職サービス記入の参照元 |
| `Resume.pdf` | 英語職務経歴書（Google Docからエクスポート） |

## Google Doc（英語版）へのアクセス

GWS CLI を使って Google Docs API 経由でアクセスできる。

```bash
# ドキュメント全文を取得（プレーンテキスト）
gws docs documents get --params '{"documentId": "1lkghEoKXK8vqbNfuEZe2LljkRcltqW6zjfyl_qXkysM"}' 2>/dev/null | python3 -c "
import json, sys
doc = json.load(sys.stdin)

def extract_text(content):
    lines = []
    for block in content:
        para = block.get('paragraph')
        if not para:
            tb = block.get('table')
            if tb:
                for row in tb.get('tableRows', []):
                    for cell in row.get('tableCells', []):
                        lines.extend(extract_text(cell.get('content', [])))
            continue
        line = ''
        for el in para.get('elements', []):
            text = el.get('textRun', {}).get('content', '')
            line += text
        lines.append(line)
    return lines

print(''.join(extract_text(doc.get('body', {}).get('content', []))))
"
```

Document ID: `1lkghEoKXK8vqbNfuEZe2LljkRcltqW6zjfyl_qXkysM`

## 転職サービス

- **Findy**: GitHubとのスキル連携あり。使用技術タグの整合性が評価に直結する
- **転職ドラフト**: 企業入札形式。成果の数値インパクトを前面に出す書き方が有効

## 方針

- `README.md` を正とし、英語版 Google Doc はそれに合わせて更新する
- 「その他エンジニアとしての自分について」セクションは転職サービス・英語版には使わない
- 英語版は翻訳ではなく英語圏のレジュメ慣習（数値強調・STAR形式）に合わせて書く
