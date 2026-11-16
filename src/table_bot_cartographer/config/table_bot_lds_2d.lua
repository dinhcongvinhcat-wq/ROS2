-- Cau hinh Cartographer cho table_bot (4 chan-banh), dung 2D LiDAR + IMU
-- Luu y: table_bot khong co lop base_footprint rieng, root frame la "base_link"

include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  tracking_frame = "base_link",
  published_frame = "odom",
  odom_frame = "odom",
  provide_odom_frame = false,        -- odom da duoc plugin DiffDrive cua Gazebo phat ra
  publish_frame_projected_to_2d = true,
  use_odometry = true,
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1,
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

MAP_BUILDER.use_trajectory_builder_2d = true

TRAJECTORY_BUILDER_2D.min_range = 0.15
TRAJECTORY_BUILDER_2D.max_range = 8.0
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 3.
-- Bat IMU: banh xe la skid-steer co dinh, odom hay mat chinh xac goc xoay
-- do truot khi re. IMU do goc xoay truc tiep giup Cartographer bot phu
-- thuoc vao odom -> giam han hien tuong map bi troi/lech.
TRAJECTORY_BUILDER_2D.use_imu_data = true
TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = true
TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.linear_search_window = 0.2
TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.angular_search_window = math.rad(30.)
TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.translation_delta_cost_weight = 10.
TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.rotation_delta_cost_weight = 10.
TRAJECTORY_BUILDER_2D.motion_filter.max_angle_radians = math.rad(0.1)
TRAJECTORY_BUILDER_2D.motion_filter.max_distance_meters = 0.02
TRAJECTORY_BUILDER_2D.motion_filter.max_time_seconds = 5.

-- Ceres scan matcher: giam trong so "bam theo pose du doan tu odom" de scan
-- duoc tu do keo ve vi tri dung hon khi odom sai lech do banh truot.
-- (mac dinh tham khao: occupied_space_weight=1., translation_weight=10., rotation_weight=40.)
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.occupied_space_weight = 1.2
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.translation_weight = 5.
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.rotation_weight = 20.

POSE_GRAPH.constraint_builder.min_score = 0.65
POSE_GRAPH.constraint_builder.global_localization_min_score = 0.7

-- Pose graph (backend): giam trong so tin tuong odometry, tang trong so
-- tin tuong ket qua scan-matching cuc bo (local SLAM) khi toi uu toan cuc.
-- (mac dinh tham khao: ca 4 gia tri deu ~1e5)
POSE_GRAPH.optimization_problem.odometry_translation_weight = 1e4
POSE_GRAPH.optimization_problem.odometry_rotation_weight = 1e4
POSE_GRAPH.optimization_problem.local_slam_pose_translation_weight = 1e5
POSE_GRAPH.optimization_problem.local_slam_pose_rotation_weight = 1e5

return options
