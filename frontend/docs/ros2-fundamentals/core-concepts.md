# ROS 2 Fundamentals

Robot Operating System 2 (ROS 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

## Architecture

ROS 2 uses a DDS (Data Distribution Service) based architecture:

- **Nodes**: Processes that perform computation
- **Topics**: Named buses over which nodes exchange messages
- **Services**: Synchronous request/response communication
- **Actions**: Asynchronous communication for long-running tasks

## Key Features

ROS 2 introduces several important features:

- Improved real-time support
- Better security
- Multi-robot support
- Cross-platform compatibility
- Quality of Service (QoS) settings

## Packages and Workspaces

In ROS 2, code is organized into packages:

- Each package contains specific functionality
- Packages are grouped into workspaces
- Build system: colcon (replaces catkin)

## Common Tools

ROS 2 provides various tools for development:

- `ros2 run`: Run nodes
- `ros2 topic`: Interact with topics
- `ros2 service`: Interact with services
- `rqt`: GUI tools
- `rviz`: 3D visualization tool

## Programming Languages

ROS 2 supports multiple programming languages:

- C++ (most common)
- Python (widely used)
- Experimental support for other languages