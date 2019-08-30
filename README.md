# Explorations in Artificial Intelligence

My overarching methodology is to develop Artificial General Intelligence
(referenced within this project as simply AI) using
almost exclusively neural networks (NN).
Building from the most task-focused AI modules, capabilities and layers will be
added, progressing up to the Capable Interpreter.

The inspiration of this work will be Evolution, Neuroscience, and Logic,
with a strong dose of Ethics.

### Evoluion
Evolution has finely tuned the human brain. The brain contains many
subconscious task-specific modules, all competing for the attention of the
concsious, so that our internal Interpreter can construct a rational narrative
of self and of the world.
For a Capable Interpreter to iteract intelligently with people, I believe it
should posess a "close-enough" analog of the human subconscious.
However the emerging digital analogs are of a different kind,
and may lead to entirely different paths to general intelligence
and enlightenment.

### Neuroscience
_To know thyself is the beginning of wisdom._<br>
&nbsp;&nbsp;― Socrates

### Logic
Propositional, predicate, mathematical with arthematic, and boolean logic.

### Ethics
It would be beautiful that a highly rational, ethical AI would
inorganically emerge from the artificial neural fog.
Would that emergence imply an ethical universe? Doubtful.
At a minimum, skills in argument, persuasion with the recognition of
fallacies such as
_false dilemma_, _straw man_, _begging the question_, and _ad hominem_ 
are needed. Humans are rascals at best.

## Maze of Twisty Little Passages
In broad brushstrokes, my AI approach is listed in the following subsections,
Build competent task-specific modules, fuse modules into an integrative complex,
and repeat.
Of course, as my work proceeds, many deadends, wrong turns,
death by monsters and vile hobgoblins,
will occur before reaching any treasure room. If ever.

_Note_: The numerical naming of the ai.K subpackages are intended to indicate
the chronological order of development.

### ai.core
This subpackage contains algorithms and data structures used by the other
ai.K subpackages.
* Memory NNs for various types.
* Various learning algrothims besides standard backprops. Hopefully, local
neuronal learning that does not require differentials.
* Graph techniques.

### ai.1 Visual
[4D Vision Neural Network Module][ai-1-readme]

A collection of NNs that are able to sense visable light and construct
a model of the 4D real world in real-time.
The four dimensions are the three spatial plus time.
The NNs should perform well on 3D (video) and 2D (images).

A set of one or more cameras are required in the production system.

#### Competencies
1. Convert a spatial/temporal binocular image stream to a version of a 
scenegraph of meshed textured objects.
2. Contain on object memory that can be fed into the NN.
3. Complete obscured portions of the scene base on prior knowledge.
4. Locate objects.
5. Differentiate objects.
6. Determine object "sameness".

#### Limitations
1. Cannot identify object classes or types (e.g. dog, cat, ball, etc).
2. Cannot identify object physical properties (e.g. squishy, hard,
weightiness, etc).

### ai.2 Auditory
[4D Binaural Neural Network Module][ai-2-readme]

A collection of NNs that are to able sense sound,
within the hearing range of humans, and construct 
a model of the 4D real world in real-time.
The four dimensions are the three spatial and time.
Sound properties of frequency, amplitude, phase, and time with be used.

A set of two or more microphones are required in the production system.

#### Competencies
1. Convert temporal binaural sound into an internal TBD representation.
2. Locate sound origin.
3. Differentiate sounds.
4. Determine sound "sameness".

#### Limitations
1. Cannot identify the class or type sound (e.g. bell, crying baby, crow, etc).

### ai.3 Visual and Auditory Fusion
_Fusion of Visual (ai.1) and Auditory (ai.2) Neural Networks_

### ai.4 Somato
_Somatosensory wnd Somatomotor Cortex_

A set of one or more actuated systems (robot components such as robotic arms
and pan-tilts) are required in the production systme.

### ai.5 Binocular Vision
_Integrate the Visual (ai.1, ai.3) and Somato (ai4) Neural Networks_

A platform of 2 cameras with pan-tilt, focus, and vergence motor control are
the target production platform.

### ai.6
Sound generation.

### ai.7
Fusion of ai.3, ai.4, ai.5, and ai.6

### ai.8
Boolean logic and arithmetic.

### ai.9
Spoken language recognition and generation.

### ai.10
Written language recognition and generation.

### ai.11
Computer Monitor Display Control

### ai.12
Arguments of Logic (e.g. straw man, etc).

# ai.2
Teach a NN the identification and location of sound. from binaural microphones.

<!-- referneces and media -->
[ai-1-readme]: https://github.com/roadnarrows-robotics/ai.1/README
[ai-2-readme]: https://github.com/roadnarrows-robotics/ai.2/README
