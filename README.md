High Performance Python: The Code
=================================

This repository contains the code from ["High Performance
Python"](http://shop.oreilly.com/product/0636920028963.do) by Micha Gorelick
and Ian Ozsvald with O'Reilly Media.  Each directory contains the examples from
the chapter in addition to other interesting code on the subject.

Topics Covered
--------------

This book ranges in topic from native Python to external modules to writing your
own modules.  Code is shown to run on one CPU, multiple coroutines, multiple
CPU's and multiple computers.  In addition, throughout this exploration a focus
is kept on keeping development time fast and learning from profiling output in
order to direct optimizations.

The following topics are covered in the code repo:

- Chapter 1: Profiling
    - What are the ways to profile your code?
    - What insights can I gain from a profile?

- Chapter 2: Understanding Performant Programming
    - How does a computer work and how does that affect my code performance?

- Chapter 3: Lists and Tuples
    - How do lists and tuples work?
    - What are the performance implications of this?

- Chapter 4: Dictionaries and Sets
    - How do dictionaries and sets work?
    - What are the performance implications of this?

- Chapter 5: Iterators
    - How do iterators work?
    - How can I use them to reduce memory in my code?
    - How can I use them to reduce the CPU operations needed in my code?

- Chapter 6: Matrix and Vector Computation
    - How does the CPU perform matrix/vector operations?
    - What are the ways I can profile the efficiency of these operations?
    - How can I speed up code given a profile?

- Chapter 7: Compiling to C
    - What are the automated ways to compile my python to C?
    - What are the manual ways to compile my python to C?
    - How can I use these technologies to speed up my code and not slow down development?

- Chapter 8: Concurrency
    - How does concurrency work and how does python support it?
    - How can I speed up multiple IO operations?
    - How can I hide IO wait? 

- Chapter 9: Multiprocessing
    - What is multiprocessing?
    - How can I speed up my code on a multiple CPU machine?
    - What are the subtleties of muli-CPU code?

- Chapter 10: Clusters and Job Queues
    - How can I extend my code to a cluster?
    - What are some of the pain-points with clusters?
    - What is a queue and how is it useful?

- Chapter 11: Using Less Ram
    - How can I use algorithms to reduce the RAM usage of my code?
    - What are tries and probabilistic data structures?

- Chapter 12: Lessons from the Field (no code)
    - Some stories from the field on performance python

Using the code base
-------------------

This code base is a live document and should be freely commented on and used.
It is distributed with a license that amounts to: don't use the code for
profit, however read the [provided license](LICENSE.md) file for the
law-jargon.  Feel free to share, fork and comment on the code!

If any errors are found, or you have a bone to pick with how we go about doing
things, leave an issue on this repo!  Just keep in mind that all code was
written for educational purposes and sometimes this means favouring readability
over "the right thing" (although in Python these two things are generally one
and the same!).

