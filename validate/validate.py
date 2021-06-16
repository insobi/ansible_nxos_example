import json
import sys, getopt

class validate():

    def __init__(self):
        self.SOURCE_FILE    = None
        self.RULE_FILE      = None
        self.OUTPUT_FILE    = None

    def loadJson(self, file_path):
        with open(file_path ,"r") as f:
            return json.load(f)


    def write(self, content):
        # print(content)
        with open(self.OUTPUT_FILE, "w") as f:
            f.write(content)
            f.close()
            print("File " + self.OUTPUT_FILE + " was created.")


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
    

    def json_extract(self, obj, key):
        """Recursively fetch values from nested JSON."""
        arr = []

        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        values = extract(obj, arr, key)
        return values


    def validate(self, rule, source):
        rule_name       = rule['rule_name']
        index           = rule['index']
        valid_key       = rule['valid_key']
        valid_value     = rule['valid_value']
        cond            = rule['condition']
        succss_msg      = rule['if_valid']
        fail_msg        = rule['if_invalid']
        resolved        = []

        index_values    = self.json_extract(source, index)
        valid_values    = self.json_extract(source, valid_key)

        for item in valid_values:
            if cond.lower() == "eq" or cond == "=" or cond == "==":
                if item == valid_value:
                    resolved.append(succss_msg)
                else:
                    resolved.append(fail_msg)

        seq = 0
        res = "["
        for item in index_values:
            res += "{\"" + index + "\":\"" + index_values[seq] + "\", \""  + valid_key + "\":\"" + valid_values[seq] + "\", \"valid\": \"" + resolved[seq] + "\"},"
            seq += 1
        res = res[:-1] + "]"
        return res

    def main(self, argv):
        self.getARGS(argv)
        rule    = self.loadJson(self.RULE_FILE)
        source  = self.loadJson(self.SOURCE_FILE)
        res     = self.validate(rule, source)
        self.write(res)       

if __name__ == "__main__":
    proc = validate()
    proc.main(sys.argv[1:])