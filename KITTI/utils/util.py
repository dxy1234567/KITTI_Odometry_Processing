def print_progress(i, N):
    """
    打印当前进度。

    Param:
        i: 当前进度（第i次迭代）
        N: 总迭代次数
    """
    if i % 100 == 0 or i == N:  # 每 100 次迭代或最后一次迭代时更新进度
        run = i / N * 100
        print("Runing: {:.2f}% done.".format(run))