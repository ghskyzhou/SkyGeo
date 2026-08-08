from pathlib import Path
import re
import sys

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

# pack.py 位于:
# SkyGeo/tools/pack/pack.py
#
# 所以 parents[2] 就是 SkyGeo/
ROOT = Path(__file__).resolve().parents[2]

EXPERIMENTS_DIR = ROOT / "experiments"
INCLUDE_DIR = ROOT / "include"


# 匹配:
#   #include <core.hpp>
#   #include "core.hpp"
#   # include <foo/bar.hpp>
INCLUDE_PATTERN = re.compile(
    r'^\s*#\s*include\s*[<"]([^>"]+)[>"]\s*$'
)

# ------------------------------------------------------------
# Find experiments
# ------------------------------------------------------------

def find_experiments():
    """
    返回 experiments/ 下所有包含 main.cpp 的一级子文件夹。
    """
    experiments = []

    for directory in EXPERIMENTS_DIR.iterdir():
        if directory.is_dir() and (directory / "main.cpp").exists():
            experiments.append(directory.name)

    return sorted(experiments)


def choose_experiment(experiments):
    """
    让用户选择要打包的实验。
    默认选择 test。
    """

    if not experiments:
        raise RuntimeError("experiments/ 下没有找到任何包含 main.cpp 的文件夹。")

    print("Available experiments:")

    for i, name in enumerate(experiments, start=1):
        print(f"  {i}. {name}")

    print()

    default = "test" if "test" in experiments else experiments[0]

    while True:
        choice = input(f"Choose experiment [{default}]: ").strip()

        # 直接回车 -> 默认
        if not choice:
            return default

        # 输入数字
        if choice.isdigit():
            index = int(choice)

            if 1 <= index <= len(experiments):
                return experiments[index - 1]

        # 输入文件夹名
        if choice in experiments:
            return choice

        print("Invalid choice. Try again.")

# ------------------------------------------------------------
# Header resolving
# ------------------------------------------------------------

def resolve_local_header(header_name, current_file):
    """
    判断一个 #include 是否是 SkyGeo 自己的头文件。

    支持:
        #include <core.hpp>
        #include <geometry/point.hpp>

    以及:
        #include "foo.hpp"

    查找顺序:
        1. 当前文件所在目录
        2. SkyGeo/include/
    """

    candidates = [
        current_file.parent / header_name,
        INCLUDE_DIR / header_name,
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate.resolve()

    return None

# ------------------------------------------------------------
# Packing
# ------------------------------------------------------------

def expand_file(path, expanded_files):
    """
    递归展开一个 cpp/hpp 文件。

    - 系统 include 保留
    - SkyGeo 本地 include 被替换成实际内容
    - 同一个本地头文件只展开一次
    - 删除 #pragma once
    """

    path = path.resolve()

    # 防止一个头文件被展开多次
    if path in expanded_files:
        return ""

    expanded_files.add(path)

    lines = path.read_text(encoding="utf-8").splitlines()

    output = []

    for line in lines:

        # 单文件打包后 pragma once 没用了
        if line.strip() == "#pragma once":
            continue

        match = INCLUDE_PATTERN.match(line)

        if not match:
            output.append(line)
            continue

        header_name = match.group(1)

        local_header = resolve_local_header(
            header_name,
            path
        )

        # ----------------------------------------------------
        # 本地 header -> 展开
        # ----------------------------------------------------

        if local_header is not None:

            output.append("")
            output.append(
                f"// ===== BEGIN {header_name} ====="
            )
            output.append("")

            expanded = expand_file(
                local_header,
                expanded_files
            )

            if expanded:
                output.append(expanded)

            output.append("")
            output.append(
                f"// ===== END {header_name} ====="
            )
            output.append("")

        # ----------------------------------------------------
        # 系统 header -> 原样保留
        # ----------------------------------------------------

        else:
            output.append(line)

    return "\n".join(output)

def pack(experiment_name):
    main_cpp = (
        EXPERIMENTS_DIR
        / experiment_name
        / "main.cpp"
    )

    output_cpp = ROOT / f"{experiment_name}.cpp"

    expanded_files = set()

    result = expand_file(
        main_cpp,
        expanded_files
    )

    # 文件末尾补 newline
    result += "\n"

    output_cpp.write_text(
        result,
        encoding="utf-8"
    )

    print()
    print(f"Packed: {main_cpp.relative_to(ROOT)}")
    print(f"Output: {output_cpp.relative_to(ROOT)}")

    print()
    print("Included project files:")

    for path in sorted(expanded_files):
        print(f"  - {path.relative_to(ROOT)}")

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    experiments = find_experiments()

    # 命令行指定：
    # python pack.py test
    if len(sys.argv) >= 2:
        experiment = sys.argv[1]

        if experiment not in experiments:
            print(f'Error: experiment "{experiment}" not found.')
            print()
            print("Available experiments:")

            for name in experiments:
                print(f"  - {name}")

            sys.exit(1)

    # 没指定参数：
    # python pack.py
    # 进入原来的交互选择
    else:
        experiment = choose_experiment(experiments)

    pack(experiment)


if __name__ == "__main__":
    main()