# aragonCLI Library | V.1 | Grano22 Dev
from sys import platform, argv
import os
import re
import inspect
from termcolor import colored

# Errors and Exceptions
class GlobalAragonCLIAPIError(Exception):
    pass

class LackOfCommandParametersError(Exception):
    pass

class InvaildRequiredParameter(Exception):
    pass

class InvaildOptionalParameter(Exception):
    pass

class InvaildNamedParameterConstruction(Exception):
    pass

class CommandAlreadyInitialized(Exception):
    pass

# END Errors and Exceptions

# CLI Visual


# END CLI Visual

class AragonOutputParser(object):
    COLORCODE = {
        'black': 0,
        'red': 1,
        'green': 2,
        'yellow': 3,
        'blue': 4,
        'magenta': 5,
        'cyan': 6,
        'white': 7
    }
 
    FORMATCODE = {
        'b': 1,  # bold
        'f': 2,  # faint
        'i': 3,  # italic
        'u': 4,  # underline
        'x': 5,  # blinking
        'y': 6,  # fast blinking
        'r': 7,  # reverse
        'h': 8,  # hide
        's': 9,  # strikethrough
    }

    @staticmethod
    def prepareOutput():
        pass

class AragonParser():
    fullCommand = ""
    commandsHistory = []
    commandParts = []

    lastCommand = ""
    lastRequiredParams = []
    lastOptionalParams = []

    lastOptionalNamedParams = {}
    lastOptionalIndexedParams = []

    stages = None
    commands = None


    def __init__(self, stages=None, commands=None, mode=""):
        if stages is None: self.stages = AragonStages()
        else: self.stages = stages
        if commands is None: self.commands = AragonCommands()
        else: self.commands = commands
        self.stages.parser = self
        self.commands.parser = self

    def parseFullCommandToParts(self, fullCommand, saveInHistory=True):
        inStr = False
        lastParsingPart = ""
        commandPieces = []
        for charInd in range(len(fullCommand)):
            if(inStr and fullCommand[charInd]=='"'):
                inStr = False
                commandPieces.append(lastParsingPart)
                lastParsingPart = ""
            elif(fullCommand[charInd]=='"'):
                inStr = True
            elif(len(lastParsingPart)>0 and len(fullCommand[charInd].strip())<len(fullCommand[charInd]) and not inStr):
                commandPieces.append(lastParsingPart)
                lastParsingPart = ""
            elif(len(fullCommand) - 1 == charInd and not inStr):
                lastParsingPart += fullCommand[charInd]
                commandPieces.append(lastParsingPart)
                lastParsingPart = ""
            elif(fullCommand[charInd].strip()!="" or inStr): lastParsingPart += fullCommand[charInd]
        if saveInHistory: self.commandsHistory.append({ "commandParts":commandPieces })
        return commandPieces

    def parseOptionalParams(self, paramsArr, namedPrefixes=["--"], indexedPrefixes="-"):
        try:
            indexedP = []
            namedP = {}
            inNamedParam = False
            founded = False
            for paramOnce in range(len(paramsArr)):
                for namedPref in namedPrefixes:
                    if paramsArr[paramOnce].find(namedPref)>-1:
                        if inNamedParam:
                            raise InvaildNamedParameterConstruction('Last named parameter doesn\'t have value')
                        inNamedParam = True
                        founded = True
                        paramsArr[paramOnce] = paramsArr[paramOnce].replace(namedPref, "")
                        break
                    founded = False
                if not founded and inNamedParam:
                    namedP[paramsArr[paramOnce - 1]] = paramsArr[paramOnce]
                    inNamedParam = False
                elif not founded:
                    paramsArr[paramOnce] = paramsArr[paramOnce].replace(indexedPrefixes, "")
                    indexedP.append(paramsArr[paramOnce])
            self.lastOptionalNamedParams = namedP
            self.lastOptionalIndexedParams = indexedP
            return [namedP, indexedP]
        except InvaildNamedParameterConstruction as invNamCons:
            self.printError(invNamCons)
        except Exception as exc:
            self.printError(exc)
            


    def startOuter(self):
        self.parser.fullCommand = " ".join(argv[1:])
        self.parser.commandParts = argv[1:]
        self.execute(argv[1], argv[2:])
        self.commandsHistory.append(self.parser.commandParts)
    
    def startInLoop(self, inputMess="Type something:", exitCommand="exit"):
        while True:
            self.stages.inputStage(inputMess)
            if len(self.commandParts)>0 and self.commandParts[0] == exitCommand:
                break
            self.stages.startStage()
        self.stages.exitStage()

    def startInLoopWithOuter(self, inputMess="Type something:", exitCommand="exit"):
        if(len(argv)>1):
            self.startOuter()
        else: self.startInLoop(inputMess, exitCommand)

    def execute(self, commandName, commandParameters=[]):
        try:
            if commandName.strip()=="": return self.stages.emptyCommandStage()
            tg = getattr(self.commands, commandName)
            if callable(tg):
                potentialArgs = len(inspect.signature(tg).parameters) - 1
                if potentialArgs > len(commandParameters): raise LackOfCommandParametersError('Lack of required parameters, given {0} but minimal is {1}'.format(len(commandParameters), potentialArgs))
                self.lastOptionalParams = commandParameters[potentialArgs:]
                tgVal = tg(self, *commandParameters[:potentialArgs])
                if callable(tgVal):
                    return tgVal(self)
                elif isinstance(tgVal, str):
                    tgVal = getattr(self.stages, tgVal)
                    if callable(tgVal):
                        return tgVal(self)
        except LackOfCommandParametersError as lackParamsErr:
            print(colored(lackParamsErr, "red"))
        except AttributeError as attrErr:
            errParams = attrErr.args[0]
            errParams = re.findall(r"(?<=\')[A-z0-9]*(?=\')", errParams)
            if errParams[0] == "AragonCommands":
                self.stages.unknownCommandStage(errParams[1])
            elif errParams[0] == "AragonStages":
                self.stages.unknownStageInstance(errParams[1])
            else: print(colored(errParams[0], "red"))
            #"An exception of type {0} occurred. Arguments:\n{1!r}".format(type(attrErr).__name__, attrErr.args)
        except Exception as unExc:
            print(colored(unExc, "red"))
        return None
    def print(self):
        pass

    def printError(self, text):
        print(colored(text, "red"))

    def printBB(self):
        pass

    def clear(self):
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            os.system("clear")
        elif platform == "win32":
            os.system("cls")


### Commands ###
def AragonCommand(CommandsMng, aliases=[], useLowerCase=False):
    try:
        def decorator(func):
            def wrapper():
                return func(CommandsMng)
            mainFuncName = func.__name__
            CommandsMng.ns.append(mainFuncName)
            setattr(CommandsMng, mainFuncName, func)
            if useLowerCase and mainFuncName.lower()!=mainFuncName:
                CommandsMng.ns.append(mainFuncName.lower())
                setattr(CommandsMng, mainFuncName.lower(), func)
            if len(aliases)>0:
                for alias in aliases:
                    if alias in CommandsMng.ns: raise CommandAlreadyInitialized(f'Command {alias} already initialized')
                    CommandsMng.ns.append(alias)
                    setattr(CommandsMng, alias, func)
            return wrapper
        return decorator
    except CommandAlreadyInitialized as caiErr:
        raise GlobalAragonCLIAPIError(caiErr)
    except Exception as exc:
        CommandsMng.printError(exc)


class AragonCommands():
    parser = None
    ns = []
    def __init__(self):
        pass
    def clear(self, p):
        p.clear()


### Stages ###
def AragonStage(StagesMng):
    def decorator(func):
        def wrapper():

            return func(StagesMng)
        StagesMng.ns.append(func.__name__)
        setattr(StagesMng, func.__name__, func)
        return wrapper
    return decorator


class AragonStages():
    parser = None
    ns = []

    def __init__(self):
        pass
    def inputStage(self, onInputMessage="Type something:"):
        self.parser.fullCommand = input(onInputMessage)
        self.parser.commandParts = self.parser.parseFullCommandToParts(self.parser.fullCommand)
    def startStage(self):
        self.parser.execute(len(self.parser.commandParts)>0 and self.parser.commandParts[0] or "", self.parser.commandParts[1:])
    def exitStage(self):
        pass
    def emptyCommandStage(self):
        print("Please enter command\n")
    def unknownCommandStage(self, commandName):
        print("Unknown command here "+"\x1b[3;31;43m"+commandName+"\x1b[0m\n")
    def unknownStageInstance(self, stageInstanceName):
        pass
    def invaildParameterStage(self):
        pass