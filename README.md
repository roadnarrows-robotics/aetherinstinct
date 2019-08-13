# ai
Explorations in Artificial Intelligence

## Maze of Twisty Little Passages
My overarching strategy to learn and develop AI.
Of course, as the work proceeds, many back steps,
turns to left rather than forward, and fleeing from monsters will occur
before reaching the treasure room. If ever.

The numerical naming of the subpackages are in the intended chronological
order of development.

### ai.core
This subpackage contains algorithms and data structures used be the other
ai.N subpackages.

### ai.1
4D vision neural network.
### ai.2
Binaural neural network.

# ai.1
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

# ai.2
Teach a NN the identification and location of sound. from binaural microphones.
