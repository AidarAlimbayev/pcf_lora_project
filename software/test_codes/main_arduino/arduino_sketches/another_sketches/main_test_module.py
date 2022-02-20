import sys
sys.path.append('/home/ayan/Документы/Projects/pcf_lora_project')

# Import hello test_module
import test_module

# Call function
test_module.hello()

# print variable
print(test_module.shark)

# call class
jesse = test_module.Octopus("Jesse", "orange")
jesse.tell_me_about_the_octopus()