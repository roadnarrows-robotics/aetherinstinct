# ai.1  Visual
_4D Vision Neural Networks_

## ai.1.1 Monocular Point Cloud
### Goal
Develop a NN to generate an XYZRGB point cloud from RGB images. A point cloud
stream is used for reinforcement training.
### Setup
#### Hardware
Intel [RealSense][intel-realsense] structured light 3D camera mounted on a
fixed hard point.
#### Software
1. The point cloud data produced by the 3D camera is split into two streams:
    * XYZRBG for reinforcement
    * RGB for input into the NN
2. Error metrics
3. Point cloud visualizers:
    * rotable point cloud visualizer
    * prediction error visualizer
#### Neural Network
1. convolutional NN CNN
2. reinforcement learning RNN
### Target Results
1. A software framework to support point cloud streaming, piping, and
visualization.
2. A final NN that should produce a point cloud with reasonable fidelity.
Since ai.1.1 is monocular, moderate error rates are expected.

## ai.1.2 Temporally Binocular Point Cloud
#### Base: ai.1.1

### Goal
Using ai.1.1 as a base, develop a NN that accepts multiple sequential
offset RGB images to generate the point cloud.
### Setup
#### Hardware
Intel [RealSense][intel-realsense] structured light 3D cameral mounted on an
actuated pan-tilt.
#### Software
1. The point cloud data produced by the 3D camera is split into two streams:
    * XYZRBG for reinforcement
    * RGB for input at t<sub>0</sub> into the NN
2. Several quick left-right, top-bottom saccades are performed to gather
additional RGB images offsets. (The XYZ data is discarded). These are feed
into the NN at times t<sub>1</sub>, t<sub>2</sub>,...
#### Neural Network
1. NN from ai.1.1
2. recurrent NN
3. attention NN \[[1][2d-pervasive-attention]\][<sup>2</sup>][gh-attn2d]

### Target Results
1. Develop the software to control a pan-tilt.
2. A final NN that should produce a point cloud with very good fidelity,
since ai.1.2 is temporally binocular.

## ai.1.3 Binocular Mesh
### Goal
Mesh NN

# TBD NOTES
Teach a NN 4D vision. Here, 4D refers to the 3 spatial dimensions plus time.
Ultimate goal: scene graph of objects include best guesses of occluded areas
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

## References
1. Maha Elbayad, Laurent Besacier, and Jakob Verbeek. 2018.
[Pervasive Attention: 2D Convolutional Networks for Sequence-to-Sequence
Prediction][2d-pervasive-attention].
In Proceedings of the 22nd Conference on Computational Natural Language Learning
(CoNLL 2018)
2. [github attention 2d repository][gh-attn2d]

<!-- references and media -->
[intel-realsense]: https://www.intel.com/content/www/us/en/architecture-and-technology/realsense-overview.html

[2d-pervasive-attention]: https://arxiv.org/abs/1808.03867
[gh-attn2d]: https://github.com/elbayadm/attn2d
[med-attn]: https://towardsdatascience.com/the-fall-of-rnn-lstm-2d1594c74ce0
