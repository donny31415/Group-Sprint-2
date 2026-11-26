# Zone filtering: Shooter U 4y back semicircle U 7y front semicircle U cone U goalkeeper
in_back_4 = (~is_sh_raw) & (players["dx"].values < 0) & (players["dist_shooter"].values <= 4.0)
in_front_7 = (~is_sh_raw) & (players["dx"].values >= 0) & (players["dist_shooter"].values <= 7.0)
in_cone = (~is_sh_raw) & in_tri
is_gk = players["is_keeper"].values == 1

keep_mask = is_sh_raw | in_back_4 | in_front_7 | in_cone | is_gk
active = players[keep_mask].copy()