import re

def StrToValue(Throw_String):

    regex_pattern_numbers =r"\d{1,3}"
    regex_pattern_Letter =r"[a-zA-Z]"

    Throw_String=Throw_String.replace("be","25")

    Value_str = re.findall(regex_pattern_numbers,Throw_String)
    Mutliplikator_str = re.findall(regex_pattern_Letter,Throw_String)

    if Mutliplikator_str == ["d"]:
        Multiplikator = 2
    elif Mutliplikator_str == ["t"]:
        Multiplikator = 3
    else:
        Multiplikator = 1
    
    Value=int(Value_str[0])*Multiplikator
    return Value, Multiplikator

if __name__ == "__main__":

    Throws = ["t20","i20","o20","dbe","be","d15"]

    for i in Throws:
        print(StrToValue(i))