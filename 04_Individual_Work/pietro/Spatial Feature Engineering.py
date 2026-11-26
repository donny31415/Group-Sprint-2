def point_to_segment_stats(px, py, ax, ay, bx, by):
    """
    Computes exact Euclidean distance and clamped projection parameter t in [0, 1]
    from point P(px, py) to line segment AB from A(ax, ay) to B(bx, by).
    """
    vx, vy = bx - ax, by - ay
    ux, uy = px - ax, py - ay
    seg_len_sq = np.maximum(vx * vx + vy * vy, 1e-8)
    t = np.clip((ux * vx + uy * vy) / seg_len_sq, 0.0, 1.0)
    proj_x, proj_y = ax + t * vx, ay + t * vy
    dist = np.sqrt((px - proj_x) ** 2 + (py - proj_y) ** 2)
    return dist, t, proj_x, proj_y

# Exact lateral clearances to Left Post segment S->(120,36), Right Post segment S->(120,44), and Goal Line
d_seg_left, t_seg_left, _, _ = point_to_segment_stats(px, py, sx_arr, sy_arr, 120.0, 36.0)
d_seg_right, t_seg_right, _, _ = point_to_segment_stats(px, py, sx_arr, sy_arr, 120.0, 44.0)
d_seg_goalline, _, _, _ = point_to_segment_stats(px, py, 120.0, 36.0, 120.0, 44.0)

# Signed lateral clearance to cone boundary (+ inside cone, - outside cone)
min_ray_dist = np.minimum(d_seg_left, d_seg_right)
signed_cone_clearance = np.where(is_sh_raw, 0.0, np.where(in_tri, min_ray_dist, -min_ray_dist))

# Normalized lateral angle fraction across cone [0 = left post ray, 1 = right post ray]
ang_left_ray = np.arctan2(36.0 - sy_arr, 120.0 - sx_arr)
ang_right_ray = np.arctan2(44.0 - sy_arr, 120.0 - sx_arr)
ang_player = np.arctan2(py - sy_arr, px - sx_arr)
cone_span = np.maximum(ang_right_ray - ang_left_ray, 1e-5)
rel_cone_pos = np.where(is_sh_raw, 0.5, np.clip((ang_player - ang_left_ray) / cone_span, -0.5, 1.5))

# Angular shadow blocked by player's body (~0.45 yd radius) relative to visible goal angle
body_occ_angle = np.where(is_sh_raw, 0.0, 2.0 * np.arctan(0.45 / np.maximum(players["dist_shooter"].values, 0.5)))
occ_fraction = np.where(in_tri, np.minimum(1.0, body_occ_angle / np.maximum(s_ang_arr, 1e-3)), 0.0)
