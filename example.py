"""
|||   Example CLI    |||
|||  Version: 0.0.1  |||
|||   Grano22 Dev    |||
"""

from libraries.aragonCLI import *

sampleParser = AragonParser()
#CLI Stages


#CLI Commands
@AragonCommand(sampleParser.commands, aliases=["V", "v"], useLowerCase=True)
def Version(p):
    print("Current version: "+str(0.01))

sampleParser.startInLoopWithOuter("test > ")