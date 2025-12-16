import os
import sys
import json
import argparse

from pycg import CallGraphGenerator
import formats

def main():
    print("begin call pycg.__main__.py")
    parser = argparse.ArgumentParser()
    parser.add_argument("entry_point",
        nargs="*",
        help="Entry points to be processed")
    parser.add_argument(
        "--package",
        help="Package containing the code to be analyzed",
        default=None
    )
    # parser.add_argument(
    #     "--fasten",
    #     help="Produce call graph using the FASTEN format",
    #     action="store_true",
    #     default=False
    # )
    # parser.add_argument(
    #     "--product",
    #     help="Package name",
    #     default=""
    # )
    # parser.add_argument(
    #     "--forge",
    #     help="Source the product was downloaded from",
    #     default=""
    # )
    # parser.add_argument(
    #     "--version",
    #     help="Version of the product",
    #     default=""
    # )
    # parser.add_argument(
    #     "--timestamp",
    #     help="Timestamp of the package's version",
    #     default=0
    # )

    parser.add_argument(
        "-o",
        "--output",
        help="Output path",
        default=None
    )
    args = parser.parse_args()
    # 核心文件分析
    cg = CallGraphGenerator(args.entry_point, args.package)
    cg.analyze()

    # if args.fasten:
    #     formatter = formats.Fasten(cg, args.package, \
    #         args.product, args.forge, args.version, args.timestamp)
    # else:
    #     formatter = formats.Simple(cg)

    formatter = formats.Simple(cg)

    if args.output:
        with open(args.output, "w+") as f:
            f.write(json.dumps(formatter.generate()))
    else:
        print (json.dumps(formatter.generate()))

# if __name__ == "__main__":
#     # input_package  = "/home/wenjinfeng/IntergrationTest"
#     # input_entry_point = "/home/wenjinfeng/IntergrationTest/test.py"
#     # output_file = "/home/wenjinfeng/IntergrationTest/output.json"
#     main()
#     # python3 __main__.py --package /home/wenjinfeng/IntergrationTest /home/wenjinfeng/IntergrationTest/test.py -o /home/wenjinfeng/IntergrationTest/output.json

if __name__ == "__main__":
    
    # main()

    print("=== 直接调用模式 ===")
    # 获取当前文件所在目录的父目录（FaaSLight_Tool 目录）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 上溯两级，得到 FaaSLight 目录
    parent_dir = os.path.dirname(os.path.dirname(current_dir))  # FaaSLight 目录

    # 构建正确的路径
    test_package = os.path.join(parent_dir, "Original_app", "app3")
    test_entry_points = [os.path.join(parent_dir, "Original_app", "app3", "main.py")]
    test_output = os.path.join(parent_dir, "Original_app", "app3", "output.json")

    # 验证路径是否存在
    if not os.path.exists(test_entry_points[0]):
        print(f"❌ 错误: 入口文件不存在 - {test_entry_points[0]}")
        print("请检查 app3/main.py 文件是否存在")
        sys.exit(1)
    
    # 保存原始命令行参数
    original_argv = sys.argv.copy()
    
    try:
        # 设置模拟的命令行参数
        sys.argv = ['pycg', '--package', test_package] + test_entry_points + ['-o', test_output]
        main()
        
    finally:
        # 恢复原始命令行参数
        sys.argv = original_argv