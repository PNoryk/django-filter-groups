def get_filter_class_with_group_label(filter_class, group_label):
    return type(f"{filter_class.__name__}WithCustomGroupLabel", (filter_class,), {"filter_group_label": group_label})
