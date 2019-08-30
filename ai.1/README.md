# ai.1 - Visual
_4D Vision Neural Networks_

## ai.1.1 Monocular Point Cloud
### Goal
Develop a NN to generate an XYZRGB point cloud from RGB images. A point cloud
stream is used for reinforcement training.
### Setup
#### Hardware Platform
Intel [RealSense][intel-realsense] structured light 3D cameral mounted on a
fixed hard point.
#### Software Architecture
1. The point cloud data produced by the 3D camera is split into two streams:
    * XYZRBG for reinforcement
    * RGB for input into the NN
### Results
1. A software framework to support point cloud streaming and plumbing.
2. A final NN that should produce a point cloud with reasonable fidelity.
Since ai.1.1 is monocular, moderate error rates are expected.

## ai.1.2 Temporally Binocular Point Cloud
### Goal
Using ai.1.1 as a base, develop a NN that accepts multiple sequential
offset RGB images to generate the point cloud.
### Setup
#### Hardware Platform
Intel [RealSense][intel-realsense] structured light 3D cameral mounted on an
actuated pan-tilt.
#### Software Architecture
1. The point cloud data produced by the 3D camera is split into two streams:
    * XYZRBG for reinforcement
    * RGB for input at t<sub>0</sub> into the NN
2. Several quick left-right, top-bottom saccades are performed to gather
additional RGB images offsets. (The XYZ data is discarded). These are feed
into the NN at times t<sub>1</sub>, t<sub>2</sub>,...
### Results
1. Develop the software to control a pan-tilt.
2. A final NN that should produce a point cloud with very good fidelity,
since ai.1.2 is temporally binocular.

## ai.1.3 Binocular Mesh
### Goal
Mesh NN

# TBD NOTES
Teach a NN 4D vision. Here, 4D refers to the 3 spatial dimensions plus time.
Ultimate goal: scene graph of objects include best guesses of obscured areas
(i.e. back of a head, opposite side of a die, etc)
### Notes
1. not identify what things are but can identify the same thing and
differentiate between things.

## phase 1
Structure light 3D camera. The cameral outputs XYZRGB point cloud.
The point cloud is feed into a meshing pipeline to generate a mesh.
The mesh is used for reinforce learning of a neural net.
The NN is fed only the RGB component. From there it auto-generates the 
mesh.

<!-- references and media -->
[intel-realsense]: https://www.intel.com/content/www/us/en/architecture-and-technology/realsense-overview.html

