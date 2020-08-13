---
layout: project
title: GameOfLife
icon: icon-github
caption: 'A Multi-threaded version of the popular Game Of Life implemented in four
  versions: Using Java8 threads, using the Skandium framework, using standard Java
  Threads and sequential'
description: 'A Multi-threaded version of the popular Game Of Life implemented in
  four versions: Using Java8 threads, using the Skandium framework, using standard
  Java Threads and sequential'
links:
- title: Link
  url: https://github.com/Gabryxx7/GameOfLife

---

##Final project of the SPM course (Distributed Systems:  paradigms and models) of University of Pisa

The goal of this project is the implementation of “Game Of Life” in Java, both in a sequential and parallel 
way. For the parallel implementation of the game, Java’s threads and a CyclicBarrier, the Skandium 
framework and the new stream features of Java 8 have been used. The project has been realized using a Map 
skeleton, and tests have been performed to observe how a parallel implementation of the application could 
improve the performances. The tests have been performed on two different machines, a Xeon E5-2650 
@2.00GHz with 8 cores and 16 threads whose credentials have been provided during the course’s classes, 
and on an Intel i7 4790k @4.00ghz with 4 cores and 8 contexts (Results and graphs of the latter may be 
found in the Statistiche folder of the project archive). 



Usage
The software will be distributed in a tarball archive which will contain the main folder with all the needed 
files to compile and execute the application. The software can be compiled and packed automatically by 
means of Apache Ant. 
By simply calling the ant command, the whole project will be compiled and packed in a jar file, and stored 
inside a jar folder.  

```bash
tar –xvzf GameOfLife.tar.gz 
Cd GameOfLife 
ant
```

After the jar file is created it will be possible to execute the software by using the command: 
```bash
java –jar jar/GameOfLife.jar
```

The above command (or by adding the –h, --help parameter) will show the following menu: 

 
```bash
 _______ _______ __ __ _______ _______ _______ ___ ___ _______ _______ 
 | || _ || |_| || | | || | | | | | | || | 
 | ___|| |_| || || ___| | _ || ___| | | | | | ___|| ___| 
 | | __ | || || |___ | | | || |___ | | | | | |___ | |___ 
 | || || || || ___| | |_| || ___| | |___ | | | ___|| ___| 
 | |_| || _ || ||_|| || |___ | || | | || | | | | |___ 
 |_______||__| |__||_| |_||_______| |_______||___| |_______||___| |___| |_______| 
 
usage: GameOfLife [-g] [-h] -i <1000> -n <30> -s <10x10,50x50,800x800...> 
       [-t <4>] [-v <seq, mt, sk, j8>] 
 -g,--graphics                        Display graphics, disabled by 
                                      default 
 -h,--help                            Print help message 
 -i,--iterations <1000>               Number of iterations for every board 
 -n,--number <30>                     Number of times to execute the test 
 -s,--size <10x10,50x50,800x800...>   Boards sizes, in the form HxW 
 -t,--threads <4>                     Maximum number of threads. If not 
                                      specified, uses all available 
                                      threads 
 -v,--version <seq, mt, sk, j8>       Version of the game to execute. If 
                                      not specified executes all possible 
                                      versions (test) and print a file 
                                      with all the results 
                                      
```


- -g , --graphics: It’s an optional parameter and it will show a Jpanel window for a graphical 
representation of the game board 
- -i, --iterations: It’s a required parameter, it specifies the amount of game steps to execute for each 
board size 
- -n, --number: It’s a required parameter and it specifies the amount of times to repeat the whole 
testing phase, so, each version of the game will compute I (iterations) steps on each of the specified 
board sizes, this whole process will be then repeated n (number) times, and the final average will be 
computed among all the obtained times 
- -s –size: It’s a required parameter and it specifies a list of board sizes on which the tests will be 
executed 
- -t, --threads: it’s an optional parameter, and it specifies the maximum number of threads to use for 
the execution. If it’s not specified, all the available threads will be used, starting from a single thread 
execution to an execution that will take advantage of all of the available threads on the machine. It’s 
used for debugging or special testing purposes. 
- -v, --version: It’s an optional parameter and it specifies which version of the game to launch. If it’s 
not specified, all the possible versions of the game will be executed during the testing phase. 