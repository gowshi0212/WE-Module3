# WE-Module3 - GenAI
Documentation of all work and assignments completed during Gen AI classes.
## Assignment 01
Pick any non-trivial problem statement from your computational thinking course and ask genAI to solve it. Iterate upon its solution to apply our principles of clean code.

## Assignment 02
Use a genAI tool to learn what the game of Yahtzee is
Engineer the genAI tool to play Yahtzee with you
Ask the genAI tool how to approach writing code for a Yahtzee scorer yourself
DO NOT ask the genAI tool to write code yet.

## Assignment 03
Create a testing strategy for the Yahtzee scorer code that was generated and document your journey.

## Assignment 04
The 1980s saw a shift from Natural Language Processing techniques aiming to codify the grammatical rules of natural language towards techniques aiming to use statistical models to generate text. One early idea which technically isn’t “AI” seeing as it is “memorizing” the training data and yet introduces us to the power contained in statistical techniques of text generation is the idea of Markov chains. Write a python function generate(filename: str, start_words: list[str], chain_length: int, num_generated: int) -> str which takes a filename, a chain length, a list of start words which has to be exactly as long as the chain_length (why?), and an integer num_generated and returns a sentence num_generated words long which sounds similar to the text contained in filename.
