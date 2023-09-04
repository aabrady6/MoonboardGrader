#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author - Aaron Brady
# Functions used to convert between grade scales - Use once raw data has been created
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Grade Conversion Methods
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Grade:
    grade = None
    def __init__(self, grade_val = str):
        self.grade = grade_val
        self.conversion = [ '6A', '6A+', '6B', '6B+', '6C', '6C+', '7A', '7A+', '7B', '7B+', '7C', '7C+', '8A', '8A+', '8B', '8B+', '8C', '8C+', '9A']

    # Convert Fontainebleau scale to TF scale
    def font_to_score(self):
        if self.grade in self.conversion:
            t = self.conversion.index(self.grade) 
            return t

    # Convert TF scale to Fontainebleau    
    def score_to_font(self):
                return self.conversion[self.grade]

    # Grade Driver, write to out file and append to list
    def grade_converter(self, grade, grade_list, out_file):
        grade = grade.font_to_score()
        out_file.write(str(grade))
        out_file.write('\n')
        grade_list.append((grade))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Hold Location Conversion Methods
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Hold:
    def __init__(self, hold = str):
        self.hold = hold
        self.letter = hold[0]
        self.number= (int(hold[1:]))
        self.index = None

    # Convert to array index value
    def get_index(self):
        char_index = ord(self.letter) - 65
        num_index = self.number - 1
        self.index = (num_index * 11) + char_index
        return self.index


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# General Array Functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create the np array for each problem. Write to ../TF Data/Arrays.txt file. 
def create_array(h, sh, eh):
    # Read and create lists of all of the holds for 3 layers
    legal_holds_problems_list = h.readlines()
    start_holds_problems_list = sh.readlines()
    end_holds_problems_list = eh.readlines()
    test_final = []
    problem = 0
    # Iterate through the problem set and isolate each problem for analysis
    for problem in range (len(legal_holds_problems_list)):
        iterating_hold = 0
        test_hold_list = [0] * 198
        test_start_list = [0] * 198
        test_end_list = [0] * 198
        # Create lists of the holds for the legal holds, starting holds, ending holds
        problem_hold_list = legal_holds_problems_list[problem]
        problem_hold_list = problem_hold_list.split(" ")
        problem_start_list = start_holds_problems_list[problem]
        problem_start_list = problem_start_list.split(" ")
        problem_end_list = end_holds_problems_list[problem]
        problem_end_list = problem_end_list.split(" ")
        # Iterate through each hold for the specific problem and add to that problem's array
        for iterating_hold in range(len(legal_holds_problems_list[problem])):
            try:
                hold_index = Hold(problem_hold_list[iterating_hold])
                hold_index = hold_index.get_index()
                test_hold_list[hold_index] = 1
            except:
                pass
            try:
                start_index = Hold(problem_start_list[iterating_hold])
                start_index = start_index.get_index()
                test_start_list[start_index] = 1
            except:
                pass
            try:
                end_index = Hold(problem_end_list[iterating_hold])
                end_index = end_index.get_index()
                test_end_list[end_index] = 1
            except:
                pass
        # Build the output array    
        test_hold_list = np.array(test_hold_list).reshape(18,11)
        test_start_list = np.array(test_start_list).reshape(18,11)
        test_end_list = np.array(test_end_list).reshape(18,11)
        test_result_array = np.stack((test_hold_list, test_start_list, test_end_list))
        test_final.append(test_result_array)
    final_array = np.array(test_final)
    return(final_array)
    
def write_to_out_file(in_array, out_file):
    pass

# Close the open files of legal, start and finish holds. 
def close_files(h, sh, eh, out_file):
    h.close()
    sh.close()
    eh.close()
    out_file.close()

            
            


    

        