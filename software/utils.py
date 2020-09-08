def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)


def num_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min