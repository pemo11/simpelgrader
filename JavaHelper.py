# =============================================================================
# file: JavaHelper.py
# =============================================================================

import shutil
from subprocess import Popen, PIPE, STDOUT,TimeoutExpired
import configparser
import Loghelper
import os
import tempfile
import re


class JavaHelper:

    def __init__(self, configPath):
        config = configparser.ConfigParser()
        config.read(configPath)
        self.javaCPath = config["path"]["javaCompilerPath"]
        self.javaPath = config["path"]["javaLauncherPath"]

    '''
    Compiles a single java file
    '''
    def compileJava(self, filePath) -> (int, str):
        dirPath = os.path.dirname(filePath)
        # -cp is always important because the java file is not in the current directory
        javaArgs = f"{self.javaCPath} -cp {dirPath} {filePath}"
        infoMessage = f"compileJava: java compiling {filePath}"
        Loghelper.logInfo(infoMessage)
        # shell=True?
        procContext = Popen(javaArgs, shell=True, env={"PATH": dirPath}, stdout=PIPE, stderr=STDOUT)
        procContext.wait()
        infoMessage = f"compileJava: java exit code={procContext.returncode}"
        Loghelper.logInfo(infoMessage)
        javaCOutput = procContext.stdout.read()
        outputText = "OK"
        if len(javaCOutput) > 0:
            # cp1252 is import for Umlaute (utf8 does not work?)
            javaCOutput = javaCOutput.decode("cp1252")
            # Pattern to extract the error message only
            outputPattern = "java:\d+:\s+(.*)\r"
            if len(re.findall(outputPattern,javaCOutput)) > 0:
                outputText = re.findall(outputPattern,javaCOutput)[0]
            else:
                outputText = "Error"
            infoMessage = f"compileJava: java compiler message={javaCOutput}"
            Loghelper.logInfo(infoMessage)

        return (procContext.returncode, outputText)

    '''
    Runs a class file
    outputChecker is a lambda/function that does determine if the output is correct
    '''
    def runJava(self, filePath, outputChecker) -> int:
        dirPath = os.path.dirname(filePath)
        javaArgs = f"{self.javaPath} -cp {dirPath} {filePath}"
        infoMessage = f"runJava: java compiling {filePath}"
        Loghelper.logInfo(infoMessage)
        outputText = "Leider nix"
        # shell=True?
        # Timeout for the java-Process
        timeOutSeconds = 15
        try:
            with Popen(javaArgs, shell=True, env={"PATH": dirPath},
                                  stdout=PIPE, stderr=STDOUT,
                                  encoding=None, errors=None) as proc:
                proc.wait(timeOutSeconds)
                outputText = proc.stdout.read()
                result = 0
                if outputChecker:
                    result = outputChecker(outputText)
            return result
        except TimeoutExpired as ex:
            infoMessage = f"runJava: TimeOutExpired for process {filePath}"
            Loghelper.logError(infoMessage)
            return -1

