# =============================================================================
# file: CompareTestHelper.py
# =============================================================================
import os
import re
from subprocess import Popen, PIPE, STDOUT,TimeoutExpired

from XmlHelper import XmlHelper
import configparser


class CompareTestHelper:

    def __init(self, configPath):
        # read the paths from the in file
        config = configparser.ConfigParser()
        config.read(configPath)
        self.javaPath = config["path"]["javaLauncherPath"]
        self.javaCPath = config["path"]["javaCompilerPath"]
        self.gradingPlanPath = config["path"]["gradingPlanPath"]

    '''
    does a text compare by running a testdriver java class and analyzing the output
    '''
    def runTextCompare(self, classPath, exercise) -> ():
        xmlHelper = XmlHelper(self.gradingPlanPath)
        dirPath = os.path.dirname(classPath)
        # get the details of the test from the grading plan xml
        result = xmlHelper.getTextCompareTest(exercise)
        if result == None:
            infoMessage = f"runTextCompare: no TextCompare test for {exercise} found"
            return (-1, infoMessage)
        # now run the test
        testRegex = result["testRegex"]
        testClass = result["testClass"]
        javaArgs = f"{self.javaPath} -cp {dirPath} {testClass}"
        procContext = Popen(javaArgs, shell=True, env={"PATH": classPath}, stdout=PIPE, stderr=STDOUT)
        procContext.wait()
        retCode = procContext.returncode
        javaLOutput = procContext.stdout.read()
        javaLOutput = javaLOutput.decode("cp1252")
        # compare each line with the regex for the test
        errorCount = 0
        # skip the empty line(s)
        allLines = [l for l in javaLOutput.split("\n") if l != ""]
        for line in allLines:
            if re.findall(testRegex, line) == None:
                errorCount += 1
            else:
                # findall returns an array with tuples
                matches = re.findall(testRegex, line)
                if len(matches) == 1:
                    # the last group is the expected value
                    expectedValue = matches[0][-1]
                    # the second last group is the delivered value
                    deliveredValue = matches[0][-2]
                    # do they match?
                    if expectedValue != deliveredValue:
                        errorCount += 1
                else:
                    errorCount += 1
            # write text compare lines to report file

        lineCountAlias = "line" if len(allLines) == 1 else "lines"
        errorCountAlias = "error" if errorCount == 1 else "errors"
        textCompareMessage = f"{len(allLines)} {lineCountAlias} with {errorCount} {errorCountAlias}"
        result = 0 if errorCount == 0 else 1
        return (result, textCompareMessage, allLines)

