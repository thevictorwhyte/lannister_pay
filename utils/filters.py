def filter_flat_type(item):
    return item['SplitType'] == 'FLAT'


def filter_percentage_type(item):
    return item['SplitType'] == 'PERCENTAGE'


def filter_ratio_type(item):
    return item['SplitType'] == 'RATIO'


# 12580 - 45 = 12535 - Flat
# 0.3 * 12535 = 3760.5, 12535 - 3760.5 = 8774.5 - Percentage
# 8774.5
# 0 - final balance
