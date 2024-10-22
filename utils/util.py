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

def print_time(start_time, end_time):
    dur_time = end_time - start_time

    hours = dur_time // 3600
    minutes = (dur_time % 3600) // 60
    seconds = round(dur_time % 60, 2)  # 保留两位小数

    if hours > 0:
        print("It takes {}h {}min {:.2f}s.".format(hours, minutes, seconds))
    else:
        print("It takes {}min {:.2f}s.".format(minutes, seconds))