# Installation
![Rolling Along][robot-wheeled]

The Aether Instinct (AI) package uses a simplified version of the
RoadNarrows LLC rnmake system to build AI.
(See [rnmake][rnmake] for more details.) 

The rnmake make system uses recursive GNU make within a structured
directory tree to make all components. The rnmake systems supports multiple
native and cross-compliled build environments. Each build environment,
called an architecture (arch), defines the tools chains and 
available resources. 

## Author's Build Machine

Component         | Version and Notes
:--------         | :----------------
&nbsp;**Hardware**
Intel CPUs        | 4 cores
Nvidia GPUs       | CUDA driver 10.1, runtime 9.0, compute 6.1
&nbsp;**System**
Ubuntu            | Bionic 18.04 LTS
GNOME             | 3.28
&nbsp;**Tool Chains and Interpreters**
bash              | 4.4
Python            | 3.6
GNU make          | 4.1
GNU gcc           | C compiler, version 7.5, standard C11
GNU c++           | C++ compiler, version 7.5, standard C++14
Nvidia nvcc       | CUDA compiler, version 9.1
swig              | 3.0
doxygen           | 1.8
&nbsp;**Deep Learning Frameworks**
pytorch           | 1.4
tensorflow        | 2.1
tensorflow_addons | 0.8
&nbsp;**Python Modules**
numpy             | 1.18
matplotlib        | 2.1
&nbsp;**3D Graphics**
UnrealEngine      | 4.24

## Instructions
**Note:** The WS symbol denotes the root prefix for the workspace, such as
`~/aetherinstinct`, `~/ai`, `/projects/nn/ai`.

### 1. Clone Repo
```bash
git clone https://github.com/roadnarrows-robotics/aetherinstinct WS
```

### 2. Source Environment
```bash
source WS/setup.sh
```

### 3. Make
```bash
cd WS
make deps
make
make install
```

## Tweaks
### package.mk
### cmds.mk
### x

<!-- references and media -->
[rnmake]: https://github.com/roadnarrows-robotics/rnr-sdk/wiki/rnmake
[robot-wheeled]: https://github.com/roadnarrows-robotics/ai/wiki/assets/images/RobotCatWheeled.png
