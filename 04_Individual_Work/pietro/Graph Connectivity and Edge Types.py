# Active edge mask:
is_sh_player = (src_sh & (~dst_post)) | (dst_sh & (~src_post))
is_sh_post = (src_sh & dst_post) | (dst_sh & src_post)
is_post_post = src_post & dst_post
is_cone_player_post = (
    (src_cone_or_gk & (~src_sh) & (~src_post) & dst_post)
    | (dst_cone_or_gk & (~dst_sh) & (~dst_post) & src_post)
)
is_player_player = (~src_sh) & (~dst_sh) & (~src_post) & (~dst_post) & (dist_pair <= 5.0)

edge_keep = is_sh_player | is_sh_post | is_post_post | is_cone_player_post | is_player_player

# 8 semantic edge types
rel_type = np.full(len(src_all), 7, dtype=np.int64)
other_tm = np.where(src_sh, n_tm[dst_all], n_tm[src_all])
other_gk = np.where(src_sh, n_gk[dst_all], n_gk[src_all])
rel_type[is_sh_player & other_gk] = 2
rel_type[is_sh_player & (~other_gk) & (other_tm == 1)] = 1
rel_type[is_sh_player & (~other_gk) & (other_tm == 0)] = 0
rel_type[is_sh_post] = 3
player_side_gk = np.where(dst_post, n_gk[src_all], n_gk[dst_all])
rel_type[is_cone_player_post & player_side_gk] = 4
rel_type[is_cone_player_post & (~player_side_gk)] = 5
rel_type[is_post_post] = 6

# Edge feature matrix (20 features per edge)
E_all = np.column_stack([
    dist_pair / 10.0, inv_dist, dx_pair / 10.0, dy_pair / 10.0,
    ddist_goal / 10.0, n_dsl[dst_all] / 10.0,
    edge_clearance, edge_ray_dist, edge_occ,
    np.maximum(n_b4[src_all], n_b4[dst_all]),
    np.maximum(n_f7[src_all], n_f7[dst_all]),
    np.maximum(n_cn[src_all].astype(np.float32), n_cn[dst_all].astype(np.float32)),
    rel_onehot,
]).astype(np.float32)
