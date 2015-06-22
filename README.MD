# Introduction

Contest Site is a website for judging, grading, and administrating programming
competitions. Quickly review submissions and reject or accept them. Grading is
available for all configured languages. File extensions are detected in order to
compile and run submissions. 

# Grading

Comparisons are made by supplying example input and output (or none). Input 
may be received via stdin or with a provided file. Test input and output is 
provided on the problem pages.

# Judging

Judges are provided with a queue page that displays all the current requests
from teams for submission. The server will run them automatically for the judge
and store the output and output diff from the expected answer.

STDIN, STDOUT, and STDERR, and other variables relating to execution are all available for the judge to see.

Buttons are used to quickly indicate whether the submission is accepted or denied.

## Points

Each problem is worth a specific amount of points which are scored based on 
whether judges accepted the solution.

## Point Deduction

To penalize for incorrect submissions, a deducation value may be set. This value
is deducted from the possible points left for the problem. Once there are no
more points available, the problem is considered failed and further attempts are
disallowed.

# Setting up Compilers

Compilation is achieved by creating a compiler in the admin panel. The compiler
settings indicate the following:

- what is the name?
- what is the extension?
- is the language compiled?
- what is the command used to compile?
- what is the command used to run?

## Filename Substitution

Templating is used to insert the following values for the run and compile
commands.

- {{fullname}}: the absolute path to the file.
- {{filname}}: the name of the file.
- {{basename}}: the name of the file without the extension (useful for java classes)

### Examples

#### Java

- compiled: yes
- compile command: "javac {{filename}}"
- run command:     "java {{basename}}"

#### Python

- compiled: no
- run command: "python {{filename}}"

# Development Environment

The environment for running this application is built into a docker image. It is
still in development and is available on github. 

github.com/leanrobot/contestsite-docker