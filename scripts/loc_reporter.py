import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

EXCLUDED_DIRS = {
    'venv', '.venv', 'env', '.git', '__pycache__', '.pytest_cache',
    'node_modules', 'instance', 'htmlcov', '.idea', '.vscode'
}

VALID_EXTENSIONS = {
    '.py': 'Python',
    '.html': 'HTML Templates',
    '.css': 'CSS Styles',
    '.js': 'JavaScript',
    '.json': 'JSON/Configs',
    '.md': 'Documentation',
    '.toml': 'Configs'
}


def calculate_loc_breakdown():
    category_counts = {}
    file_counts = {}
    total_loc = 0
    total_test_loc = 0
    total_source_loc = 0

    for root, dirs, files in os.walk(ROOT_DIR):
        # Filter out excluded directories in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith('.')]

        rel_root = os.path.relpath(root, ROOT_DIR)
        is_test_dir = rel_root.startswith('tests')

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in VALID_EXTENSIONS:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        count = len(lines)
                        total_loc += count

                        lang = VALID_EXTENSIONS[ext]
                        category_counts[lang] = category_counts.get(lang, 0) + count
                        file_counts[lang] = file_counts.get(lang, 0) + 1

                        if is_test_dir:
                            total_test_loc += count
                        else:
                            total_source_loc += count
                except Exception as e:
                    pass

    report = []
    report.append("=" * 65)
    report.append("  SHOPSENSE AI — ACCURATE LOC & CODEBASE AUDIT REPORT")
    report.append("=" * 65)
    report.append(f"{'Category / Language':<25} | {'Files':<8} | {'Lines of Code':<15}")
    report.append("-" * 65)
    for lang, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        report.append(f"{lang:<25} | {file_counts.get(lang, 0):<8} | {count:<15,}")
    report.append("-" * 65)
    report.append(f"{'Total Source LOC':<25} | {'':<8} | {total_source_loc:<15,}")
    report.append(f"{'Total Test LOC':<25} | {'':<8} | {total_test_loc:<15,}")
    report.append(f"{'TOTAL GENUINE LOC':<25} | {'':<8} | {total_loc:<15,}")
    report.append("=" * 65)

    return "\n".join(report)


if __name__ == '__main__':
    print(calculate_loc_breakdown())
