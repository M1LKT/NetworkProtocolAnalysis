def standrdizedData(**kwargs):
    """
    标准化数据的函数。

    Args:
        **kwargs: 关键字参数，表示要标准化的数据。

    Returns:
        list: 标准化后的数据列表，每个元素都是一个字典，包含一个键值对。

    """
    StandrdizedData = []
    for key, value in kwargs.items():
        data={key:value}
        StandrdizedData.append(data)
    return StandrdizedData
