import json
import sys, getopt

class validation():

    def __init__(self):
        self.SOURCE_FILE    = None
        self.RULE_FILE      = None
        self.OUTPUT_FILE    = None
    
    def loadJson(self, file_path):
        with open(file_path ,"r") as f:
            return json.load(f)
    
    def write(self, content):
        print(content)
        with open(self.OUTPUT_FILE, "w") as f:
            f.write(content)
            f.close()
            print("\t===> Created " + self.OUTPUT_FILE)

    def getARGS(self, argv):
        usage = 'python validation.py -r [RULE_FILE] -s [SOURCE_FILE] -o [OUTPUT_FILE]'
        try:
            opts, args = getopt.getopt(argv, "s:r:o:",["source=", "rule=", "output="])
        except getopt.GetoptError:
            print (usage)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print (usage)
                sys.exit()
            elif opt in ("-s", "--source"):
                self.SOURCE_FILE = arg
            elif opt in ("-r", "--rule"):
                self.RULE_FILE = arg
            elif opt in ("-o", "--output"):
                self.OUTPUT_FILE = arg
    
    def checkEqual(self, foo, bar):
        if foo == bar:
            return True
        else:
            return False
        
    def validate(self, rule, source):
        rule_name   = rule['rule_name']
        valid_key   = rule['rule']['valid_key']
        valid_value = rule['rule']['valid_value']
        cond        = rule['rule']['condition']
        succss_msg  = rule['rule']['when_validated']
        fail_msg    = rule['rule']['when_not_validated']

        res = "["
        for item in source:
            try:
                tmp = item[valid_key]
            except:
                print("Not found key: %s" % valid_key)
                exit(2)

            if cond.lower() == "eq" or cond == "=" or cond == "==":
                if self.checkEqual(valid_value, item[valid_key]):
                    item.update({"validate": succss_msg})
                else:
                    item.update({"validate": fail_msg})
                res += str(item) + ","
        res = res[:-1] + "]"
        return res.replace("'", "\"")

    def main(self, argv):
        self.getARGS(argv)
        rule    = self.loadJson(self.RULE_FILE)
        data    = self.loadJson(self.SOURCE_FILE)
        res     = self.validate(rule=rule, source=data)
        self.write(res)       

if __name__ == "__main__":
    proc = validation()
    proc.main(sys.argv[1:])