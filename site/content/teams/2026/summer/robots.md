---
title: Robots
menu:
  main:
    identifier: robots-2026
    parent: summer-2026
    weight: 20
---

The Summer 2026 Robots team focuses on building, testing, and demonstrating physical robot systems through multiple technical tracks. Each track goes deep on a different robotics skill, and teams will collaborate so tools from one track can support the others.

Get the code for these projects at the [League Robotics GitHub](https://github.com/league-robotics) and the docs from the [League Robotics Documentation](https://league-robotics.github.io/).

## Track 1: Odometry and Robot Localization

This track focuses on estimating where a robot is on the field over time. Students will compare dead-wheel odometers and optical-flow odometers, then test how each method behaves during acceleration, turning, and wheel slip. The goal is to improve real-time location accuracy so path-following and autonomous routines become more reliable.

<div style="text-align: center; margin: 1rem 0;">
  <img src="/images/robots-2026-track1-topdown.png" alt="Top-down robotics field view with AprilTag detections on two robots" style="width: 100%; max-width: 600px; height: auto;" />
</div>

Project deep dive: [Path planning robot chase demo](track1-path-planning-chase)

Learn more:

* Odometry (Wikipedia): https://en.wikipedia.org/wiki/Odometry
* Dead reckoning (Wikipedia): https://en.wikipedia.org/wiki/Dead_reckoning
* Optical flow (Wikipedia): https://en.wikipedia.org/wiki/Optical_flow
* WPILib kinematics and odometry docs: https://docs.wpilib.org/en/stable/docs/software/kinematics-and-odometry/index.html

## Track 2: Machine Vision on Raspberry Pi

This track goes beyond prebuilt vision controllers by writing custom vision pipelines on Raspberry Pi camera systems. Students will learn camera calibration, homography, AprilTag reading, and object detection so they can build scene understanding that fits their own robot goals and field conditions.

Learn more:

* OpenCV camera calibration tutorial: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
* Homography (Wikipedia): https://en.wikipedia.org/wiki/Homography
* AprilTag project: https://april.eecs.umich.edu/software/apriltag
* OpenCV object detection (DNN module): https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html

## Track 3: Control Algorithms

This track focuses on closed-loop control and state estimation for smooth, synchronized movement. Students will implement PID controllers, explore Kalman filters, and tune multi-servo coordination so mechanisms can move together with less oscillation and better repeatability.

Learn more:

* PID controller (Wikipedia): https://en.wikipedia.org/wiki/PID_controller
* Kalman filter (Wikipedia): https://en.wikipedia.org/wiki/Kalman_filter
* University of Michigan CTMS PID introduction: https://ctms.engin.umich.edu/CTMS/index.php?example=Introduction&section=ControlPID
* A gentle Kalman filter introduction (UNC): https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf

## Track 4: ROS (Robot Operating System)

This track covers installing and running ROS, then building ROS nodes that support teams across all other tracks. Students will learn the ROS ecosystem and package workflow, and they will act as integration support for localization, vision, and control projects.

Learn more:

* ROS (Wikipedia): https://en.wikipedia.org/wiki/Robot_Operating_System
* ROS official site: https://www.ros.org/
* ROS 2 documentation: https://docs.ros.org/en/rolling/index.html
* ROS package index: https://index.ros.org/

## Collaboration Goal

By the end of the term, each track should produce reusable demos and reference notes, and the ROS track should help connect those pieces into shared robot software components.

<!-- BEGIN GENERATED MEETINGS - edited by scripts/gen_meetings.py -->
## Meetings

See the **[meeting calendar](/calendar/)** for all upcoming session dates, times, and how to enroll.
<!-- END GENERATED MEETINGS -->
