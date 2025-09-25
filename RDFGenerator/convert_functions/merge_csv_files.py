import pandas as pd

def merge_csv_files(table1_path, table2_path, output_path):
    """
    合并两个 CSV 文件，第一个表格只有1行时增加行数与第二个表格一样，内容复制第1行，
    最后将两个表格横向合并并输出为一个新的 CSV 文件。

    :param table1_path: 第一个 CSV 文件路径。
    :param table2_path: 第二个 CSV 文件路径。
    :param output_path: 输出的 CSV 文件路径。
    """
    # 读取两个 CSV 文件
    table1 = pd.read_csv(table1_path)
    table2 = pd.read_csv(table2_path)

    # 如果 table1 只有1行，扩展它的行数到与 table2 一样
    if len(table1) == 1:
        table1 = pd.concat([table1] * len(table2), ignore_index=True)

    # 合并两个表格（横向合并）
    result = pd.concat([table1, table2], axis=1)

    # 将合并后的结果输出为 CSV 文件
    result.to_csv(output_path, index=False)

    print(f"合并后的结果已保存为 {output_path}")

# 示例使用
table1_path = 'table1.csv'  # 第一个 CSV 文件路径
table2_path = 'table2.csv'  # 第二个 CSV 文件路径
output_path = 'output.csv'  # 输出合并后的 CSV 文件路径

merge_csv_files(table1_path, table2_path, output_path)
