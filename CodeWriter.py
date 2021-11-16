"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    output_file = None
    current_line = -1

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_file = output_stream

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        pass

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        if command == "add":
            self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M+D\nM=D\n@SP\nM=M+1\n")
        if command == "sub":
            self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\nM=D\n@SP\nM=M+1\n")
        if command == "neg":
            self.output_file.write("@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n")
        if command == "eq":
            self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M+D\n@FALSE."
                                   + str(self.current_line) + "\nD;JNT\nM=-1\n@SP\nM=M-1\n@CONTINUE."
                                   + str(self.current_line) + "\n0;JMP\n(FALSE." + str(self.current_line) +
                                   ")\nM=0\n@SP\nM=M+1\n(CONTINUE." + str(self.current_line) + ")\n")
        if command == "gt":
            self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@FALSE."
                                   + str(self.current_line) + "\nD;JLE\nM=-1\n@CONTINUE."
                                   + str(self.current_line) + "\n0;JMP\n(FALSE." + str(self.current_line) +
                                   ")\nM=0\n(CONTINUE." + str(self.current_line) + ")\n@SP\nM=M+1\n")
        if command == "lt":
            self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@FALSE."
                                   + str(self.current_line) + "\nD;JGT\nM=-1\n@SP\nM=M-1\n@CONTINUE."
                                   + str(self.current_line) + "\n0;JMP\n(FALSE." + str(self.current_line) +
                                   ")\nM=0\n@SP\nM=M+1\n(CONTINUE." + str(self.current_line) + ")\n")
        if command == "and":
            self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@FALSE" + str(self.current_line) +
                                   "\nD;JEQ\n@SP\nM=M-1\nA=M\nD=M\n@FALSE" + str(self.current_line + 1) +
                                   "\nD;JEQ\nM=-1\n@CONTINUE." + str(self.current_line + 1) +
                                   "\n0;JMP\n(FALSE." + str(self.current_line) +
                                   ")\n@SP\nM=M-1\nA=M\nD=M\n@FALSE" + str(self.current_line + 1) +
                                   "\nD;JEQ\nM=-1\n@CONTINUE." + str(self.current_line + 1) +
                                   "\n0;JMP\n(FALSE." + str(self.current_line + 1) + ")\nM=0\n(CONTINUE." +
                                   str(self.current_line) + ")\n@SP\nM=M+1\n")
        if command == "or":
            self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\n@TRUE." + str(self.current_line) +
                                   "\nD;JLT\nD=M\n@TRUE." + str(self.current_line) + "\nD;JLT\nM=0\n@CONTINUE."
                                   + str(self.current_line) + "\n0;JMP\n(TRUE." + str(self.current_line) +
                                   ")\nM=0\n(CONTINUE." + str(self.current_line) + ")\n@SP\nM=M+1\n")
        if command == "not":
            self.output_file.write("@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        str_index = str(index)
        if command == "C_PUSH":
            if segment == "LCL" or segment == "ARG" or segment == "THIS" or segment == "THAT":
                self.output_file.write("@" + str_index + "\n D=A @" + segment +
                                       "\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            if segment == "CONSTANT":
                self.output_file.write("@" + str_index + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            if segment == "TEMP":
                self.output_file.write("@" + str_index + "\nD=A\n@5\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            if segment == "STATIC":
                self.output_file.write("@Foo." + str_index + "\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            if segment == "POINTER":
                if index == 0:
                    self.output_file.write("@THIS\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
                else:
                    self.output_file.write("@THAT\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        else:
            if segment == "LCL" or segment == "ARG" or segment == "THIS" or segment == "THAT":
                self.output_file.write("@" + str_index + "\nD=A\n@" + segment +
                                       "\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            if segment == "TEMP":
                self.output_file.write("@" + str_index + "\nD=A\n@5\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nD=M\n@R13\nA=M\nM=D"
                                                         "\n")
            if segment == "STATIC":
                self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@Foo." + str_index + "\nM=D\n")
            if segment == "POINTER":
                if index == 0:
                    self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@THIS\nA=M\n")
                else:
                    self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@THAT\nA=M\n")

    def close(self) -> None:
        """Closes the output file."""
        self.output_file.close()
